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

def confirm(prompt="¿La información ingresada es correcta? "):
    return ask(prompt + "(s/n/c): ", check=lambda v: v.lower() in ("s", "n", "c"), error="Responde s(i), n(o) o c(ancelar).").lower()

def pick_supplier(inventory, prompt):
    for sid, data in inventory.items():
        print(f"- {data['name']} ({sid})")
    return ask(prompt, check=lambda v: v.upper() in inventory, error="El ID ingresado no corresponde a un proveedor válido.").upper()

def find_product(inventory, pid):
    for sid, supplier in inventory.items():
        if pid in supplier["products"]:
            return sid, supplier["products"][pid]
    return None

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
