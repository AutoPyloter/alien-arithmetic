#!/bin/bash
cd "$(dirname "$0")"
w() { for i in $(seq 0 8); do a=$(( $1 + i*500000000000 )); b=$(( a + 500000000000 )); ./descartes_cores $a $b >> c13_$2.txt 2>> ce13_$2.txt; done; }
w 1000000000000 A &
w 5500000000000 B &
wait
