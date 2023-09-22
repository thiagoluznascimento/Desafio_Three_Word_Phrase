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
        pagina_archive_imagens = self._parser_slug_archive(pagina_resultado_busca)
        paginas_resultado_busca_archive = self._obtem_slugs_archive(pagina_archive_imagens)
        url_imagens = self._parse_slug_imagens(paginas_resultado_busca_archive)
        listas_paginas_imagens = self._obtem_paginas_imagens(url_imagens)
        resultado_slugs_imgs = self._extrai_link_imagens(listas_paginas_imagens)
        links_imagens = self._parser_slugs_imagens(resultado_slugs_imgs)
        self._baixa_arquivos_gif(links_imagens)
        logging.info("Finalização do download das imagens!")

    def _busca_imagens(self):
        '''
        Faz a requisição e retorna o resultado html em text da primeira página
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
        Obtem e retorna o link archive que contém os outros links das imgs
        '''
        soup = BeautifulSoup(pagina_resultado_busca, 'html.parser')
        link = soup.find(href="/archive.htm")
        slug = link.get('href')
        url_archive = self.URL_BUSCA + slug

        return url_archive

    def _obtem_slugs_archive(self, pagina_archive_imagens):
        '''
        Faz a requisição e retorna a pág archive_imagens html em text
        '''
        try:
            response = requests.get(pagina_archive_imagens)
            response.raise_for_status()
            logging.info("Requisitando página archive..")
        except Exception as e:
            logging.error(f'Ao requsitar archive - Erro: {str(e)}')

        return response.text

    def _parse_slug_imagens(self, paginas_resultado_busca_archive):
        listas_slugs = []
        soup = BeautifulSoup(paginas_resultado_busca_archive, 'html.parser')
        spans_links = soup.select('span.links a')
        for link in spans_links:
            slug = link.get('href')
            url = self.URL_BUSCA + slug
            if url:
                listas_slugs.append(url)

        return listas_slugs

    def _obtem_paginas_imagens(self, url_imagens):
        lista_paginas = []
        for url in url_imagens:
            try:
                response = requests.get(url)
                response.raise_for_status()
                logging.info("Aguarde.. carregando páginas HTML")
                lista_paginas.append(response.text)
            except Exception as e:
                logging.error(f'Ao buscar página HTML - Erro: {str(e)}')

        return lista_paginas

    def _extrai_link_imagens(self, listas_paginas_imagens):
        listas_img_tag = []
        for pagina in listas_paginas_imagens:
            soup = BeautifulSoup(pagina, 'html.parser')
            tabela = soup.find('table', {'width': '403', 'border': '0'})
            if tabela:
                imagens = tabela.find_all('img')
                for imagem in imagens:
                    src = imagem.get('src')
                    if src:
                        listas_img_tag.append(src)

        return listas_img_tag

    def _parser_slugs_imagens(self, resultado_slugs_imgs):
        lista_links = []
        for slug_img in resultado_slugs_imgs:
            lista_link = self.URL_BUSCA + slug_img
            lista_links.append(lista_link)

        return lista_links

    def _baixa_arquivos_gif(self, links_imagens):
        if not os.path.exists('imagens_gif'):
            os.makedirs('imagens_gif')
            logging.info('Pasta criada com sucesso!')
        logging.info("Iníciando download das imagens..")
        caminho_arquivo = os.path.join('imagens_gif')
        for url_gif in links_imagens:
            try:
                response = requests.get(url_gif)
                response.raise_for_status()
                nome_arquivo = self._obtem_md5(response.content) + ".gif"
                caminho_completo = os.path.join(caminho_arquivo, nome_arquivo)
                if not os.path.exists(caminho_completo):
                    with open(caminho_arquivo + '/' + nome_arquivo, 'wb') as f:
                        f.write(response.content)
                        logging.info(f'Imagem com Hash-MD5: {nome_arquivo} salva com sucesso!')
                else:
                    logging.info(f'Arquivo {nome_arquivo} já existe. Ignorando o download.')
            except Exception as e:
                logging.error(f'Ao baixar imagem - Erro: {str(e)}')

    def _obtem_md5(self, conteudo_imagem):
        md5_hash = hashlib.md5(conteudo_imagem).hexdigest()
        return md5_hash
