#!/usr/bin/env python3
"""Map known AMR protein/ORF IDs to CD-HIT cluster IDs."""

from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orf-ids", type=Path, required=True)
    parser.add_argument("--clusters", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    orfs = {x.strip() for x in args.orf_ids.read_text().splitlines() if x.strip()}
    matches = set()
    current = None

    with args.clusters.open() as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(">Cluster"):
                current = line.split()[1]
            elif line.endswith("*") and current is not None:
                orf_id = line.split(">")[1].split("...")[0]
                if orf_id in orfs:
                    matches.add(current)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as fh:
        for cluster in sorted(matches, key=int):
            fh.write(f"Cluster_{cluster}\n")

    print(f"Known AMR clusters: {len(matches):,}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
