"""Sending test request to the api."""
import requests

payload = {
    "sepal_length": 6.3,
    "sepal_width": 2.3,
    "petal_length": 4.4,
    "petal_width": 1.3,
}
r = requests.get("http://0.0.0.0:5000/predict/flower", params=payload)
print(r.json())
