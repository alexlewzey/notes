import pandas as pd


def compare_ids(a, b):
    print(id(a) == id(b), id(a), id(b))


df = pd.Series(range(10)).to_frame("n")

df_ref = df
df_copy = df.copy()
print("dfs")
compare_ids(df, df_ref)
compare_ids(df, df_copy)
print()

print("lists")
a = ["a", "b", "c"]
b = ["a", "b", "c"]
compare_ids(a, b)
print()

print("ints")
a = 5
b = 5
compare_ids(a, b)
print()

print("tuples")
a = ("a", "b", "c")
b = ("a", "b", "c")
compare_ids(a, b)
