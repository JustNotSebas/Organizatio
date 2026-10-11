# Per Aspera Ad Astra

# Programa: "Organizatio"
# Metas de este corte:
# 1. Memoria consistente de proveedores y productos
# 2. Habilidad de añadir o eliminar proveedores y productos
# 3. Consulta rápida de un producto por su ID

# Solo para hacerme la vida mas facil
from funcs import ask, save_data, load_data

# Memoria
inventory = {}

# Funciones
def manage_suppliers(action):
    if action == "add":
        print("Añadiendo un nuevo proveedor. Por favor completa los siguientes datos:")
        while True:
            supplier_id = ask("ID interno: ", check=lambda v: v != "" and v not in inventory, error="Ingresa un ID único y valido.")
            name = ask("Nombre legal: ", check=lambda v: v != "", error="Ingresa un nombre válido.")
            contact = ask("Correo electrónico de contacto: ", check=lambda v: "@" in v and "." in v, error="Ingresa una dirección de correo válida.")
            days = ask("Dias de entrega: ", int, lambda v: v > 0, "Ingresa un valor válido (Debe ser mayor a 0).")
            min_qty = ask("Cantidad mínima de ordenes por producto: ", int, lambda v: v > 0, "Ingresa un valor válido (Debe ser mayor a 0).")
            print(f"""
Ingresaste la siguiente información: 
ID Interno: {supplier_id}
Nombre: {name}
Correo electrónico: {contact}
Dias de entrega de productos: {days}
Cantidad minima de ordenes por producto: {min_qty}
            """)
            confirm = ask("¿La información ingresada es correcta? (s/n/c): ", check=lambda v: v.lower() in ("s", "n", "c"), error="Responde s(i), n(o) o c(ancelar).").lower()
            if confirm == "s":
                inventory[supplier_id] = {
                    "name": name,
                    "contact": contact,
                    "active": True,
                    "shipping_days": days,
                    "min_order_qty": min_qty,
                    "products": {},
                }
                print("Proveedor añadido.")
                save_data(inventory)
                break
            elif confirm == "n":
                print("Reiniciando.")
            elif confirm == "c":
                print("Cancelando.")
                return

    elif action == "remove":
        pass
    else:
        print("Acción invalida.")

def manage_products(action):
    if action == "add":
        pass
    elif action == "remove":
        pass
    else:
        print("Acción invalida.")

def check_products():
    pass

def main():
    global inventory
    inventory = load_data()
    action = input("== ")
    if action == "print":
        print(inventory)
    else:
        manage_suppliers(action)

main()
