# BioHacks 2021

This is our BCBSU BioHacks 2021 submission. Authors: Tiantian Li, John Liu.

# Introduction

Multiple sequence alignment (MSA) refers to the [sequential alignment of three or more biological sequences, generally protein, DNA, or RNA](https://en.wikipedia.org/wiki/Multiple_sequence_alignment). The problem is quite simple to understand, given some set of n sequences, we wish to transform these sequences into some set of n' sequences, such that all the n' sequences are of the same length, by inserting gaps into the sequence. We want to do this while minimizing two primary targets:

1. differences between all pairs of sequences
2. minimizing the number of gaps inserted

The biggest problem with MSA is that, [even a naive dynamic programming approach is an NP-complete problem](https://www.liebertpub.com/doi/10.1089/cmb.1994.1.337); that means that its very difficult to compute!

There are of course, numerous optimizations and clever heuristics that can significantly improve our runtimes, but even then, to get a quality result, takes significant time.

# GA-MSA

The Genetic Algorithm-Multiple Sequence Alignment (GA-MSA) is a new approach to MSA using a Genetic Algorithm (GA).

## Installation

Download the datasets tool at https://www.ncbi.nlm.nih.gov/datasets/docs/command-line-start/. We use this free tool to get data from the National Library of Medicine. Extract the tool to the root of this repository and run the following command:
`./datasets download virus genome taxon 2697049 --released-since 03/10/2021 --filename SARS2-all-031021.zip`

 This will download all the SARS-CoV-2 genomes since March 10, 2021. Feel free to change this date. Note that the filesize can be quite large (in the gigabytes!). When finished, extract the ncbi_dataset folder inside the ZIP to the root directory of this repository.

