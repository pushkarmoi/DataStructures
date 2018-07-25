from numpy.random import choice


class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = self.right = self.up = self.down = None


class SkipList(object):
    def __init__(self, chance=0.3):
        self.lists = [None]	# list of pointers to lists
        self.chance = chance  # chance of adding a node to the upper level
        return

    def search(self, value):
        status, _ = self.internalsearch(value)
        return status

    def internalsearch(self, value, additions=True):  # returns->  status, (success/failPOINT)
        level = 0
        temp = None

        if len(self.lists) == 1 and (self.lists[0] is None):
            return False, None

        for currlist in self.lists:
            if value == currlist.value:
                return True, currlist
            elif value > currlist.value:
                temp = currlist
                break
            else:
                level += 1

        if not temp:
            return False, self.lists[-1]  # returns a

        while temp:
            if temp.value == value:
                return True, temp
            elif (temp.right is None) or (temp.right.value > value):
                if temp.down is None:
                    return False, temp
                temp = temp.down
                level += 1
            else:
                temp = temp.right
                if (temp.up is None) and (additions):
                    above = self.insertAbove(temp.value, level)  # source of spikes in run time
                    if above:
                        if level == 0: level += 1  # as a new level was added above by insertAbove
                        above.down = temp
                        temp.up = above

    def insertAbove(self, nodeValue, nodeLevel):
        x = choice([0, 1], p=[1-self.chance, self.chance])  # a numpy function!
        if x == 0:
            return False  # do not insert above

        if nodeLevel == 0:
            newnode = Node(nodeValue)
            self.lists.insert(0, newnode)
            return newnode
        else:
            return self.insertAtLevel(nodeValue, nodeLevel-1)

    def insertAtLevel(self, value, level):  # only level 1+
        if level not in range(0, len(self.lists)):
            print("Wrong arg as level, insertAtLevel, level=", level, ", size of list-store=", len(self.lists))
            return None
        temp = self.lists[level]  # will be not None
        if temp is None: print("invariant compromised, insertAtLevel")

        if temp.value == value:
            return None
        if temp.value > value:
            newnode = Node(value)
            newnode.right = temp
            temp.left = newnode
            self.lists[level] = newnode
            return newnode

        while True:
            if (temp.right is None) or (temp.right.value > value):
                # insert b/w temp and temp.right
                newnode = Node(value)
                newnode.right = temp.right
                newnode.left = temp
                temp.right = newnode
                if newnode.right: newnode.right.left = newnode
                return newnode
            else:
                temp = temp.right

    def insert(self, value):
        status, failpoint = self.internalsearch(value)
        if not status:
            if failpoint is None:
                old_first = self.lists[0]
                newnode = Node(value)
                self.lists[0] = newnode
                newnode.right = old_first
                if old_first:
                    old_first.left = newnode
                return True
            
            newnode = Node(value)
            for i, currlist in enumerate(self.lists):
                if currlist is failpoint:  # yes, failpoint is first element
                    if value < currlist.value:
                        old_first = currlist
                        self.lists[i] = newnode
                        newnode.right = old_first
                        if old_first:
                            old_first.left = newnode
                        return True
                    else:
                        break

            newnode.right = failpoint.right
            newnode.left = failpoint
            failpoint.right = newnode
            if newnode.right: newnode.right.left = newnode
            return True
        else:
            # num already exists
            return True

    def delete(self, value, search=True, node=None):
        if search:
            status, successpoint = self.internalsearch(value, additions=False)
            if not status:
                print("inside delete couldnt find node=", value, "in the tree")
                return False  # num not present
            else:
                result = self.delete(value, search=False, node=successpoint)
                # fix structure
                i = len(self.lists) - 2
                while i>=0:
                    if self.lists[i] is None:
                        del self.lists[i]
                    i -= 1
                return result
        elif node:
            if node.down:
                self.delete(value, search=False, node=node.down)
            if node.left:
                node.left.right = node.right
            if node.right:
                node.right.left = node.left
            if node.up:
                node.up.down = None
            if node.down:
                print("INVARIANT ERROR in recursive delete, down still present.")
            if not node.left:
                for i, currlist in enumerate(self.lists):
                    if currlist is node:
                        self.lists[i] = node.right
                        break
            return True
        else:
            print("invariant compromised, delete (entry node is None)")
            return False

    def printlists(self):
        for currlist in self.lists:
            if currlist is None:
                print("None")
                continue
            else:
                temp = currlist
                while temp:
                    print(temp.value, end="--")
                    temp = temp.right
                print()

    def invariantcheck(self):
        for level, currlist in enumerate(self.lists):
            # level check
            if (currlist is None) and (level != 0):
                print("self.list points to NONE, when level=", level)
                return False
            temp = currlist
            while temp:
                if temp.right and (temp.value > temp.right.value):
                    print("left key is greater than right key", temp.value, temp.right.value)
                    self.printlists()
                    return False
                if (temp.up and level==0) or (temp.up and (temp.up.value != temp.value)):
                    print("up value doesnt match current", temp.value, temp.up.value)
                if (temp.down and level==(len(self.lists)-1)) or (temp.down and (temp.value != temp.down.value)):
                    print("down value doesnt match current", temp.value, temp.down.value)
                temp = temp.right
        
        return True

