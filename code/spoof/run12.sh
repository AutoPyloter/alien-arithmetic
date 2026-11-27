#!/bin/bash
# iki çekirdek, her biri 9 parça; her parça bitince e*.txt'ye satır yazar
cd "$(dirname "$0")"
w() { for i in $(seq 0 8); do a=$(( $1 + i*50000000000 )); b=$(( a + 50000000000 )); ./descartes_squares $a $b >> r12_$2.txt 2>> e12_$2.txt; done; }
w 100000000000 A &
w 550000000000 B &
wait
