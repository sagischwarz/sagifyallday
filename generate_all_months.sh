#!/bin/bash

mkdir -p monthly_puzzles

generate_month() {
    month=$1
    echo "Generating puzzles for month $month..."
    python3 german_word_generator.py -y -m $month >monthly_puzzles/$month.txt
    echo "Finished generating puzzles for month $month"
}

export -f generate_month

echo {1..12} | tr ' ' '\n' | xargs -P 12 -I {} bash -c 'generate_month {}'

echo "All puzzles have been generated successfully!"
echo "Results are saved in the monthly_puzzles directory."
