s = 'AhjdfF'
print(s.lower())


def add(a, b):
    return a + b


def test():
    for j in range(4):
        yield j


g = test()

for n in [1, 10, 5]:
    print('--->',n)
    g = (add(n, i) for i in g)

print("--->", list(g))
