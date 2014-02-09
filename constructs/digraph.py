# -*- coding: utf-8 -*-

# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Copyright (C) 2014 Yahoo! Inc. All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import six

from constructs import ordereddict


class _DFSIter(object):
    def __init__(self, graph, source):
        self.graph = graph
        self.source = source

    def __iter__(self):
        if not self.graph.has_node(self.source):
            raise ValueError("Source node %r not found" % (self.source))
        stack = [self.source]
        visited = set()
        while stack:
            node = stack.pop()
            if id(node) in visited:
                continue
            yield node
            visited.add(id(node))
            stack.extend(self.successors_iter(node))


class DirectedGraph(object):
    """A directed graph class."""
    def __init__(self, name=None):
        self._adj = {}
        self._pred = {}
        self._nodes = ordereddict.OrderedDict()
        self._name = name
        self._frozen = False

    @property
    def name(self):
        return self._name

    def __len__(self):
        return len(self._nodes)

    def __contains__(self, node):
        return self.has_node(node)

    def empty(self):
        return len(self._nodes) == 0

    def has_node(self, node):
        return node in self._nodes

    def freeze(self):
        self._frozen = True

    def __iter__(self):
        for node in self.nodes_iter():
            yield node

    def copy(self):
        c = DirectedGraph(name=self.name)
        for (node, data) in self.nodes_iter(include_data=True):
            c.add_node(node, **data)
        for (u, v, data) in self.edges_iter(include_data=True):
            c.add_edge(u, v, **data)
        return c

    def add_node(self, node, **data):
        if self._frozen:
            raise RuntimeError("Can not add nodes to a frozen graph")
        if node not in self._nodes:
            self._nodes[node] = {}
            self._adj[node] = ordereddict.OrderedDict()
            self._pred[node] = []
        self._nodes[node].update(data)

    def dfs_iter(self, source):
        return _DFSIter(self, source)

    def edges_iter(self, include_data=False):
        for u in six.iterkeys(self._nodes):
            for (v, data) in six.iteritems(self._adj[u]):
                if include_data:
                    yield (u, v, data)
                else:
                    yield (u, v)

    def successors_iter(self, node, include_data=False):
        if not self.has_node(node):
            raise ValueError("Node %r not found" % (node))
        for (succ, data) in six.iteritems(self._adj[node]):
            if include_data:
                yield (succ, data)
            else:
                yield succ

    def predecessors_iter(self, node, include_data=False):
        if not self.has_node(node):
            raise ValueError("Node %r not found" % (node))
        for pred in self._pred[node]:
            if not include_data:
                yield pred
            else:
                yield (pred, self._adj[pred][node])

    def remove_node(self, node):
        if not self.has_node(node):
            raise ValueError("Node %r not found" % (node))
        if self._frozen:
            raise RuntimeError("Can not remove nodes from a frozen graph")
        self._nodes.pop(node)
        self._pred.pop(node)
        self._adj.pop(node)
        for (_node, connected_to) in six.iteritems(self._adj):
            if node in connected_to:
                connected_to.pop(node)
        for (_node, preds) in six.iteritems(self._pred):
            if node in preds:
                preds.remove(node)

    def has_edge(self, u, v):
        if not self.has_node(u):
            raise ValueError("Node %r not found" % (u))
        if not self.has_node(v):
            raise ValueError("Node %r not found" % (v))
        connected_to = self._adj[u]
        if v in connected_to:
            return True
        return False

    def add_edge(self, u, v, **data):
        if not self.has_node(u):
            raise ValueError("Node %r not found" % (u))
        if not self.has_node(v):
            raise ValueError("Node %r not found" % (v))
        if self._frozen:
            raise RuntimeError("Can not add edges to a frozen graph")
        connected_to = self._adj[u]
        if u not in self._pred[v]:
            self._pred[v].append(u)
        if v in connected_to:
            connected_to[v].update(data)
        else:
            connected_to[v] = dict(data)

    def nodes_iter(self, include_data=False):
        for (node, data) in six.iteritems(self._nodes):
            if include_data:
                yield (node, data)
            else:
                yield node
