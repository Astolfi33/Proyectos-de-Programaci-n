import unittest
import sys
import io

from utilidades import *


def red(fun, *args, **kwargs):
    '''
    Run a function with sys.stdout redirected to a string.
    This is useful to test functions that print to stdout.
    '''
    saved = sys.stdout
    out = io.StringIO()
    sys.stdout = out
    try:
        fun(*args, **kwargs)
    finally:
        sys.stdout = saved
    return out.getvalue()


class TestUtilidades(unittest.TestCase):

    @unittest.skipIf('cifrar' not in globals(),
                     "el método cifrar no está implementado")
    def test_cifrar(self):
        self.assertEqual(cifrar('hola mundo', 0), 'HOLA MUNDO')
        r = cifrar('hola mundo', 20)
        self.assertEqual(r, 'ÁDÚT AJBWD')
        r = cifrar('adiós, mundo', 20) 
        self.assertEqual(r, 'TWÉRH, AJBWD')

    @unittest.skipIf('descifrar' not in globals(),
                     "el método descifrar no está implementado")
    def test_descifrar(self):
        d = descifrar('TWÉRH, AJBWD', 20)
        self.assertEqual(d, 'ADIÓS, MUNDO')
        d = descifrar('ÁDÚT AJBWD', 20)
        self.assertEqual(d, 'HOLA MUNDO')

    def test_convertir(self):
        assert (euros_a_bitcoins(10000) - 0.22) < 0.1
        assert (bitcoins_a_euros(2) - EURO_BITCOIN_RATE * 2) < 1

    def test_contar(self):
        assert contar_vocales('esto son ocho vocales') == 8
        assert contar_vocales('  3 vocales ') == 3

    def test_palindromo(self):
        assert es_palindromo('ella te da detalle') == True
        assert es_palindromo('  Este texto no es un palindromo ') == False

    def test_temperaturas(self):
        assert max_temperaturas([12.0, 3.0, 4.0, 17.0, 26.0], 11) == [12.0, 17.0, 26.0]
        assert max_temperaturas([12.0, 3.0, 4.0, 17.0, 26.0], 32) == []

    def test_productos_vacios(self):
        productos.clear()
        v = red(mostrar_productos)
        assert 'No hay productos' in v
        assert len(productos) == 0

    def test_insertar(self):
        insertar('prueba')
        insertar('final')
        assert len(productos) == 2
        assert productos[0] == 'prueba'
        assert productos[1] == 'final'

    def test_borrar(self):
        productos.clear()
        insertar('prueba')
        insertar('final')
        borrar(1)
        assert len(productos) == 1
        borrar(0)
        assert len(productos) == 0

    def test_mostrar_productos(self):
        productos.clear()
        v = red(mostrar_productos)
        assert 'No hay productos' in v
        assert ':' not in v
        insertar('prueba')
        v = red(mostrar_productos)
        assert 'prueba' in v

if __name__ == '__main__':
    unittest.main(verbosity=0)

