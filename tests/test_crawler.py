from unittest.mock import patch, Mock
from unittest import TestCase
# import os

from src.crawler import BucadorTHREEWORDPHRASE


class TestBucadorTHREEWORDPHRASE(TestCase):

    def setUp(self):
        self.instancia_crawler = BucadorTHREEWORDPHRASE('URL_BUSCA')
        self.url = "http://threewordphrase.com/"
        self.link_archive = "http://threewordphrase.com//archive.htm"

        with open('./tests/fixtures/resultado_da_busca.html') as arquivo:
            self.pagina_resultado_busca = arquivo.read()
        with open('./tests/fixtures/resultado_busca_archive.html') as arquivo:
            self.pagina_resultado_busca_archive = arquivo.read()

        self.lista_urls = [
            'http://threewordphrase.com//fatdog.htm', 'http://threewordphrase.com//gottabegood.htm',
            'http://threewordphrase.com//dogs.htm', 'http://threewordphrase.com//fivebro.htm',
            'http://threewordphrase.com//forgiveness.htm', 'http://threewordphrase.com//bombasstitties.htm',
            'http://threewordphrase.com//cowboys2.htm', 'http://threewordphrase.com//cowboys1.htm'
        ]
        # self.urls_imagens = self.instancia_crawler._extrai_url_imagens(self.pagina_resultado_busca_archive)test_obtem_paginas_imagens
        self.htmls = self.instancia_crawler._obtem_paginas_imagens(self.lista_urls)

    def test_busca_imagens(self):
        with patch('requests.get', return_value=Mock(text=self.pagina_resultado_busca)) as mock_get:
            html_obtido = self.instancia_crawler._busca_imagens()
            self.assertEqual(self.pagina_resultado_busca, html_obtido, "Página diferente da esperada.")
            mock_get.assert_called_once_with(self.url)

    def test_parser_slug_archive(self):
        link_esperado = self.link_archive
        link_obtido = self.instancia_crawler._parser_slug_archive(self.pagina_resultado_busca)
        self.assertEqual(link_esperado, link_obtido)

    def test_obtem_html_archive(self):
        link_archive_imagens = "http://threewordphrase.com//archive.htm"
        with patch('requests.get', return_value=Mock(text=self.pagina_resultado_busca_archive)) as mock_get:
            html_obtido = self.instancia_crawler._obtem_html_archive(link_archive_imagens)
            self.assertEqual(self.pagina_resultado_busca_archive, html_obtido, "Pagina diferente da esperada.")
            mock_get.assert_called_once_with(self.link_archive)

    def test_extrai_url_imagens(self):
        urls_imagens = self.instancia_crawler._extrai_url_imagens(self.pagina_resultado_busca_archive)
        self.assertIsInstance(urls_imagens, list)
        self.assertGreater(len(urls_imagens), 0)
        for url in urls_imagens:
            self.assertTrue(url.startswith('http'))
        for link in self.lista_urls:
            self.assertIn(link, urls_imagens, "Não existe essas URLs na fixture")

    def test_obtem_paginas_imagens(self):
        htmls = self.instancia_crawler._obtem_paginas_imagens(self.lista_urls)
        self.assertIsInstance(htmls, list)
        self.assertEqual(len(htmls), len(self.lista_urls))
        for html in htmls:
            self.assertIsInstance(html, str)

    def test_extrai_link_imagens(self):
        nomes_imagens = self.instancia_crawler._extrai_link_imagens(self.htmls)
        # import pdb; pdb.set_trace()
        for nome in nomes_imagens:
            self.assertIsInstance(nomes_imagens, list)
            self.assertEqual(len(nomes_imagens), len(self.htmls))
            self.assertIsInstance(nome, str)

    def test_parser_nomes_imagens(self):
        pass
        
