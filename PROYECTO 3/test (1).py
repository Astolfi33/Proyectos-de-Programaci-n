import unittest
import sys
import os
import io
from contextlib import contextmanager

from unittest import mock, skipIf
from habilidades import MenuPrompt,Habilidad,Divisas,Menu,MenuComas,MenuPreguntas

SUBCOMANDOS = False

try:
    from habilidades import HabilidadSubcomandos, ListaDeLaCompra
    print("Se va a comprobar el apartado de Subcomandos")
    print("Para evitarlo, comenta las clases relacionadas con ese apartado.")
    SUBCOMANDOS = True
except ImportError:
    print("NO se va a comprobar el apartado Subcomandos porque las clases "
          "HabilidadSubcomandos y ListaDeLaCompra no han sido desarrolladas")


@contextmanager
def redirected():
    '''
    Context manager para capturar las salida de print (sys.stdout en general).
    Nos va a permitir capturar la salida por pantalla de las funciones del ejercicio.
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

def stub_stdin(testcase_inst, inputs):
    stdin = sys.stdin

    def cleanup():
        sys.stdin = stdin

    testcase_inst.addCleanup(cleanup)
    sys.stdin = io.StringIO(inputs)


class TestHabilidades(unittest.TestCase):

    def test_habilidad(self):
        '''Comemular que se puede crear una habilidad'''
        h = Habilidad(nombre='test', descripcion='prueba')
        assert h!=None


    def test_divisas(self):
        usd2euro = Divisas('usd2euro', tasa=0.85)
        assert round(85 - usd2euro.invocar(100)) == 0
        euro2usd = Divisas('euro2usd', tasa=1/0.85)
        assert round(117.65 - euro2usd.invocar(100)) == 0

    def test_menu(self):

        habilidades = [
            Divisas('usd2euro', tasa=0.85, descripcion='Conversión de dólares a euros'),
            Divisas('euro2usd', tasa=1/0.85, descripcion='Conversión de euros a dólares'),
        ]
        m = Menu(habilidades)
        with redirected() as out:
            m.emular('ayuda')
            m.emular('usd2euro 100')
            m.emular('euro2usd 100')
            m.emular('ayuda noexiste')
            m.emular('ayuda usd2euro')
            out = out.getvalue()
            salida = '''
        > ayuda
        Habilidades disponibles:
                usd2euro:       Conversión de dólares a euros
                euro2usd:       Conversión de euros a dólares
        > usd2euro 100
        85.0
        > euro2usd 100
        117.65
        > ayuda noexiste
        Habilidad no encontrada: noexiste
        > ayuda usd2euro
        Convertir una cantidad la divisa original a la divisa objetivo
        '''

        for line in salida:
            assert line in out

    def test_listadelacompra(self):
        from habilidades import ListaDeLaCompra
        t = ListaDeLaCompra(nombre='mi lista de la compra')
        t.invocar('insertar', 'Cebollas')
        assert any(p["nombre"] == "Cebollas" for p in t.productos)

    @skipIf(not SUBCOMANDOS, "No se ha desarrollado el apartado de subcomandos")
    def test_menu_subcomandos(self):
        habilidades = [
            Divisas('usd2euro', tasa=0.85),
            Divisas('euro2usd', tasa=1/0.85),
            ListaDeLaCompra('listadelacompra', 'Gestión de la lista de la compra')
        ]
        with redirected() as out:
            m = Menu(habilidades)
            m.emular('ayuda')
            for line in '''Habilidades disponibles:
    usd2euro:
    Conversión de divisas
    euro2usd:
    Conversión de divisas
    listadelacompra: Gestión de la lista de la compra''':
                assert line in out.getvalue()


            m.emular('ayuda listadelacompra')

            for line in '''Comando:
    listadelacompra
    Descripción:
    Gestión de la lista de la compra
    Subcomandos:
    insertar: Insertar un producto nuevo
    borrar: Borrar un producto
    listar: Mostrar el listado de productos
    cantidad: Mostrar el número de productos en la lista''':
                assert line in out.getvalue()

            m.emular('listadelacompra insertar "Cebollas"')
            m.emular('listadelacompra insertar "Pimientos"')
            m.emular('listadelacompra listar')
            assert '''0: Cebollas''' in out.getvalue()
            assert '''1: Pimientos''' in out.getvalue()
            m.emular('listadelacompra borrar 0')
            m.emular('listadelacompra listar')
            assert '''0: Pimientos''' in out.getvalue()
            out = out.getvalue()

    def test_menu_prompt(self):
        stub_stdin(self, 'salir\n')
        m = MenuPrompt([], prompt='$')
        with redirected() as out:
            m.lanzar()
            assert '$' in out.getvalue()

    def test_menu_comas(self):
        m = MenuComas([])
        stub_stdin(self, 'ayuda,noexiste\nsalir\n')
        with redirected() as out:
            m.lanzar()
            assert 'Habilidad no encontrada: noexiste' in out.getvalue()

    def test_menu_preguntas(self):
        m = MenuPreguntas([])
        stub_stdin(self, 'ayuda\nnoexiste\n\nsalir\n\n')
        with redirected() as out:
            m.lanzar()
            assert 'Habilidad no encontrada: noexiste' in out.getvalue()

if __name__ == '__main__':
    unittest.main(verbosity=1)
