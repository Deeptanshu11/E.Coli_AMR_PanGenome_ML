#!/usr/bin/env python3
"""Build a genome x CD-HIT cluster presence/absence matrix from .clstr and FAA files."""

from pathlib import Path
import argparse
from collections import defaultdict
import pandas as pd


def parse_clusters(clstr_file):
    clusters = defaultdict(list)
    current = None
    with clstr_file.open() as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(">Cluster"):
                current = int(line.split()[1])
            elif ">" in line and current is not None:
                protein_id = line.split(">")[1].split("...")[0]
                clusters[current].append(protein_id)
    return clusters


def map_proteins_to_genomes(faa_dir):
    mapping = {}
    faa_files = sorted(faa_dir.glob("*.PATRIC.faa"))
    for faa in faa_files:
        genome_id = faa.name.removesuffix(".PATRIC.faa")
        with faa.open() as fh:
            for line in fh:
                if line.startswith(">"):
                    protein_id = line[1:].split()[0]
                    mapping[protein_id] = genome_id
    return faa_files, mapping


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clusters", type=Path, required=True)
    parser.add_argument("--faa-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    clusters = parse_clusters(args.clusters)
    faa_files, protein_to_genome = map_proteins_to_genomes(args.faa_dir)

    genomes = sorted(f.name.removesuffix(".PATRIC.faa") for f in faa_files)
    cluster_ids = sorted(clusters)

    matrix = pd.DataFrame(
        0, index=genomes,
        columns=[f"Cluster_{c}" for c in cluster_ids],
        dtype="uint8"
    )

    for cluster_id, proteins in clusters.items():
        col = f"Cluster_{cluster_id}"
        for protein in proteins:
            genome = protein_to_genome.get(protein)
            if genome is not None:
                matrix.at[genome, col] = 1

    matrix.index.name = "genome_id"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    matrix.to_csv(args.output)

    print(f"Clusters: {len(cluster_ids):,}")
    print(f"Genomes: {len(genomes):,}")
    print(f"Matrix shape: {matrix.shape}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
