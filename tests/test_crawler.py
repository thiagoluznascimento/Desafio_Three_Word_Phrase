from unittest.mock import patch, Mock
from unittest import TestCase
# import os

from src.crawler import BucadorTHREEWORDPHRASE


class TestBucadorTHREEWORDPHRASE(TestCase):

    def setUp(self):
        self.instancia_crawler = BucadorTHREEWORDPHRASE('URL_BUSCA')
        self.url = "http://threewordphrase.com/"
        self.link = "http://threewordphrase.com//archive.htm"

        with open('./tests/fixtures/resultado_da_busca.html') as arquivo:
            self.pagina_resultado_busca = arquivo.read()
        with open('./tests/fixtures/resultado_busca_archive.html') as arquivo:
            self.pagina_resultado_busca_archive = arquivo.read()

    def test_busca_imagens(self):
        with patch('requests.get', return_value=Mock(text=self.pagina_resultado_busca)) as mock_get:
            html_obtido = self.instancia_crawler._busca_imagens()
            self.assertEqual(self.pagina_resultado_busca, html_obtido, "Página diferente da esperada.")
            mock_get.assert_called_once_with(self.url)

    def test_parser_slug_archive(self):
        link_esperado = self.link
        link_obtido = self.instancia_crawler._parser_slug_archive(self.pagina_resultado_busca)
        self.assertEqual(link_esperado, link_obtido)

    def test_obtem_slugs_archive(self):
        with patch('requests.get', return_value=Mock(textt=self.pagina_resultado_busca_archive)) as mock_get:
            html_obtido = self.instancia_crawler._obtem_slugs_archive(self.link)
            self.assertEqual(self.pagina_resultado_busca_archive, html_obtido, "Pagina diferente da esperada.")
            mock_get.assert_called_once_with(self.url)
