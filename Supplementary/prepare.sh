#!/bin/bash

# basic mode
echo "prepare code..."
git clone https://github.com/fuqi-jia/cdcl_ocac.git
unzip benchmarks.zip

echo "split..."
python split.py benchmarks SAT_RAND_10000_s50 50
cp -r SAT_RAND_10000_s50 CVC5_SAT_RAND_10000_s50

echo "add tag..."
python add_tag.py CVC5_SAT_RAND_10000_s50

# build cdcl_ocac
echo "build cdcl_ocac..."
cd cdcl_ocac/
mkdir 1200
rm -rf build/
pip install toml
pip install pyparsing
./configure.sh --auto-download --poly --cocoa
cd build/
make -j12
cd ../../

if [ $# -eq 1 ];
then
    # build other solvers
    # z3
    echo "build z3..."
    wget https://github.com/Z3Prover/z3/archive/refs/tags/z3-4.13.0.zip
    unzip z3-4.13.0.zip
    cd z3-z3-4.13.0/
    python scripts/mk_make.py
    cd build/
    make -j120
    cd ../../
    mv z3-z3-4.13.0/ z3/
    cp z3_run.sh z3/
    mv z3/z3_run.sh z3/run.sh
    mkdir z3/1200

    # optimathsat
    echo "build optimathsat..."
    wget https://optimathsat.disi.unitn.it/releases/optimathsat-1.7.4/optimathsat-1.7.4-linux-64-bit.tar.gz
    tar -xvf optimathsat-1.7.4-linux-64-bit.tar.gz
    mv optimathsat-1.7.4-linux-64-bit/ optimathsat/
    cp -r optimathsat/ optimathsat_bin/
    mv optimathsat/ optimathsat_lin/
    cp optimathsat_bin_run.sh optimathsat_bin/
    cp optimathsat_lin_run.sh optimathsat_lin/
    mv optimathsat_bin/optimathsat_bin_run.sh optimathsat_bin/run.sh
    mv optimathsat_lin/optimathsat_lin_run.sh optimathsat_lin/run.sh
    mkdir optimathsat_bin/1200
    mkdir optimathsat_lin/1200
fi
