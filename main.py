from collections import defaultdict


# The condition that you can use to define whether a character is counted
def is_valid_character(character):
    # CHANGE this as you want
    return character.isalpha()


# Loads in the file
def load_and_get_pair_counts(file_path):
    # Initialize an empty string to store the file contents
    pair_counts = defaultdict()

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
                    pair_counts[tuple(sorted([first, second]))] += 1

    # Return the pair_counts
    return pair_counts


# Given sorted counts, uses Kruskal's algorithm to build the maximum spanning tree between the letters in the vocab
def get_max_spanning_tree(sorted_pairs):
    # Initialize the letters that we've found so far and the connections in our max spanning tree
    connected_letters = set()
    connections = set()

    # Go through though the graph (the sorted list is reversed)
    for pair in sorted_pairs:
        # If there is a node that hasn't been visited yet
        if pair[0] not in connected_letters or pair[1] not in connected_letters:
            # Add that connection to the final max spanning tree
            connections.add(pair)
            # And say we've visited those nodes
            connected_letters.add(pair[0])
            connected_letters.add(pair[1])



# Runs the code on the characters for the file provided
def main(file_path):
    # Load in all the words
    pair_counts = load_and_get_pair_counts(file_path)

    # Sort them based on the value
    sorted_pairs = sorted(pair_counts.items(), key=lambda item: item[1], reverse=True)

    # Get the
    blacks, whites = get_max_spanning_tree(sorted_pairs)


if __name__ == '__main__':
    main("Datasets/50_paragraph_lipsum.txt")


