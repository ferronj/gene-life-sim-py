import random


def analyze_genome_parameters(start_code, stop_code):
    genomes = []
    for i in range(100):
        genomes.append(create_random_genome(stop_code))

    sum = 0
    count = 0
    start_idx = []
    start_count = 0

    for g in genomes:
        sum += len(g)
        count += 1
        start_loc = search_binary_string(g, start_code)
        start_idx.append(start_loc)
        start_count += len(start_loc)

    mean = sum / count
    mean_start = start_count / count

    print(f'mean genome length: {mean}; mean genes per genome: {mean_start}')


def split_genome(genome, start_code, stop_code):
    # init genes list
    gene_list = []
    # cut the stop codon out of genome
    stop_length = len(stop_code)
    genome_ = genome[:-stop_length]
    # get indices of all start code locations
    gene_starts = search_binary_string(genome_, start_code)
    for idx, start_idx in enumerate(gene_starts):
        if idx < len(gene_starts) - 1:
            # start the genome slice after the start_code
            slice_start = start_idx + len(start_code)
            # end the slice at index of next gene start code
            slice_end = gene_starts[idx + 1]
            gene = genome_[slice_start:slice_end]
            # only append genes with sequences
            if len(gene) > 0:
                gene_list.append(gene)
    return gene_list
    

def create_random_genome(stop_code):
    write_genome = True
    genome = str(random.randint(0, 1))
    while write_genome:
        genome += str(random.randint(0, 1))
        if stop_code in genome:
            write_genome = False
    return genome


def search_binary_string(binary_string, sequence):
    positions = []
    index = binary_string.find(sequence)
    while index != -1:
        positions.append(index)
        index = binary_string.find(sequence, index+len(sequence))
    return positions