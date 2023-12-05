from unittest.mock import patch, Mock
from unittest import TestCase

import os
from src.crawler import BuscadorTheeWordPhrase


class TestBuscadorTheeWordPhrase(TestCase):

    def setUp(self):
        self.instancia_crawler = BuscadorTheeWordPhrase()
        self.URL_BUSCA = "http://threewordphrase.com/archive.htm"        
        self.URL_PRINCIPAL = "http://threewordphrase.com/"

        self.urls_esperadas = [
            'http://threewordphrase.com/report.htm', 'http://threewordphrase.com/reallybig.htm',
            'http://threewordphrase.com/serial.htm', 'http://threewordphrase.com/explorer.htm', 
            'http://threewordphrase.com/favor.htm', 'http://threewordphrase.com/nautical.htm',
            'http://threewordphrase.com/planecrash.htm', 'http://threewordphrase.com/pressure.htm',
            'http://threewordphrase.com/goneatya.htm'
        ]

        with open('./tests/fixtures/resultado_busca.html') as f:
            self.pagina_resultado_busca = f.read()

        self.paginas = []
        with open('./tests/fixtures/paginas/pagina01.html', 'r') as f:
            self.pagina01 = f.read()
            self.paginas.append(self.pagina01)
        with open('./tests/fixtures/paginas/pagina02.html', 'r') as f:
            self.pagina02 = f.read()
            self.paginas.append(self.pagina02)
        with open('./tests/fixtures/paginas/pagina03.html', 'r') as f:
            self.pagina03 = f.read()
            self.paginas.append(self.pagina03)
        with open('./tests/fixtures/pagina_nao_encontrada.html', 'r') as f:
            self.pagina_nao_encontrada = f.read()     

    def test__obtem_pagina_archive(self):
        with patch('requests.get', return_value=Mock(text=self.pagina_resultado_busca)) as mock_get:
            html_obtido = self.instancia_crawler._obtem_pagina_archive(self.URL_BUSCA)
        self.assertEqual(self.pagina_resultado_busca, html_obtido, "Pagina diferente da esperada.")
        self.assertEqual(mock_get.call_count, 1, "O numero de chamada é diferente do esperado.")

    def test_lanca_exception_quando_pagina_archive_nao_encontrada(self):
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.text = []
            mock_response.raise_for_status.side_effect=Exception
            mock_get.return_value=mock_response
            self.assertEqual(self.instancia_crawler._obtem_pagina_archive(['conteudo_url']),[])

    def test_extrai_url_imagens_da_pagina_archive(self):
        urls_esperadas = [
            'http://threewordphrase.com/report.htm', 'http://threewordphrase.com/reallybig.htm',
            'http://threewordphrase.com/serial.htm', 'http://threewordphrase.com/explorer.htm', 
            'http://threewordphrase.com/favor.htm', 'http://threewordphrase.com/nautical.htm',
            'http://threewordphrase.com/planecrash.htm', 'http://threewordphrase.com/pressure.htm',
            'http://threewordphrase.com/goneatya.htm'
        ]
        urls_obtidas = self.instancia_crawler._extrai_url_imagens(self.pagina_resultado_busca)
        for url in urls_esperadas:
            self.assertIn(url, urls_obtidas)

    def test_obtem_paginas_imagens(self):
        lista_mock = [
            Mock(text=self.pagina01),
            Mock(text=self.pagina02),
            Mock(text=self.pagina03)
        ]
        lista_urls = [
            'http://threewordphrase.com/report.htm', 'http://threewordphrase.com/reallybig.htm',
            'http://threewordphrase.com/serial.htm'
        ]
        with patch('requests.get', side_effect=lista_mock) as mock_get:
            htmls_obtidos = self.instancia_crawler._obtem_paginas_imagens(lista_urls)
            htmls_esperados = self.paginas
            self.assertEqual(htmls_esperados, htmls_obtidos)
        self.assertEqual(mock_get.call_count, 3, "O numero de chamada é diferente do esperado")

    def test_lanca_exception_quando_pagina_imagem_nao_encontrada(self):
        with patch('requests.get') as mock_get:
            obj_mock = Mock()
            obj_mock.text = []
            obj_mock.raise_for_status.side_effect=Exception
            mock_get.return_value=obj_mock
            self.assertEqual(self.instancia_crawler._obtem_paginas_imagens(['conteudo_url']),[])
        
    def test_extrai_links_imagens(self):
        lista_links = [
            'http://threewordphrase.com/report.gif', 'http://threewordphrase.com/reallybig.gif',
            'http://threewordphrase.com/serial.gif'
        ]
        links_obtidos = self.instancia_crawler._extrai_links_imagens(self.paginas)
        links_esperados = lista_links
        # import pdb; pdb.set_trace()
        self.assertEqual(links_obtidos, links_esperados)
    
    def test_baixa_imagens_tirinhas(self):
        lista_mock = [
            Mock(content=b'algum conteudo imagem'),
            Mock(content=b'outro conteudo imagem')
        ]
        lista_links = [
            'http://threewordphrase.com/report.gif', 'http://threewordphrase.com/reallybig.gif'
        ]
        # import pdb; pdb.set_trace()

        with patch('requests.get', side_effect=lista_mock) as mock_get:
            self.instancia_crawler._baixa_imagens_tirinhas(lista_links)
            self.assertEqual(mock_get.call_count, 2, "O numero de chamada é diferente do esperado")

        path_arquivo1 = './Imagens_Thee_Word_Phrase/report 6508dd5772207c1e56b173cf1679c71a.gif'
        path_arquivo2 = './Imagens_Thee_Word_Phrase/reallybig 9417f7442247e132a527e0a8f4cd6966.gif'

        with open(path_arquivo1, 'rb') as f:
            self.assertEqual(f.read(), b'algum conteudo imagem')
        os.remove(path_arquivo1)
        with open(path_arquivo2, 'rb') as f:
            self.assertEqual(f.read(), b'outro conteudo imagem')
        os.remove(path_arquivo2)

    def test_lanca_exception_quando_url_imagem_nao_e_encontrada(self):
        with patch('requests.get') as mock_get:
            obj_mock = Mock()
            obj_mock.raise_for_status.side_effect=Exception
            mock_get.return_value=obj_mock
            self.assertIsNone(self.instancia_crawler._baixa_imagens_tirinhas(['conteudo_url_invalida']))

    def test_obtem_md5(self):
        conteudo_imagem = b'algum conteudo imagem'
        hash_obtido = self.instancia_crawler._obtem_md5(conteudo_imagem)
        hash_esperado = '6508dd5772207c1e56b173cf1679c71a'
        self.assertEqual(hash_obtido, hash_esperado)

    def test_baixa_imagens(self):
        lista_de_mocks = [
            Mock(text=self.pagina_resultado_busca),
            *[Mock(text=self.pagina01)] * 294,
            *[Mock(content=b'algum conteudo imagem')] * 294
        ]

        with patch('requests.get', side_effect=lista_de_mocks) as mock_get:
            self.instancia_crawler.baixa_imagens()
            self.assertEqual(mock_get.call_count, 589, "O numero de chamada é diferente do esperado")

        path_arquivo1 = './Imagens_Thee_Word_Phrase/report 6508dd5772207c1e56b173cf1679c71a.gif'
        with open(path_arquivo1, 'rb') as f:
            self.assertEqual(f.read(), b'algum conteudo imagem')
        os.remove(path_arquivo1)
