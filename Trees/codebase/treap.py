import random
import sys 


class TreapNode(object):
    def __init__(self, value):
        self.value = value
        self.priority = float(round(random.uniform(0.0, 1.0), 3))
        self.left = None
        self.right = None
        self.parent = None


class Treap(object):
    def __init__(self):
        self.root = None

    def search(self, value):
        temp = self.root
        while True:
            if temp is None:
                return False
            elif temp.value == value:
                return True
            elif value < temp.value:
                temp = temp.left
            else:
                temp = temp.right

    def insert(self, value):
        # add as in normal BST.
        node = TreapNode(value)
        if self.root is None:
            self.root = node
            return True

        temp = self.root
        while True:
            if temp.value == value:
                return True
            elif value < temp.value:
                if temp.left is None:
                    temp.left = node
                    node.parent = temp
                    break
                else:
                    temp = temp.left
            else:
                if temp.right is None:
                    temp.right = node
                    node.parent = temp
                    break
                else:
                    temp = temp.right

        # now, rotate as to satisfy heap-ordered tree on "priority"
        parent = node.parent
        while parent:
            if parent.priority <= node.priority:
                return True
            else:
                if parent.left is node:
                    self.rightrotate(node)
                else:
                    self.leftrotate(node)
            parent = node.parent

        # you reached, the top, (the root)
        self.root = node
        return True

    def delete(self, value):
        # go to that value.
        # do rotations, such that it becomes a leaf.
        # then just delete it.
        temp = self.root
        while True:
            if temp is None:
                return False
            elif temp.value == value:
                break
            elif value < temp.value:
                temp = temp.left
            else:
                temp = temp.right

        todelete = temp
        while (todelete.left is not None) or (todelete.right is not None):
            mins = []
            if todelete.left: mins.append(todelete.left.priority)
            if todelete.right: mins.append(todelete.right.priority)
            minima = min(mins)
            if todelete.left and (minima == todelete.left.priority):
                self.rightrotate(todelete.left)  # goes up
            elif todelete.right and (minima == todelete.right.priority):
                self.leftrotate(todelete.right)  # goes up

        parent = todelete.parent
        if parent.left is todelete:
            parent.left = None
        else:
            parent.right = None
        del todelete
        return True

    def leftrotate(self, entry):  # entry goes up!
        entry.parent.right = entry.left
        if entry.left:
            entry.left.parent = entry.parent

        org_parent = entry.parent.parent
        entry.parent.parent = entry

        entry.left = entry.parent
        entry.parent = org_parent

        if org_parent:
            if entry.left is org_parent.right:
                org_parent.right = entry
            else:
                org_parent.left = entry
        else:
            self.root = entry

    def rightrotate(self, entry):  # entry goes up!
        entry.parent.left = entry.right
        if entry.right:
            entry.right.parent = entry.parent

        org_parent = entry.parent.parent
        entry.parent.parent = entry

        entry.right = entry.parent
        entry.parent = org_parent

        if org_parent:
            if entry.right is org_parent.right:
                org_parent.right = entry
            else:
                org_parent.left = entry
        else:
            self.root = entry

    def inorder(self, root, buf):
        if root is None:
            return
        else:
            self.inorder(root.left, buf)
            buf.append(root.value)
            self.inorder(root.right, buf)

    def sanitycheck(self):
        # print through BFS and then traverse all to get height
        # make a list, store tuples; (value, depth)
        # nodes with same depth go on one line
        if self.root is None:
            print("Sanity check: No root")
            return

        frontier = [(self.root, 0)]
        index = 0

        while index < len(frontier):  # there are elements which haven't been processed
            entry = frontier[index][0]
            depth = frontier[index][1]
            index += 1
            neighbors = []
            if entry.left:
                    if entry.left.priority < entry.priority: print("NOT HEAP ORDERED!")
                    neighbors.append(entry.left)
            if entry.right:
                    if entry.right.priority < entry.priority: print("NOT HEAP ORDERED!")
                    neighbors.append(entry.right)
            for n in neighbors:
                    temp_tuple = (n, depth+1)
                    frontier.append(temp_tuple)

        # print the frontier, depth-wise
        print("Printing tree")
        depth = 0
        while len(frontier) > 0:
            val = frontier[0][0].value
            prio = frontier[0][0].priority
            dep = frontier[0][1]
            if dep != depth:
                print()
                print(str((val, prio)), end="  ")
                depth = dep
            else:
                print(str((val, prio)), end="  ")
            del frontier[0]
        print()

