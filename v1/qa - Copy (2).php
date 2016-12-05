<?php

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
		
		$ret['hints'] = Array();
		$ret['hints']['interval'] = Array(ord(min(str_split($data))), ord(max(str_split($data))));
		$ret['hints']['dictionary'] = implode("", array_unique(str_split($orderedData)));
		
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
	
	public function decompress($desc) {
		$this->desc = $desc;
		$arr = array_fill(0, $desc['len'], 0);
		$this->deduceArrayFromSum($arr, $desc['sum'], 0, $desc['len'], $desc['hints']['interval'][1], $desc['hints']['interval'][0]);
	}
	
	protected function deduceArrayFromSum($arr, $sum, $offset, $maxOffset, $li, $mi) {
		if($offset<=$maxOffset){
			if ($sum>0) {
				for($i=min($li, $sum); $i>=$mi; $i--) {
					if ( $sum>=$i) {
						$arr[$offset] = $i;
						$this->deduceArrayFromSum($arr, $sum-$i, $offset+1, $maxOffset, $i, $mi);
					}
				}
			}
			if ($sum==0) {
				$this->gotSumDistribution($arr);
			}
		}
	}
	
	protected function gotSumDistribution($arr) {
		$dataArr = Array();
		foreach($arr as $v) {
			$dataArr[] = chr($v);
		}
		$data = implode("", $dataArr);
		
		if(crc32($data)===$this->desc['ordered']['hashes']['crc32']) {
			printf("[ord]    Found a crc32 match with '%s'\n", $data);
			printf("[ord]    Start permutations\n");
			$this->pc_permute($arr);
		}
	}
	
	protected function pc_permute($items, $perms = array( )) {
		if (empty($items)) { 
			#printf("Got %s<br/>", implode(", ", $perms));
			$this->gotPermutation($perms);
		}  else {
			for ($i = count($items) - 1; $i >= 0; --$i) {
				 $newitems = $items;
				 $newperms = $perms;
				 list($foo) = array_splice($newitems, $i, 1);
				 array_unshift($newperms, $foo);
				 $this->pc_permute($newitems, $newperms);
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
			printf("[raw]    Found a crc32 match with '%s'\n", $data);
			if(md5($data)===$this->desc['raw']['hashes']['md5']) {
				printf("[raw]    Found a md5 match with '%s'\n", $data);
				if(sha1($data)===$this->desc['raw']['hashes']['sha1']) {
					printf("[raw]    Found a sha1 match with '%s'\n", $data);
					printf("[raw]    Data decomrpess finished\n");
					$this->foundMatch($dataArr);
				}
			}
		}
	}
	
	protected function foundMatch($dataArr) {
		exit();
	}
	
	protected function dbg($arr) {
		#printf("Found: %s\n", implode(", ", $arr));
		
		$val = Array();
		foreach($arr as $v) {
			$val[] = chr($v);
		}
		
		printf("Found: %s\r", implode("", $val));
	}
}

ini_set("error_reporting", INI_ALL);


$compressor = new qac();
#file_put_contents("arch.txt", serialize($compressor->compress("ana")));
#file_put_contents("arch.txt", serialize($compressor->compress("mere")));
file_put_contents("arch.txt", serialize($compressor->compress("anaaremere")));
#file_put_contents("arch.txt", serialize($compressor->compress("anaaremereanaaremereanaaremereanaaremereanaaremereanaaremereanaaremereanaaremereanaaremereanaaremere")));

$decompressor = new qad();
$decompressor->decompress(unserialize(file_get_contents("arch.txt")));
