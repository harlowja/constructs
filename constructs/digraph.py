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

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class DirectedGraph(object):
    """A directed graph class."""
    def __init__(self, name=None):
        self._adj = {}
        self._nodes = OrderedDict()
        self._name = name

    @property
    def name(self):
        return self._name

    def __len__(self):
        return len(self._nodes)

    def __contains__(self, node):
        return self.has_node(node)

    def has_node(self, node):
        return node in self._nodes

    def add_node(self, node, **data):
        if node not in self._nodes:
            self._nodes[node] = {}
            self._adj[node] = OrderedDict()
        self._nodes[node].update(data)

    def edges_iter(self, include_data=False):
        for u in six.iterkeys(self._nodes):
            for (v, data) in six.iteritems(self._adj[u]):
                if include_data:
                    yield (u, v, data)
                else:
                    yield (u, v)

    def remove_node(self, node):
        if not self.has_node(node):
            raise ValueError("Node %r not found" % (node))
        self._nodes.pop(node)
        self._adj.pop(node)
        for (_u, connected_to) in six.iteritems(self._adj):
            if node in connected_to:
                connected_to.pop(node)

    def add_edge(self, u, v, **data):
        if not self.has_node(u):
            raise ValueError("Node %r not found" % (u))
        if not self.has_node(v):
            raise ValueError("Node %r not found" % (v))
        connected_to = self._adj[u]
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
