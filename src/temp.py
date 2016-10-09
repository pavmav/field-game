import pandas

d = [{"yy": 5, "jj": 9}, {"jj": 77, "yy": 86}]
r = pandas.DataFrame.from_dict(*[d])
# r = r.append([{"jj":77, "yy":86}])
# print r


def foo(x, y):
    return x * y

d = {"func": foo,
     "kwargs": {"x": 5,
                "y": 7}}

print d["func"](**d["kwargs"])