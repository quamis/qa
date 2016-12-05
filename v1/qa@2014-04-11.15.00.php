<?php

/**
- deduceArrayFromSum poate fi optimizat:
	- paralelizare
	-
	- permutarile pot fi accelerate punand hash-uri mici(crc32) pt fiecare 10 caractere in lista de hint-uri


 - la deduceArrayFromSum, e posibils a nu aiba sens sa trimiti hint-urile cu partialSums cand am un dictionar f variat per numarul de caractere de input
	(pt stringul aaabbbeee am un dictionar de 3 caractere, pt stringul 123sewTYR am un dicctionar de 9 caractere, partialSums nu mai ajuta asa tare)


	de ce depinde asa mult de marimea has-ului si a ferestrei pt SUM? macar marimea pt sum as o pot mari

*/

class qac {
	public function compress($data, $options = Array()) {
		$ret = Array();

		$ret['len'] = strlen($data);
		$ret['sum'] = $this->binarySum($data);

		$ret['raw'] = Array();
		$ret['raw']['hashes'] = Array();
		$ret['raw']['hashes']['crc32'] =   	crc32($data);
		$ret['raw']['hashes']['md5'] = 		md5($data);
		$ret['raw']['hashes']['sha1'] = 	sha1($data);

		$windowSize = 4;
		// "auto" windowsize
		/*
		$cntArr = Array();
		foreach(str_split($data) as $ch) {
			$cntArr[$ch]++;
		}
		$windowSize = max(12, min($cntArr));
		*/

		$ret['raw']['hints']['partialCrc32']['windowSize'] = $windowSize;
		$ret['raw']['hints']['partialCrc32']['crc32'] = Array();
		$idx = 0;
		while($windowSize<strlen($data)) {
			$a = array();
			$a['crc32'] = crc32(substr($data, -$windowSize));
			$ret['raw']['hints']['partialCrc32']['crc32'][] = $a;

			#$windowSize = ceil($windowSize*1.5);
			#$windowSize+= $ret['raw']['hints']['partialCrc32']['windowSize']+min($idx, $ret['raw']['hints']['partialCrc32']['windowSize']);
			$windowSize+= $ret['raw']['hints']['partialCrc32']['windowSize'];
			$idx++;
		}
		#var_dump($windowSize);


		$a = str_split($data);
		rsort($a);
		$orderedData = implode("", $a);

		$ret['ordered'] = Array();
		$ret['ordered']['hashes'] = Array();
		$ret['ordered']['hashes']['crc32'] =   	crc32($orderedData);
		$ret['ordered']['hints'] = Array();
		$ret['ordered']['hints']['partialSums'] = Array();

		#$windowSize = 12;
		// "auto" windowsize
		$cntArr = Array();
		foreach(str_split($data) as $ch) {
			$cntArr[$ch]++;
		}
		$windowSize = max(12, min($cntArr));
		#var_dump($windowSize);
		$windowSize = 4;	// 4 seems like a magic number, its the fastest in my tests

		$ret['ordered']['hints']['partialSums']['windowSize'] = $windowSize;
		$ret['ordered']['hints']['partialSums']['sums'] = Array();
		$slices = str_split($orderedData, $windowSize);
		foreach($slices as $slice) {
			$a = array();
			$a['sum'] = $this->binarySum($slice);
			$a['interval'] = Array(ord(min(str_split($slice))), ord(max(str_split($slice))));

			$a['dictionary'] = Array();
			foreach(array_unique(str_split($slice)) as $ch) {
				$a['dictionary'][] = ord($ch);
			}
			sort($a['dictionary']);

			$ret['ordered']['hints']['partialSums']['sums'][] = $a;
		}

		$ret['hints'] = Array();
		$ret['hints']['interval'] = Array(ord(min(str_split($data))), ord(max(str_split($data))));

		$ret['sum'] = $this->binarySum($data);

		#var_dump($ret); exit();
		return $ret;
	}

	protected function binarySum($data) {
		$ret = 0;
		$len = strlen($data);
		for($i=0; $i<$len; $i++) {
			$ret+= ord($data[$i]);
		}

		return $ret;
	}

}

class qad {
	protected $desc = Array();
	protected $cache = Array();

	public function decompress($desc) {
		$this->desc = $desc;
		$arr = array_fill(0, $this->desc['len'], 0);

		if($this->desc['ordered']['hints']['partialSums']) {
			$this->log(sprintf("Using partial sums for deduceArrayFromSum()\n"));
			$this->cache['partial'] = $arr;

			$windowIndex = 0;
			$windowSize = $this->desc['ordered']['hints']['partialSums']['windowSize'];
			$arr1 = array_fill(0, $windowSize, 0);

			/*
			foreach($this->desc['ordered']['hints']['partialSums']['sums'] as $k=>$v) {
				unset($this->desc['ordered']['hints']['partialSums']['sums'][$k]['dictionary']);
			}
			*/


			if($this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['dictionary']) {
				$this->log(sprintf("Using dictionary for deduceArrayFromSum()\n"));
				rsort($this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['dictionary']);
				$this->deduceArrayFromSum_withDict(Array($this, "gotSumDistribution_partial", Array('windowSize'=>$windowSize, 'windowIndex'=>$windowIndex, 'windowCount'=>count($this->desc['ordered']['hints']['partialSums']['sums']))),
					$arr1, $this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['sum'], 0, $windowSize,
					$this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['dictionary'][0],
					$this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['dictionary']
				);
			}else {
				$this->log(sprintf("Using interval for deduceArrayFromSum()\n"));
				$this->deduceArrayFromSum_onInterval(Array($this, "gotSumDistribution_partial", Array('windowSize'=>$windowSize, 'windowIndex'=>$windowIndex, 'windowCount'=>count($this->desc['ordered']['hints']['partialSums']['sums']))),
					$arr1, $this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['sum'], 0, $windowSize,
					$this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['interval'][1], $this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['interval'][0]
				);
			}
		}
		else {
			$this->log(sprintf("Using brute-force for deduceArrayFromSum()\n"));
			$this->deduceArrayFromSum_onInterval(Array($this, "gotSumDistribution"), $arr, $this->desc['sum'], 0, $this->desc['len'],
				$this->desc['hints']['interval'][1], $this->desc['hints']['interval'][0]
			);
		}
	}

	// @see http://stackoverflow.com/a/12651587/11301
	protected function deduceArrayFromSum_withDict($callback, $arr, $sum, $offset, $maxOffset, $li, $dict) {
		if($offset<=$maxOffset){
			if ($sum>0) {
				#var_dump($li); var_dump($dict); exit();
				foreach($dict as $i) {
					if ( $sum>=$i && $i<=$li) {
						$arr[$offset] = $i;
						$this->deduceArrayFromSum_withDict($callback, $arr, $sum-$i, $offset+1, $maxOffset, $i, $dict);
					}
				}
			}
			elseif ($sum==0) {
				$cbo = $callback;
				$cb = Array($cbo[0], $cbo[1]);
				unset($cbo[0]);
				unset($cbo[1]);
				call_user_func_array($cb, Array($arr, $cbo[2]));
			}
		}
	}

	protected function deduceArrayFromSum_onInterval($callback, $arr, $sum, $offset, $maxOffset, $li, $mi) {
		if($offset<=$maxOffset){
			if ($sum>0) {
				for($i=min($li, $sum); $i>=$mi; $i--) {
					if ( $sum>=$i) {
						$arr[$offset] = $i;
						$this->deduceArrayFromSum_onInterval($callback, $arr, $sum-$i, $offset+1, $maxOffset, $i, $mi);
					}
				}
			}
			elseif ($sum==0) {
				$cbo = $callback;
				$cb = Array($cbo[0], $cbo[1]);
				unset($cbo[0]);
				unset($cbo[1]);
				call_user_func_array($cb, Array($arr, $cbo[2]));
			}
		}
	}

	protected function gotSumDistribution_partial($arr, $options) {
		$szmincalc = (($options['windowIndex'])*$options['windowSize']);
		$szmaxcalc = (($options['windowIndex']+1)*$options['windowSize']);
		$szmax = min($this->desc['len'], $szmaxcalc);
		if($szmaxcalc!=$szmax) {
		}

		for($i=$szmincalc; $i<$szmax; $i++) {
			$this->cache['partial'][$i] = $arr[$i-$szmincalc];
		}

		$windowIndex = $options['windowIndex']+1;
		if($windowIndex==$options['windowCount']) {
			#var_dump($this->cache['partial']);
			#$this->log(sprintf("Found correct sum for '%s'\r", $this->reimplodeSafe($this->cache['partial'])));
			$this->log(sprintf("Found correct a sum for text\r"));
			$this->gotSumDistribution($this->cache['partial']);
			return;
		}

		$arr1 = array_fill(0, $options['windowSize'], 0);
		if($this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['dictionary']) {
			rsort($this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['dictionary']);
			$this->deduceArrayFromSum_withDict(Array($this, "gotSumDistribution_partial", Array('windowSize'=>$options['windowSize'], 'windowIndex'=>$windowIndex, 'windowCount'=>$options['windowCount'])),
				$arr1, $this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['sum'], 0, $options['windowSize'],
				$this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['dictionary'][0],
				$this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['dictionary']
			);
		}
		else {
			$this->deduceArrayFromSum_onInterval(Array($this, "gotSumDistribution_partial", Array('windowSize'=>$options['windowSize'], 'windowIndex'=>$windowIndex, 'windowCount'=>$options['windowCount'])),
				$arr1, $this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['sum'], 0, $options['windowSize'],
				$this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['interval'][1], $this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['interval'][0]);
		}

	}

	protected function gotSumDistribution($arr) {
		$data =  $this->reimplode($arr);
		if(crc32($data)===$this->desc['ordered']['hashes']['crc32']) {
			$this->log("\n\n");
			$this->log(sprintf("[ord]    Found a crc32 match with '%s'\n", $data));
			$this->log(sprintf("[ord]    Start permutations\n"));

			if($this->desc['raw']['hints']['partialCrc32']) {
				$this->cache['pc_permuteWithPartialSums']['startTime'] = microtime(true);
				$this->log(sprintf("[ord]    Using partialCrc32 to compute all permutations\n"));

				$s = $this->reimplode($arr);
				$this->pc_permuteWithPartialSums_faster($s, "");
			}
			else {
				$this->cache['pc_permute']['startTime'] = microtime(true);
				$this->log(sprintf("[ord]    Using brute-force to compute all possible permutations\n"));
				$this->pc_permute($arr);
			}
		}
	}


	/*
	seems baed on http://www.geekviewpoint.com/java/numbers/permutation
	C implementation: http://stackoverflow.com/a/11213654/11301
	also, look at http://alistairisrael.wordpress.com/2009/09/22/simple-efficient-pnk-algorithm/    (SEP(n,k) Algorithm Illustrated)


	@see also, PHP: http://stackoverflow.com/a/2617080/11301
	*/
	protected function pc_permuteWithPartialSums_faster($string, $perms = "", $depth=0) {
		$partialCrc32 = $this->desc['raw']['hints']['partialCrc32'];
		$this->cache[__FUNCTION__]['loops']++;
		$this->cache[__FUNCTION__]['partialPerms']++;

		if (!$string) {
			$this->cache[__FUNCTION__]['perms']++;
			$this->gotPermutation($perms);
		}  else {
			$lperms = strlen($perms);
			if( $lperms > $partialCrc32['windowSize']) {
				$crc32ok = true;
				$crc32failIndex = 0;

				$idx = (int)(floor(($lperms-1)/$partialCrc32['windowSize'])-1);
				$windowSize = ($idx+1) * $partialCrc32['windowSize'];

				$slice = substr($perms , -$windowSize);
				if(crc32($slice) != $partialCrc32['crc32'][$idx]['crc32']) {
					$crc32ok = false;
					$crc32failIndex = $this->desc['len'] - $windowSize;

					if($this->cache[__FUNCTION__]['loops']>10000) {
						$this->log(sprintf("[FastCheck]: Slice '%s' on level %d mismatched @%d, recdepth:%d, partialPerms:%d\r",
								substr(preg_replace("/[^a-zA-Z0-9]/", "_", $slice), 0, 30),
								$idx, $crc32failIndex, $depth, $this->cache[__FUNCTION__]['partialPerms']));
						$this->cache[__FUNCTION__]['loops'] = 0;
					}
				}

				if(!$crc32ok) {
					return 1;
				}
			}


			$lc = null;
			for ($i = strlen($string) - 1; $i >= 0; --$i) {
				 if($lc === $string[$i]){
					continue;
				 }

				 $newitems = $string;
				 $newperms = $perms;

				 $foo = $newitems[$i];
				 $lc = $foo;
				 $newitems = substr($newitems, 0, $i) . substr($newitems, $i+1);
				 $newperms = $foo.$newperms;
				 $retLvl = $this->pc_permuteWithPartialSums_faster($newitems, $newperms, $depth+1);

				 if($retLvl) {
					return $retLvl-1;
				 }
			 }
		}
	}

	protected function pc_permuteWithPartialSums($string, $perms = "", $depth=0) {
		$partialCrc32 = $this->desc['raw']['hints']['partialCrc32'];

		if (!$string) {
			$this->cache[__FUNCTION__]['loops']++;
			$this->cache[__FUNCTION__]['perms']++;

			$crc32ok = true;
			$crc32failIndex = 0;

			$windowSize = $partialCrc32['windowSize'];
			$lws = $windowSize;
			$idx = 0;
			while($windowSize<$this->desc['len']) {
				if(crc32(substr($perms, -$windowSize))!=$partialCrc32['crc32'][$idx]['crc32']) {
					#print_r($perms);
					$crc32ok = false;
					$crc32failIndex = $this->desc['len'] - $windowSize;
					$this->log(sprintf("Slice %s[%d] / %s mismatched @ %d, recdepth:%d\r", md5($perms), $idx, str_replace("\n", "", substr($perms, -$windowSize)), $crc32failIndex, $depth));
					break;
				}

				$lws = $windowSize;
				#$windowSize = ceil($windowSize*1.5);
				#$windowSize+= $partialCrc32['windowSize']+min($idx, $partialCrc32['windowSize']);
				$windowSize+= $partialCrc32['windowSize'];

				$idx++;
				#if($idx) {
				#	var_dump($windowSize); exit();
				#}


			}

			if($this->cache[__FUNCTION__]['loops']>250) {
				$ts = microtime(true);
				$ops = $this->cache[__FUNCTION__]['perms']/($ts-$this->cache[__FUNCTION__]['startTime']);
				#$this->log(sprintf("Perm: '%s'[l:%d][fidx:%d][ops:%.1f][ttl:%d]\r", $this->reimplodeSafeStr($perms), strlen($perms), $crc32failIndex, $ops, $this->cache[__FUNCTION__]['perms']));
				$this->log(sprintf("Perm: '%s'[l:%d][fidx:%d][ops:%.1f][ttl:%d]\r", "", strlen($perms), $crc32failIndex, $ops, $this->cache[__FUNCTION__]['perms']));
				$this->cache[__FUNCTION__]['loops'] = 0;
			}

			if($crc32ok) {
				$this->gotPermutation($perms);
			}
			else {
				return $crc32failIndex;
			}
		}  else {
			$lc = null;
			for ($i = strlen($string) - 1; $i >= 0; --$i) {
				 $newitems = $string;
				 $newperms = $perms;

				 if($lc === $newitems[$i]){
					continue;
				 }

				 $foo = $newitems[$i];
				 $lc = $foo;
				 $newitems = substr($newitems, 0, $i) . substr($newitems, $i+1);
				 $newperms = $foo.$newperms;
				 $retLvl = $this->pc_permuteWithPartialSums($newitems, $newperms, $depth+1);

				 if($retLvl) {
					return $retLvl-1;
				 }
			 }
		}
	}

	protected function pc_permute($items, $perms = array(), $options = Array()) {
		if (empty($items)) {
			$this->cache[__FUNCTION__]['loops']++;
			$this->cache[__FUNCTION__]['perms']++;
			if($this->cache[__FUNCTION__]['loops']==2500) {
				$s = $this->reimplodeSafe($perms);
				$ts = microtime(true);
				$ops = $this->cache[__FUNCTION__]['perms']/($ts-$this->cache[__FUNCTION__]['startTime']);
				#$this->log(sprintf("Perm: '%s'[l:%d][ops:%.1f][ttl:%d]\r", $s, strlen($s), $ops, $this->cache[__FUNCTION__]['perms']));
				$this->log(sprintf("Perm: '%s'[l:%d][ops:%.1f][ttl:%d]\r", "", strlen($s), $ops, $this->cache[__FUNCTION__]['perms']));
				$this->cache[__FUNCTION__]['loops'] = 0;
			}
			$this->gotPermutation($this->reimplode($perms));
		}  else {
			for ($i = count($items) - 1; $i >= 0; --$i) {
				 $newitems = $items;
				 $newperms = $perms;
				 list($foo) = array_splice($newitems, $i, 1);
				 array_unshift($newperms, $foo);
				 $this->pc_permute($newitems, $newperms, $options);
			 }
		}
	}


	protected function gotPermutation($data) {
		#var_dump(crc32($data)); var_dump($this->desc['raw']['hashes']['crc32']); exit();

		if(crc32($data)===$this->desc['raw']['hashes']['crc32']) {
			$this->log("\n\n");
			$this->log(sprintf("[raw]    Found a crc32 match with '%s'\n", $data));
			if(md5($data)===$this->desc['raw']['hashes']['md5']) {
				$this->log(sprintf("[raw]    Found a md5 match with '%s'\n", $data));
				if(sha1($data)===$this->desc['raw']['hashes']['sha1']) {
					$this->log(sprintf("[raw]    Found a sha1 match with '%s'\n", $data));
					$this->log(sprintf("[raw]    Data decomrpess finished\n"));
					$this->foundMatch($data);
				}
			}
		}
	}

	protected function foundMatch($dataArr) {
		printf("\n\n");
		var_dump($data);
		exit();
	}

	protected function reimplode($arr) {
		$val = Array();
		foreach($arr as $v) {
			$val[] = chr($v);
		}

		return implode("", $val);
	}

	protected function reimplodeSafe($arr) {
		$val = Array();
		foreach($arr as $v) {
			if($v>=0x20 && $v<=0xfe) {
				$val[] = chr($v);
			}
			else {
				$val[] = "?";
			}
		}

		return implode("", $val);
	}

	protected function reimplodeSafeStr($str) {
		return "";
		/*
		$arr = str_split($str);
		foreach($arr as $k=>$v) {
			$arr[$k] = ord($v);
		}
		return $this->reimplodeSafe($arr);
		*/
	}


	protected function log($str) {
		$tm = microtime(true);
		if(!$this->cache[__FUNCTION__]['time']) {
			$this->cache[__FUNCTION__]['time'] = $tm;
		}

		printf("[%6.3f] %s", $tm - $this->cache[__FUNCTION__]['time'], $str);
		flush();
	}
}

ini_set("error_reporting", INI_ALL);
ini_set('xdebug.max_nesting_level', 20480);


$compressor = new qac();
#file_put_contents("arch.txt", serialize($compressor->compress("ana")));
#file_put_contents("arch.txt", serialize($compressor->compress("mere")));
#file_put_contents("arch.txt", serialize($compressor->compress("anaaremere")));
#file_put_contents("arch.txt", serialize($compressor->compress("anaaremerele")));	# 0.2s
#file_put_contents("arch.txt", serialize($compressor->compress("anaaremereghere"))); # 0.89s
#file_put_contents("arch.txt", serialize($compressor->compress("anaaremereanaaremereanaaremere")));	# 1.5s
#file_put_contents("arch.txt", serialize($compressor->compress("anaaremereanaaremereanaaremereanaaremereanaaremereanaaremereanaaremereanaaremereanaaremereanaaremere")));	# 0.14s

#file_put_contents("arch.txt", serialize($compressor->compress("CbC66")));
#file_put_contents("arch.txt", serialize($compressor->compress("CbC669xGds")));
#file_put_contents("arch.txt", serialize($compressor->compress("CbC669xGdsrVxVz"))); # 0.8
#file_put_contents("arch.txt", serialize($compressor->compress("CbC669xGdsrVxVzewGmtAdgRN"))); # 1.2s
#file_put_contents("arch.txt", serialize($compressor->compress("CbC669xGdsrVxVzewGmtAdgRNPXyHHCh8HG9aGZAvyc73pHSmB"))); # 37s
#file_put_contents("arch.txt", serialize($compressor->compress("CbC669xGdsrVxVzewGmtAdgRNPXyHHCh8HG9aGZAvyc73pHSmBuufV6DSNzRwtc3hQsD6vMKC3fasWbkBUtnjKSSRvtA8eED5yzu")));

#file_put_contents("arch.txt", serialize($compressor->compress("\xa0\x32\x10\x16\x1f\x0e\xb6\x82\x8c\xb3"))); # 0.1s
#file_put_contents("arch.txt", serialize($compressor->compress("\x2c\x9a\x4e\xc7\xf8\xc5\xa1\xb8\x4c\x6d\x29\x0e\x4c\x4e\x00"))); # 0.06s
#file_put_contents("arch.txt", serialize($compressor->compress("\x77\x07\xe6\x37\xff\xec\x2c\x20\xf5\x40\x40\xb6\x41\x40\x9f\x6d\x4d\x83\x7b\xb3"))); # 6s
#file_put_contents("arch.txt", serialize($compressor->compress("\xb8\xe9\x17\x22\x9a\x77\x35\x6d\x99\x66\x4c\x6d\xae\x32\x16\x1e\x0e\xf5\x71\x41\x66\x75\x7d\xd4\x0c"))); # 6s
file_put_contents("arch.txt", serialize($compressor->compress("\x9c\x8f\xac\xe2\x42\x70\xc9\x7a\x85\x9d\x62\xb5\x0d\x2f\x87\xc1\x55\x68\x5e\x4f\xfe\xd7\xd1\xe1\x3e\xf8\x5a\x42\x29\x75\xf8\x72\x9f\x11\x52\x54\x49\xf0\x00\x7b\x24\x61\xab\xf5\x70\x5f\x04\x3c\x25\x90"))); # 135s

#file_put_contents("arch.txt", serialize($compressor->compress(file_get_contents("in01.txt")))); # 24s
#file_put_contents("arch.txt", serialize($compressor->compress(file_get_contents("in02.txt"))));
#file_put_contents("arch.txt", serialize($compressor->compress(file_get_contents("in03.txt"))));

$decompressor = new qad();
$decompressor->decompress(unserialize(file_get_contents("arch.txt")));

printf("\n\n done, no decompression possible\n\n");
