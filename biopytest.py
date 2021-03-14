from time import perf_counter
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import pairwise2
from Bio.Align.Applications import MuscleCommandline

def compute_fitness(seqs):
    num_diffs = 0
    # Iterate through each index of the sequence
    for i in range(len(seqs[0].seq)):
        # Check if the pairwise sequences differ, if they do,
        # count it as a difference
        for j in range(len(seqs) - 1): 
            if seqs[j].seq[i] != seqs[j + 1].seq[i]:
                num_diffs += 1
    return num_diffs

# Application entry point
if __name__ == '__main__':
    input_file = './samples/input_5_items.fasta'
    output_file = './outputs/biopy_output.fasta'

    print('Aligning with Biopython...')
    biopython_start_time = perf_counter()
    muscle_cline = MuscleCommandline("muscle.exe", input=input_file, out=output_file)
    muscle_cline()
    aligned_list = [elem for elem in SeqIO.parse(output_file, "fasta")]
    biopython_end_time = perf_counter()
    print(f'Fitness score of Biopython alignment (lower is better): {compute_fitness(aligned_list)}')
    print(f'Done! Took {biopython_end_time - biopython_start_time}s')
    
