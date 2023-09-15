# import os

import requests
from bs4 import BeautifulSoup


class BucadorTHREEWORDPHRASE:

    URL_BUSCA = "http://threewordphrase.com/"

    def __init__(self, URL_BUSCA):
        self.url = URL_BUSCA

    def baixa_imagens(self):
        pagina_resultado_busca = self._busca_imagens()
        archive_imagens = self._parser_slug_archive(pagina_resultado_busca)
        slugs_imgens = self._obtem_slugs_imagens(archive_imagens)
        imagens = self._parse_slug_imagens(slugs_imgens)
        print(imagens)

    def _busca_imagens(self):
        '''
        Faz a requisição e retorna o resultado html em text
        '''
        response = requests.get(self.URL_BUSCA)
        # if response.status_code == 200:
        #     print("Sucess")
        # else:
        #     print("Falha ao obter html")
        return response.text

    def _parser_slug_archive(self, pagina_resultado_busca):
        '''
        Obtem o link archive que contém os outros links das imgs
        '''
        soup = BeautifulSoup(pagina_resultado_busca, 'html.parser')
        link = soup.find(href="/archive.htm")
        slug = link.get('href')
        url_archive = self.URL_BUSCA + slug
        return url_archive

    def _obtem_slugs_imagens(self, archive_imagens):
        response = requests.get(archive_imagens)
        return response.text

    def _parse_slug_imagens(self, slugs_imgens):
        listas_slugs = []
        soup = BeautifulSoup(slugs_imgens, 'html.parser')
        for link in soup.find_all('a'):
            slug = link.get('href')
            url = self.URL_BUSCA + slug
            if url:
                listas_slugs.append(url)
        return listas_slugs


if __name__ == "__main__":

    crawler = BucadorTHREEWORDPHRASE('URL_BUSCA')
    crawler.baixa_imagens()
