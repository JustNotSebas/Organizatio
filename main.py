# Per Aspera Ad Astra

# Programa: "Organizatio"
# Metas de este corte:
# 1. Memoria consistente de proveedores y productos
# 2. Habilidad de añadir o eliminar proveedores y productos
# 3. Consulta rápida de un producto por su ID

# Solo para hacerme la vida mas facil
from funcs import ask, save_data, load_data, pick_supplier, confirm
import sys

# Memoria
inventory = {}

# Funciones
def manage_suppliers(action):
    if action == "add":
        print("Añadiendo un nuevo proveedor. Por favor completa los siguientes datos:")
        while True:
            sid = ask("ID interno: ", check=lambda v: v != "" and v.upper() not in inventory, error="Ingresa un ID único y valido.").upper()
            name = ask("Nombre legal: ", check=lambda v: v != "", error="Ingresa un nombre válido.")
            contact = ask("Correo electrónico de contacto: ", check=lambda v: "@" in v and "." in v, error="Ingresa una dirección de correo válida.")
            days = ask("Dias de entrega: ", int, lambda v: v > 0, "Ingresa un valor válido (Debe ser mayor a 0).")
            min_qty = ask("Cantidad mínima de ordenes por producto: ", int, lambda v: v > 0, "Ingresa un valor válido (Debe ser mayor a 0).")
            print(f"""
Ingresaste la siguiente información: 
ID Interno: {sid}
Nombre: {name}
Correo electrónico: {contact}
Dias de entrega de productos: {days}
Cantidad minima de ordenes por producto: {min_qty}
            """)
            c = confirm()
            if c == "s":
                inventory[sid] = {
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
            elif c == "n":
                print("Reiniciando.")
            elif c == "c":
                print("Cancelando.")
                return
            
    elif action == "remove":
        if not inventory:
            print("No hay proveedores en la base de datos.")
            return
        print("Eliminando un proveedor. Mostrando los proveedores existentes:")
        sid = pick_supplier(inventory, "Escribe el ID del proveedor a eliminar: ")
        print(f"Proveedor seleccionado: {inventory[sid]['name']} ({sid})")
        c = confirm("¿Deseas eliminar este proveedor? ")
        if c == "s":
            del inventory[sid]
            save_data(inventory)
            print("Proveedor eliminado.")
        else:
            print("No se han realizado cambios.")

    elif action == "check":
        if not inventory:
            print("No hay proveedores en la base de datos.")
            return
        print("Mostrando la información de un proveedor en la base de datos.")
        sid = pick_supplier(inventory, "Escribe el ID del proveedor a mostrar: ")
        print(f"""
Proveedor seleccionado:
ID Interno: {sid}
Nombre: {inventory[sid]['name']}
Correo electrónico: {inventory[sid]['contact']}
Dias de entrega de productos: {inventory[sid]['shipping_days']}
Cantidad minima de ordenes por producto: {inventory[sid]['min_order_qty']}
Productos: 
""")    
           
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

try:
    main()
except KeyboardInterrupt:
    print("\nCtrl+C was pressed. Exiting.")
    sys.exit(0)
