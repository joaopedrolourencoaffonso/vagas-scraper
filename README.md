# vagas-scraper

<p align="center"><a href="https://joaopedrolourencoaffonso.github.io/vagas-scraper/"><img src="https://github.com/joaopedrolourencoaffonso/vagas-scraper/blob/master/logo.jpeg?raw=true" width="250" height="250"></a></p>

Este script Python foi desenvolvido para web scraping de sites de empregos e geração de um relatório sobre o número de vagas abertas relacionadas a diferentes competências na área de TI. O script utiliza várias bibliotecas, incluindo `requests`, `BeautifulSoup`, `matplotlib`, `reportlab`, `PyPDF2`, `argparse` e `tqdm`.

## Características

- Extrai informações de sites de empregos como vagas.com, catho.com e infojobs.com.
- Gera histogramas para visualizar o número de postos de trabalho para diferentes competências.
- Suporta as seguintes competências: Certificados, Linguagens de Programação, Bases de Dados, Web Frameworks e Ferramentas de DevOps.
- Gera histogramas individuais e os combina em um relatório PDF abrangente.

## Uso

Para usar o script, siga estas etapas:

1. Certifique-se de que as bibliotecas necessárias estejam instaladas. Você pode instalá-los usando `pip`:
    ```
    pip install requests beautifulsoup4 matplotlib reportlab pypdf2 argparse tqdm
    ```

2. Personalize o comportamento do script modificando os argumentos da linha de comando. As opções disponíveis incluem `--certs`, `--langs`, `--databases`, `--webframeworks`, `--ferramentas`,`--estados`,`--PDF` e `--completo`. Use essas opções para gerar relatórios para competências específicas ou gerar um relatório completo em PDF.

3. Execute o script:
    ```bash
    # Gera arquivos PNG contendo gráficos sobre certificações e bancos de dados mais requisitados
    python scraper.py --certs --databases
    # Gera um relatório PDF contendo os gráficos de linguagem de programação e framework web
    python scraper.py --langs --webframeworks --pdf
    # Gera um relatório PDF contendo todas as opções
    python scraper.py --completo
    ```

4. O script irá extrair informações de sites de empregos, gerar histogramas e armazenar os resultados em um arquivo CSV chamado `registro.csv`. Histogramas individuais serão salvos como arquivos PNG.

5. Se a opção `--completo` for usada, o script combinará os histogramas gerados em um relatório PDF abrangente denominado `carrossel.pdf`.

6. Abaixo, alguns exemplos de histogramas, você pode conferir um exemplo de [relatório PDF aqui](https://github.com/joaopedrolourencoaffonso/vagas-scraper/blob/master/PDFs/carrossel.pdf).

<p align="center">
  <img src="https://raw.githubusercontent.com/joaopedrolourencoaffonso/vagas-scraper/master/graficos/certificados-vagas.png" alt="Vagas por certificado no 'vagas'" style="width:400px;height:300px;">
    
<p align="center">
  <img src="https://raw.githubusercontent.com/joaopedrolourencoaffonso/vagas-scraper/master/graficos/certificados-catho.png" alt="Vagas por certificado na Catho" style="width:400px;height:300px;">

<p align="center">
  <img src="https://raw.githubusercontent.com/joaopedrolourencoaffonso/vagas-scraper/master/graficos/certificados-infojobs.png" alt="Vagas por linguagem no 'vagas'" style="width:400px;height:300px;">

## Aviso

Observe que os resultados fornecidos por este script não são 100% precisos e devem ser tratados como uma visão geral do mercado de trabalho na respectiva área. A precisão das informações depende da confiabilidade e consistência dos sites de emprego que estão sendo copiados.

Sinta-se à vontade para personalizar o roteiro de acordo com seus requisitos específicos e competências de interesse.

## Contribuindo

Contribuições são bem-vindas! Se você tiver sugestões, melhorias ou correções de bugs, sinta-se à vontade para abrir um problema ou enviar uma solicitação de pull.
