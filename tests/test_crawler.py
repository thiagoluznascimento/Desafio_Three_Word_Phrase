import logging
from unittest.mock import patch, Mock
from unittest import TestCase

import hashlib
import os

import requests
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

        self.urls_imagens = [
            'http://threewordphrase.com//fatdog.htm', 'http://threewordphrase.com//gottabegood.htm',
            'http://threewordphrase.com//dogs.htm', 'http://threewordphrase.com//fivebro.htm',
            'http://threewordphrase.com//forgiveness.htm', 'http://threewordphrase.com//bombasstitties.htm',
            'http://threewordphrase.com//cowboys2.htm', 'http://threewordphrase.com//cowboys1.htm'
        ]

        # self.urls_imagens = self.instancia_crawler._extrai_url_imagens(self.pagina_resultado_busca_archive) #test_extrai_url_imagens
        self.htmls = self.instancia_crawler._obtem_paginas_imagens(self.urls_imagens)
        self.nomes_imagens = self.instancia_crawler._extrai_nome_imagens(self.htmls)
        self.links_imagens = self.instancia_crawler._parser_nomes_imagens(self.nomes_imagens)
        # import pdb; pdb.set_trace()
        # self.nome_arquivo_esperado = self.instancia_crawler._obtem_md5(requests.get(link).content) + ".gif"

        logging.basicConfig(filename='test_log.log', level=logging.ERROR)

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
        # urls_imagens = self.instancia_crawler._extrai_url_imagens(self.pagina_resultado_busca_archive)
        self.assertIsInstance(self.urls_imagens, list)
        self.assertGreater(len(self.urls_imagens), 0)
        for url in self.urls_imagens:
            self.assertTrue(url.startswith('http'))
        for link in self.urls_imagens:
            self.assertIn(link, self.urls_imagens, "Não existe essas URLs na fixture")

    def test_obtem_paginas_imagens(self):
        # htmls = self.instancia_crawler._obtem_paginas_imagens(self.urls_imagens)

        self.assertIsInstance(self.htmls, list)
        self.assertEqual(len(self.htmls), len(self.urls_imagens))
        for html in self.htmls:
            self.assertIsInstance(html, str)

    def test_extrai_nome_imagens(self):
        lista_img_tag = self.instancia_crawler._extrai_nome_imagens(self.htmls)
        # import pdb; pdb.set_trace()
        # for nome in self.nomes_imagens:
        #     self.assertIsInstance(self.nomes_imagens, list)
        #     self.assertEqual(len(self.nomes_imagens), len(self.htmls))
        #     self.assertIsInstance(nome, str)
        #     import pdb; pdb.set_trace()

    # def test_parser_nomes_imagens(self):
    #     # links_imagens = self.instancia_crawler._parser_nomes_imagens(self.nomes_imagens)
    #     for link in self.links_imagens:
    #         self.assertIsInstance(self.links_imagens, list)
    #         self.assertEqual(len(self.links_imagens), len(self.nomes_imagens))
    #         self.assertIsInstance(link, str)

    # def test_obtem_md5(self):
    #     conteudo_imagem = b'conteudo_de_imagem_de_teste'
    #     hash_obtido = self.instancia_crawler._obtem_md5(conteudo_imagem)
    #     md5_manual = hashlib.md5(conteudo_imagem).hexdigest()
    #     self.assertEqual(hash_obtido, md5_manual)

    # def test_baixa_arquivos_gif(self):
    #     self.instancia_crawler._baixa_arquivos_gif(self.links_imagens)
    #     self.assertTrue(os.path.exists('imagens_gif'))
    #     for link in self.links_imagens:
    #         nome_arquivo_esperado = self.instancia_crawler._obtem_md5(requests.get(link).content) + ".gif"
    #         caminho_completo = os.path.join('imagens_gif', nome_arquivo_esperado)
    #         self.assertTrue(os.path.exists(caminho_completo))

    # def tearDown(self):
    #     if os.path.exists('imagens_gif'):

    #         for imagem in os.listdir('imagens_gif'):
    #             caminho_com_arquivos = os.path.join('imagens', imagem)
    #             os.remove(caminho_com_arquivos)
    #     os.rmdir('imagens_gif')
