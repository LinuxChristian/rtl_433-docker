#!/bin/bash
cd rtl_433/
mkdir build
cd build
cmake ../
make
make install
