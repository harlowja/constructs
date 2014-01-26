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

from constructs import tiny_tree


class TestTinyTree(testtools.TestCase):
    def test_not_empty(self):
        t = tiny_tree.Tree()
        t.root = tiny_tree.Node("a")
        self.assertFalse(t.empty())
        self.assertEqual(1, t.node_count())

    def test_dfs_iter(self):
        t = tiny_tree.Tree()
        t.root = tiny_tree.Node("a")
        t.root.add(tiny_tree.Node("b"))
        t.root[0].add(tiny_tree.Node("c"))
        t.root.add(tiny_tree.Node("d"))
        nodes = list(t.root.dfs_iter(include_self=True))
        nodes = [n.item for n in nodes]
        self.assertEqual(['a', 'b', 'c', 'd'], nodes)

    def test_bfs_iter(self):
        t = tiny_tree.Tree()
        t.root = tiny_tree.Node("a")
        t.root.add(tiny_tree.Node("b"))
        t.root[0].add(tiny_tree.Node("c"))
        t.root[0][0].add(tiny_tree.Node("c.1"))
        t.root[0][0].add(tiny_tree.Node("c.2"))
        t.root.add(tiny_tree.Node("d"))
        nodes = list(t.root.bfs_iter(include_self=True))
        nodes = [n.item for n in nodes]
        self.assertEqual(['a', 'd', 'b', 'c', 'c.2', 'c.1'], nodes)
