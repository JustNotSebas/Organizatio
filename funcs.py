import json

def ask(prompt, cast=str, check=None, error="Entrada inválida."):
    while True:
        try:
            value = cast(input(prompt).strip())
        except ValueError:
            print(error)
            continue
        if check and not check(value):
            print(error)
            continue
        return value
    
def save_data(data):
    with open("inventory.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
def load_data():
    try:
        with open("inventory.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return data
