#!/bin/bash
timet=$2

function testAll() {
    for file in $@ -r;do 
        if test -f $file;then 
            echo --------------------------------------------------
            # echo $file
	    cd optimathsat_bin/bin/
            start=$[$(date +%s%N)/1000000]
            timeout $timet ./optimathsat -optimization=true -model_generation=true -opt.strategy=bin ../../$file || { echo "command failed"; }
	    cd ../../
            end=$[$(date +%s%N)/1000000]
            take=$(( end - start ))
            echo $file : ${take} ms.
        fi
        if test -d $file;then
            testAll $file/*
        fi
    done
}

testAll $1
