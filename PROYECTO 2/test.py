import unittest
import sys
import io
from contextlib import contextmanager

from listadelacompra import *


@contextmanager
def redirected():
    '''
    Context manager para capturar las salida de print (sys.stdout en general).
    Nos va a permitir capturar la salida por pantalla de las funciones del ejercicio.

    Sería mejor separar el código de mostrar_tareas en dos funciones: una que devuelve el
    texto, y otra que llama a la primera y lo muestra. Así no haría falta este tipo de
    programación avanzada.
    '''
    saved = sys.stdout
    out = io.StringIO()
    sys.stdout = out
    try:
        yield out
    finally:
        sys.stdout = saved


def red(fun, *args, **kwargs):
    with redirected() as out:
        fun(*args, **kwargs)
    return out.getvalue()


class TestProductos(unittest.TestCase):

    def setUp(self):
        productos.clear()

    def test_insertar(self):
        # nombre, precio, categoria, etiquetas=(), prioridad=3
        insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)
        assert len(productos) == 3

    def test_cambiar(self):
        insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        cambiar_estado(1)
        assert len(productos) == 2
        for t in productos:
            assert (t["nombre"] == 'Huevos') == t["comprado"]
    
    def test_precio(self):
        insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        actualizar_precio(0, 1.5)
        assert len(productos) == 2
        for t in productos:
            assert (t["precio"] == 1.5) == (t["nombre"] == 'Arroz integral')


    def test_ordenar(self):
        insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 0)
        insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)
        assert productos[0]["nombre"] == 'Arroz integral'
        ordenar()
        assert productos[0]["nombre"] == 'Desmaquillante'
        assert productos[1]["nombre"] == 'Arroz integral'
        assert productos[2]["nombre"] == 'Huevos'
        cambiar_estado(0)
        ordenar()
        assert productos[0]["nombre"] == 'Arroz integral'
        assert productos[1]["nombre"] == 'Huevos'
        assert productos[2]["nombre"] == 'Desmaquillante'

    def test_mostrar(self):
        insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)
        v = red(mostrar_productos)
        assert 'Arroz integral' in v
        assert '0.72' in v
        assert 'Alimentación' in v
        assert 'risotto' in v
        assert 'Huevos' in v
        assert 'Desmaquillante' in v
        assert 'Cosméticos' in v

    def test_mostrar_no_comprados(self):
        insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)

        cambiar_estado(0)
        v = red(mostrar_productos, comprados=False)
        assert 'Huevos' in v
        assert 'Desmaquillante' in v

        assert 'Arroz integral' not in v
    
    def test_mostrar_categoria(self):
        insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)

        v = red(mostrar_productos, categorias=['Alimentación'])
        assert 'Huevos' in v
        assert 'Arroz integral' in v

        assert 'Desmaquillante' not in v

    def test_mostrar_etiquetas(self):
        insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)

        v = red(mostrar_productos, etiquetas=('arroz a la cubana',))
        assert 'Huevos' in v
        assert 'Arroz integral' in v

        assert 'Desmaquillante' not in v

if __name__ == '__main__':
    unittest.main(verbosity=1)
