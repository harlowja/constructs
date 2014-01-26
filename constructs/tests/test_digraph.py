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

import testtools

from constructs import digraph


class TestDirectedGraph(testtools.TestCase):
    def test_not_empty(self):
        g = digraph.DirectedGraph()
        g.add_node(1)
        self.assertFalse(g.empty())
        self.assertEqual(1, len(g))

    def test_is_empty(self):
        g = digraph.DirectedGraph()
        self.assertTrue(g.empty())

    def test_nodes_iter(self):
        g = digraph.DirectedGraph()
        g.add_node(1)
        g.add_node(2)
        self.assertEqual([1, 2], list(g.nodes_iter()))

    def test_edges_iter(self):
        g = digraph.DirectedGraph()
        g.add_node(1)
        g.add_node(2)
        g.add_edge(1, 2)
        g.add_edge(1, 1)
        self.assertEqual([(1, 2), (1, 1)], list(g.edges_iter()))

    def test_successors_predecessors(self):
        g = digraph.DirectedGraph()
        g.add_node(1)
        g.add_node(2)
        g.add_edge(1, 2)
        self.assertEqual([2], list(g.successors_iter(1)))
        self.assertEqual([1], list(g.predecessors_iter(2)))
        self.assertEqual([], list(g.predecessors_iter(1)))
        self.assertEqual([], list(g.successors_iter(2)))

    def test_add_bad_edge(self):
        g = digraph.DirectedGraph()
        g.add_node(1)
        self.assertRaises(ValueError, g.add_edge, 1, 2)

    def test_add_remove_node(self):
        g = digraph.DirectedGraph()
        g.add_node(1)
        g.add_node(2)
        self.assertEqual(2, len(g))
        g.remove_node(1)
        self.assertEqual(1, len(g))

    def test_basic_iter(self):
        g = digraph.DirectedGraph()
        g.add_node(1)
        g.add_node(2)
        g.add_node(3)
        self.assertEqual([1, 2, 3], list(g))

    def test_freeze(self):
        g = digraph.DirectedGraph()
        g.add_node(1)
        self.assertEqual(1, len(g))
        g.freeze()
        self.assertRaises(RuntimeError, g.remove_node, 1)
        self.assertEqual(1, len(g))
        self.assertRaises(RuntimeError, g.add_node, 2)
        self.assertRaises(RuntimeError, g.add_edge, 1, 1)

    def test_freeze_copy(self):
        g = digraph.DirectedGraph()
        g.add_node(1)
        self.assertEqual(1, len(g))
        g.freeze()
        self.assertRaises(RuntimeError, g.remove_node, 1)
        g2 = g.copy()
        g2.add_node(2)
        self.assertEqual(1, len(g))
        self.assertEqual(2, len(g2))
        g2.add_edge(1, 2)
        self.assertEqual(1, len(list(g2.edges_iter())))
        self.assertEqual(0, len(list(g.edges_iter())))

    def test_add_remove_node_edges(self):
        g = digraph.DirectedGraph()
        g.add_node(1)
        g.add_node(2)
        g.add_edge(1, 2)
        self.assertEqual([(1, 2)], list(g.edges_iter()))
        self.assertTrue(g.has_edge(1, 2))
        self.assertEqual([1], list(g.predecessors_iter(2)))
        g.remove_node(1)
        self.assertEqual([], list(g.edges_iter()))
        self.assertRaises(ValueError, g.has_edge, 1, 2)
        self.assertFalse(g.has_node(1))
        self.assertEqual([], list(g.predecessors_iter(2)))
