import unittest
from faker import Faker
import random
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

        self.data_factory = Faker()

        Faker.seed(1000)

        self.data = []
        self.albumes = []
        self.medios = [Medio.CD, Medio.CASETE, Medio.DISCO]

        for i in range(0, 10):
            self.data.append((
                self.data_factory.unique.name(),
                self.data_factory.random_int(1800, 2021),
                self.data_factory.text(),
                random.choice(self.medios)))
            self.albumes.append(
                Album(
                    titulo=self.data[-1][0],
                    ano=self.data[-1][1],
                    descripcion=self.data[-1][2],
                    medio=self.data[-1][3],
                    canciones=[]
                ))
            self.session.add(self.albumes[-1])

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
        album = self.session.query(Album).filter(
            Album.titulo == 'Signos' and Album.medio == Medio.DISCO).first()

        self.assertEqual(album.titulo, 'Signos')
        self.assertEqual(album.ano, 1986)

    def test_constructor(self):
        for album, dato in zip(self.albumes, self.data):
            self.assertEqual(album.titulo, dato[0])
            self.assertEqual(album.ano, dato[1])
            self.assertEqual(album.descripcion, dato[2])
            self.assertEqual(album.medio, dato[3])

    def test_agregar_album_with_fake(self):
        self.data.append((self.data_factory.unique.name(), self.data_factory.random_int(
            1800, 2021), self.data_factory.text(), random.choice(self.medios)))

        resultado = self.coleccion.agregar_album(
            titulo=self.data[-1][0], anio=self.data[-1][1], descripcion=self.data[-1][2], medio=self.data[-1][3])

        self.assertEqual(resultado, True)

    def test_agregar_album_repetido_with_fake(self):
        resultado = self.coleccion.agregar_album(
            titulo=self.data[-1][0],
            anio=self.data[-1][1],
            descripcion=self.data[-1][2],
            medio=self.data[-1][3])

        self.assertNotEqual(resultado, True)

    def test_editar_album_with_fake(self):
        self.data.append((self.data_factory.unique.name(), self.data_factory.random_int(
            1800, 2021), self.data_factory.text(), random.choice(self.medios)))

        resultado1 = self.coleccion.editar_album(
            album_id=1,
            titulo=self.data[-1][0],
            anio=self.data[-1][1],
            descripcion=self.data[-1][2],
            medio=self.data[-1][3])

        resultado2 = self.coleccion.editar_album(
            album_id=2,
            titulo=self.data[-3][0],
            anio=self.data[-3][1],
            descripcion=self.data[-3][2],
            medio=self.data[-3][3])

        self.assertTrue(resultado1)
        self.assertFalse(resultado2)

    def test_albumes_iguales_with_fake(self):
        album_nuevo = self.albumes[0]
        album_recuperado = self.coleccion.dar_album_por_id(1)

        self.assertIs(album_nuevo, self.albumes[0])
        self.assertIsNot(album_recuperado, self.albumes[0])

    def test_elemento_en_conjunto_with_fake(self):
        album_nuevo = Album(
            titulo=self.data_factory.unique.name(),
            ano=self.data_factory.random_int(1800, 2021),
            descripcion=self.data_factory.text(),
            medio=random.choice(self.medios),
            canciones=[]
        )

        album_existente = self.albumes[2]

        self.assertIn(album_existente, self.albumes)
        self.assertNotIn(album_nuevo, self.albumes)

    def test_instancia_clase_with_fake(self):
        self.assertIsInstance(self.albumes[0], Album)
        self.assertNotIsInstance(self.coleccion, Album)
    
    def test_verificar_almacenamiento_agregar_album_with_fake(self):
        self.data.append((self.data_factory.unique.name(), self.data_factory.random_int(1800, 2021), self.data_factory.text(), random.choice(self.medios)))
        self.coleccion.agregar_album(
            titulo = self.data[-1][0],
            anio = self.data[-1][1],
            descripcion = self.data[-1][2],
            medio = self.data[-1][3])
        
        album = self.session.query(Album).filter(Album.titulo == self.data[-1][0] and Album.ano == self.data[-1][1]).first()
        
        self.assertEqual(album.titulo, self.data[-1][0])
        self.assertEqual(album.ano, self.data[-1][1])
        self.assertEqual(album.descripcion, self.data[-1][2])
        self.assertIn(album.medio, self.medios)
