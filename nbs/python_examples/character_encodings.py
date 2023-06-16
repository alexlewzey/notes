"""Demonstrating the mapping from character to ascii/unicode and from ascii/unicode to
binary representation."""
chars = "abcde"
encoding = [ord(char) for char in chars]
bits = [f"{idx:b}" for idx in encoding]
print(chars)
print(" ".join([str(idx) for idx in encoding]))
print(" ".join(bits))

# the first character is 65
print(f"{65:b}", ord("A"), bytes("A", "utf-8"), b"A"[0])

assert b"abc" == bytes("abc", "utf-8")
assert ord("A") == b"A"[0]
assert str(b"abc", encoding="utf-8") == "abc"

print()
emoji = "😀"
char_ = bytes(emoji, "utf-8")
encoding = [byte_ for byte_ in char_]
bits = [f"{byte_:b}" for byte_ in encoding]
hexs = [hex(byte_) for byte_ in encoding]
print(emoji)
print(char_)
print(encoding)
print(bits)
print(hexs)

print()
with open("numba_.py", "rb") as f:
    content = f.read()[:30]
print(content)
print(" ".join([str(byte_) for byte_ in content]))
print(" ".join([f"{byte_:b}" for byte_ in content]))
