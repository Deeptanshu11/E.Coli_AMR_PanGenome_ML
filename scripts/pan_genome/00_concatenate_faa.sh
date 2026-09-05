#!/bin/bash
set -euo pipefail

# Concatenate protein FASTA files before CD-HIT clustering.
# Usage: ./00_concatenate_faa.sh /path/to/faa_directory output/all_sequences.faa

faa_dir="${1:?Provide the directory containing .faa files}"
output_faa="${2:?Provide the output FASTA path}"

mkdir -p "$(dirname "$output_faa")"
cat "$faa_dir"/*.faa > "$output_faa"
echo "Concatenated protein FASTA written to: $output_faa"
