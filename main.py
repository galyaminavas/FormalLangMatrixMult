from scipy import sparse
import numpy
import sys
import time
from copy import copy
from utils import parse_to_graph_from_path, parse_to_grammar_from_path


def create_initial_matrices(graph, gram):
    size = graph.vertices.__len__()
    dictionary = {}
    for nt in gram.nonterms:
        key = str(nt)
        empty_value = [[False for i in range(size)] for i in range(size)]
        dictionary[key] = empty_value
    for r in graph.edges:
        rule_array = r.split(' ')
        rule_from = rule_array[0]
        rule_symbol = rule_array[1]
        rule_to = rule_array[2]
        if rule_symbol in gram.terms:
            for rule in gram.rules:
                gr_rule = rule.split(' ')
                gr_rule_nonterm = gr_rule[0]
                gr_rule_prod = gr_rule[1]
                if rule_symbol == gr_rule_prod:
                    dictionary[str(gr_rule_nonterm)][int(rule_from)][int(rule_to)] = True
    return dictionary


def mult_global_cycle(grammar, dictionary):
    is_something_changed = False
    for r in grammar.rules:
        r_array = r.split(' ')
        if len(r_array) == 3:
            r_from = r_array[0]
            r_result_fst = r_array[1]
            r_result_snd = r_array[2]
            initial_matrix = copy(dictionary[r_from])
            dictionary[r_from] += dictionary[r_result_fst] @ dictionary[r_result_snd]
            if not numpy.array_equal(initial_matrix.toarray(), dictionary[r_from].toarray()):
                is_something_changed = True
    while is_something_changed:
        is_something_changed = False
        for r in grammar.rules:
            r_array = r.split(' ')
            if len(r_array) == 3:
                r_from = r_array[0]
                r_result_fst = r_array[1]
                r_result_snd = r_array[2]
                initial_matrix = copy(dictionary[r_from])
                dictionary[r_from] += dictionary[r_result_fst] @ dictionary[r_result_snd]
                if not numpy.array_equal(initial_matrix.toarray(), dictionary[r_from].toarray()):
                    is_something_changed = True


def calc_solution_from_path(graph_path, grammar_path, output_name):
    graph = parse_to_graph_from_path(graph_path)
    grammar = parse_to_grammar_from_path(grammar_path)
    dictionary = create_initial_matrices(graph, grammar)
    size = graph.vertices.__len__()
    for key in dictionary:
        dictionary[key] = sparse.csr_matrix(dictionary[key], dtype=bool)

    start = time.time() * 1000.0
    mult_global_cycle(grammar, dictionary)
    end = time.time() * 1000.0
    print('Time for multiplication: ', round(end - start))

    answer = ''
    list_of_keys = []
    # start = time.time()
    for keys in dictionary:
        list_of_keys.append(keys)
    list_of_keys.sort()
    for keys in list_of_keys:
        dictionary[keys] = sparse.csr_matrix(dictionary[keys], dtype=bool).toarray()
        answer += str(keys)
        for i in range(size):
            for j in range(size):
                if dictionary[keys][i][j]:
                    answer += ' {} {}'.format(i, j)
        answer += '\n'
    output_file = open(output_name, 'w')
    output_file.write(answer)
    output_file.close()
    # end = time.time()
    # print('Time for output: ', end - start)


if __name__ == '__main__':
    if len(sys.argv) == 4:
        # start = time.time()
        calc_solution_from_path(sys.argv[2], sys.argv[1], sys.argv[3])
        # end = time.time()
        # print('Time for full algorithm: ', end - start)
    else:
        print('Incorrect amount of arguments, run script like this: '
              'python main.py [grammar_path] [graph_path] [output_file_name]')
