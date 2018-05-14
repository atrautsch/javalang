import pickle
from collections import deque

import six


class MetaNode(type):
    def __new__(mcs, name, bases, dict):
        attrs = list(dict['attrs'])
        dict['attrs'] = list()

        for base in bases:
            if hasattr(base, 'attrs'):
                dict['attrs'].extend(base.attrs)

        dict['attrs'].extend(attrs)

        return type.__new__(mcs, name, bases, dict)


@six.add_metaclass(MetaNode)
class Node(object):
    attrs = ()

    def __init__(self, **kwargs):
        values = kwargs.copy()

        for attr_name in self.attrs:
            value = values.pop(attr_name, None)
            setattr(self, attr_name, value)

        if values:
            raise ValueError('Extraneous arguments')

    def __equals__(self, other):
        if type(other) is not type(self):
            return False

        for attr in self.attrs:
            if getattr(other, attr) != getattr(self, attr):
                return False

        return True

    def __repr__(self):
        return type(self).__name__

    def __iter__(self):
        return walk_tree(self)

    def filter(self, pattern):
        for path, node in self:
            if ((isinstance(pattern, type) and isinstance(node, pattern)) or
                (node == pattern)):
                yield path, node

    @property
    def children(self):
        return [getattr(self, attr_name) for attr_name in self.attrs]
    
    @property
    def position(self):
        if hasattr(self, "_position"):
            return self._position

    @property
    def end_position(self):
        if hasattr(self, "_end_position"):
            return self._end_position


def walk_tree2(root):
    """The standard recursive ast dfs traversal from javalang."""
    children = None

    if isinstance(root, Node):
        yield (), root
        children = root.children
    else:
        children = root

    for child in children:
        if isinstance(child, (Node, list, tuple)):
            for path, node in walk_tree(child):
                yield (root,) + path, node


def _parent_path(node, parent_links):
    """We are ineffectively iterating over a list of tuples here."""
    pp = ()

    while node:
        for pl in parent_links:
            if pl[0] == node:
                if pl[1]:  # CompilationUnit has None as parent but we do not want that added
                    pp = (pl[1],) + pp
                node = pl[1]
                break
        else:
            break
    return pp


def walk_tree(root):
    """We iteratively dfs the ast."""
    qu = deque()
    parent_links = [(root, None)]  # parent or child can be a list so we can not use a key value pair

    yield (), root

    node = root

    while node or qu:
        children = []
        if isinstance(node, (list, tuple)):
            children = node
        if isinstance(node, Node):
            children = node.children

        for c in reversed(children):  # reverse the children because we emulate a stack
            parent_links.append((c, node))
            qu.append(c)

        try:
            node = qu.pop()
        except IndexError:
            node = None

        if isinstance(node, Node):
            pp = _parent_path(node, parent_links)
            yield pp, node


def dump(ast, file):
    pickle.dump(ast, file)


def load(file):
    return pickle.load(file)
