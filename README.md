# Vagas Scraper

Este script Python "_scrapea_" o site "vagas.com.br" para recuperar o número de vagas para certificações específicas e gera um histograma com base nos dados coletados. O script utiliza a biblioteca de solicitações para fazer solicitações HTTP, a biblioteca BeautifulSoup para analisar o conteúdo HTML e a biblioteca matplotlib para plotar o histograma.

## Instalação

1. Clone o repositório em sua máquina local ou baixe o arquivo de script.
2. Instale as dependências necessárias executando o seguinte comando:
    ```
    pip install requests beautifulsoup4 matplotlib
    ```

## Uso

1. Modifique a lista `urls` para incluir as certificações para as quais você deseja raspar vagas de emprego. Cada URL deve corresponder a uma certificação específica.
2. Execute o script usando o seguinte comando:
    ```
    python vagas.py
    ```
3. O script irá raspar as páginas da web, recuperar o número de vagas de emprego e salvar os dados em um arquivo CSV chamado "vagas.csv".
4. Além disso, um histograma será plotado usando os dados coletados e a imagem resultante será salva como "vagas.png".

<p align="center">
  <img src="https://raw.githubusercontent.com/joaopedrolourencoaffonso/vagas-scraper/master/vagas.png" alt="Exemplo de Gráfico" style="width:400px;height:300px;">

## Contribuindo

Contribuições são bem-vindas! Se você tiver sugestões, melhorias ou correções de bugs, sinta-se à vontade para abrir um problema ou enviar uma solicitação de pull.
