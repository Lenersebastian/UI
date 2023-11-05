import copy
import random


def make_string_1_byte(string):
    while len(string) != 8:
        string = '0' + string
    return string


def create_first_generation():
    array_of_people = []
    for k in range(number_of_children_in_each_gen):
        array_of_strings = []
        for i in range(64):
            person_string = ""
            for j in range(8):
                person_string += str(random.randint(0, 1))
            array_of_strings.append(person_string)
        array_of_people.append(array_of_strings)
    return array_of_people


def check_if_treasure_found(pos, treasures):
    if pos in treasures:
        return True
    else:
        return False


def out_of_map_coordinates():
    arr_of_bad_coordinates = []
    for i in range(size_of_map + 2):
        arr_of_bad_coordinates.append(i)
        arr_of_bad_coordinates.append(i * 10)
        arr_of_bad_coordinates.append(i + size_of_map * 10 + 10)
        arr_of_bad_coordinates.append(i * 10 + size_of_map + 1)
    return arr_of_bad_coordinates


def virtual_machine(arr_of_genes):  # function returns fitness
    position = 74
    treasures = [25, 33, 47, 52, 65]
    counter = 0
    index_of_address = 0
    steps_of_person = ""
    # program stops after 500 steps or when it reaches last cell
    while counter != 500 and index_of_address != 64:
        counter += 1
        index_of_value = int(arr_of_genes[index_of_address][2:], 2)
        if index_of_value > 63 or index_of_value < 0:  # program stops when index is out of range
            break
        if arr_of_genes[index_of_address][:2] == "00":
            if arr_of_genes[index_of_value] == "11111111":  # increment is cyclic
                arr_of_genes[index_of_value] = "00000000"
            else:
                arr_of_genes[index_of_value] = make_string_1_byte(bin(int(arr_of_genes[index_of_value], 2) + 1)[2:])
        elif arr_of_genes[index_of_address][:2] == "01":
            if arr_of_genes[index_of_value] == "00000000":  # decrement is cyclic
                arr_of_genes[index_of_value] = "11111111"
            else:
                arr_of_genes[index_of_value] = make_string_1_byte(bin(int(arr_of_genes[index_of_value], 2) - 1)[2:])
        elif arr_of_genes[index_of_address][:2] == "10":
            index_of_address = index_of_value - 1
        else:
            if arr_of_genes[index_of_value][6:] == "00":
                position += 10
                steps_of_person += "H"
            elif arr_of_genes[index_of_value][6:] == "01":
                position -= 10
                steps_of_person += "D"
            elif arr_of_genes[index_of_value][6:] == "10":
                position += 1
                steps_of_person += "P"
            else:
                position -= 1
                steps_of_person += "L"
            if position in wrong_coordinates:
                break
            if check_if_treasure_found(position, treasures):
                treasures.remove(position)
                if len(treasures) == 0:
                    # print(steps_of_person)
                    # break
                    exit(steps_of_person)
        index_of_address += 1
    return 5 - len(treasures), steps_of_person


def choose_random_players(number_of_players, parents):
    indexes_of_players = []
    for p in range(number_of_players):
        index = random.randint(0, number_of_children_in_each_gen - 1 - len(parents))  # minus elitists
        while index in indexes_of_players and index:
            index = random.randint(0, number_of_children_in_each_gen - 1 - len(parents))
        indexes_of_players.append(index)
    return indexes_of_players


def tournament_selection():
    parents = elitism()
    num_of_parents = number_of_children_in_each_gen - how_many_new_blood - how_many_elitists
    number_of_players_in_tournament_selection = num_of_parents//5

    for i in range(num_of_parents):
        winners_indexes = []
        players = choose_random_players(number_of_players_in_tournament_selection, parents)
        while len(players) != 1:
            player_a = random.randint(0, len(players) - 1)
            player_b = random.randint(0, len(players) - 1)
            while player_b == player_a:
                player_b = random.randint(0, len(players) - 1)
            if arr_of_fitness[players[player_a]] > arr_of_fitness[players[player_b]]:
                winners_indexes.append(players[player_a])
            else:
                winners_indexes.append(players[player_b])
            players[player_a] = -1
            players[player_b] = -1
            players.remove(-1)
            players.remove(-1)
            if len(players) < 2:
                players = winners_indexes
                winners_indexes = []
        parents.append(players[0])
    return parents


def roulette_selection():
    parents = elitism()
    fitness_of_population = 0
    num_of_parents = number_of_children_in_each_gen - how_many_new_blood - how_many_elitists
    for i in range(num_of_parents):
        fitness_of_population += arr_of_fitness[i]
    for i in range(num_of_parents):
        sum_of_fitness = 0
        index = 0
        roulette = random.uniform(0, fitness_of_population)
        while roulette > sum_of_fitness:
            sum_of_fitness += arr_of_fitness[index]
            index += 1
        parents.append(index - 1)
    return parents


def mutation_chance(string):  # mutation chance is 20%, revert last bit
    rand_number = random.randint(1, 100)
    if rand_number < 21:
        is_mutating = True
    else:
        is_mutating = False
    if is_mutating:
        if string[7] == '1':
            string = string[:7] + '0'
        else:
            string = string[:7] + '1'
    return string


def elitism():
    elitists = []
    for i in range(how_many_elitists):
        value_of_parent = max(arr_of_fitness)
        parent_index = arr_of_fitness.index(value_of_parent)
        elitists.append(parent_index)
        arr_of_fitness.remove(value_of_parent)
    return elitists


def new_blood():
    new_people = []
    for i in range(how_many_new_blood):
        array_of_strings = []
        for k in range(64):
            person_string = ""
            for j in range(8):
                person_string += str(random.randint(0, 1))
            array_of_strings.append(person_string)
        new_people.append(array_of_strings)
    return new_people


def create_next_gen(parents_indexes, old_gen):  # random parent + random other parent -> 2 kids
    next_gen = new_blood()
    parents = copy.deepcopy(parents_indexes)
    if len(parents) % 2 == 1:
        parents.append(parents[0])
    while len(parents) != 0:
        random_a_index = random.randint(0, len(parents)-1)
        random_b_index = random.randint(0, len(parents)-1)
        while random_a_index == random_b_index:
            random_a_index = random.randint(0, len(parents)-1)
        parent_a = old_gen[parents[random_a_index]]
        parent_b = old_gen[parents[random_b_index]]
        index_of_changing_gene = random.randint(0, 63)
        child_a = []
        child_b = []
        for j in range(64):
            if j < index_of_changing_gene:
                child_a.append(mutation_chance(parent_a[j]))
                child_b.append(mutation_chance(parent_b[j]))
            else:
                child_a.append(mutation_chance(parent_b[j]))
                child_b.append(mutation_chance(parent_a[j]))
        parents[random_a_index] = "X"
        parents[random_b_index] = "X"
        parents.remove("X")
        parents.remove("X")
        next_gen.append(child_a)
        next_gen.append(child_b)
    return next_gen


def print_best_guy_in_gen():
    print(max(arr_of_fitness))


#########################################################################
number_of_children_in_each_gen = int(input("How many people in each gen? "))
selection_type = input("Tournament(1) or roulette(2)? ")
how_many_gens = int(input("How many generations? "))
how_many_elitists = int(input("How many elitists will be in each selection? "))
how_many_new_blood = number_of_children_in_each_gen // 10

size_of_map = 7
wrong_coordinates = out_of_map_coordinates()
generations = [create_first_generation()]
continue_to_find_all_treasures = True
index_of_gen = 0

while continue_to_find_all_treasures:
    arr_of_fitness = []
    for person in generations[index_of_gen]:
        treasures_find, steps = virtual_machine(person)
        if treasures_find == 5:
            continue_to_find_all_treasures = False
            break
        arr_of_fitness.append(1 + treasures_find - len(steps) / 1000)
    print_best_guy_in_gen()
    if selection_type == "1":
        par_indexes = tournament_selection()
    else:
        par_indexes = roulette_selection()
    generations.append(create_next_gen(par_indexes, generations[index_of_gen]))
    index_of_gen += 1
    if index_of_gen == how_many_gens:
        con = input("Program did not find a solution, do you want to keep going?(yes/no) ")
        if con == "yes":
            how_many_gens += int(input("How many generations? "))
        else:
            exit("No solution")
