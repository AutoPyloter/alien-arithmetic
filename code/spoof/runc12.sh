#!/bin/bash
cd "$(dirname "$0")"
w() { for i in $(seq 0 4); do a=$(( $1 + i*90000000000 )); b=$(( a + 90000000000 )); ./descartes_cores $a $b >> c12_$2.txt 2>> ce12_$2.txt; done; }
w 100000000000 A &
w 550000000000 B &
wait
