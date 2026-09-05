#!/usr/bin/env bash
# Screen genome FASTA files for a >=99% identity hit to the reference 16S rRNA sequence.
# Uses blastn -subject; no persistent BLAST database is required.

set -euo pipefail

REFERENCE_16S="${1:?Usage: $0 reference_16S.fa genome_fna_dir output_ids.txt}"
GENOME_DIR="${2:?Usage: $0 reference_16S.fa genome_fna_dir output_ids.txt}"
OUTPUT_FILE="${3:?Usage: $0 reference_16S.fa genome_fna_dir output_ids.txt}"

mkdir -p "$(dirname "$OUTPUT_FILE")"
: > "$OUTPUT_FILE"

shopt -s nullglob
files=("$GENOME_DIR"/*.fna)

for file in "${files[@]}"; do
    if blastn \
        -query "$REFERENCE_16S" \
        -subject "$file" \
        -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" \
        -max_target_seqs 1 \
        -perc_identity 99 \
        | grep -q .; then
        basename "$file" >> "$OUTPUT_FILE"
    fi
done

echo "16S-screened genomes saved to: $OUTPUT_FILE"
