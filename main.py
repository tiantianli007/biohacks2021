import os
import re

# Sequence file to inspect
seq_file = open(os.path.join('.', 'ncbi_dataset', 'data', 'genomic.fna'))
# Required search terms in sequence title to take
# For this hackathon, we're looking at the University of Alabama sequences
seq_required_terms = ['AL-UAB-GX[0-9]+/2021', 'complete genome']

class ProteinSequence:
    """Defines a protein sequence."""
    def __init__(self, title):
        self.title = title
        self.sequence = ''
        self.num_A = 0
        self.num_C = 0
        self.num_G = 0
        self.num_T = 0

# Application entry point
if __name__ == '__main__':
    
    # Parse the input sequencing file
    protein_seqs = []
    is_adding_seq = False
    for line_num, line in enumerate(seq_file):
        # '>' marks the beginning of a new sequence
        if line.startswith('>'):
            if None not in [re.search(term, line) for term in seq_required_terms]:
                protein_seqs.append(ProteinSequence(line))
                is_adding_seq = True
            else:
                is_adding_seq = False
        else:
            # If this line does begin with '>', it must be describing
            # a genome sequence. Add this line to our sequence only if
            # we are currently processing one of our selected genomes
            if is_adding_seq:
                protein_seqs[-1].sequence += line
    
    
    # With a list of proteins to compare, first compute the number of ACGTs
    for seq in protein_seqs:
        for elem in seq.sequence:
            if elem == 'A':
                seq.num_A += 1
            elif elem == 'C':
                seq.num_C += 1
            elif elem == 'G':
                seq.num_G += 1
            elif elem == 'T':
                seq.num_T += 1
    
    # Print out results
    for seq in protein_seqs:
        print('')
        print(f'Looking at: {seq.title}')
        print(f'A: {seq.num_A}')
        print(f'C: {seq.num_C}')
        print(f'G: {seq.num_G}')
        print(f'T: {seq.num_T}')