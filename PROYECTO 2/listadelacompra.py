from typing import Any, Optional



'''
Módulo de gestión la lista de la compra

Un producto es un diccionario con las siguientes claves:

* nombre, prioridad, precio, etiquetas, categoria, comprado

Por ejemplo:

producto = {
  "nombre": "Huevo",
  "precio": 12.50,
  "etiquetas": ("huevos fritos", "empanada"),
  "categoria": "Alimentación",
  "comprado": False
}
'''

productos:list[dict] = []

def insertar(nombre: str, precio: float|int, categoria: str, etiquetas:tuple[str]=(), prioridad:int=3) -> None:
    '''Añade un producto nuevo a la lista con los parámetros dados'''
    if isinstance(etiquetas,str):
        etiquetas = tuple(sorted(etiquetas.split(',')))
        
    nuevo_producto:dict[str, Any] = {
            "nombre": str(nombre),
            "precio": float(precio), 
            "categoria": str(categoria),
            "etiquetas": etiquetas,
            "prioridad": int(prioridad),
            "comprado": False
            }
    if nuevo_producto in productos:
        return
    productos.append(nuevo_producto) # Añadimos ese diccionario a la lista de productos

def borrar(indice: int) -> None:
    '''Borra de la lista el producto que se encuentra en la posición indicada'''
    indice = int(indice)
    if 0 <= indice < len(productos): # Comprobar que esté en ese rango
        del productos[indice]
    else:
        print("Indice fuera de rango")

def actualizar_precio(indice: int, precio: float) -> None:
    '''Actualiza el precio del producto con el índice dado'''
    indice = int(indice)
    precio = float(precio)
    if 0 <= indice < len(productos): # Comprobar que esté en el rango
        productos[indice]["precio"] = precio
    else:
        print("Indice fuera de rango")

    
def cambiar_estado(indice: int) -> None:
    '''Cambia el estado del producto con el índice dado entre comprado o no'''
    indice = int(indice)
    if 0 <= indice < len(productos):  # Comprobar que esté en el rango
        productos[indice]["comprado"] = not productos[indice]["comprado"]
    else:
        print("Indice fuera de rango")
        
            
def mostrar_productos(comprados: bool = True, etiquetas: tuple[str] = (), categorias: list[str] = []):
    '''
    Muestra por pantalla todos los productos con su información. Si un producto ya ha sido comprado, se marca con una x al comienzo.
    La prioridad se indicará mediante el uso de asteriscos (*), es decir, un artículo con prioridad 5 se representará mediante cinco asteriscos (*****).
    Si comprados es False, no se muestran los productos ya comprados.
    etiquetas es una tupla o lista con etiquetas o aclaraciones.
    Si está vacía, se muestran todos los productos. Si contiene alguna etiqueta, sólo se muestran los productos que tengan todas las etiquetas proporcionadas.
    Categorias es una lista con las categorías que se quieren obtener. Si está vacía, se muestran todos los productos. Si contiene alguna categoría, solo se muestran los productos cuya categoría esté contenida en la lista.
    '''
    
    # Problemas: No se está pasando a la función el parámetro comprados
    
    # Asegurar que comprados sea un booleano(para el menú)
    if isinstance(comprados, str):
        if comprados.lower() == "true":
            comprados = True
        elif comprados.lower() == "false":
            comprados = False
    
    
    
    
    # Asegurar que categorias sea una lista(para el menú)
    if isinstance(categorias, str):
        categorias = [c.strip() for c in categorias.split(',') if c.strip()]
            
        
    # Aseguramos que etiquetas sea una tupla(para el menú)
    if isinstance(etiquetas, str):
        etiquetas = tuple(e.strip().lower() for e in etiquetas.split(',') if e.strip())
            
        
    filtrados:list[dict] = [] # Aquí iremos añadiendo los productos que pasen los filtros

    # Recorremos la lista de productos
    print(f"Filtrando productos -> Comprados: {comprados}, Etiquetas: {etiquetas}, Categorías: {categorias}")
    for producto in productos:
        
   
        # Filtrar productos por etiquetas
        if etiquetas and not set(etiquetas).issubset(producto["etiquetas"]):
            continue  # Si no contiene todas las etiquetas, se omite el producto

        # Filtrar productos por categorías
        if categorias and producto["categoria"] not in categorias:
            continue  # Si la categoría no está en la lista de categorías, se omite el producto
                    
                    
        # Filtrar productos según el estado de comprado si comprados es False
        if not comprados and producto["comprado"]:
            continue
        
        filtrados.append(producto)        
            
    
    # Recorremos la lista de productos que pasan el filtro
    for producto in filtrados:
        estado: str = "[X]" if producto["comprado"] else "[ ]"
        prioridad: str = "*" * producto["prioridad"]
        etiquetas2:str = " ".join(f"#{etiqueta}" for etiqueta in producto["etiquetas"])
            
        print(f"{estado} {producto['categoria']} - {producto["nombre"]} - {prioridad} - {producto["precio"]}€ - {etiquetas2}")
        

def salir() -> None:
    '''Finaliza el programa'''
    exit()

def ordenar():
    '''Ordena la lista de productos en función de su prioridad, y de si han sido ya comprados o no.'''
    
    for i in range(1, len(productos)):  # Comienza desde el segundo producto
        actual = productos[i]
        j = i - 1
        
        
        # Comparar el producto actual con los anteriores según la prioridad y si se han comprado
        while j >= 0 and (
            actual["prioridad"] > productos[j]["prioridad"] or
            (actual["prioridad"] == productos[j]["prioridad"] and not actual["comprado"] and productos[j]["comprado"])
        ):
            productos[j + 1] = productos[j]  # Mueve el producto a la siguiente posición
            j -= 1
        
        productos[j + 1] = actual  # Coloca el producto actual en la posición correcta

    

    # Mover los productos comprados al final de la lista
    # Separar los productos comprados de los no comprados
    no_comprados = [producto for producto in productos if not producto["comprado"]]
    comprados = [producto for producto in productos if producto["comprado"]]

    # Concatenar las listas: primero los no comprados, luego los comprados
    productos[:] = no_comprados + comprados


    
def mostrar_ayuda() -> None:
    '''Muestra todos los comandos disponibles y su documentación'''
    
    ayuda: str = "Estos son los comandos disponibles:\n"
    for clave, valor in comandos.items(): # Recorrer los valores del diccionario
        ayuda += f"{clave} -> {valor.__doc__.strip()}\n" # Añadir al string la documentación de cada función
        ayuda += '-'*10
        ayuda += '\n'
    print(ayuda)

comandos = {
    "mostrar": mostrar_productos,  # Muestra los productos
    "insertar": insertar,  # Inserta un nuevo producto
    "borrar": borrar,  # Borra un producto por índice
    "ordenar": ordenar,# Ordena los productos
    "precio": actualizar_precio,
    "comprado": cambiar_estado,  # Marca un producto como comprado
    "ayuda": mostrar_ayuda,  # Muestra los comandos disponibles
    "salir": salir  # Termina el programa
}



def menu():
    '''
    Menú interactivo para modificar la lista de la compra.
    Acciones:

    -  mostrar
    -  insertar <nombre>; <precio>; <categoria>; <etiquetas separadas por comas>; <prioridad>
    -  borrar <indice>
    -  precio <numero>; <precio>
    -  comprado <numero>
    -  ayuda
    -  salir
    
    '''
    while True:
        comando = input("-> ").strip()  # Convertir el comando a minusculas y quitar espacios de más
        partes: list[str] = comando.split(maxsplit=1)
        partes[0] = partes[0].lower()
        
        match partes:
            case [comando] if comando in comandos: # Si el comando está en el diccionario de comandos
                funcion = comandos[comando]
                funcion()
                
            case [comando, args] if comando in comandos: # Si el comando está en el diccionario de comandos
                funcion = comandos[comando]
                argumentos = [arg.strip() for arg in args.split(";")]
                funcion(*argumentos)
                
            case _: # Si no hace match, ejecuta la funcion de ayuda
                funcion = comandos['ayuda']
                funcion()
                    
            


def prueba_2():
    productos.clear()  # Limpiar la lista de productos antes de la prueba
    insertar('Hierbabuena', 1.5, 'Alimentación', ['coctail'], 1)
    insertar('Garbanzos', 0.68, 'Alimentación', ['cocido', 'humus'], 3)
    
    print('-- Debería mostrar hierbabuena antes que garbanzos, porque se insertó antes')
    mostrar_productos()

    ordenar()
    print('-- Debería mostrar Garbanzos antes, porque tiene prioridad mayor')
    mostrar_productos()

    cambiar_estado(0)
    print('-- Debería mostrar Hierbabuena antes, porque no está comprada')
    mostrar_productos()


def prueba_manual():
    print('Insertando 3 productos')
    insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)
    insertar('Garbanzos', 0.68, 'Alimentación', ('cocido', 'hummus'), 3)
    insertar('Hierbabuena', 1.5, 'Alimentación', ('cocktails', 'postres'), 1)

    seccion('Lista de la compra sin ordenar ni formatear')

    print(productos)

    seccion('Lista de la compra sin ordenar ni formatear (con cambio)')
    print('Cambiando un producto a comprado')
    cambiar_estado(0)
    print(productos)

    seccion('Lista de la compra sin ordenar')
    mostrar_productos()

    seccion('Lista de la compra filtradas')
    mostrar_productos(etiquetas=('cocido', ))

    seccion('Lista de la compra ordenadas')
    ordenar()
    mostrar_productos()


def seccion(texto):
    print()
    print('-' * 10, texto, '-' * 40)
    print()


if __name__ == "__main__":
    menu()