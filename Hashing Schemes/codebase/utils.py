class LinkedListNode(object):
    def __init__(self):
        self.next = None
        self.value = None  # has to be tuple (k, v).


class LinkedList(object):
    def __init__(self):
        self.head = None
        self.tail = None

    def search(self, key):  # returns (key, value) of first occurrence O(n)
        if self.head is None:
            return False
        temp = self.head

        while temp:
            if temp.value[0] == key:
                return temp.value
            else:
                temp = temp.next

        return False  # nothing found

    def insert(self, k_v_tuple):  # doesn't check for duplicates (caller should) O(1)
        new_node = LinkedListNode()
        new_node.next = None
        new_node.value = k_v_tuple

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def update(self, k_v_tuple):  # update all the occurrences
        temp = self.head
        while temp:
            if temp.value[0] == k_v_tuple[0]:
                temp.value = k_v_tuple
            temp = temp.next

    def delete(self, key):  # deletes all instances   O(n)
        while self.head and self.head.value[0] == key:  # skip the start of the list
            self.head = self.head.next

        if self.head is None:  # nothing left, (empty list)
            self.tail = None
            return

        temp = self.head
        while True:
            while temp.next and temp.next.value[0] == key:
                temp.next = temp.next.next
            if temp.next:
                temp = temp.next
            else:
                break
        self.tail = temp

    def printlist(self):
        temp = self.head
        if temp is None:
            return
        while temp:
            print("(", temp.value, ")", end="\t")
            temp = temp.next
        print()
