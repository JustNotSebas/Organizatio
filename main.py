# Ad astra infinitum Per aspera
 
from funcs import ask, load_data, get_alerts
from back import inventory, manage_suppliers, manage_products, sell_product, restock_product, show_alerts

def main():
    inventory.update(load_data())
    print("\nBienvenido al sistema de inventario Organizatio.")
    n = len(get_alerts(inventory))
    if n:
        print(f"Tienes {n} alerta(s) activa(s). Revisa la opción 9.")
    while True:
        print("""
Selecciona una opción:
1) Añadir un proveedor
2) Eliminar un proveedor
3) Consultar un proveedor

4) Añadir un producto
5) Eliminar un producto
6) Consultar un producto

7) Registrar una venta
8) Añadir stock
9) Ver alertas

0) Salir del programa.
""")
        choice = ask("Selecciona tu opción deseada: ", int, lambda v: v in range(10), "La opción ingresada no es válida.")
        if choice == 1:
            manage_suppliers("add")
        elif choice == 2:
            manage_suppliers("remove")
        elif choice == 3:
            manage_suppliers("check")
        elif choice == 4:
            manage_products("add")
        elif choice == 5:
            manage_products("remove")
        elif choice == 6:
            manage_products("check")
        elif choice == 7:
            sell_product()
        elif choice == 8:
            restock_product()
        elif choice == 9:
            show_alerts()
        elif choice == 0:
            print("Saliendo del programa.")
            break
        print("\nRegresando al menú principal.")

try:
    main()
except KeyboardInterrupt:
    print("\nCtrl+C fue presionado. Saliendo.")
    exit()
