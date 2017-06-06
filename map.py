class Node:
    def __init__(self,key,value):
        self.key = key
        self.value = value

    def __eq__(self, other):
        return self.key == other.key

class Map:
    def __init__(self,init_size,hash=hash):
        self.__slot = [[] for _ in range(init_size)]
        self.__size = init_size
        self.hash = hash

    def put(self,key,value):
        node = Node(key,value)
        address = self.hash(node.key) % self.__size
        self.__slot[address].append(node)

    def get(self,key,default = None):
        address = self.hash(key) % self.__size
        for node in self.__slot[address]:
            if node.key == key:
                return node.value
        return default

    def remove(self,key):
        address = self.hash(key) % self.__size
        try:
            self.__slot[address].remove(Node(key, None))
            # 等值判断 的标准是 Node.__eq__()方法
            # key 一样认为这两个是一致的
        except ValueError:
            print("error")

if __name__ == "__main__":
    map = Map(16)

    for i in range(20):
        map.put(i,i)

    map.remove(3)

    for i in range(20):
        print(map.get(i,"not set"))