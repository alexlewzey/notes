"""How to read and write a stream of bytes."""
import io

bytes_io = io.BytesIO()
data = "lasdjflkasdjf"
bytes_io.write(data.encode(encoding="utf-8"))
bytes_io.seek(0)
wrapper = io.TextIOWrapper(bytes_io)
output = wrapper.read()

print(output)
assert data == output
