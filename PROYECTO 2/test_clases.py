import unittest
import sys
import io
from contextlib import contextmanager

from listadelacompra_clases import *

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
        self.l = ListaCompra()

    def test_insertar(self):
        # nombre, precio, categoria, etiquetas=(), prioridad=3
        self.l.insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        self.l.insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        self.l.insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)
        assert len(self.l.productos) == 3

    def test_cambiar(self):
        self.l.insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        self.l.insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        self.l.cambiar_estado(1)
        assert len(self.l.productos) == 2
        for t in self.l.productos:
            assert (t.nombre == 'Huevos') == t.comprado
    
    def test_precio(self):
        self.l.insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        self.l.insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        self.l.actualizar_precio(0, 1.5)
        assert len(self.l.productos) == 2
        for t in self.l.productos:
            assert (t.precio == 1.5) == (t.nombre == 'Arroz integral')


    def test_ordenar(self):
        self.l.insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        self.l.insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 0)
        self.l.insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)
        assert self.l.productos[0].nombre == 'Arroz integral'
        self.l.ordenar()
        assert self.l.productos[0].nombre == 'Desmaquillante'
        assert self.l.productos[1].nombre == 'Arroz integral'
        assert self.l.productos[2].nombre == 'Huevos'
        self.l.cambiar_estado(0)
        self.l.ordenar()
        assert self.l.productos[0].nombre == 'Arroz integral'
        assert self.l.productos[1].nombre == 'Huevos'
        assert self.l.productos[2].nombre == 'Desmaquillante'

    def test_mostrar(self):
        self.l.insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        self.l.insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        self.l.insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)
        v = red(self.l.mostrar_productos)
        assert 'Arroz integral' in v
        assert '0.72' in v
        assert 'Alimentación' in v
        assert 'risotto' in v
        assert 'Huevos' in v
        assert 'Desmaquillante' in v
        assert 'Cosméticos' in v

    def test_mostrar_no_comprados(self):
        self.l.insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        self.l.insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        self.l.insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)

        self.l.cambiar_estado(0)
        v = red(self.l.mostrar_productos, comprados=False)
        assert 'Huevos' in v
        assert 'Desmaquillante' in v

        assert 'Arroz integral' not in v
    
    def test_mostrar_categoria(self):
        self.l.insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        self.l.insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        self.l.insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)

        v = red(self.l.mostrar_productos, categorias=['Alimentación'])
        assert 'Huevos' in v
        assert 'Arroz integral' in v

        assert 'Desmaquillante' not in v

    def test_mostrar_etiquetas(self):
        self.l.insertar('Arroz integral', 0.72, 'Alimentación', ('risotto', 'arroz a la cubana'))
        self.l.insertar('Huevos', 1.20, 'Alimentación', ('arroz a la cubana', 'tortilla'), 1)
        self.l.insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)

        v = red(self.l.mostrar_productos, etiquetas=('arroz a la cubana',))
        assert 'Huevos' in v
        assert 'Arroz integral' in v

        assert 'Desmaquillante' not in v

if __name__ == '__main__':
    unittest.main(verbosity=1)
