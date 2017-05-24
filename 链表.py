class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class list_A:
    def __init__(self):
        self.head = None
        self.tail = None
    def append(self,data):
        node = Node(data)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def iter(self):
        cur = self.head
        while cur:
            yield cur.data
            cur = cur.next

    def insert(self,idx,value):
        cur = None
        cur_in = 0
        while cur_in < idx:
            if cur is None:
                cur = self.head
            else:
                cur = cur.next
            if cur is None:
                raise Exception('list is not long enough')
            cur_in = cur_in + 1
        node = Node(value)
        node.next = cur.next
        cur.next = node
        if node.next is None:
            self.tail = node

    def remove(self,inx):
        if inx == 0:
            self.head = self.next
            if self.head is None:
                self.tail = None
            return
        cur_in = 0
        cur = None
        while cur_in < inx:
            if cur is None:
                cur = self.head
            else:
                cur = cur.next
            if cur is None:
                raise Exception("list is not long enough")
            cur_in = cur_in + 1
        cur.next = cur.next.next
        if cur.next is None:
            self.tail = cur

if __name__ == '__main__':
    A = list_A()
    for i in range(10):
        A.append(i)

    A.insert(6,10)

    A.remove(3)

    A.remove(6)

    for i in A.iter():
        print(i)
