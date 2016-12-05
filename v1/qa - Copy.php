<?php

/**
- deduceArrayFromSum poate fi optimizat: 
	- paralelizare
	- 
	- permutarile pot fi accelerate punand hash-uri mici(crc32) pt fiecare 10 caractere in lista de hint-uri

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
		
		$ret['ordered']['hints']['partialSums']['windowSize'] = $windowSize;
		$ret['ordered']['hints']['partialSums']['sums'] = Array();
		$slices = str_split($orderedData, $windowSize);
		foreach($slices as $slice) {
			$a = array();
			$a['sum'] = $this->binarySum($slice);
			$a['interval'] = Array(ord(min(str_split($slice))), ord(max(str_split($slice))));
			$ret['ordered']['hints']['partialSums']['sums'][] = $a;
		}
		
		$ret['hints'] = Array();
		$ret['hints']['interval'] = Array(ord(min(str_split($data))), ord(max(str_split($data))));
		$ret['hints']['dictionary'] = implode("", array_unique(str_split($orderedData)));
		
		
		$ret['sum'] = $this->binarySum($data);
		
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
		$arr = array_fill(0, $desc['len'], 0);
		
		if($desc['ordered']['hints']['partialSums']) {
			$this->log(sprintf("Using partial sums for deduceArrayFromSum()\n"));
			$this->cache['partial'] = $arr;
			
			$windowIndex = 0;
			$windowSize = $desc['ordered']['hints']['partialSums']['windowSize'];
			$arr1 = array_fill(0, $windowSize, 0);
			$this->deduceArrayFromSum(Array($this, "gotSumDistribution_partial", Array('windowSize'=>$windowSize, 'windowIndex'=>$windowIndex, 'windowCount'=>count($desc['ordered']['hints']['partialSums']['sums']))), 
				$arr1, $desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['sum'], 0, $windowSize, $desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['interval'][1], $desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['interval'][0]);
		}
		else {
			$this->log(sprintf("Using brute-force for deduceArrayFromSum()\n"));
			$this->deduceArrayFromSum(Array($this, "gotSumDistribution"), $arr, $desc['sum'], 0, $desc['len'], $desc['hints']['interval'][1], $desc['hints']['interval'][0]);
		}
	}
	
	protected function deduceArrayFromSum($callback, $arr, $sum, $offset, $maxOffset, $li, $mi) {
		if($offset<=$maxOffset){
			if ($sum>0) {
				for($i=min($li, $sum); $i>=$mi; $i--) {
					if ( $sum>=$i) {
						$arr[$offset] = $i;
						$this->deduceArrayFromSum($callback, $arr, $sum-$i, $offset+1, $maxOffset, $i, $mi);
					}
				}
			}
			if ($sum==0) {
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
			$this->log(sprintf("Found correct sum for '%s'\r", $this->reimplode($this->cache['partial'])));
			$this->gotSumDistribution($this->cache['partial']);
			return;
		}
		
		$arr1 = array_fill(0, $options['windowSize'], 0);
		$this->deduceArrayFromSum(Array($this, "gotSumDistribution_partial", Array('windowSize'=>$options['windowSize'], 'windowIndex'=>$windowIndex, 'windowCount'=>$options['windowCount'])), 
			$arr1, $this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['sum'], 0, $options['windowSize'], $this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['interval'][1], $this->desc['ordered']['hints']['partialSums']['sums'][$windowIndex]['interval'][0]);
	}
	
	protected function gotSumDistribution($arr) {
		$data =  $this->reimplode($arr);
		if(crc32($data)===$this->desc['ordered']['hashes']['crc32']) {
			$this->log(sprintf("[ord]    Found a crc32 match with '%s'\n", $data));
			$this->log(sprintf("[ord]    Start permutations\n"));
			$this->pc_permute($arr);
		}
	}
	
	
	/*
	seems baed on http://www.geekviewpoint.com/java/numbers/permutation
	C implementation: http://stackoverflow.com/a/11213654/11301
	also, look at http://alistairisrael.wordpress.com/2009/09/22/simple-efficient-pnk-algorithm/    (SEP(n,k) Algorithm Illustrated)
	*/
	protected function pc_permute($items, $perms = array( ), $options = Array()) {
		if (empty($items)) { 
			$this->cache[__METHOD__]['loops']++;
			$this->cache[__METHOD__]['perms']++;
			if($this->cache[__METHOD__]['loops']==2500) {
				$s = $this->reimplode($perms);
				$this->log(sprintf("Perm: '%s'[%d][%d]\r", $s, strlen($s), $this->cache[__METHOD__]['perms']));
				$this->cache[__METHOD__]['loops'] = 0;
			}
			$this->gotPermutation($perms);
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

	protected function gotPermutation($arr) {
		#$this->dbg($arr);
		
		$dataArr = Array();
		foreach($arr as $v) {
			$dataArr[] = chr($v);
		}
		$data = implode("", $dataArr);
		
		#var_dump(crc32($data)); var_dump($this->desc['raw']['hashes']['crc32']); exit();
		
		if(crc32($data)===$this->desc['raw']['hashes']['crc32']) {
			$this->log(sprintf("[raw]    Found a crc32 match with '%s'\n", $data));
			if(md5($data)===$this->desc['raw']['hashes']['md5']) {
				$this->log(sprintf("[raw]    Found a md5 match with '%s'\n", $data));
				if(sha1($data)===$this->desc['raw']['hashes']['sha1']) {
					$this->log(sprintf("[raw]    Found a sha1 match with '%s'\n", $data));
					$this->log(sprintf("[raw]    Data decomrpess finished\n"));
					$this->foundMatch($dataArr);
				}
			}
		}
	}
	
	protected function foundMatch($dataArr) {
		exit();
	}
	
	protected function reimplode($arr) {
		$val = Array();
		foreach($arr as $v) {
			$val[] = chr($v);
		}
		
		return implode("", $val);
	}

	
	protected function log($str) {
		$tm = microtime(true);
		if(!$this->cache[__METHOD__]['time']) {
			$this->cache[__METHOD__]['time'] = $tm;
		}
	
		printf("[%6.3f] %s", $tm - $this->cache[__METHOD__]['time'], $str);
		flush();
	}
}

ini_set("error_reporting", INI_ALL);
ini_set('xdebug.max_nesting_level', 2048);


$compressor = new qac();
#file_put_contents("arch.txt", serialize($compressor->compress("ana")));
#file_put_contents("arch.txt", serialize($compressor->compress("mere")));
#file_put_contents("arch.txt", serialize($compressor->compress("anaaremere")));
file_put_contents("arch.txt", serialize($compressor->compress("anaaremereanaaremereanaaremereanaaremereanaaremereanaaremereanaaremereanaaremereanaaremereanaaremere")));

$decompressor = new qad();
$decompressor->decompress(unserialize(file_get_contents("arch.txt")));
