import os
import re
from random import randint, random
from math import floor
from time import perf_counter

# Sequence file containing the sequences to perform MSA on
seq_file = os.path.join('.', 'samples', 'input_5_items.fasta')

### Genetic algorithm parameters ###

# Number of generations to go through
num_generations = 40

# The chance that a gene inside an individual
# shoulder undergo mutation
# Mutation is defined as randomly shifting around one gap
mutation_rate = 0.50

# Population size, this is equal to how many different instances of
# the genomes we want to perform MSA there are on
population_size = 100

# Percentage of the strongest of the current population that will go on
# to the next generation, these individuals will go as is (no mutations)
percent_strongest_to_next_gen = 0.3

# Percentage of the population to be completely new random individuals
percent_pop_random = 0.05

# Percentage of the strongest to be crossed over (mixed together)
# for the next generation, these will have random mutations
percent_crossover = 1.0 - percent_strongest_to_next_gen - percent_pop_random

# When crossing over two individuals, this is the percentage
# that any particular gene (which is a sequence) will be swapped
percent_gene_swap = 0.5

class ProteinSequence:
    """Defines a protein sequence."""
    def __init__(self, title, seq=''):
        self.title = title
        self.raw_seq = seq

class Population:
    """A population contains a fixed number of protein sequences."""
    def __init__self(self, pop_size):
        pass

def load_sequences(filepath):
    """Loads all the sequences from the given file.
    Returns
        A list of ProteinSequence's
    """
    # Parse the input sequencing file
    protein_seqs = []
    with open(filepath) as f:
        for line in f:
            # '>' marks the beginning of a new sequence
            if line.startswith('>'):
                protein_seqs.append(ProteinSequence(line.rstrip()))
            else:
                # If this line does not begin with '>', it must be describing
                # a genome sequence
                protein_seqs[-1].raw_seq += line.rstrip()
    return protein_seqs

def insert_mutation(seq):
    """Inserts a random mutation into the sequence.
    This is done by randomly inserting one gap in the sequence.
    """

    # Randomly generate an index to insert the gap to
    insert_idx = randint(0, len(seq.raw_seq))
    # Create the new sequence
    new_raw_seq = seq.raw_seq[:insert_idx] + '-' + seq.raw_seq[insert_idx:]
    return ProteinSequence(seq.title, new_raw_seq)

def do_mutation(seq):
    """Mutates a sequence by removing a random gap, and inserting a random gap."""
    idx_gaps = []
    for idx, c in enumerate(seq.raw_seq):
        if c == '-':
            idx_gaps.append(idx)
    
    # Of course, if there are no gaps, then simply return the original sequence back
    if len(idx_gaps) == 0:
        return seq
    else:
        # Randomly choose a gap to remove
        rand_idx = randint(0, len(idx_gaps) - 1)
        remove_idx = idx_gaps[rand_idx]
        removed_raw_seq = seq.raw_seq[:remove_idx] + seq.raw_seq[remove_idx + 1:]

        # Then, randomly insert a mutation
        return insert_mutation(ProteinSequence(seq.title, removed_raw_seq))

def create_individual_from(seqs, desired_seq_len):
    """Generates a single individual from a list of sequences.
    An individual is a list of sequences,
    whose sequence length are all the same, this is done by
    randomly inserting gaps.
    """
    indiv = []
    for seq in seqs:
        new_seq = ProteinSequence(seq, seq.raw_seq)
        while len(new_seq.raw_seq) != desired_seq_len:
            new_seq = insert_mutation(new_seq)
        indiv.append(ProteinSequence(new_seq.title, new_seq.raw_seq))
    return indiv

def create_population_from(seqs, population_size):
    """Creates a population from the list of given sequences.
    Returns
        A list of individuals. An individual is a list of sequences,
        whose sequence length are all the same, this is done by
        randomly inserting gaps. 
    """

    # Find the length of the longest sequence
    # All shorter sequences will be lengthened to match n
    n = 0
    for seq in seqs:
        n = max(n, len(seq.raw_seq))
    return [create_individual_from(seqs, n) for i in range(population_size)]

def compute_fitness(pop):
    """Computes the overall fitness score of the population. The lower the better
    For simplicity, this function will return the number of differences overall.
    Of course, for the future, there are many optimizations and heuristics that
    can be employed here to give a better cost function. We want to minimize
    the number of differences, so the lower the better.
    """

    num_diffs = 0
    # Iterate through each index of the sequence
    for i in range(len(pop[0].raw_seq)):
        # Check if the pairwise sequences differ, if they do,
        # count it as a difference
        for j in range(len(pop) - 1):
            if pop[j].raw_seq[i] != pop[j + 1].raw_seq[i]:
                num_diffs += 1
    return num_diffs

def crossover(parent_A, parent_B):
    """Crosses over two individuals.
    Randomly selected sequences from the individuals are swapped.
    """

    new_indiv = []
    for i in range(len(parent_A)):
        # Generate a random (floating point) number between 0 and 1
        # If the number is smaller than percent_gene_swap, take parent A's sequence
        # otherwise, take parent B's sequence
        new_indiv.append(parent_A[i] if random() <= percent_gene_swap else parent_B[i])
    for idx, gene in enumerate(new_indiv):
        if random() <= mutation_rate:
            new_indiv[idx] = do_mutation(gene)
    return new_indiv

# Application entry point
if __name__ == '__main__':
    # Get the original unaligned sequences
    orig_sequences = load_sequences(seq_file)
    
    # Time the execution
    exe_start_time = perf_counter()

    # Create the initial population
    current_pop = create_population_from(orig_sequences, population_size)

    # Get the sequence length, this will be consistent across all sequences
    seq_len = len(current_pop[0][0].raw_seq)

    num_most_fit = floor(len(current_pop) * percent_strongest_to_next_gen)
    num_random = floor(len(current_pop) * percent_pop_random)
    num_crossover = floor(len(current_pop) * percent_crossover)
    best_indiv_seen = None

    # Because floating point operations and flooring might skew the numbers
    while num_most_fit + num_random + num_crossover != population_size:
        num_crossover += 1
    
    print(f'Sequence length: {seq_len}')
    print(f'Individual size: {len(current_pop[0])}')
    print(f'Population size: {len(current_pop)}')
    print(f'For each generation:')
    print(f'\tNumber most fit: {num_most_fit}')
    print(f'\tNumber random: {num_random}')
    print(f'\tNumber crossover: {num_crossover}')

    # Iterate through the specified number of generations
    # producing a (hopefully) stronger population each time
    for gen in range(num_generations):
        # First compute the fitness scores of each individual
        fitness_scores = [compute_fitness(indiv) for indiv in current_pop]

        # Create a list of tuples in the form: (indiv, score)
        indivs = [(current_pop[i], fitness_scores[i]) for i in range(population_size)]

        # Sort by ascending scores
        indivs.sort(key=lambda elem: elem[1])
        print(f'Generation {gen + 1}, Top 10 scores (lower is better): {[indiv[1] for indiv in indivs[:10]]}')

        # Keep track of the best individual seen
        if best_indiv_seen == None:
            best_indiv_seen = indivs[0]
        else:
            if indivs[0][1] < best_indiv_seen[1]:
                best_indiv_seen = indivs[0]

        # Initialize the next generation population
        next_pop = []

        # Take the most fit individuals, and add them as-is
        # to the next generation
        most_fit = indivs[:num_most_fit]
        next_pop.extend([indiv[0] for indiv in most_fit])

        # Generate some random individuals
        for i in range(num_random):
            next_pop.append(create_individual_from(orig_sequences, seq_len))

        # Crossover the most fit individuals
        for i in range(num_crossover):
            # Randomly select two different parents from the most fit to crossover
            idx_A = randint(0, num_most_fit - 1)
            idx_B = idx_A
            while idx_B == idx_A:
                idx_B = randint(0, num_most_fit - 1)
            parent_A = most_fit[idx_A][0]
            parent_B = most_fit[idx_B][0]
            next_pop.append(crossover(parent_A, parent_B))
        
        # Finally, update the population
        current_pop = next_pop
    

    exe_end_time = perf_counter()
    print(f'Done! Took {exe_end_time - exe_start_time}s')
    print(f'Score of best individual seen so far: {best_indiv_seen[1]}')
