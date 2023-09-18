import logging

import hashlib
import os

import requests
from bs4 import BeautifulSoup


class BucadorTHREEWORDPHRASE:

    URL_BUSCA = "http://threewordphrase.com/"

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self, URL_BUSCA):
        self.url = URL_BUSCA

    def baixa_imagens(self):
        pagina_resultado_busca = self._busca_imagens()
        archive_imagens = self._parser_slug_archive(pagina_resultado_busca)
        slugs_imgens = self._obtem_slugs_imagens(archive_imagens)
        url_imagens = self._parse_slug_imagens(slugs_imgens)
        url_gif_list = self._obtem_url_gif(url_imagens)
        self._baixa_arquivos_gif(url_gif_list)
        logging.info("Finalização do downloader das imagens!")

    def _busca_imagens(self):
        '''
        Faz a requisição e retorna o resultado html em text
        '''
        try:
            response = requests.get(self.URL_BUSCA)
            response.raise_for_status() # Verifica erros HTTP
            logging.info("Iníciando buscas das imagens..")
        except Exception as e:
            logging.error(f'Ao buscar imagem - Erro: {str(e)}')
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
        spans_links = soup.select('span.links a')
        for link in spans_links:
            slug = link.get('href')
            url = self.URL_BUSCA + slug
            if url:
                listas_slugs.append(url)
        return listas_slugs

    def _obtem_url_gif(self, url_imagens):
        urls = url_imagens
        listas_url = []
        for i in range(len(urls)):
            urls[i] = urls[i].replace('.htm', '.gif')
        for url in urls:
            if url:
                listas_url.append(url)
        return listas_url

    def _baixa_arquivos_gif(self, url_gif_list):
        if not os.path.exists('imagens_gif'):
            os.makedirs('imagens_gif')
        caminho_arquivo = os.path.join('imagens_gif')
        for i, url_gif in enumerate(url_gif_list):
            try:
                response = requests.get(url_gif)
                response.raise_for_status()
                nome_arquivo = self._obtem_md5(response.content) + ".gif"
                with open(caminho_arquivo + "/" + nome_arquivo, 'wb') as f:
                    f.write(response.content)
                    logging.info(f'Imagem com Hash-MD5: {nome_arquivo} salva com sucesso!')
            except Exception as e:
                logging.error(f'Ao baixar imagem - Erro: {str(e)}')

    def _obtem_md5(self, conteudo_imagem):
        md5_hash = hashlib.md5(conteudo_imagem).hexdigest()
        return md5_hash
