class Node:
    def __init__(self,data):
        self.data = data
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
        return node.data

func_map = {
    '+':lambda x,y:x+y,
    '-':lambda x,y:x-y,
    '*':lambda x,y:x*y,
    '/':lambda x,y:x/y
}

# ( 3 + 6 / 2 ) * 4 / ( 2 + ( 6 / ( 1 + 1 ) + 5 ) )
# ( 6 / 2 + 3 ) * 4 / ( 2 + ( 6 / ( 1 + 1 ) + 5 ) )

def sub_s(stk):
    while True:
        i = stk.pop()
        if stk.top is not None:
            if stk.top.data in "+-*/":
                meth = stk.pop()
                i = func_map[meth](i,stk.pop())
                stk.push(i)
        else:
            break
    return i

def fromat(str):
    str = str.replace("+", " + ")
    str = str.replace("-", " - ")
    str = str.replace("*", " * ")
    str = str.replace("/", " / ")
    str = str.replace("(", " ( ")
    str = str.replace(")", " ) ")
    return str

def cacl(expr):
    stk = stack()
    stk2 = stack()
    stk3 = stack()
    for i in fromat(expr).split():
        if i in "(+-*/":
            stk.push(i)
            continue
        if i.strip() == "":
            continue
        try:
            i = int(i)
        except:
            try:
                i = float(i)
            except:
                if i in ")":
                    while True:
                        if stk.top.data != '(':
                            i = stk.pop()
                            if isinstance(i,(int,float)):
                                if stk3.top is not None:
                                    stk3.push(i)
                                else:
                                    stk2.push(i)
                            elif i in "+-":
                                if stk3.top is not None:
                                    stk2.push(sub_s(stk3))
                                stk2.push(i)
                            elif i in "*/":
                                if stk3.top is None:
                                    stk3.push(stk2.pop())
                                stk3.push(i)
                            else:
                                raise Exception("错误的表达式 --------")
                        else:
                            stk.pop()
                            if stk3.top is not None:
                                stk2.push(sub_s(stk3))
                            i = sub_s(stk2)
                            break
                    else:
                        raise Exception("没有跳出循环")
                else:
                    raise Exception("需要 (")
        stk.push(i)

    while stk.top:
        i = stk.pop()
        if isinstance(i,(int,float)):
            if stk3.top is not None:
                stk3.push(i)
            else:
                stk2.push(i)
        elif i in "+-":
            if stk3.top is not None:
                stk2.push(sub_s(stk3))
            stk2.push(i)
        elif i in "*/":
            if stk3.top is None:
                stk3.push(stk2.pop())
            stk3.push(i)
        else:
            raise Exception("错误的表达式")

    if stk3.top is not None:
        stk2.push(sub_s(stk3))
    return sub_s(stk2)

if __name__ == "__main__":
    print(cacl("(60 + 2 * 3.2) / ( 20 + ( 6 / ( 1 + 10 ) + 5 ) )"))
