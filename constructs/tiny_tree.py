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


class _DFSIter(object):
    """Depth first iterator (non-recursive) over the child nodes."""
    def __init__(self, root, include_self=False):
        self.root = root
        self.include_self = bool(include_self)

    def __iter__(self):
        stack = []
        if self.include_self:
            stack.append(self.root)
        else:
            for child_node in self.root:
                stack.append(child_node)
        while stack:
            node = stack.pop()
            # Visit the node.
            yield node
            # Traverse the left & right subtree.
            for child_node in reversed(list(node)):
                stack.append(child_node)


class Tree(object):
    """A tree root class."""
    def __init__(self, root=None):
        self.root = root
        self.metadata = {}

    def empty(self):
        """Returns if the tree has any nodes."""
        return self.root is None

    def node_count(self):
        """Returns how many nodes are in this tree."""
        if self.empty():
            return 0
        return 1 + self.root.child_count(only_direct=False)


class Node(object):
    """A n-ary tree node class."""
    def __init__(self, item, **kwargs):
        self.item = item
        self.parent = None
        self.metadata = dict(kwargs)
        self._children = []

    def add(self, child):
        child.parent = self
        self._children.append(child)

    def empty(self):
        """Returns if the node is a leaf node."""
        return self.child_count() == 0

    def path_iter(self, include_self=True):
        """Yields back the path from this node to the root node."""
        if include_self:
            node = self
        else:
            node = self.parent
        while node is not None:
            yield node
            node = node.parent

    def __contains__(self, item):
        """Returns if this item exists in this node or this nodes children."""
        return self.find(item) is not None

    def __getitem__(self, index):
        # NOTE(harlowja): 0 is the right most index, len - 1 is the left most
        return self._children[index]

    def child_count(self, only_direct=True):
        """Returns how many children this node has, either only the direct
        children of this node or inclusive of all children nodes of this node.
        """
        if not only_direct:
            count = 0
            for _node in self.dfs_iter():
                count += 1
            return count
        return len(self._children)

    def __iter__(self):
        """Iterates over the direct children of this node (right->left)."""
        for c in self._children:
            yield c

    def index(self, item):
        """Finds the child index of a given item, searchs in added order."""
        index_at = None
        for (i, child) in enumerate(self._children):
            if child.item == item:
                index_at = i
                break
        if index_at is None:
            raise ValueError("%s is not contained in any child" % (item))
        return index_at

    def dfs_iter(self, include_self=False):
        """Depth first iteration (non-recursive) over the child nodes."""
        return _DFSIter(self, include_self=include_self)


def _pformat(node, level):
    if level == 0:
        yield str(node.item)
        prefix = ""
    else:
        yield "__%s" % (node.item)
        prefix = " " * 2
    children = list(node)
    for (i, child) in enumerate(children):
        for (j, text) in enumerate(_pformat(child, level + 1)):
            if j == 0 or i + 1 < len(children):
                text = prefix + "|" + text
            else:
                text = prefix + " " + text
            yield text


def pformat(tree):
    """Recursively formats a tree into a nice string representation.

    Example Input:
     yahoo = tt.Tree(tt.Node("CEO"))
     yahoo.root.add(tt.Node("Infra"))
     yahoo.root[0].add(tt.Node("Boss"))
     yahoo.root[0][0].add(tt.Node("Me"))
     yahoo.root.add(tt.Node("Mobile"))
     yahoo.root.add(tt.Node("Mail"))

    Example Output:
     CEO
     |__Infra
     |  |__Boss
     |     |__Me
     |__Mobile
     |__Mail
    """
    if tree.empty():
        return ''
    buf = six.StringIO()
    for line in _pformat(tree.root, 0):
        buf.write(line + "\n")
    return buf.getvalue().strip()
