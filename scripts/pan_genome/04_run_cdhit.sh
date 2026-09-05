#!/usr/bin/env bash
# CD-HIT step used to generate the cluster file consumed by the pan-genome script.

set -euo pipefail

FAA="${1:?Usage: $0 combined_proteins.faa output_prefix}"
PREFIX="${2:?Usage: $0 combined_proteins.faa output_prefix}"

cd-hit -i "$FAA" -o "$PREFIX" -c 0.95 -n 5 -d 0 -T 8 -M 16000
