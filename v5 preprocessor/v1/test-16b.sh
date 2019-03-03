#!/bin/bash

# for benchmarking, use something like:
#python3 -mtimeit -s'import preprocess100' 'preprocess100.test_algo_nocompress(preprocess100.data, preprocess100.preprocess_012, preprocess100.unpreprocess_100)';


function runtest() {
    local INDEX=$1;
    echo "####################################################################";
    python3 -mtimeit -s'import preprocess100' --number=1 --repeat=1 "preprocess100.data=preprocess100.datas[$INDEX]; newdata=preprocess100.test_algo_nocompress(preprocess100.data, preprocess100.preprocess_012, preprocess100.unpreprocess_100);";
}

runtest 0;
runtest 1;
