import json

import numpy as np
import requests

endpoint = "http://0.0.0.0:3000/predict"

data = json.dumps(np.random.rand(1, 7).tolist())
res = requests.post(endpoint, headers={"content_type": "application/json"}, data=data)
print(res.status_code, json.loads(res.text)[0])
