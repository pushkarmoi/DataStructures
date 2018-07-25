class AVLNode(object):
    def __init__(self, value):
        self.value = value
        self.height = -1
        self.left = None
        self.right = None
        self.parent = None


class AVL(object):
    def __init__(self):
        self.root = None

    def search(self, value):
        status, node = self.internalsearch(value)
        return status

    def internalsearch(self, value):
        temp = self.root
        while True:
            if temp is None:
                return False, None
            elif temp.value == value:
                return True, temp
            elif value < temp.value:
                temp = temp.left
            else:
                temp = temp.right

    def insert(self, value, entry=None):  # insert and balance
        node = AVLNode(value)
        node.height = 0

        if self.root is None:
            self.root = node
            return True

        if entry is None:
            entry = self.root

        # compare with value and insert in left/right subtree
        if entry.value == value:
            return True
        elif value < entry.value:
            if entry.left is None:
                entry.left = node
                node.parent = entry
            else:
                self.insert(value, entry=entry.left)
        elif value > entry.value:
            if entry.right is None:
                entry.right = node
                node.parent = entry
            else:
                self.insert(value, entry=entry.right)

        # rebalance? (entry might change)
        l_height, r_height = self.getheights(entry)  # fresh height! after insert
        difference = abs(l_height - r_height)
        if difference > 1:
            self.rebalance(entry)  # REBALANCE ALSO UPDATES ALL THE HEIGHTS
        else:
            l_height, r_height = self.getheights(entry)
            entry.height = 1 + max(l_height, r_height)

        return True

    def delete(self, value):
        # delete as in BST.
        # if actually deleted? Then go up, and rebalance.
        status, entry = self.internalsearch(value)
        if not status:
            return False

        if entry.left and entry.right:
            # find successor,
            # call delete on that
            successor = self.getSuccessor(entry)
            if not successor:
                print("invariant violated, no successor for node with left & right children!")
            val_to_put = successor.value
            self.delete(val_to_put)
            entry.value = val_to_put
            return True
        else:
            #  nothing on left/right
            if (entry.left is None) and entry.right:
                temp = entry.right
                entry.value = temp.value
                entry.height = temp.height
                entry.left = temp.left
                entry.right = temp.right
                if entry.left: entry.left.parent = entry
                if entry.right: entry.right.paent = entry
                parent = entry.parent
            elif (entry.left is None) and entry.left:
                temp = entry.left
                entry.value = temp.value
                entry.height = temp.height
                entry.left = temp.left
                entry.right = temp.right
                if entry.left: entry.left.parent = entry
                if entry.right: entry.right.paent = entry
                parent = entry.parent
            else:
                parent = entry.parent
                if value > parent.value: parent.right = None
                else: parent.left = None

        # readjust the height, and rebalance wherever required
        while parent is not None:
            l_h, r_h = self.getheights(parent)
            parent.height = 1 + max(l_h, r_h)
            if abs(l_h - r_h) > 1:
                self.rebalance(parent)
            parent = parent.parent
        return True

    def rebalance(self, entry):
        if entry is None:
            return
        l_height = -1
        if entry.left is not None: l_height = entry.left.height
        r_height = -1
        if entry.right is not None: r_height = entry.right.height

        if r_height > (1 + l_height):
            r_l_height = -1
            if entry.right.left is not None: r_l_height = entry.right.left.height
            r_r_height = -1
            if entry.right.right is not None: r_r_height = entry.right.right.height

            if r_r_height >= r_l_height:  # right-right is heavy
                self.leftrotation(entry)
            else:  # right-left is heavy
                self.rightrotation(entry.right)
                self.leftrotation(entry)
        elif l_height > (1 + r_height):
            l_l_height = -1
            if entry.left.left is not None: l_l_height = entry.left.left.height
            l_r_height = -1
            if entry.left.right is not None: l_r_height = entry.left.right.height

            if l_l_height >= l_r_height:  # left-left is heavy
                self.rightrotation(entry)
            else:  # left-right is heavy
                self.leftrotation(entry.left)
                self.rightrotation(entry)

    def leftrotation(self, entry):  # on the parent node (entry goes down)
        parent = entry.parent
        right_subtree = entry.right

        if right_subtree is None:
            return

        # left-child of right tree
        if right_subtree.left:
            right_subtree.left.parent = entry
        entry.right = right_subtree.left
        l_h, r_h = self.getheights(entry)
        entry.height = 1 + max(l_h, r_h)

        # update right_subtree
        right_subtree.left = entry
        entry.parent = right_subtree

        l_h, r_h = self.getheights(right_subtree)
        right_subtree.height = 1 + max(l_h, r_h)

        # attach to tree
        right_subtree.parent = parent
        if parent:
            if parent.left is entry:
                parent.left = right_subtree
            else:
                parent.right = right_subtree

        # must be th root node.
        if parent is None:
            self.root = right_subtree
        return

    def rightrotation(self, entry):  # on the parent node (entry goes down)
        parent = entry.parent
        left_subtree = entry.left

        if left_subtree is None:
            return

        # right child of left subtree
        if left_subtree.right: left_subtree.right.parent = entry
        entry.left = left_subtree.right
        l_h, r_h = self.getheights(entry)
        entry.height = 1 + max(l_h, r_h)

        # update left-subtree
        left_subtree.right = entry
        entry.parent = left_subtree

        l_h, r_h = self.getheights(left_subtree)
        left_subtree.height = 1 + max(l_h, r_h)
        # attach to tree
        left_subtree.parent = parent
        if parent:
            if parent.left is entry:
                parent.left = left_subtree
            else:
                parent.right = left_subtree

        # must be th root node.
        if parent is None:
            self.root = left_subtree

        return

    def getSuccessor(self, node):
        if (node is None) or (node.right is None):
            return None

        temp = node.right
        while temp.left is not None:
            temp = temp.left

        return temp

    def getheights(self, entry):  # return height of children (-1,-1 if no children)
        left_height = -1
        right_height = -1
        if entry is None:
            return None
        if entry.left is not None:
            left_height = entry.left.height
        if entry.right is not None:
            right_height = entry.right.height
        return left_height, right_height

    def traverse(self, entry, buffer):
        if entry is None:
            return
        else:
            self.traverse(entry.left, buffer)
            buffer.append(entry.value)
            self.traverse(entry.right, buffer)

    def sanitycheck(self):
        # print through BFS and then traverse all to get height
        # make a list, store tuples; (value, depth)
        # nodes with same depth go on one line
        print("doing sanity check!")
        if self.root is None:
            print("Sanity check: No root")
            return

        frontier = [(self.root, 0)]
        index = 0

        while index < len(frontier):
            entry = frontier[index][0]
            depth = frontier[index][1]
            index += 1

            # do height check
            l_h, r_h = self.getheights(entry)
            if abs(l_h - r_h) > 1:
                print("Height not balanced at value=", entry.value)
            else:
                neighbors = []
                if entry.left:
                    neighbors.append(entry.left)
                if entry.right:
                    neighbors.append(entry.right)
                for n in neighbors:
                    temp_tuple = (n, depth+1)
                    frontier.append(temp_tuple)

        # print the frontier, depth-wise
        print("height check done. Printing tree")
        depth = 0
        while len(frontier) > 0:
            val, dep = frontier[0]
            if dep != depth:
                print()
                print(val.value, end="  ")
                depth = dep
            else:
                print(val.value, end="  ")
            del frontier[0]
        print()



