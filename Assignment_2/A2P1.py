import numpy as np
import random

def generate_chromosome(bit_len):
    # Random binary array of size bit_len
    chromosome = np.random.randint(low = 0, high = 2, size = bit_len)
    return chromosome

def generate_population(population_size, bit_len):
    # Generating population
    population = []
    for _ in range(population_size):
        population.append(generate_chromosome(bit_len))
    return population
        
def fitness_function(population, population_size, bit_len):
    # Calculating the ideal value
    ideal_value = int("".join(str(1) for x in range(bit_len)), 2)

    # Calculating fitness values
    fitness_values = []
    for i in range(population_size):
        fitness_values.append((int("".join(str(x) for x in population[i]), 2) / ideal_value, population[i]))
    
    # Sorting list by fitness ratio
    fitness_values.sort(reverse=True, key=lambda tupl: tupl[0])
    return fitness_values

def selection(fitness_values, population_size):
    # Selecting the top n-1 best values
    temp = fitness_values[ : population_size-1]

    # Choosing the rest, to make it n again, randomly
    rest = random.choice(fitness_values)
    temp.append(rest)
    return temp

def crossover(selected_values, population_size, bit_len):
    # Convering np array to string array
    selected_values = ["".join([str(x) for x in a]) for a in selected_values]

    # Generating crossover selection criteria randomly
    crossover_indices = [x for x in range(population_size)]
    random.shuffle(crossover_indices)

    # Creating even length indices for ease xD
    if len(crossover_indices) % 2 !=0:
        temp = random.choice(crossover_indices)
        crossover_indices.append(temp)

    # Actual Crossover Criteria, and Crossover
    while crossover_indices:
        start_index = random.randint(3, bit_len//2)
        end_index = bit_len
        first_chromosome = selected_values[crossover_indices[0]]
        second_chromosome = selected_values[crossover_indices[1]]
        
        temp1 = first_chromosome[start_index:end_index]
        temp2 = second_chromosome[start_index:end_index]

        first_chromosome = first_chromosome[0:start_index]+temp2
        second_chromosome = second_chromosome[0:start_index]+temp1

        selected_values[crossover_indices[0]] = first_chromosome
        selected_values[crossover_indices[1]] = second_chromosome

        crossover_indices.pop(0)
        crossover_indices.pop(0)

    # Converting back to np array
    selected_values = [np.array(list(selected_values[i]), dtype=int) for i in range(population_size)]
    return selected_values

def mutation(crossover_values, population_size, bit_len):
    # Random number of bits will mutate
    no_bits_to_be_change = random.randint(1, bit_len//3)
    for i in range(population_size):
        for _ in range(no_bits_to_be_change):
            random_index = random.randint(0, bit_len-1)
            crossover_values[i][random_index] = int(not crossover_values[i][random_index])

    return crossover_values

def genetic_algo(population_size, bit_len):
    generations = 0
    # Calculating the ideal value
    ideal_value = int("".join(str(1) for x in range(bit_len)), 2)

    population = generate_population(population_size, bit_len)
    # print(population, end="\n\n")
    while True:
        generations += 1
        fitness_values = fitness_function(population, population_size, bit_len)
        # print(fitness_values, end="\n\n")
        selected_values = selection(fitness_values, population_size)
        # Removing fitness values, only keeping the population
        selected_values = [b for a,b in selected_values]
        # print(selected_values, end="\n\n")
        crossover_values = crossover(selected_values, population_size, bit_len)
        # print(crossover_values, end="\n\n")
        mutated_values = mutation(crossover_values, population_size, bit_len)
        # print(mutated_values, end="\n\n")
        population = mutated_values

        check_ideal_solution = []
        for i in range(population_size):
            check_ideal_solution.append(int("".join(str(x) for x in mutated_values[i]), 2))
        if ideal_value in check_ideal_solution:
            break
    return generations

if __name__ == "__main__":
    population_size = 4
    bit_len = 8
    for bit_len in range(8,17):
        for population_size in range(4,11):
            generations = genetic_algo(population_size, bit_len)
            #print(generations)
            print(bit_len, population_size, " : ", generations)
        print()
