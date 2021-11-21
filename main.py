# Author: Ethan Cook
# Date created: 11/19/2021
# Brief: a script that takes in a csv file of nodes and node attributes, and generates a gml file
# creating edges using whatever attribute the user decides

import os
import csv

NUM_ATTRIBUTES_PER_NODE = 3
LINKING_ATTRIBUTE_INDEX = 0
CSV_FILE_TO_PARSE = "instrument-dataset-test.csv"


class Node:
    genres = []

    def __init__(self, node_id, name, country, instrument_family, genres):
        self.node_id = node_id
        self.name = name
        self.country = country
        self.instrument_family = instrument_family
        self.genres = genres

    def print_node(self):
        print(self.node_id, self.name, self.country, self.instrument_family, self.genres)


def createNodesList(filename):
    print("parsing:", filename)
    try:
        csvfile = open(filename, 'r')
        csv_reader = csv.reader(csvfile, delimiter=',')
    except IOError:
        print("File access failed")
        exit()

    instruments = []
    line_count = 0

    for line in csv_reader:
        genres = []
        if line_count != 0:
            x = range(4, 14)
            for i in x:
                if line[i]:
                    genres.append(line[i])
            instruments.append(Node(line[0], line[1], line[2], line[3], genres))
        else:
            line_count += 1

    return instruments


def generateGml(instrument_list):
    gml = open("instrument-gml.txt", "w")
    gml.write("graph\n[\n")

    for instrument in instrument_list:
        instrument.print_node()

    # TODO: add nodes
    for instrument in instrument_list:
        gml.write(f" node\n [\n id {str(instrument.node_id)}\n label \"{instrument.name}\"\n ]\n")

    # TODO: add edges
    # from 1st node to the node before last
    for i in range(0, len(instrument_list) - 1):
        # from the node after i to the last node
        print(i)
        for j in range(i + 1, len(instrument_list)):
            generateEdges(gml, instrument_list[i], instrument_list[j])

    gml.write("]")


# this takes the gml writer, the node1, and the node2. It will then go through their genres and make edges
def generateEdges(gml_file, instr1, instr2):
    similar_genres = (set(instr1.genres) & set(instr2.genres))
    for genre in similar_genres:
        gml_file.write(f" edge\n [\n source {instr1.node_id}\n target {instr2.node_id}\n label \"{str(genre)}\"\n ]\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    instruments = createNodesList(CSV_FILE_TO_PARSE)
    generateGml(instruments)

