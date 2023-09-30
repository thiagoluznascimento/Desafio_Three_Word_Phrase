# Desafio THREE WORD PHRASE

Segundo desafio apresentado ao Justiça Fácil.

## Descrição do desafio
O objetivo do desafio é construir um programa que:
1. Baixe todas as tirinhas do site threewordphrase.com;
2. Salve as imagens localmente;
3. O nome de cada arquivo deve ser o MD5 da tirinha (ex.: o nome do arquivo referente ao quadrinho threewordphrase.com/parkour.htm será `164481b21c0e8a25ca3e27e890375d1e.png)`;
4. Numa segunda vez que o programa for rodado, deve haver um verificador para que, caso o arquivo já exista, ele não seja salvo/sobrescrito localmente;
5. O programa deve ter tratamento de erros e exceções e não deve ser encerrado prematuramente em caso de exceções não criticas;
6. O programa deve ser feito utilizando o paradigma Programação Orientada a Objetos;
7. O programa deve ter testes unitários;
8. Cada ação executada pelo programa deve emitir um log no terminal (ex.: início da execução do programa, conclusão de um download especifico, falha em um download especifico e fim da execução).

## Funcionalidades do programa
* Faz requisição no site threewordphrase.com;
* Faz a requisição em /archive.htm
* Parsea e faz requisição em cada link/página contida dentro de /archive.htm
* Baixa as imagens de cada página requisitada

## Preparação do ambiente de desenvolvimento
Para executar o projeto é necessário ter o Python instalado e seguir os passos:

1. Clonar o repositório:
``` bash
git clone https://github.com/thiagoluznascimento/Desafio_Three_Word_Phrase.git
```

2. Instalar as seguintes bibliotecas:
```bash
pip install requests
pip install beautifulsoup4
```

3. Crie um ambiente virtual
```bash
virtualenv venv -p python3.7
```

4. Instale os requirements.txt
```bash
pip install -r requirements/dev.txt4
```

## Como executar o programa
5. Comando para executar o projeto.
```bash
python run.py
```

## Como executar os testes
6. Comando para executar os testes.
```bash
pytest -v tests/test_crawler.py
```

## Dificuldades:
Uma das dificuldades que tive, foi na obtenção das urls finais que contém as imagens. Pois a estratégia que eu havia traçado, eu estava pegando todos os atributos de href(`href="report.htm"`) e fazendo um `.replace('.htm', '.gif')`, esta forma "não estária correto", pois, não podemos confiar no nome da imagem como ser o nome do html, pois pode não ser igual. Pode não ser `.gif`. 
Outra dificuldade que tive, foi em relação aos testes..
Especificamente ao testar o método, `def _extrai_nome_imagens(self)`
ao debugar mais a fundo o meu código de testes, percebi que o meu método, `def test_extrai_nome_imagens(self)` não estava me retornando a lista de nomes das imagens explo, não me retornava:`['report.gif', 'reallybig.gif', 'serial.gif', n... ]`. como solução ultilizei Regex para parsear a lista de páginas html que o método recebe. 


