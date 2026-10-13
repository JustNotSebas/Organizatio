# Per Aspera Ad Astra

# Programa: "Organizatio"
# Metas de este corte:
# 1. Memoria consistente de proveedores y productos
# 2. Habilidad de añadir o eliminar proveedores y productos
# 3. Consulta rápida de un producto por su ID

# Funciones de Python utilizadas que NO han sido explicadas:
# 1. Importación de funciones de otro archivo
# 2. Diccionarios (incluido iteración con .items())
# 3. Guardado y cargado de información JSON desde y hacia un archivo (with open())
# 4. lambda (Tecnicamente es solo una función pequeña in-line, pero es mencionada por si acaso)
# 5. Manejo de excepciones (try/except)

from funcs import ask, save_data, load_data, pick_supplier, confirm, find_product

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
Productos:""")    
        for pid, product in inventory[sid]["products"].items():
            print(f"  - {product['name']} ({pid}): {product['amount']} uds")     
    else:
        print("Acción invalida.")

def manage_products(action):
    if not inventory:
            print("No puedes administrar productos sin un proveedor registrado anteriormente.")
            return
    if action == "add":
        print("Añadiendo un producto. Selecciona el proveedor:")
        sid = pick_supplier(inventory, "ID del proveedor: ")
        while True:
            pid = ask("ID del producto: ",
                    check=lambda v: v != "" and find_product(inventory, v.upper()) is None,
                    error="Ingresa un ID único y válido. (Los ID no se pueden repetir, incluso entre diferentes proveedores.)").upper()
            name = ask("Nombre del producto: ", check=lambda v: v != "", error="Ingresa un nombre válido.")
            amount = ask("Cantidad en stock: ", int, lambda v: v >= 0, "Debe ser 0 o más.")
            cost = ask("Costo al proveedor: ", float, lambda v: v > 0, "Debe ser mayor a 0.")
            price = ask("Precio de venta: ", float, lambda v: v > 0, "Debe ser mayor a 0.")
            reorder_at = ask("Reordenar cuando queden: ", int, lambda v: v >= 0, "Debe ser 0 o más.")
            print(f"""
Ingresaste la siguiente información: 
Proveedor del producto: {inventory[sid]["name"]}
ID Interno: {pid}
Nombre: {name}
Cantidad en stock: {amount}
Costo de compra al proveedor: {cost}
Precio de venta al público: {price}
Reordenar cuando queden: {reorder_at} unidades.""")
            if cost > price:
                print("Advertencia: Estas vendiendo este producto a perdida (el costo al proveedor es mayor que el precio al público).")
            c = confirm()
            if c == "s":
                inventory[sid]["products"][pid] = {
                    "name": name, 
                    "amount": amount, 
                    "cost": cost,
                    "price": price, 
                    "reorder_at": reorder_at,
                }
                save_data(inventory)
                print("Producto añadido.")
                break
            elif c == "n":
                print("Reiniciando.")
            elif c == "c":
                print("Cancelando.")
                return
    elif action == "remove":
        print("Eliminando un producto. Recuerda tener a la mano el ID interno del producto a eliminar.")
        pid = ask("ID del producto a eliminar: ", check=lambda v: v != "", error="Ingresa un ID.").upper()
        found = find_product(inventory, pid)
        if found is None:
            print("El ID que ingresaste no corresponde a un producto en la base de datos.")
            return
        sid = found[0]
        product = found[1]
        print(f"Producto seleccionado: {product['name']} ({pid}) de {inventory[sid]['name']}")
        if confirm("¿Deseas eliminar este producto? ") == "s":
            del inventory[sid]["products"][pid]
            save_data(inventory)
            print("Producto eliminado.")
        else:
            print("No se han realizado cambios.")
    elif action == "check":
        print("Mostrando la información de un producto.")
        pid = ask("ID del producto a mostrar: ", check=lambda v: v != "", error="Ingresa un ID.").upper()
        found = find_product(inventory, pid)
        if found is None:
            print("El ID que ingresaste no corresponde a un producto en la base de datos.")
            return
        sid = found[0]
        product = found[1]
        print(f"""
Producto seleccionado:
ID Interno: {pid}
Nombre: {product["name"]}
Proveedor: {inventory[sid]["name"]}
Cantidad en stock: {product["amount"]}
Costo de compra al proveedor: {product["cost"]}
Precio de venta al público: {product["price"]}
Reordenar cuando queden: {product["reorder_at"]} unidades.""")
    else:
        print("Acción invalida.")

def main():
    inventory.update(load_data())
    print("""
Bienvenido al sistema de inventario Organizatio.
(!!! No finalizado !!!)""")
    while True:
        print("""
Selecciona una opción:
1) Añadir un proveedor
2) Eliminar un proveedor
3) Consultar un proveedor

4) Añadir un producto
5) Eliminar un producto
6) Consultar un producto

0) Salir del programa.
""")
        choice = ask("Selecciona tu opción deseada: ", int, lambda v: v in range(7), "La opción ingresada no es válida.")
        if choice == 1:
            manage_suppliers("add")
        if choice == 2:
            manage_suppliers("remove")
        if choice == 3:
            manage_suppliers("check")
        if choice == 4:
            manage_products("add")
        if choice == 5:
            manage_products("remove")
        if choice == 6:
            manage_products("check")
        if choice == 0:
            print("Saliendo del programa.")
            break
        print("\nRegresando al menú principal.")
try:
    main()
except KeyboardInterrupt:
    print("\nCtrl+C was pressed. Exiting.")
    exit()
