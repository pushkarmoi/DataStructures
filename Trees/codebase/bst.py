class BSTNode(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST(object):
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

    def insert(self, value):  # add new
        node = BSTNode(value)

        if self.root is None:
            self.root = node
            return True

        if self.search(value):  # already exists
            return True

        temp = self.root
        while True:
            if value < temp.value:
                if temp.left is None:
                    temp.left = node
                    break
                else:
                    temp = temp.left
            else:
                if temp.right is None:
                    temp.right = node
                    break
                else:
                    temp = temp.right

        return True

    def delete(self, value):
        status, node = self.internalsearch(value)
        if not status:
            return False

        if (node.left is None) and (node.right is None):
            self.replaceWith(node.value, None)
        elif node.left is None:
            self.replaceWith(node.value, node.right)
        elif node.right is None:
            self.replaceWith(node.value, node.left)
        else:
            successor = self.getSuccessor(node)
            if not successor:
                return False
            val_to_put = successor.value
            self.delete(val_to_put)
            node.value = val_to_put

        return 0

    def getSuccessor(self, node):
        if (node is None) or (node.right is None):
            return False
        temp = node.right
        while temp.left is not None:
            temp = temp.left
        return temp

    def replaceWith(self, value, toReplace):
        if self.root is None:
            return False
        if self.root.value == value:
            self.root = toReplace
            return True

        temp = self.root
        while True:
            if value < temp.value:
                if temp.left is None:
                    return False
                if temp.left.value == value:
                    temp.left = toReplace
                    return True
                temp = temp.left
            else:
                if temp.right is None:
                    return False
                if temp.right.value == value:
                    temp.right = toReplace
                    return True
                temp = temp.right

