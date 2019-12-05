def get_comb(num):
    comb = []
    get_comb_rec(comb, [], [], num)
    return comb

def get_comb_rec(comb, visited, tail, num):
    temp = tail.copy()
    visited.append(num)
    for i in range(1, int((num) / 2) + 1):
        pair = []
        pair.append(num - i)
        pair.append(i)
        tail.extend(pair)
        comb.append(tail.copy())
        for j in pair:
            if j not in visited:
                tail.remove(j)
                get_comb_rec(comb, visited, tail, j)
                tail.append(j)
        tail = temp.copy()

def show(comb, num):
    s= str(num)
    for cmb in comb:
        s += "\n" + str(cmb[0])
        for i, n in enumerate(cmb):
            if i != 0:
                s += "+" + str(n)
    print(s)

def main():
    num = int(input("Enter a number: "))
    comb = get_comb(num)
    show(comb, num)

main()
