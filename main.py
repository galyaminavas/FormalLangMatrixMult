def generate_cycle_graph_str(n):
    if n < 2:
        return 'error'
    else:
        output_string = ''
        for i in range(n - 1):
            output_string += '{} a {}\n'.format(i, i + 1)
        output_string += '{} a 0'.format(n - 1)
        return output_string


class Grammar:
    def __init__(self):
        self.terms = []
        self.nonterms = []
        self.rules = []

    def add_terms(self, terms):
        for t in terms:
            self.terms.append(t)

    def add_nonterms(self, nonterms):
        for n in nonterms:
            self.nonterms.append(n)

    def add_rules(self, rules):
        for r in rules:
            self.rules.append(r)

    def add_rule_string(self, rule_str):
        components = rule_str.split(' ')
        if len(components) == 2:
            if components[0] not in self.nonterms:
                self.nonterms.append(components[0])
            if components[1] not in self.terms:
                self.terms.append(components[1])
            self.rules.append(rule_str)
        else:
            if len(components) == 3:
                if components[0] not in self.nonterms:
                    self.nonterms.append(components[0])
                if components[1] not in self.nonterms:
                    self.nonterms.append(components[1])
                if components[2] not in self.nonterms:
                    self.nonterms.append(components[2])
                self.rules.append(rule_str)


def parse_to_grammar(input_string):
    input_array = input_string.split('\n')
    grammar = Grammar()
    #     grammar.add_rules(input_array)
    for elem in input_array:
        grammar.add_rule_string(elem)
    return grammar


# grammar_string = 'S A B\n' \
#                  'S S1 B\n' \
#                  'S1 A S\n' \
#                  'A a\n' \
#                  'B b'
# # resulting_grammar = parse_to_grammar(grammar_string)

# print(resulting_grammar.terms)
# print(resulting_grammar.nonterms)
# print(resulting_grammar.rules)


class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []

    def add_vertices(self, vertices):
        for v in vertices:
            self.vertices.append(v)

    def add_edges(self, edges):
        for e in edges:
            self.edges.append(e)

    def add_edge_string(self, edge_str):
        components = edge_str.split(' ')
        if len(components) == 3:
            if components[0] not in self.vertices:
                self.vertices.append(components[0])
            if components[2] not in self.vertices:
                self.vertices.append(components[2])
            self.edges.append(edge_str)


def parse_to_graph(input_string):
    input_array = input_string.split('\n')
    graph = Graph()
    for elem in input_array:
        graph.add_edge_string(elem)
    return graph


graph_string = '0 a 1\n' \
               '1 a 2\n' \
               '2 a 0\n' \
               '2 b 3\n' \
               '3 b 2'


# resulting_graph = parse_to_graph(graph_string)
# print(resulting_graph.vertices)
# print(resulting_graph.edges)


def create_initial_matrix(graph, gram):
    size = graph.vertices.__len__()
    matrix = [[0 for i in range(size)] for i in range(size)]
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
                    matrix[int(rule_from)][int(rule_to)] = gr_rule_nonterm
    return matrix


# resulting_init_matrix = create_initial_matrix(resulting_graph, resulting_grammar)
# print(resulting_init_matrix)


def create_matrices_for_nonterms(grammar, matrix):
    dictionary = {}
    size = len(matrix)
    for nt in grammar.nonterms:
        key = str(nt)
        value = [[0 for i in range(size)] for i in range(size)]
        for i in range(size):
            for j in range(size):
                if matrix[i][j] == key:
                    value[i][j] = 1
                else:
                    value[i][j] = 0
        dictionary[key] = value
    return dictionary


# resulting_dict = create_matrices_for_nonterms(resulting_grammar, resulting_init_matrix)
# print(resulting_dict)


import numpy

def matrices_to_boolean(dictionary):
    for k in dictionary:
        dictionary[k] = numpy.array(dictionary[k], dtype=bool)
    return dictionary


# resulting_boolean_dict = matrices_to_boolean(resulting_dict)
# print(resulting_boolean_dict)


def mult_two_matrices(m1, m2):
    a = numpy.array(m1, dtype=bool)
    b = numpy.array(m2, dtype=bool)
    return numpy.dot(a, b)
    # return 1*numpy.dot(a,b)


def add_matrix(matrix, result_to_add):
    return matrix.__add__(result_to_add)

from copy import copy

def mult_global_cycle(grammar, dictionary):
    is_something_changed = False
    for r in grammar.rules:
        r_array = r.split(' ')
        if len(r_array) == 3:
            r_from = r_array[0]
            r_result_fst = r_array[1]
            r_result_snd = r_array[2]
            initial_matrix = copy(dictionary[r_from])
            dictionary[r_from] = add_matrix(dictionary[r_from], mult_two_matrices(dictionary[r_result_fst],
                                                                                  dictionary[r_result_snd]))
            if not numpy.array_equal(initial_matrix, dictionary[r_from]):
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
                dictionary[r_from] = add_matrix(dictionary[r_from],
                                                mult_two_matrices(dictionary[r_result_fst], dictionary[r_result_snd]))
                if not numpy.array_equal(initial_matrix, dictionary[r_from]):
                    is_something_changed = True


def calc_solution(graph_str, grammar_str):
    graph = parse_to_graph(graph_str)
    grammar = parse_to_grammar(grammar_str)
    matrix = create_initial_matrix(graph, grammar)
    dictionary = create_matrices_for_nonterms(grammar, matrix)
    size = len(matrix)
    matrix_with_sets = [[[] for k in range(size)] for k in range(size)]
    matrices_to_boolean(dictionary)
    mult_global_cycle(grammar, dictionary)
    for keys in dictionary:
        for i in range(size):
            for j in range(size):
                if dictionary[keys][i][j] != 0:
                    matrix_with_sets[i][j].append(keys)
    return matrix_with_sets

# print(calc_solution(graph_string, grammar_string))

graph_cycle = generate_cycle_graph_str(1000)
grammar_cycle = 'S a\n' \
                'S S S\n' \
                'S N S\n' \
                'N S S'


import time

start = time.time()
print(calc_solution(graph_cycle, grammar_cycle))
end = time.time()
print(end - start)
