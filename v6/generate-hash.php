<?php
/**
 * run with:
 *  reset && php -f ./generate-hash.php autoGenerateHash=autoGenerateHash_v2 action=autoRebuildStr
 */


// $letter = 'a'; $str = "abacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabacabac";
// $letter = 'a'; $str = "Ana are mere si pere si banane si muraturi si alte bunataturi.Ana are mere si pere si banane si muraturi si alte bunataturi.Ana are mere si pere si banane si muraturi si alte bunataturi.Ana are mere si pere si banane si muraturi si alte bunataturi.";
// $letter = 'a'; $str = "Ana are mere si pere si banane si muraturi si alte bunataturi.";
// $letter = 'a'; $str = "Ana are mere si pere si banane.";
// $letter = 'a'; $str = "abacabacabacabacabacabacabacabacabacabac";
$letter = 'a'; $str = "abacabacabacabacabacabac";
// $letter = 'a'; $str = "abacabacabacabacabac";
// $letter = '.'; $str = ".b.c.b.c";
// $letter = '.'; $str = ".b..b.";


$R = [];
$cliarg = implode("&", array_slice($argv, 1));
parse_str($cliarg, $R);

// function myhash($str) {
//     return crc32($str);
// }

function myhash1($str, $letter) {
    return crc32($str);

    $sum = 0;
    for ($i=0; $i<strlen($str); $i++) {
        // $sum = $i + (ord($str[$i]) ^ $sum);
        $sum = $sum + ($str[$i]==$letter?$i+1:-1);
    }

    return $sum;
}

function myhash2($str, $letter) {
    return md5($str);
}

function generateHash($str, $letter) {
    $hash1 = myhash1($str, $letter);
    $hash2 = myhash2($str, $letter);
    $nstr = str_replace($letter, '', $str);

    return [
        $letter,
        $nstr,
        strlen($str) - strlen($nstr),
        $hash1,
        $hash2,
        '01'
    ];
}


function autoGenerateHash_v1($str) {
    $letterBins = [];
    $strlen = strlen($str);
    for ($i=0; $i<$strlen; $i++) {
        if (!array_key_exists($str[$i], $letterBins)) {
            $letterBins[$str[$i]] = 0;
        }
        $letterBins[$str[$i]]++;
    }

    ksort($letterBins);

    $hashes = [];
    foreach ($letterBins as $letter=>$x) {
        $h = generateHash($str, $letter);
        $str = $h[1];
        $hashes[]= $h;
    }


    return $hashes;
}


function autoGenerateHash_v2($str) {
    $letterBins = [];
    $strlen = strlen($str);
    for ($i=0; $i<$strlen; $i++) {
        if (!array_key_exists($str[$i], $letterBins)) {
            $letterBins[$str[$i]] = 0;
        }
        $letterBins[$str[$i]]++;
    }

    krsort($letterBins);

    $hashes = [];
    foreach ($letterBins as $letter=>$x) {
        $h = generateHash($str, $letter);
        $str = $h[1];
        $hashes[]= $h;
    }

    return $hashes;
}

switch($R['autoGenerateHash']) {
    case 'autoGenerateHash_v2':
        $hashesData = autoGenerateHash_v2($str);
    break;

    case 'autoGenerateHash_v1':
    default:
        $hashesData = autoGenerateHash_v1($str);
    break;
}
$hashesData = array_map(function($h) {
    $h[1] = null;
    return $h;
}, $hashesData);

$compressedString = "";
foreach ($hashesData as $hashData) {
    $compressedString.= pack("CLLL", $hashData[0], $hashData[2], $hashData[3], $hashData[4]).$hashData[5];
}
printf("\n compresses to %d bytes, from %d bytes", strlen($compressedString), strlen($str));

printf("\n\n -------------------------------------------------\n\n");

function autoRebuildStr($hashesData) {
    $times = [];
    $str = "";
    foreach (array_reverse($hashesData) as $idx=>$hashData) {
        $t1 = microtime(true);
        $hashData[1] = $str;
        printf("\n>>> [%d/%d] rebuildStr: %s", $idx, count($hashesData), json_encode($hashData));
        $str = rebuildStr($hashData);

        $t2 = microtime(true);
        $times[]= $t2-$t1;
        printf("\n>>> hash matched for str: %s", $str);
    }

    printf("\n!!! str=%s", $str);
    printf("\n!!! took %.1fs", array_sum($times));
    return $str;
}

function rebuildStr($hashData) {
    list($letter, $nstr, $strlenDiff, $hash1, $hash2, $version) = $hashData;

    $strPositions = [];
    $strPositionMax = 0;
    for ($i=0; $i<$strlenDiff; $i++) {
        $strPositions[$i] = $i;
        $strPositionMax = $i;
    }


    $initialStrlen = strlen($nstr) + $strlenDiff;
    $lastJ = null;
    printf("\n");
    do {
        $str = str_repeat('X', $initialStrlen); // TODO: we should initialize this only once

        $ni = 0;
        for ($i=0; $i<$initialStrlen; $i++) {
            if (in_array($i, $strPositions)) {  // TODO: can we skip in_array?
                $str[$i] = $letter;
            }
            else {
                $str[$i] = $nstr[$ni];
                $ni++;
            }
        }

        $nhash1 = myhash1($str, $letter);
        // printf("\n> %s [%s]", $str, $nhash1);
        // printf("\n> %s", $str);
        printf("\r> %s", $str);

        $hashFound = false;
        // if ($nhash1>$hash1) { // optimization
        //     $iterated = false;
        //     if (!$iterated) {
        //         for ($j=0; $j<$strlenDiff-1; $j++) {
        //             if ($strPositions[$j]+1<$strPositions[$j+1]) {
        //                 $strPositions[$j]++;
        //                 $iterated = true;
        //                 $lastJ = $j;
        //                 // printf("\n loop, %d, %d", $j, $strPositions[$j]);

        //                 for ($j1=0; $j1<$j; $j1++) {
        //                     $strPositions[$j1] = $j1;
        //                 }
        //                 break;
        //             }
        //         }
        //     }

        //     if (!$iterated) {
        //         if ($strPositions[$strPositionMax]<$initialStrlen-1) {
        //             $strPositions[$strPositionMax]++;
        //             $lastJ = null;
        //             for ($j=0; $j<count($strPositions)-1; $j++) {
        //                 $strPositions[$j] = $j;
        //             }
        //             // printf("\n incr");
        //         }
        //         else {
        //             die("\nFINISH< NOTHING FOUND\n\n");
        //         }
        //     }
        //     continue;
        // }

        if ($nhash1==$hash1 && myhash2($str, $letter)==$hash2) {
            $hashFound = true;
            return $str;
        }
        else {
            // v1
            // $iterated = false;
            // for ($j=$strlenDiff-2; $j>=0; $j--) {
            //     if ($strPositions[$j]+1<$strPositions[$j+1]) {
            //         $strPositions[$j]++;
            //         $iterated = true;
            //         break;
            //     }
            // }

            // if (!$iterated) {
            //     if ($strPositions[$strPositionMax]<$initialStrlen-1) {
            //         $strPositions[$strPositionMax]++;
            //         for ($j=0; $j<count($strPositions)-1; $j++) {
            //             $strPositions[$j] = $j;
            //         }
            //     }
            //     else {
            //         die("FINISH< NOTHING FOUND");
            //     }
            // }


            $iterated = false;
            if (!$iterated) {
                for ($j=0; $j<$strlenDiff-1; $j++) {
                    if ($strPositions[$j]+1<$strPositions[$j+1]) {
                        $strPositions[$j]++;
                        $iterated = true;
                        $lastJ = $j;
                        // printf("\n loop, %d, %d", $j, $strPositions[$j]);

                        for ($j1=0; $j1<$j; $j1++) {
                            $strPositions[$j1] = $j1;
                        }
                        break;
                    }
                }
            }

            if (!$iterated) {
                if ($strPositions[$strPositionMax]<$initialStrlen-1) {
                    $strPositions[$strPositionMax]++;
                    $lastJ = null;
                    for ($j=0; $j<count($strPositions)-1; $j++) {
                        $strPositions[$j] = $j;
                    }
                    // printf("\n incr");
                }
                else {
                    die("\nFINISH< NOTHING FOUND\n\n");
                }
            }
        }
    } while(!$hashFound);

    die("\n\nFOUND !!!!!!\n\n");

}

if ($R['action']=='autoRebuildStr') {
    autoRebuildStr($hashesData);
}
echo "\n\n";
