import logging
import hashlib
import os

import requests
from bs4 import BeautifulSoup


class BuscadorTheeWordPhrase:

    URL_BUSCA = "http://threewordphrase.com/archive.htm"
    URL_PRINCIPAL = "http://threewordphrase.com/"
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def baixa_imagens(self):
        pagina_resultado_busca_archive = self._obtem_pagina_archive(self.URL_BUSCA)
        urls_imagens = self._extrai_url_imagens(pagina_resultado_busca_archive)
        lista_paginas_imagens = self._obtem_paginas_imagens(urls_imagens)
        links_imagens = self._extrai_links_imagens(lista_paginas_imagens)
        self._baixa_imagens_tirinhas(links_imagens)
        logging.info("Finalização do download das imagens!")

    def _obtem_pagina_archive(self, URL_BUSCA):
        '''
        Faz requisição e retorna a pág archive html contendo todos os links de cada página
        '''
        try:
            response = requests.get(URL_BUSCA)
            response.raise_for_status()
            logging.info("Requisitando página archive..")
        except Exception as e:
            logging.error(f'Ao requsitar archive - Erro: {str(e)}')

        return response.text

    def _extrai_url_imagens(self, pagina_resultado_busca_archive):
        '''
        Parsea pagina_archive e retorna a lista de urls
        '''
        lista_urls = []
        soup = BeautifulSoup(pagina_resultado_busca_archive, 'html.parser')
        spans_links = soup.select('span.links a')
        for link in spans_links:
            slug_completo = link.get('href')
            slug = slug_completo.split("/")[-1]
            url = self.URL_PRINCIPAL + slug
            lista_urls.append(url)

        return lista_urls

    def _obtem_paginas_imagens(self, urls_imagens):
        '''
        Parsea urls_imagens e retorna a lista de paginas html de cada imagem
        '''
        lista_paginas = []
        for indice, url in enumerate(urls_imagens):
            try:
                response = requests.get(url)
                response.raise_for_status()
                logging.info(f"Aguarde.. carregando página HTML indice: {indice}")
                lista_paginas.append(response.text)
            except Exception as e:
                logging.error(f'Ao buscar página HTML - Erro: {str(e)}')

        return lista_paginas

    def _extrai_links_imagens(self, lista_paginas_imagens):
        '''
        Parsea lista_paginas_imagens e retorna uma lista de links das imagens
        '''
        listas_img_tag = []
        lista_links = []
        for pagina in lista_paginas_imagens:
            soup = BeautifulSoup(pagina, 'html5lib')
            tabela = soup.select_one('div[align="center"] > table + table')
            imagens = tabela.find_all('img')
            for imagem in imagens:
                src = imagem.get('src')
                nome_img = src.split("/")
                listas_img_tag.append(nome_img[-1])
        for nome_img in listas_img_tag:
            link = self.URL_PRINCIPAL + nome_img
            lista_links.append(link)

        return lista_links

    def _baixa_imagens_tirinhas(self, links_imagens):
        if not os.path.exists('Imagens_Thee_Word_Phrase'):
            os.makedirs('Imagens_Thee_Word_Phrase')
            logging.info('Pasta criada com sucesso!')
        logging.info("Iníciando download das imagens..")
        caminho_arquivo = os.path.join('Imagens_Thee_Word_Phrase')
        for url_gif in links_imagens:
            try:
                response = requests.get(url_gif)
                response.raise_for_status()
                nome_imagem = url_gif.split("/")[-1]
                nome_sem_extensao = nome_imagem.split(".")[0]
                extensão = '.' + nome_imagem.split('.')[-1]
                nome_hash = self._obtem_md5(response.content)
                nome_arquivo = '%s %s %s' % (nome_sem_extensao, nome_hash, extensão)
                caminho_completo = os.path.join(caminho_arquivo, nome_arquivo)
                if not os.path.exists(caminho_completo):
                    with open(caminho_arquivo + '/' + nome_arquivo, 'wb') as f:
                        f.write(response.content)
                        logging.info(
                            f'Nome Da imagem: {nome_sem_extensao} com Hash-MD5: '
                            f'{nome_hash} salva com sucesso!'
                        )
                else:
                    logging.info(f'Arquivo {nome_arquivo} já existe. Ignorando o download.')
            except Exception as e:
                logging.error(f'Ao baixar imagem - Erro: {str(e)}')

    def _obtem_md5(self, conteudo_imagem):
        md5_hash = hashlib.md5(conteudo_imagem).hexdigest()
        return md5_hash
