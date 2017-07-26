from collections import defaultdict


def tree():
    return defaultdict(tree)


def dump_tree(t, path):
    for node in path:
        t = t[node]


def dicts(t):
    return {k.title: dicts(t[k]) for k in t} 
