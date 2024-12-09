import shlex
from typing import Any

class Habilidad:
    '''Abstracción del concepto de habilidad en un asistente.'''

    def __init__(self, nombre:str, descripcion:str|None=None):
        self.nombre = nombre
        self.descripcion = descripcion or self.__doc__

    def invocar(self) -> None:
        """Invocar la habilidad. No acepta parámetros"""
        raise NotImplementedError("Este método debe ser implementado por subclases")

    def ayuda(self) -> None:
        """Devolver la descripción de la habilidad"""
        texto:str = self.descripcion or self.__doc__ # Será la descripción que proporcionemos o en su defecto la documentación de la clase
        print(texto)

class Saludar(Habilidad):
    """Saludar, dando el nombre indicado en self.nombre"""
    
    def invocar(self) -> None:
        """Saludar al usuario."""
        print(f"Hola, soy {self.nombre}")
        
class Despedir(Habilidad):
    """Despedirse, dando el nombre indicado en self.nombre"""
    
    def invocar(self) -> None:
        """Despedir al usuario."""
        print(f"Adiós desde {self.nombre}")
        
class SaludarAAlguien(Habilidad):
    '''Saludar a alguien, personalizando el saludo con un nombre.'''
    def invocar(self, nombre:str = "anónimo") -> None: # Si no se pasa un nombre, será "anónimo"
        print(f"Hola, {nombre}, yo soy {self.nombre}") 

class Divisas(Habilidad):
    """Conversión de divisas con una tasa de conversión personalizada."""

    def __init__(self, nombre: str, descripcion: str = None, tasa: float = 1.0):
        super().__init__(nombre, descripcion)
        self.tasa = tasa

    def invocar(self, cantidad: float) -> float:
        """
        Convierte una cantidad de divisas según la tasa.
        Parámetro cantidad: Cantidad a convertir.
        """
        if isinstance(cantidad, str):
            if cantidad.lower() == "ayuda": # Si le pasamos como argumento ayuda, llama a la ayuda específica
                    self.ayuda()
                    return None
        try:
            cantidad = float(cantidad)  # Convierte str a float si es necesario
            return round(cantidad * self.tasa, 2)
        except ValueError:
            print("Error: La cantidad debe ser un número.")
            return 0.0


    
class Menu:
    '''Menú interactivo de gestión de habilidades.'''

    def __init__(self, habilidades:list[Habilidad]):
        # habilidades es una LISTA
        # self.habilidades es un diccionario de nombre -> habilidad
        self.habilidades: dict[str, Any] = {}
        for habilidad in habilidades:
            self.habilidades[habilidad.nombre] = habilidad # Asignamos los pares clave-valor

    def ayuda(self, habilidad: str | None = None) -> None:
        """
        Muestra ayuda del uso del menú.
        Parámetro habilidad: Nombre de la habilidad para mostrar ayuda específica.
        """
        if habilidad is None:  # Ayuda general
            print("Habilidades disponibles:")
            for hab in self.habilidades.values():
                print(f"\t{hab.nombre}:\t{hab.descripcion}") 
        elif habilidad in self.habilidades:  # Ayuda específica
            self.habilidades[habilidad].ayuda()  # Llama al método ayuda de la habilidad
        else:  # Habilidad no encontrada
            print(f"Habilidad no encontrada: {habilidad}")


    def lanzar(self) -> None:
        '''Recibe instrucciones del usuario en bucle.'''
        while True:
            linea:str = input('> ')
            if self.ejecutar(linea): # Si es True(salir), se detiene la ejecución
                break

    def convertir_linea(self, linea:str) -> tuple[str, list[str]]:
        comando, *args = shlex.split(linea) # Divide la sentencia entre comando y argumentos
        return comando, args

    def ejecutar(self, linea:str) -> bool:
        '''
        Recibe una línea del usuario y ejecuta la acción requerida

        Devuelve True cuando se desea parar la ejecución.
        '''
        comando, args = self.convertir_linea(linea) # Separa comando y argumentos antes de llamar a ningún método
        
        if comando == "salir":  # Comando para salir del menú
            return True
        elif comando == "ayuda":  # Comando para mostrar ayuda
            habilidad = args[0] if args else None # Depende si es ayuda general o ayuda específica
            self.ayuda(habilidad)
        elif comando in self.habilidades:  # Comando para invocar una habilidad
            if args and args[0].lower() == "ayuda":
                self.habilidades[comando].ayuda()
            
            else:
                resultado = self.habilidades[comando].invocar(*args)
                if resultado:
                    print(resultado)
        else:  # Comando no reconocido
            print(f"Comando '{comando}' no reconocido.")

        return False

    def emular(self, linea: str) -> None:
        """Simula la ejecución de un comando para pruebas."""
        print(f"> {linea}")
        self.ejecutar(linea)



class MenuComas(Menu):
    """Menú en el que el comando y los argumentos se proporcionan separados por comas."""

    def convertir_linea(self, linea: str) -> tuple[str, list[str]]:
        """
        Convierte una línea con comas en un comando y una lista de argumentos.
        Parámetro linea: Línea ingresada por el usuario.
        """
        tokens = [token.strip() for token in linea.split(",")]
        comando = tokens[0]
        args = tokens[1:]
        return comando, args

class MenuPrompt(Menu):
    """Menú en el que el símbolo al principio de cada línea es configurable."""

    def __init__(self, habilidades: list[Habilidad], prompt: str = "> "):
        """
        Inicializa el menú con un prompt personalizado.
        Parámetro habilidades: Lista de habilidades disponibles.
        Parámetro prompt: Símbolo inicial para cada línea.
        """
        super().__init__(habilidades)
        self.prompt = prompt

    def lanzar(self) -> None:
        """
        Recibe instrucciones del usuario en bucle, usando un prompt personalizado.
        """
        while True:
            linea = input(self.prompt)
            if self.ejecutar(linea):
                break

class MenuPreguntas(Menu):
    """Menú en el que primero se pide el comando y luego los argumentos uno a uno."""

    def lanzar(self) -> None:
        """Recibe el comando primero y luego solicita los argumentos uno por uno."""
        while True:
            comando = input("> ").strip()
            if comando.lower() == "salir":
                break
            if comando.lower() == "ayuda":
                self.ayuda()
                continue
            if comando not in self.habilidades:
                print(f"Habilidad no encontrada: {comando}")
                continue

            args = []
            while True:
                arg = input(f"Argumento {len(args)}: ").strip()
                if not arg:  # Finaliza la captura de argumentos
                    break
                if arg.lower() == "ayuda":  # Detecta "ayuda" como comando independiente
                    self.habilidades[comando].ayuda()
                    break
                args.append(arg)

            # Invoca la habilidad con los argumentos capturados
            if args and args[-1].lower() != "ayuda":
                try:
                    resultado = self.habilidades[comando].invocar(*args)
                    if resultado is not None:
                        print(resultado)
                except Exception as e:
                    print(f"Error al ejecutar el comando: {e}")




def prueba_menu_simple():
    habilidades = [
        Divisas('bitcoin2euro', tasa=49929.38, descripcion='Conversión de bitcoins a euros'),
        Divisas('euro2bitcoin', tasa=1/49929.38, descripcion='Conversión de euros a bitcoins'),
    ]
    m = Menu(habilidades)
    m.emular('ayuda')
    m.emular('bitcoin2euro 100')
    m.emular('euro2bitcoin 100')
    m.emular('ayuda noexiste')
    m.emular('ayuda bitcoin2euro')




  
class HabilidadSubcomandos(Habilidad):
    """Un tipo de habilidad que permite invocar varios subcomandos."""

    def subcomandos(self) -> dict[str, callable]:
        """
        Devuelve un diccionario de subcomandos a funciones.
        Ejemplo:
            {
                "insertar": self.insertar,
                "borrar": self.borrar,
            }
        """
        return {}

    def invocar(self, subcomando: str, *args: str) -> None:
        """
        Ejecuta un subcomando con los argumentos proporcionados.
        Parámetro subcomando: Nombre del subcomando a ejecutar.
        Parámetro args: Argumentos para el subcomando.
        """
        comandos = self.subcomandos()
        if subcomando in comandos:
            comandos[subcomando](*args)
        else:
            print(f"Subcomando '{subcomando}' no reconocido.")

    def ayuda(self) -> None:
        """
        Muestra información sobre los subcomandos disponibles.
        """
        print(f"Comando:\t{self.nombre}")
        print(f"Descripción:\t{self.descripcion}")
        print("Subcomandos:")
        for subcomando, metodo in self.subcomandos().items():
            print(f"  {subcomando}:\t{metodo.__doc__}")



class Contador(Habilidad):
    """Contador de vocales en una cadena de texto."""
        
    def invocar(self, texto: str) -> str:
        """Cuenta y muestra el número de vocales en el texto proporcionado."""
        contador: int = 0
        for char in texto.lower():
            if char in "aeiouáéíóúäëïöü":
                contador += 1
        return f"El texto tiene {contador} vocales."
        

class DetectorPalindromos(Habilidad):
    """Detector de palíndromos."""

    def invocar(self, texto: str) -> str:
        """
        Determina si el texto proporcionado es un palíndromo.
        Ignora espacios y diferencias entre mayúsculas y minúsculas.
        """
        if texto.lower() == "ayuda":
            self.ayuda()
        texto2 = texto.lower().replace(" ", "")
        es_palindromo = texto2 == texto2[::-1]
        
        if es_palindromo:
            respuesta: str = "Sí"
        else:
            respuesta = "No"
        return f"¿Es un palíndromo?: {respuesta}"


class ListaDeLaCompra(HabilidadSubcomandos):
    """Gestión avanzada de lista de la compra."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.productos = []

    def subcomandos(self) -> dict[str, callable]:
        """
        Define los subcomandos disponibles.
        """
        return {
            "insertar": self.insertar,
            "borrar": self.borrar,
            "listar": self.listar,
            "cantidad": self.cantidad,
        }
        
    def invocar(self, subcomando: str, *args: str) -> None:
        comandos = self.subcomandos()
        if subcomando in comandos:
            comandos[subcomando](*args)  
            return None
        else:
            print(f"Subcomando '{subcomando}' no reconocido.")

    def insertar(self, nombre: str, precio: float|int = 0.0, categoria: str="Sin categoría",
                 etiquetas: str = "", prioridad: int = 3) -> str|None:
        """
        Inserta un producto nuevo. Las etiquetas se separan por un |
        """
        try:
            producto = {
                "nombre": nombre,
                "precio": float(precio),
                "categoria": categoria,
                "etiquetas": etiquetas.split("|"),
                "prioridad": int(prioridad),
                "comprado" : False
            }
            self.productos.append(producto)
            
            print(f"Producto '{nombre}' añadido a la lista.")
        except:
            return "Error al añadir el producto: verifica los valores de precio y prioridad."

    def listar(self) -> str|None:
        """Muestra el listado de productos."""
        if not self.productos:
            print("La lista está vacía.")
            return
        for indice, producto in enumerate(self.productos):
            etiquetas2 = " ".join(f"#{etiqueta}" for etiqueta in producto["etiquetas"])
            prioridad: str = "*" * producto["prioridad"]
            recuadro: str = "[X]" if producto['comprado'] else "[ ]"
            print(f" {recuadro} {indice}: {producto['nombre']} - {producto['categoria']} - {prioridad} - {producto['precio']} - {etiquetas2}")


    def borrar(self, indice: str) -> str|None:
        """Borra un producto de la lista."""
        try:
            indice = int(indice)
            producto = self.productos.pop(indice)
            print(f"Producto '{producto['nombre']}' eliminado.")
        except:
            return "Índice no válido."

    def cantidad(self) -> None:
        """Muestra el número de productos en la lista."""
        print (f"Hay {len(self.productos)} productos en la lista.")

    def ayuda(self) -> None:
        """
        Muestra información sobre los subcomandos disponibles.
        """
        print(f"Comando:\t{self.nombre}")
        print(f"Descripción:\t{self.descripcion}")
        print("Subcomandos:")
        for subcomando, metodo in self.subcomandos().items():
            print(f"  {subcomando}:\t{metodo.__doc__.strip()}")


def prueba_menu_subcomandos():
    habilidades = [
        Divisas('bitcoin2euro', tasa=49929.38),
        Divisas('euro2bitcoin', tasa=1/49929.38),
        ListaDeLaCompra('listadelacompra', 'Gestión de la lista de la compra')
    ]
    m = Menu(habilidades)
    m.emular('ayuda')
    m.emular('ayuda listadelacompra')
    m.emular('listadelacompra insertar "plátanos canarios" 5.25 Alimentación "frutas,postre"')
    m.emular('listadelacompra insertar Pimientos 1.50 Alimentación')
    m.emular('listadelacompra listar')
    m.emular('listadelacompra borrar 0')
    m.emular('listadelacompra listar')

if __name__ == '__main__':
    euro2usd = Divisas(nombre="euro2usd", tasa=1.06, descripcion="Convierte euros a dólares estadounidenses")
    usd2euro = Divisas(nombre="usd2euro", tasa= 0.95, descripcion="Converte dólares estadounidenses en euros")
    vocales = Contador(nombre="vocales", descripcion="Cuenta en nº de vocales en un string")
    palindromo = DetectorPalindromos(nombre="palindromo", descripcion="Reconoce si un string es un palíndromo")
    lista = ListaDeLaCompra(nombre = "compra")
    
    habilidades = [euro2usd,usd2euro,vocales,palindromo,lista]
    menu = MenuPreguntas(habilidades)
    menu.lanzar()




    

