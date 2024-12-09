
class Producto:
    
    def __init__(self, nombre:str, precio:float|int, categoria: str, etiquetas: tuple[str] = (), prioridad:int = 3):
        # Forzamos algunos tipos para el menú
        self.nombre = nombre
        self.precio = float(precio)
        self.etiquetas = etiquetas
        self.categoria = categoria
        self.prioridad = int(prioridad)
        self.comprado:bool = False
    
        
class ListaCompra:
    
    def __init__(self):
        self.productos:list[Producto] = [] # Inicializamos la lista de productos vacía
        self.comandos: dict = {
        "insertar":self.insertar,
        "borrar": self.borrar,
        "precio": self.actualizar_precio,
        "comprado": self.cambiar_estado,
        "mostrar": self.mostrar_productos,
        "ordenar": self.ordenar,
        "salir": self.salir,
        "ayuda": self.mostrar_ayuda
    }
        
    def insertar(self, nombre: str, precio:float, categoria: str, etiquetas:tuple[str] = (), prioridad: int = 3) -> None:
        '''Añade un producto nuevo a la lista con los parámetros dados'''
        
        if isinstance(etiquetas, str):
            etiquetas = tuple(etiquetas.split(",")) # Si etiquetas es un string, lo convierte a tupla separando sus elementos por comas
        
        precio = float(precio)
        prioridad = int(prioridad)
        
        
        producto:Producto = Producto(nombre.strip(), precio, categoria.strip(), etiquetas, prioridad) # Creamos un objeto de la clase Producto
        
        if producto in self.productos:
            return
        
        self.productos.append(producto) # Lo añadimos a la lista
        
    def borrar(self, indice:int) -> None:
        '''Borra de la lista el producto que se encuentra en la posición indicada'''
        indice = int(indice) # Hacemos que el índice sea un entero(para el menú)
        if 0 <= indice < len(self.productos): # Si está en ese rango, ejecuta la instrucción
            del self.productos[indice]
        else:
            print("Indice fuera de rango")
        
    def actualizar_precio(self, indice:int, precio:float) -> None:
        '''Actualiza el precio del producto con el índice dado'''
        # Forzamos el tipo (para el menú)
        indice = int(indice) 
        precio = float(precio)
        if 0 <= indice < len(self.productos): # Si está en ese rango, se ejecuta la instrucción
            self.productos[indice].precio = precio # El nuevo precio será el parámetro que pase el usuario
            
        else:
            print("Indice fuera de rango")
        
    def cambiar_estado(self, indice:int) -> None:
        '''Cambia el estado del producto con el índice dado entre comprado o no'''
        # Forzamos el tipo(para el menú)
        indice = int(indice)
        if 0 <= indice < len(self.productos): # Si está en ese rango, se ejecuta la instrucción
            self.productos[indice].comprado = not self.productos[indice].comprado # Cambia el estado de True a False o viceversa
            
        else:
            print("Indice fuera de rango")
        
    def mostrar_productos(self, comprados: bool = True, etiquetas: tuple[str] = (), categorias: list[str] = []):
        '''
        Muestra por pantalla todos los productos con su información, aplicando los filtros opcionales.
        '''
        if isinstance(comprados, str):
            if comprados.lower() == "true":
                comprados = True
            elif comprados.lower() == "false":
                comprados = False       
        
        if isinstance(categorias, str):
            categorias = [c.strip() for c in categorias.split(',') if c.strip()]
        
        
        if isinstance(etiquetas, str):
            etiquetas = tuple(e.strip().lower() for e in etiquetas.split(',') if e.strip())
        
        # Depuración: Mostrar filtros aplicados
        print(f"Filtrando productos -> Comprados: {comprados}, Etiquetas: {etiquetas}, Categorías: {categorias}")

        filtrados: list[Producto] = []

        for producto in self.productos:
            
            producto_categoria = producto.categoria.strip()
            producto_etiquetas = {et.strip().lower() for et in producto.etiquetas if et.strip()}

            # Filtro de etiquetas
            if etiquetas and not set(etiquetas).issubset(producto_etiquetas):
                continue

            # Filtro de categorías
            if categorias and producto_categoria not in categorias:
                continue

            # Filtro de estado de comprado
            if not comprados and producto.comprado:
                continue

            filtrados.append(producto)

        # Mostrar los productos filtrados
        for producto in filtrados:
            estado: str = "[X]" if producto.comprado else "[ ]"
            prioridad: str = "*" * producto.prioridad
            etiquetas_str: str = " ".join(f"#{et.strip()}" for et in producto.etiquetas)
            print(f"{estado} {producto.categoria} - {producto.nombre} - {prioridad} - {producto.precio}€ - {etiquetas_str}")


        
              
    def ordenar(self) -> None:        
        '''Ordena la lista de productos en función de su prioridad, y de si han sido ya comprados o no.'''
    
        for i in range(1, len(self.productos)):  # Comienza desde el segundo producto
            actual:Producto = self.productos[i]
            j = i - 1 # self.productos[j] será el anterior a self.productos[i]
        
        
            # Comparar el producto actual con los anteriores según la prioridad y si se han comprado
            while j >= 0 and (
                actual.prioridad > self.productos[j].prioridad or
                (actual.prioridad == self.productos[j].prioridad and not actual.comprado and self.productos[j].comprado)
            ):
                self.productos[j + 1] = self.productos[j]  # Mueve el producto a la siguiente posición
                j -= 1
        
            self.productos[j + 1] = actual  # Coloca el producto actual en la posición correcta

    
        # Separar los productos comprados de los no comprados
        no_comprados:list[Producto] = [producto for producto in self.productos if not producto.comprado]
        comprados:list[Producto] = [producto for producto in self.productos if producto.comprado]

        # Concatenar las listas, primero los no comprados, luego los comprados
        self.productos[:] = no_comprados + comprados
        
    def salir(self) -> None:
        '''Finaliza el programa'''
        exit()


    def mostrar_ayuda(self,comandos:dict) -> None:
        '''Muestra todos los comandos disponibles y su documentación'''
        ayuda:str ="Estos son los comandos disponibles:\n"
        for clave, valor in comandos.items():
            ayuda += f"{clave} -> {valor.__doc__.strip()}\n"
            ayuda += '-'*10
            ayuda += "\n"
        print(ayuda)

    

def menu():
    l: ListaCompra = ListaCompra()
    
    while True:
        entrada = input("-> ").strip()
        comando: list[str] = entrada.split(maxsplit=1)  # Dividimos la entrada en el comando y sus argumentos (si tiene)
        comando_principal: str = comando[0].lower()
        argumentos = comando[1] if len(comando) > 1 else ""
        
        match len(comando):
            case 1:
                if comando_principal == "ayuda":
                    l.mostrar_ayuda(l.comandos)
                    
                elif comando_principal in l.comandos:
                    funcion = l.comandos[comando_principal]
                    funcion()
                else:
                    l.mostrar_ayuda(l.comandos)
                    
            case 2:
                if comando_principal in l.comandos:
                    funcion = l.comandos[comando_principal]
                    argumentos = [arg.strip() for arg in argumentos.split(";")]  # Los argumentos vienen separados por ;
                    funcion(*argumentos)
                else:
                    l.mostrar_ayuda(l.comandos)



                
        
if __name__ == "__main__":
    menu()