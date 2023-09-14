from collections import defaultdict
import random


# The condition that you can use to define whether a character is counted
def is_valid_character(character):
    # CHANGE this as you want
    return character.isalpha()


# Given two characters, returns a tuple with those two characters in order
def pair(first, second):
    return tuple(sorted([first, second]))


# Given a pair and a letter, returns the other letter if the original letter is in the pair and "" otherwise
def find_other(pair, letter):
    if pair[0] == letter:
        return pair[1]
    if pair[1] == letter:
        return pair[0]
    return ""


# Loads in the file
def load_and_get_pair_counts(file_path):
    # Initialize an empty string to store the file contents
    pair_counts = defaultdict(int)

    # Load the file
    with open(file_path, 'r') as file:
        # Iterate through each line in the file
        for line in file:
            # Go through each character pair in that line
            for i in range(len(line) - 1):
                first = line[i]
                second = line[i + 1]
                if is_valid_character(first) and is_valid_character(second):
                    # Adds +1 to the two characters, sorted
                    pair_counts[pair(first, second)] += 1

    # Return the pair_counts
    return pair_counts


# METHOD 2: Build it iteratively, making sure that each new node is an improvement
def iteratively_color_nodes(pairs, pair_counts, print_info):
    # Initialize
    connected_letters = set()
    black_letters = set()
    white_letters = set()

    # Start with a pair
    first_pair = pairs.pop(0)
    black_letters.add(first_pair[0])
    white_letters.add(first_pair[1])
    connected_letters.add(first_pair[0])
    connected_letters.add(first_pair[1])

    # Iterate through the rest of them
    not_finished = True
    while not_finished:
        if print_info:
            print("Starting new loop with ", connected_letters)
        not_finished = False
        # Find the first pair with a letter that exists in our graph
        for pair in pairs:
            # If it's a connection that doesn't have one new node, continue
            if bool(pair[0] not in connected_letters) == bool(pair[1] not in connected_letters):
                continue

            # Find the letter that doesn't exist in our graph
            new_node = pair[1] if pair[0] in connected_letters else pair[0]

            # Find the sum of the nodes containing that letter, if it was white and black
            if_existing_becomes_white = 0
            if_existing_becomes_black = 0
            for maybe_pair in pairs:
                other_letter = find_other(maybe_pair, new_node)
                if other_letter in black_letters:
                    if_existing_becomes_white += pair_counts[maybe_pair]
                if other_letter in white_letters:
                    if_existing_becomes_black += pair_counts[maybe_pair]

            # Choose the color that maximizes the point total
            if if_existing_becomes_black > if_existing_becomes_white:
                black_letters.add(new_node)
            else:
                white_letters.add(new_node)

            # Add the new node to the connected letters and break
            connected_letters.add(new_node)
            not_finished = True
            break

    # When done iteratively coloring, return the blacks and the whites
    return black_letters, white_letters


# METHOD 1: Given sorted counts, uses Kruskal's algorithm to build the maximum spanning tree between the letters in the vocab
def get_max_spanning_tree(sorted_pairs, print_info):
    # Initialize the letters that we've found so far and the connections in our max spanning tree
    connected_letters = set()
    connections = set()
    black_letters = set()
    white_letters = set()

    # Go through though the graph (the sorted list is reversed)
    for pair in sorted_pairs:
        # If there is a node that hasn't been visited yet
        if pair[0] not in connected_letters or pair[1] not in connected_letters:
            # Add that connection to the final max spanning tree
            connections.add(pair)
            # And say we've visited those nodes
            connected_letters.add(pair[0])
            connected_letters.add(pair[1])
            # If pair[0] is in the black letters, pair[1] is in the white. Otherwise, reverse it
            if pair[0] in black_letters:
                white_letters.add(pair[1])
            else:
                black_letters.add(pair[1])
                white_letters.add(pair[0])  # We have no guarantee this isn't the first iteration

    # Print the info if requested
    if print_info:
        print(f"The black letters are {black_letters}")
        print(f"The white letters are {white_letters}")
        print(f"The connections are {connections}\n")

    # Return all the info
    return black_letters, white_letters, connections


# METHOD 3: Randomly colors each letter with a 50/50 chance of being one or the other
def randomly_color(sorted_pairs):
    # Initialize the letters that we've found so far and the connections in our max spanning tree
    connected_letters = set()
    black_letters = set()
    white_letters = set()

    # Add each letter to a random set
    for pair in sorted_pairs:
        for letter in pair:
            if letter not in connected_letters:
                if random.random() > 0.5:
                    black_letters.add(letter)
                else:
                    white_letters.add(letter)
            connected_letters.add(letter)

    # Return
    return black_letters, white_letters


# Returns the accuracy of the color division
def get_accuracy_given_counts(blacks, pair_counts):
    # Initialize the counters
    correct = 0
    incorrect = 0

    # Iterate over the pair counts to see if the pairs are compatible
    for pair, value in pair_counts.items():
        # Both letters should be in one of the categories
        first = pair[0]
        second = pair[1]
        # If they're in the same category
        if bool(first in blacks) == bool(second in blacks):
            incorrect += value
        else:
            correct += value

    # Return the accuracy
    accuracy = correct / (correct + incorrect)
    print(f'The accuracy is {accuracy}\n')
    return accuracy


# Runs the code on the characters for the file provided
def main(file_path):
    # Load in all the words
    pair_counts = load_and_get_pair_counts(file_path)

    # Sort them based on the value, and remove all letters next to themselves
    sorted_items = sorted(pair_counts.items(), key=lambda item: item[1], reverse=True)
    prefiltered_sorted_pairs = [item[0] for item in sorted_items]
    sorted_pairs = []
    for pair in prefiltered_sorted_pairs:
        if pair[0] != pair[1]:
            sorted_pairs.append(pair)
    print(f"The pair counts are as follows: \n {sorted_items} \n")

    # Get the relevant infos, and print them if you want
    print_info = False
    blacks_1, whites_1, connections_1 = get_max_spanning_tree(sorted_pairs, print_info)
    blacks_2, whites_2 = iteratively_color_nodes(sorted_pairs, pair_counts, print_info)
    blacks_3, whites_3 = randomly_color(sorted_pairs)

    # Get the accuracy on the training data if desired
    get_accuracy = True
    if get_accuracy:
        print("Accuracy given method 1:")
        get_accuracy_given_counts(blacks_1, pair_counts)
        print("Accuracy given method 2:")
        get_accuracy_given_counts(blacks_2, pair_counts)
        print("Accuracy given method 3:")
        get_accuracy_given_counts(blacks_3, pair_counts)


if __name__ == '__main__':
    main("Datasets/50_paragraph_lipsum.txt")
    # main("Datasets/test_random.txt")


