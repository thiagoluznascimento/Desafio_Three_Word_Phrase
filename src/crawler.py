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
        link_archive_imagens = self._parser_slug_archive(pagina_resultado_busca)
        pagina_resultado_busca_archive = self._obtem_html_archive(link_archive_imagens)
        urls_imagens = self._extrai_url_imagens(pagina_resultado_busca_archive)
        listas_paginas_imagens = self._obtem_paginas_imagens(urls_imagens)
        resultado_nomes_imagens = self._extrai_nome_imagens(listas_paginas_imagens)
        # import pdb; pdb.set_trace()
        links_imagens = self._parser_nomes_imagens(resultado_nomes_imagens)
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
        Parsea pagina_resultado_busca etorna o link archive que contém os outros links das imgs
        '''
        soup = BeautifulSoup(pagina_resultado_busca, 'html.parser')
        link = soup.find(href="/archive.htm")
        slug = link.get('href')
        url_archive = self.URL_BUSCA + slug

        return url_archive

    def _obtem_html_archive(self, link_archive_imagens):
        '''
        Faz a requisição e retorna a pág archive_imagens html em text
        '''
        try:
            response = requests.get(link_archive_imagens)
            response.raise_for_status()
            # import pdb; pdb.set_trace()
            logging.info("Requisitando página archive..")
        except Exception as e:
            logging.error(f'Ao requsitar archive - Erro: {str(e)}')

        return response.text

    def _extrai_url_imagens(self, pagina_resultado_busca_archive):
        '''
        Parsea pagina_resultado_busca_archive e retorna a lista de urls que contém o html de cada imagem
        '''
        lista_urls = []
        soup = BeautifulSoup(pagina_resultado_busca_archive, 'html.parser')
        spans_links = soup.select('span.links a')
        for link in spans_links:
            slug = link.get('href')
            url = self.URL_BUSCA + slug
            if url:
                lista_urls.append(url)

        return lista_urls

    def _obtem_paginas_imagens(self, urls_imagens):
        '''
        Parsea urls_imagens e retorna a lista de paginas html
        '''
        lista_paginas = []
        for url in urls_imagens:
            try:
                response = requests.get(url)
                response.raise_for_status()
                logging.info("Aguarde.. carregando páginas HTML")
                lista_paginas.append(response.text)
            except Exception as e:
                logging.error(f'Ao buscar página HTML - Erro: {str(e)}')

        return lista_paginas

    def _extrai_nome_imagens(self, listas_paginas_imagens):
        '''
        Parsea listas_paginas_imagens e retorna uma lista de nomes de cada imagem.gif
        '''
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

            # import pdb; pdb.set_trace()
        return listas_img_tag

    def _parser_nomes_imagens(self, resultado_nomes_imagens):
        '''
        Parsea a lista resultado_nomes_imagens que contém os nomes das imagens e retorna lista_links das imagens
        '''
        lista_links = []
        for nome_img in resultado_nomes_imagens:
            lista_link = self.URL_BUSCA + nome_img
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
