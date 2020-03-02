import json

def can_purchase(amount, lock):
    with lock:
        with open("user_settings.json", "r") as jsonFile:
            data = json.load(jsonFile)
        cur = data["money"]
        if amount < cur:
            data["money"] = cur - amount
            with open("user_settings.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                return True
        else:
            return False
