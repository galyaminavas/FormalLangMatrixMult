import sys


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


def parse_to_grammar_from_path(grammar_path):
    try:
        f = open(grammar_path, 'r')
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)
    grammar = Grammar()
    lines = f.read().splitlines()
    for line in lines:
        grammar.add_rule_string(line)
    f.close()
    return grammar


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


def parse_to_graph_from_path(graph_path):
    try:
        f = open(graph_path, 'r')
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)
    graph = Graph()
    lines = f.read().splitlines()
    for line in lines:
        graph.add_edge_string(line)
    f.close()
    return graph
