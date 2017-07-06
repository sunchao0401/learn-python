print(
'''
给出一个区间[a, b]，计算区间内“神奇数”的个数。
神奇数的定义：存在不同位置的两个数位，组成一个两位数（且不含前导0），且这个两位数为质数。
比如：153，可以使用数字3和数字1组成13，13是质数，满足神奇数。同样153可以找到31和53也为质数，只要找到一个质数即满足神奇数。
'''
)
def is_prime(number):
    for i in range(2,number):
        if number % i == 0:
            return False
    return True

def find_magic(a, b):
    count = 0
    for i in range(a,b+1):
        mark = False
        ret = []
        for j in str(i):
            ret.append(j)

        if len(ret) == 1:
            k = ret.pop()
            if is_prime(int(k)):
                mark = True

        while len(ret) > 1:
            k = ret.pop()
            if int(k) == 0:
                continue
            for j in ret:
                if int(j) == 0:
                    continue
                if is_prime(int(k + j)) or is_prime(int(j + k)):
                    mark = True
                    break
        if mark:
            count += 1
    print(count)

if __name__ == "__main__":
    number  = input()
    x = int(number.split()[0])
    y = int(number.split()[1])
    find_magic(x,y)