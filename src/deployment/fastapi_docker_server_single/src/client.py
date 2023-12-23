import requests

with open("example_data.json", "rb") as f:
    data = f.read()

res = requests.post(
    "http://localhost:80/predict",
    headers={"Content-Type": "application/json"},
    data=data,
)
print(res.status_code, res.text)
