#!/bin/bash

INPUT_CHOMSKY_FILE=$1
INPUT_GRAPH_FILE=$2
OUTPUT_FILE=$3

python3 ./FormalLangMatrixMult/main.py $INPUT_CHOMSKY_FILE $INPUT_GRAPH_FILE $OUTPUT_FILE