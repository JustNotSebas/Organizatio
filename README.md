# Organizatio

Sistema de inventario por consola, escrito en Python. Permite administrar proveedores y productos, registrar ventas y entradas de mercancía, y muestra alertas cuando un producto necesita reabastecerse. Toda la información se guarda en un archivo JSON, así que se conserva entre ejecuciones.

## Cómo ejecutarlo

Requiere Python 3.8 o superior (no usa librerías externas). Desde la carpeta del proyecto:

```
python main.py
```

El archivo `inventory.json` se lee y se guarda en la carpeta desde la que se ejecuta el comando. Si no existe, se crea al guardar por primera vez.

## Estructura del proyecto

| Archivo | Función |
|---|---|
| `main.py` | Punto de entrada. Contiene el menú principal y llama a las funciones de `back.py`. |
| `back.py` | Lógica del sistema: proveedores, productos, ventas, reabastecimiento y panel de alertas. Contiene el diccionario `inventory` (la memoria del programa). |
| `funcs.py` | Funciones de ayuda reutilizables: preguntas con validación, confirmaciones, búsqueda, guardado/carga y cálculo de alertas. |
| `inventory.json` | Base de datos. Se genera automáticamente. |

## Estructura de los datos

`inventory` es un diccionario de proveedores; cada proveedor contiene un diccionario de productos:

```json
{
    "USS1": {
        "name": "Google",
        "contact": "ventas@google.com",
        "shipping_days": 10,
        "min_order_qty": 90,
        "products": {
            "DSS1": {
                "name": "Chrome",
                "amount": 101,
                "cost": 9000.0,
                "price": 40000.0,
                "reorder_at": 3
            }
        }
    }
}
```

| Campo | Significado |
|---|---|
| `shipping_days` | Días que tarda el proveedor en entregar un pedido. |
| `min_order_qty` | Cantidad mínima que el proveedor exige por producto en cada pedido. |
| `amount` | Unidades en stock (puede ser negativo si hay sobreventa). |
| `cost` / `price` | Costo al proveedor y precio de venta al público. |
| `reorder_at` | Punto de reorden: con este stock o menos, el producto entra en alerta. |

Los IDs (de proveedores y de productos) se convierten siempre a MAYÚSCULAS al guardarse. El ID de un producto es único en toda la base de datos, incluso entre proveedores distintos.

## Funciones

### main.py

**`main()`**: función principal.
1. Carga los datos del archivo en `inventory` con `inventory.update(load_data())`.
2. Saluda y, si hay productos en alerta, muestra cuántos (`get_alerts`). Esto se hace después de cargar los datos, porque antes `inventory` estaría vacío.
3. Muestra el menú en un ciclo `while True`, pide la opción y ejecuta la función correspondiente.
4. Al terminar cada acción vuelve al menú, hasta elegir la opción 0 o presionar `Ctrl + C`. Como cada acción guarda sus cambios al completarse, cerrar el programa en cualquier momento no pierde datos.

| Opción | Acción | Función llamada |
|---|---|---|
| 1 | Añadir un proveedor | `manage_suppliers("add")` |
| 2 | Eliminar un proveedor | `manage_suppliers("remove")` |
| 3 | Consultar un proveedor | `manage_suppliers("check")` |
| 4 | Añadir un producto | `manage_products("add")` |
| 5 | Eliminar un producto | `manage_products("remove")` |
| 6 | Consultar un producto | `manage_products("check")` |
| 7 | Registrar una venta | `sell_product()` |
| 8 | Añadir stock | `restock_product()` |
| 9 | Ver alertas | `show_alerts()` |
| 0 | Salir | (termina el ciclo) |

### back.py

**`manage_suppliers(action)`**: el parámetro `action` selecciona entre tres funciones.
- `add`: ciclo que pide ID, nombre, correo, días de entrega y cantidad mínima por pedido. Valida cada dato al momento de pedirlo (ID único y no vacío, correo con `@` y `.`, números mayores a 0). Luego muestra un resumen y pide confirmar: `s` guarda, `n` repite el formulario y `c` cancela y regresa al menú.
- `remove`: si no hay proveedores, cancela. Si los hay, muestra la lista, pide el ID, muestra el proveedor elegido y pide confirmación. Eliminar un proveedor elimina también todos sus productos.
- `check`: si no hay proveedores, cancela. Si los hay, pide el ID y muestra todos sus datos junto con sus productos y el stock de cada uno.

**`manage_products(action)`**: primero verifica que exista al menos un proveedor; si no, cancela. Luego, según `action`:
- `add`: pide el proveedor (`pick_supplier`) y entra a un ciclo que pide ID del producto, nombre, stock (0 o más), costo, precio y punto de reorden. Si el costo es mayor que el precio, muestra una advertencia de venta a pérdida (solo informa). Confirmación igual que en proveedores.
- `remove`: pide el ID, busca el producto en todos los proveedores con `find_product`, muestra su nombre y su proveedor, y pide confirmación.
- `check`: pide el ID y muestra todos los datos del producto y el nombre de su proveedor.

**`sell_product()`**: registra una venta.
1. Pide el ID y busca el producto. Si no existe, cancela.
2. Si el stock es 0 o menos, bloquea la venta.
3. Pide las unidades vendidas (mayor a 0). Si son más que el stock, avisa cuál será el stock resultante, pero **permite** la venta (sobreventa).
4. Tras confirmar, resta las unidades, guarda y muestra el stock restante. Si el stock quedó en 0 o menos, muestra `ALERTA CRÍTICA`; si quedó entre 1 y el punto de reorden, muestra `ALERTA`.

**`restock_product()`**: registra la llegada de mercancía.
1. Pide el ID y las unidades recibidas (mayor a 0).
2. Si son menos que `min_order_qty` del proveedor, avisa, pero no bloquea (la mercancía podría no venir de un pedido, por ejemplo una devolución).
3. Tras confirmar, suma las unidades y guarda. Antes de sumar guarda en `was_alert` si el producto estaba en alerta, para poder avisar después si la alerta dejó de ser válida, si sigue vigente, o no decir nada si el producto nunca estuvo en alerta.

**`show_alerts()`**: obtiene las alertas con `get_alerts`, las ordena de menor a mayor stock (lo más grave primero) y las imprime con `alert_line`. Al final ofrece reabastecer llamando a `restock_product()`. Si no hay alertas, lo indica y termina.

### funcs.py

- **`ask(prompt, cast=str, check=None, error="Entrada inválida.")`**: pide un dato en un ciclo `while True` hasta que sea válido. `cast` convierte el texto al tipo deseado (`int`, `float`, `str`); si la conversión falla (`ValueError`) o si `check` (una función que devuelve `True` o `False`) rechaza el valor, muestra `error` y vuelve a pedirlo. Siempre aplica `.strip()` a lo escrito.
- **`confirm(prompt)`**: usa `ask` para aceptar solo `s`, `n` o `c` (en mayúscula o minúscula) y devuelve la letra en minúscula.
- **`pick_supplier(inventory, prompt)`**: imprime la lista de proveedores y pide un ID válido (sin importar mayúsculas). Repite hasta recibir uno existente y lo devuelve en mayúsculas.
- **`find_product(inventory, pid)`**: busca un ID de producto en todos los proveedores. Devuelve `(id_del_proveedor, datos_del_producto)` o `None` si no lo encuentra.
- **`save_data(data)`**: escribe el diccionario completo en `inventory.json` (UTF-8, sangría de 4 espacios, conservando acentos con `ensure_ascii=False`).
- **`load_data()`**: lee `inventory.json` y devuelve su contenido. Si el archivo no existe o no es un JSON válido, devuelve un diccionario vacío.
- **`alert_line(inventory, sid, pid, product)`**: construye el texto de una alerta con el nombre y ID del producto, su estado (`N uds`, `AGOTADO` o `SOBREVENDIDO (N uds por surtir)`), su punto de reorden y los datos del proveedor (mínimo por pedido y días de entrega).
- **`get_alerts(inventory)`**: recorre todos los productos y devuelve una lista de `(sid, pid, product)` con los que cumplen `amount <= reorder_at`.

## Reglas de diseño

- **Las alertas no se guardan:** `get_alerts` las recalcula cada vez comparando el stock actual con el punto de reorden. Por eso desaparecen solas al reabastecer y no hay nada que borrar.
- **El sistema informa, casi nunca bloquea:** se permite la sobreventa, el reabastecimiento por debajo del mínimo del proveedor y los productos con costo mayor al precio, todos con aviso. Los bloqueos son: stock inicial negativo al crear un producto y vender un producto cuyo stock ya es 0 o menos.
- **Guardado inmediato:** cada acción que modifica datos llama a `save_data` al terminar, por lo que no hay función de "guardar".

## Definiciones de funciones de Python utilizadas

1. **Importación de funciones de otro archivo** (`from funcs import ask, ...`): permite dividir el programa en varios archivos y reutilizar sus funciones. Se separó el programa en tres archivos para ordenar el código: menú, lógica y funciones de ayuda.

2. **Diccionarios**: como `inventory = {}`, guardan información en pares `clave: valor` y se accede al valor por su clave (`inventory["USS1"]["name"]`). Pueden anidarse (los `products` dentro de cada proveedor). `.items()` recorre cada clave junto con su valor (`for sid, supplier in inventory.items()`), y `.update()` agrega al diccionario los datos de otro, usado en `main()` para cargar los datos guardados. Cuando una función obtiene un producto (por ejemplo `sid, product = found`), `product` es una **referencia** al mismo diccionario que está dentro de `inventory`, no una copia; por eso `product["amount"] -= qty` actualiza el inventario directamente antes de guardar.

3. **Guardado y cargado de JSON con `with open()`**: `json.dump` escribe un diccionario en un archivo y `json.load` lo lee de vuelta. `with open(...)` abre el archivo y lo cierra solo al terminar el bloque, incluso si ocurre un error.

4. **`lambda`**: una función pequeña de una sola línea, sin `def`. Se escribe `lambda parámetro: expresión`. Se usa para las validaciones de `ask` (por ejemplo `lambda v: v > 0`, donde `v` es lo que escribió el usuario) y como criterio de orden en `alerts.sort(key=lambda a: a[2]["amount"])`, que ordena las alertas por el stock de cada producto sin definir una función aparte.

5. **Manejo de excepciones (`try/except`)**: permite capturar errores en lugar de que el programa se detenga. Se usa para detectar entradas que no se pueden convertir a número (`ValueError` en `ask`), para manejar un archivo ausente o dañado (`FileNotFoundError`, `json.JSONDecodeError` en `load_data`) y para cerrar con un mensaje al presionar `Ctrl + C` (`KeyboardInterrupt` en `main.py`).

6. **Desempaquetado de tuplas** (`sid, product = found`): `find_product` devuelve dos valores juntos y esta sintaxis los separa en dos variables en una sola línea.

7. **`.sort(key=...)`**: ordena una lista en el mismo lugar; el parámetro `key` indica por qué valor comparar los elementos.

## Documentación adicional

El archivo `Manual_de_Usuario_Organizatio.pdf` explica el uso del programa desde el punto de vista de quien lo opera: cada opción del menú, las reglas de validación, el sistema de alertas, el respaldo de datos y la solución de problemas.
