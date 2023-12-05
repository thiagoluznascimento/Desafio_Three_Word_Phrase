# Desafio THREE WORD PHRASE

Segundo desafio apresentado ao Justiça Fácil.

## Descrição do desafio
O objetivo do desafio é construir um programa que:
1. Baixe todas as tirinhas do site threewordphrase.com;
2. Salve as imagens localmente;
3. O nome de cada arquivo deve ser o MD5 da tirinha (ex.: o nome do arquivo referente ao quadrinho threewordphrase.com/parkour.htm será `164481b21c0e8a25ca3e27e890375d1e.gif)`;
4. Numa segunda vez que o programa for rodado, deve haver um verificador para que, caso o arquivo já exista, ele não seja salvo/sobrescrito localmente;
5. O programa deve ter tratamento de erros e exceções e não deve ser encerrado prematuramente em caso de exceções não criticas;
6. O programa deve ser feito utilizando o paradigma Programação Orientada a Objetos;
7. O programa deve ter testes unitários;
8. Cada ação executada pelo programa deve emitir um log no terminal (ex.: início da execução do programa, conclusão de um download especifico, falha em um download especifico e fim da execução).

## Funcionalidades do programa
* Faz a requisição em /archive.htm
* Parsea e faz requisição em cada link/página contida dentro de /archive.htm
* Baixa as imagens de cada página requisitada

## Preparação do ambiente de desenvolvimento
Para executar o projeto é necessário ter o Python 3.7 instalado e seguir os passos:

1. Clonar o repositório:
``` bash
git clone https://github.com/thiagoluznascimento/Desafio_Three_Word_Phrase.git
```

2. Crie um ambiente virtual
```bash
virtualenv venv -p python3.7
```
3. Comando para ativar o ambiente virtual
```bash
source venv/bin/activate  
```

4. Instale os requirements.txt
```bash
pip install -r requirements.txt
```

## Como executar o programa
5. Comando para executar o projeto.
```bash
python run.py
```

## Como executar os testes
6. Comando para executar os testes de modo verbose.
```bash
pytest -v tests/test_crawler.py
```
## Execute o Flake8
7. Comando para executar o flake8.
```bash
flake8 src/crawler.py   
```

## Dificuldades:
Uma das dificuldades que tive, foi na obtenção das urls finais que contém as imagens. Pois a estratégia que eu havia traçado, não estava de certa forma correta. Eu estava pegando todos os atributos de href(`href="report.htm"`) e fazendo um `.replace('.htm', '.gif')`. Com o auxílio prestado no canal dev-aprendisado no programa slack foi me informado que, não podemos confiar no nome da imagem como sendo o nome do html, pois pode não ser igual. Pode não ser `.gif` e o link da imagem pode mudar. 
A segunda dificuldade que tive, foi em relação aos testes..
Especificamente ao testar o método, `def _extrai_links_imagens(self)`
ao debugar mais a fundo o meu código de testes, percebi que o meu método, `def test_extrai_links_imagens` não estava me retornando a lista de links das imagens. Exemplo, não me retornava:`['http://threewordphrase.com/report.gif', 'http://threewordphrase.com/reallybig.gif', 'http://threewordphrase.com/serial.gif', n... ]`. Foi onde tive novamente o auxílio dos colegas de trabalho onde eles me pediram para que estudasse sobre o soupsieve que seria a melhor opção para esse caso.
E por fim tive um pouco de dúvida ao baixar todas as imagens. Onde, na página archive, me mostra 294 imagens, menos 2 que estão com erro 404, Logo, teriam que ter 292 imagens, mas ao verificar as imagens dentro pasta percebi que tinham 294 imagens. Então ao analisar mais a fundo, percebi que a página threewordphrase.com/sasquatch.htm contém três imagens sendo assim, completando as 294 imagens.