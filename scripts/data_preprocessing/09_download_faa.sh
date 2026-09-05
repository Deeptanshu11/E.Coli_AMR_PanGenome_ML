#!/usr/bin/env bash
# Download protein FASTA files from the BV-BRC/PATRIC genome FTP tree.
# Usage: bash 09_download_faa.sh genome_ids.txt output_directory

set -euo pipefail

IDS="${1:?Usage: $0 genome_ids.txt output_directory}"
OUT="${2:?Usage: $0 genome_ids.txt output_directory}"

BASE_URL="ftp://ftp.patricbrc.org/genomes"
mkdir -p "$OUT"

while IFS= read -r genome_id; do
    [[ -z "$genome_id" ]] && continue
    wget -nc -P "$OUT" "${BASE_URL}/${genome_id}/${genome_id}.PATRIC.faa"
done < "$IDS"
