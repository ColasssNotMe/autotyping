import json

data = {"num1": "10", "num2": "20", "num3": "30"}

with open("data.json", "w") as f:
    json.dump(data, f)

with open("data.json", "r") as f:
    print(json.load(f["num1"]))
