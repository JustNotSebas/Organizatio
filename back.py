from funcs import ask, save_data, pick_supplier, confirm, find_product, get_alerts, alert_line

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

def show_alerts():
    alerts = get_alerts(inventory)
    if not alerts:
        print("No hay alertas de reabastecimiento.")
        return
    alerts.sort(key=lambda a: a[2]["amount"])
    print("Alertas de reabastecimiento:")
    for sid, pid, product in alerts:
        print("  - " + alert_line(inventory, sid, pid, product))
    if confirm("¿Deseas reabastecer alguno de estos productos ahora? ") == "s":
        restock_product()

# Ventas y reabastecimiento
def sell_product():
    if not inventory:
        print("No hay proveedores en la base de datos.")
        return
    print("Registrando una venta.")
    pid = ask("ID del producto vendido: ", check=lambda v: v != "", error="Ingresa un ID.").upper()
    found = find_product(inventory, pid)
    if found is None:
        print("El ID que ingresaste no corresponde a un producto en la base de datos.")
        return
    sid, product = found
    if product["amount"] <= 0:
        print(f"{product['name']} ({pid}) no tiene stock para vender.")
        return
    print(f"Producto seleccionado: {product['name']} ({pid}), stock actual: {product['amount']}")
    qty = ask("Unidades vendidas: ", int, lambda v: v > 0, "Debe ser mayor a 0.")
    if qty > product["amount"]:
        print(f"Aviso: vendes {qty} uds y el stock quedará en {product['amount'] - qty}.")
    if confirm(f"¿Registrar la venta de {qty} uds? ") != "s":
        print("No se han realizado cambios.")
        return
    product["amount"] -= qty
    save_data(inventory)
    print(f"Venta registrada. Stock restante: {product['amount']} uds.")
    if product["amount"] < 1:
        print("ALERTA CRÍTICA: " + alert_line(inventory, sid, pid, product))
    elif product["amount"] <= product["reorder_at"]:
        print("ALERTA: " + alert_line(inventory, sid, pid, product))

def restock_product():
    if not inventory:
        print("No hay proveedores en la base de datos.")
        return
    print("Añadiendo stock.")
    pid = ask("ID del producto a reabastecer: ", check=lambda v: v != "", error="Ingresa un ID.").upper()
    found = find_product(inventory, pid)
    if found is None:
        print("El ID que ingresaste no corresponde a un producto en la base de datos.")
        return
    sid, product = found
    supplier = inventory[sid]
    was_alert = product["amount"] <= product["reorder_at"]
    print(f"Producto seleccionado: {product['name']} ({pid}), stock actual: {product['amount']}")
    qty = ask("Unidades recibidas: ", int, lambda v: v > 0, "Debe ser mayor a 0.")
    if qty < supplier["min_order_qty"]:
        print(f"Aviso: {supplier['name']} exige un mínimo de {supplier['min_order_qty']} uds por pedido.")
    if confirm(f"¿Añadir {qty} uds? ") != "s":
        print("No se han realizado cambios.")
        return
    product["amount"] += qty
    save_data(inventory)
    print(f"Stock actualizado: {product['amount']} uds.")
    if product["amount"] <= product["reorder_at"]:
        print("ALERTA: sigue por debajo del umbral. " + alert_line(inventory, sid, pid, product))
    elif was_alert:
        print("La alerta de este producto ya no es válida y fue retirada.")
