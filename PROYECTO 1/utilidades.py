EURO_BITCOIN_RATE = 44471.78

# SUMA DE DOS NÚMEROS CUALESQUIERA

def sumar_numeros(num1: int|float, num2: int|float) -> int|float:
    '''Suma los dos numeros proporcionados.'''
    suma = num1 + num2
    return suma  
# CONVERSOR DE EURO A BITCOIN

def euros_a_bitcoins(euros: int | float) -> int | float:
  '''Convierte una cantidad de euros a bitcoins. 1 bitcoin = 44570.17 €'''
  bitcoin = round(euros / EURO_BITCOIN_RATE, 2) # Establecemos la conversión e imponemos un redondeo a dos decimales
  return bitcoin
  
# CONVERSOR DE BITCOIN A EURO

def bitcoins_a_euros(bitcoin: int | float) -> int | float:
  '''Convierte una cantidad de bitcoins a euros. 1 bitcoin = 44570.17 €'''
  euros = round(bitcoin * EURO_BITCOIN_RATE, 2) # Establecemos la conversión e imponemos un redondeo a dos decimales
  return euros

# CONTADOR DE VOCALES

def contar_vocales(texto: str) -> int:
  '''Devuelve el número de vocales que tiene el texto dado.'''
  vocales = "aeiouàèìòùäëïöü"
  texto = texto.lower() # Pasamos el string a minúsculas para evitar errores por mayúsculas
  contador = 0 # Inicialmente el contador está a cero
  for letra in texto:
    if letra in vocales:
      contador += 1 # Por cada vocal sumará 1 al contador hasta recorrer el string completo
  return contador
# DETECTOR DE PALINDROMOS

def es_palindromo(texto: str) -> bool:
  '''Detecta si un texto es palíndromo o no'''
  texto = ''.join(texto.split())
  texto = texto.lower() # Juntamos el texto para que el programa se centre en los caracteres
  return texto == texto[::-1]

# DETECTOR DE MAXIMOS DE TEMPERATURAS

def max_temperaturas(temperaturas: list[float], umbral: float) -> list[float]:
  '''Detecta qué mediciones de temperatura han superado el umbral dado'''
  altas_temperaturas = list() # Creamos una lista vacía que tendrá números de tipo float
  for temperatura in temperaturas: # Recorremos la lista
    if temperatura > umbral:
      altas_temperaturas.append(temperatura) # Si supera el umbral lo incluimos en la lista
  return altas_temperaturas

# LISTA DE LA COMPRA

productos: list[str] = []
for contador, productos in enumerate(productos, start = 0): # Hacemos que la lista esté enumerada
  print(contador, productos)

def insertar(producto: str) -> None:
  '''Añade un producto a la lista'''
  productos.append(producto) # Inserta cada producto al final de la lista
  

def borrar(numero: int) -> None:
  '''Borra el producto en el índice dado de lista de productos.'''
  # productos.pop(numero) # Elimina un producto en función del índice que ocupa
  del productos[numero]

def mostrar_productos() -> None:
  '''Muestra la lista de productos con sus índices.'''
  if len(productos) == 0: # Si no hay productos en la lista, se imprimirá por pantalla ese mensaje
    print("No hay productos")
  else:
    print(productos)
    
def cantidad() -> int:
  '''Devuelve el número de productos.'''
  return len(productos)

# CIFRADO DE TEXTO

def cifrar(texto: str, desplazamiento: int) -> str:
  '''
  Transforma un texto dado usando cifrado César con un desplazamiento dado.

  Utiliza esta lista de caracteres: ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ
  
  Si un caracter no se encuentra en la lista, se deja intacto.
  '''
  alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ"
  texto = texto.upper() # Primero convertimos el texto a mayúsculas
  resultado = ""
  
  # Recorremos cada caracter del texto
  for char in texto:
    if char in alfabeto: 
    # Solo aplicamos el cifrado de las letras de la A a la Z
      nueva_posicion = (alfabeto.index(char) + desplazamiento) % 32 # Calculamos la nueva posición
      resultado += alfabeto[nueva_posicion]
    else:
    # Si no es una letra, lo dejamos tal y como está
      resultado += char
    
  return resultado
# DESCIFRADO DE TEXTO

def descifrar(cifrado: str, desplazamiento: int) -> str:
  '''
  Aplicada a un texto cifrado con el mismo desplazamiento,
  devuelve el texto original.
  '''
  alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ"
  cifrado = cifrado.upper() # Primero convertimos el texto a mayúsculas
  resultado = ""
  
  # Recorremos cada caracter del texto cifrado
  for char in cifrado:
    if char in alfabeto: 
    # Solo aplicamos el cifrado de las letras de la A a la Z
      nueva_posicion = (alfabeto.index(char) - desplazamiento) % 32 # Calculamos la nueva posición
      resultado += alfabeto[nueva_posicion]
    else:
      # Si no es una letra, lo dejamos tal y como está
      resultado += char
  
  return resultado


# MENU INTERACTIVO


from typing import List

def mostrar_menu() -> None:
    """Muestra las instrucciones de uso del asistente"""
    print("Menú interactivo\n")

def ejecutar_comando(comando: str) -> None:
    """Interpreta y ejecuta los comandos del usuario en función de la entrada de texto."""
    
    # Separar el comando de sus argumentos
    partes = comando.split()
    if len(partes) == 0:
        print("Comando no reconocido")
        return
    
    # Obtener el primer argumento como el comando principal
    comando_principal = partes[0].lower()

    # Comandos disponibles
    if comando_principal == 'convertir':
        # Comando: convertir euros bitcoins <cantidad>
        if len(partes) == 4 and partes[1] == 'euros' and partes[2] == 'bitcoins':
            cantidad = float(partes[3])
            print(euros_a_bitcoins(cantidad))
        # Comando: convertir bitcoins euros <cantidad>
        elif len(partes) == 4 and partes[1] == 'bitcoins' and partes[2] == 'euros':
            cantidad = float(partes[3])
            print(bitcoins_a_euros(cantidad))
        else:
            print("Comando no reconocido")

    elif comando_principal == 'contar':
        # Comando: contar <texto>
        if len(partes) > 1:
            texto = ' '.join(partes[1:])
            print(contar_vocales(texto))
        else:
            print("Comando no reconocido")
    
    elif comando_principal == 'palindromo':
      # Comando: palindromo <texto>
      texto = ' '.join(partes[1:])
      if len(partes) > 1:
        print(es_palindromo(texto))
      else:
        print("Comando no reconocido")
        
    elif comando_principal == 'cifrar':
        # Comando: cifrar <desplazamiento> <texto>
        if len(partes) > 2:
            desplazamiento = int(partes[1])
            texto = ' '.join(partes[2:])
            print(cifrar(texto, desplazamiento))
        else:
            print("Comando no reconocido")

    elif comando_principal == 'descifrar':
        # Comando: descifrar <desplazamiento> <texto cifrado>
        if len(partes) > 2:
            desplazamiento = int(partes[1])
            texto = ' '.join(partes[2:])
            print(descifrar(texto, desplazamiento))
        else:
            print("Comando no reconocido")

    elif comando_principal == 'temperaturas':
        # Comando: temperaturas <lista de temperaturas separadas por comas> <umbral>
        if len(partes) == 3:
            temperaturas = list(map(float, partes[1].split(',')))
            umbral = float(partes[2])
            print(max_temperaturas(temperaturas, umbral))
        else:
            print("Comando no reconocido")

    elif comando_principal == 'productos':
        # Subcomando: productos
        if len(partes) == 1:
            print(mostrar_productos())
        # Subcomando: productos nuevo <producto>
        elif len(partes) == 3 and partes[1] == 'nuevo':
            producto = partes[2]
            insertar(producto)
            print(f"0: {producto}")
        # Subcomando: productos borrar <índice>
        elif len(partes) == 3 and partes[1] == 'borrar':
            indice = int(partes[2])
            borrar(indice)
        else:
            print("Comando no reconocido")

    elif comando_principal == 'salir':
        # Comando: salir
        print("¡Adiós!")
        exit()
    
    else:
        # Comando no reconocido
        print("Comando no reconocido")

def ejecutar_menu() -> None:
    """Bucle principal del menú interactivo."""
    mostrar_menu()
    while True:
        comando = input("-> ")
        ejecutar_comando(comando)

# Llamada al menú interactivo
if __name__ == "__main__":
    ejecutar_menu()

  

  