class Node:
    def __init__(self,value):
        self.value = value
        self.next = None

class stack:
    def __init__(self):
        self.top = None

    def push(self,value):
        node = Node(value)
        node.next = self.top
        self.top = node

    def pop(self):
        node = self.top
        self.top = node.next
        return  node.value

if __name__ == "__main__":
    stk = stack()
    exp = '{a*[x/(x+y)]}'
    for i in exp:
        if i in '{[(':
            stk.push(i)
        elif i in '}])':
            v = stk.top.value
            if i == "}" and v != "{":
                raise Exception("{}")
            elif i == "]" and v != "[":
                raise Exception("[]")
            elif i == ")" and v != "(":
                raise Exception("()")
            stk.pop()
    if stk.top is not None:
        raise Exception("stack is failed")
    print("OK")