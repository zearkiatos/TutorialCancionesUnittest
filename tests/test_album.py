import unittest
from src.logica.coleccion import Coleccion
from src.modelo.album import Album, Medio
from src.modelo.declarative_base import Session


class AlbumTestCase(unittest.TestCase):

    def tearDown(self):
        self.session = Session()

        busqueda = self.session.query(Album).all()

        for album in busqueda:
            self.session.delete(album)

        self.session.commit()
        self.session.close()

    def setUp(self):
        self.coleccion = Coleccion()

        self.session = Session()

        self.album1 = Album(titulo='Corazones', ano=1990,
                            descripcion='No tiene', medio=Medio.CD, canciones=[])
        self.album2 = Album(titulo='La voz de los 80s', ano=1984,
                            descripcion='No tiene', medio=Medio.CASETE, canciones=[])
        self.album3 = Album(titulo='Pateando piedras', ano=1986,
                            descripcion='No tiene', medio=Medio.DISCO, canciones=[])
        self.album4 = Album(titulo='La cultura de la basura', ano=1987,
                            descripcion='No tiene', medio=Medio.DISCO, canciones=[])

        self.session.add(self.album1)
        self.session.add(self.album2)
        self.session.add(self.album3)
        self.session.add(self.album4)

        self.session.commit()
        self.session.close()

    def test_agregar_album(self):
        resultado = self.coleccion.agregar_album(
            titulo="Nada personal", anio=1985, descripcion="No tiene", medio=Medio.CASETE)

        self.assertEqual(resultado, True)

    def test_agregar_album_repetido(self):
        resultado = self.coleccion.agregar_album(
            titulo="Corazones", anio=1985, descripcion="No tiene", medio=Medio.CASETE)

        self.assertNotEqual(resultado, True)

    def test_editar_album(self):
        resultado1 = self.coleccion.editar_album(
            album_id=1, titulo="Corazones Remastered", anio=1985, descripcion="No tiene", medio=Medio.CASETE)
        resultado2 = self.coleccion.editar_album(
            album_id=2, titulo="Pateando piedras", anio=1985, descripcion="No tiene", medio=Medio.CASETE)

        self.assertTrue(resultado1)
        self.assertFalse(resultado2)

    def test_albumes_iguales(self):
        album_nuevo = self.album1
        album_recuperado = self.coleccion.dar_album_por_id(1)

        self.assertIs(album_nuevo, self.album1)
        self.assertIsNot(album_recuperado, self.album1)

    def test_elemento_en_conjunto(self):
        conjunto = [self.album1, self.album2, self.album3]

        self.assertIn(self.album1, conjunto)
        self.assertNotIn(self.album4, conjunto)

    def test_instacia_clase(self):
        self.assertIsInstance(self.album1, Album)
        self.assertNotIsInstance(self.coleccion, Album)

    def test_verificar_almacenamiento_agregar_album(self):
        self.coleccion.agregar_album(
            titulo="Signos", anio=1986, descripcion="No tiene", medio=Medio.DISCO)
        self.session = Session()
        album = self.session.query(Album).filter(Album.titulo == 'Signos' and Album.medio == Medio.DISCO).first()

        self.assertEqual(album.titulo, 'Signos')
        self.assertEqual(album.ano, 1986)