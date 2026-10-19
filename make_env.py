import json
from dotenv import dotenv_values

v = {k: x for k, x in dotenv_values("env").items() if not k.startswith("AWS_") and x}
json.dump({"Variables": v}, open("env.json", "w"))
print(list(v))