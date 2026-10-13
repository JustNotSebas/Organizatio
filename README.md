## Funciones:

1. manage_suppliers (Administrar proveedores)
Incluye un parametro "action" que permite cambiar entre las tres funciones:
- add (añadir) = Un loop que pide la siguiente información: Id del proveedor, nombre, correo, dias de entrega de los productos (al cliente) y la cantidad minima que se debe pedir de un producto para ordenarlo. Se pide confirmar al cliente con una función de ayuda, decir que si lo añade al archivo, decir que no repite la acción y decir cancelar regresa al menú principal. El ID debe ser único, y se convierte a MAYUSCULAS a la hora de guardarlo.
- remove (eliminar) = Verifica primero si hay proveedores en el archivo de datos, y si no, cancela la acción. Después, pide el ID interno del proveedor a eliminar, muestra el nombre e ID, y pide la confirmación para eliminarlo o cancelar. Eliminar un proveedor tambien elimina todos sus productos asociados.
- check (mostrar) = Verifica primero si hay proveedores en el archivo de datos, y si no, cancela la acción. Después, pide el ID interno del proveedor a mostrar, y muestra en consola toda la información que se coloco en el comando add, asi como cualquier producto que se haya añadido despues

2. manage_products (Administrar productos)
Globalmente, la funcion verifica primero si hay proveedores en el archivo de datos, y si no, cancela la acción.
Incluye un parametro "action" que permite cambiar entre las tres funciones:
- add (añadir) = Primero pide el ID de un proveedor valido, e inicia un loop que pide la siguiente información: Id del producto, nombre, cantidad del stock en el momento, costo al proveedor, precio de venta al público y la cantidad necesaria para pedir nuevos productos en inventario. Si el costo al proveedor es mayor que el precio al público, el sistema avisa que el producto se vende a perdida. Se pide confirmar al cliente con una función de ayuda, decir que si lo añade al archivo, decir que no repite la acción y decir cancelar regresa al menú principal. El ID debe ser único entre todos los productos de todos los proveedores, y se convierte a MAYUSCULAS a la hora de guardarlo.
- remove (eliminar) = Pide el ID interno del producto a eliminar, muestra el nombre y el proveedor al que pertenece, y pide la confirmación para eliminarlo o cancelar. 
- check (mostrar) = Pide el ID interno del producto a mostrar y muestra en consola toda la información que se coloco en el comando add, asi como el nombre del proveedor.

3. main (Función principal)
Al iniciar, el programa carga los datos que existan en el archivo de datos.
Después, saluda al usuario y muestra el menú de opciones:
1) Añadir un proveedor
2) Eliminar un proveedor
3) Consultar un proveedor
4) Añadir un producto
5) Eliminar un producto
6) Consultar un producto
0) Salir del programa.
El programa pide la opción y ejecuta la función correspondiente con su parametro respectivo, y al terminar la función, regresa al menú principal, donde el ciclo se repite hasta seleccionar la opción 0 o presionar el comando Control + C, que cierra el programa instantaneamente independientemente de donde se encuentre el usuario. (Toda la información es guardada a la hora de completar un comando add/remove exitosamente, asi que esto no produce perdida de datos)

## Definiciones:

1. Diccionarios: Como la variable inventory = {}, es un espacio en memoria que sostiene información organizada en "pares" (clave: valor), accediendo a sus valores correspondientes gracias a las claves correspondientes. Se pueden añadir diccionarios dentro de otros diccionarios (como products dentro de cada proveedor). La función .items() se usa para mostrar cada clave junto con su valor, usado para recorrer la información de forma rápida. La función .update() se usa para añadir datos dentro del diccionario, usado para cargar los datos en la función main()

2. lambda: Una pequeña función de una sola linea, sin necesidad de ser declarada con def. Se usa como "lambda parámetro: expresión". Se utiliza para validar la condición de cada campo de entrada (con la función de ayuda "ask") sin necesidad de repetir el mismo código constantemente (ej. lambda v: v > 0, con v siendo el entero que el usuario ingrese), lo que ayuda a optimizar el tamaño del archivo y mejorar la legibilidad del codigo.

3. Funciones de ayuda (funcs.py): Pequeñas funciones creadas de forma separada para repetir acciones del codigo que se usan de forma repetitiva. Incluyen:
- ask: Encadena input() en un loop "while True", permitiendo verificar instantaneamente si la respuesta del usuario es válida antes de enviarla al resto del codigo.
- confirm: Encadena la función ask() con 3 opciones: S(i), N(o) y C(ancelar).
- pick_supplier: Utiliza los datos de la base de datos para mostrar en la consola el nombre e ID de los proveedores añadidos, y encadena la función ask() para solicitar un ID interno de proveedor.
- find_product: Utiliza los datos de la base de datos para buscar un ID de producto entre todos los proveedores de la tienda, regresando los datos del producto y proveedor, o regresa None (ninguno) si no encuentra el ID registrado.
- save_data: Abre un archivo inventory.json con la función "with open" y escribe la información del inventario en memoria, guardandolo permanentemente.
- load_data: Abre un archivo inventory.json existente y regresa la información para cargarla en memoria. Si el archivo no existe o esta corrupto, simplemente no regresa información, solo un diccionario vacio.
