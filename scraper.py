import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
import PyPDF2
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Gerador de relatório sobre área de TI');
parser.add_argument('--certs',action="store_true",default=False, help='Gera relatório sobre vagas de emprego por certificados de TI.');
parser.add_argument('--langs',action="store_true",default=False, help='Gera relatório sobre vagas de emprego por linguagens de programação.');
parser.add_argument('--databases',action="store_true",default=False, help='Gera relatório sobre vagas de emprego por software de bancos de dados');
parser.add_argument('--webframeworks',action="store_true",default=False, help='Gera relatório sobre vagas de emprego por framework web');
parser.add_argument('--ferramentas',action="store_true",default=False, help='Gera relatório sobre vagas de emprego por ferramenta de Devops');
parser.add_argument('--estados',action="store_true",default=False, help='Gera relatório sobre vagas de emprego por Estado');
parser.add_argument('--pdf',action="store_true",default=False, help='Gera relatório pdf com base nas opções');
parser.add_argument('--completo',action="store_true",default=False, help='Gera relatório pdf completo, i.e., todas as opções disponíveis');

args = parser.parse_args();


if __name__ == "__main__":
    png_files = [];

    if args.certs or args.completo:
        print("\n---- Extraindo informações sobre certificados ----\n");
        
        from variables import vagas_certs, catho_certs, infojobs_certs

        registro, dicionario = pega_pagina(vagas_certs,"vagas.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "vagas.com", "certificados-vagas","#00cc66","Certificação");

        registro, dicionario = pega_pagina(catho_certs,"catho.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "catho.com", "certificados-catho","#ff0066","Certificação");

        registro, dicionario = pega_pagina(infojobs_certs,"infojobs.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "infojobs.com", "certificados-infojobs","#003399","Certificação");

        png_files = adiciona(png_files,["certificados-vagas.png","certificados-catho.png","certificados-infojobs.png"]);

    if args.langs or args.completo:
        print("\n---- Extraindo informações sobre Linguagens de Programação ----\n");
        
        from variables import vagas_langs, catho_langs, infojobs_langs

        registro, dicionario = pega_pagina(vagas_langs,"vagas.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "vagas.com", "languages-vagas","#00cc66","Linguagem de Programação");

        registro, dicionario = pega_pagina(catho_langs,"catho.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "catho.com", "languages-catho","#ff0066","Linguagem de Programação");

        registro, dicionario = pega_pagina(infojobs_langs,"infojobs.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "infojobs.com", "languages-infojobs","#003399","Linguagem de Programação");

        png_files = adiciona(png_files,["languages-vagas.png","languages-catho.png","languages-infojobs.png"]);

    if args.databases or args.completo:
        print("\n---- Extraindo informações sobre Bancos de Dados ----\n");
        
        from variables import vagas_databases, catho_databases, infojobs_databases

        registro, dicionario = pega_pagina(vagas_databases,"vagas.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "vagas.com", "databases-vagas","#00cc66","Banco de Dados");

        registro, dicionario = pega_pagina(catho_databases,"catho.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "catho.com", "databases-catho","#ff0066","Banco de Dados");

        registro, dicionario = pega_pagina(infojobs_databases,"infojobs.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "infojobs.com", "databases-infojobs","#003399","Banco de Dados");

        png_files = adiciona(png_files,["databases-vagas.png","databases-catho.png","databases-infojobs.png"]);

    if args.webframeworks or args.completo:
        print("\n---- Extraindo informações sobre Frameworks Web ----\n");
        
        from variables import vagas_webframeworks, catho_webframeworks, infojobs_webframeworks

        registro, dicionario = pega_pagina(vagas_webframeworks,"vagas.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "vagas.com", "webframeworks-vagas","#00cc66","Frameworks Web");

        registro, dicionario = pega_pagina(catho_webframeworks,"catho.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "catho.com", "webframeworks-catho","#ff0066","Frameworks Web");

        registro, dicionario = pega_pagina(infojobs_webframeworks,"infojobs.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "infojobs.com", "webframeworks-infojobs","#003399","Frameworks Web");

        png_files = adiciona(png_files,["webframeworks-vagas.png","webframeworks-catho.png","webframeworks-infojobs.png"]);

    if args.ferramentas or args.completo:
        print("\n---- Extraindo informações sobre DevOps ----\n");
        
        from variables import vagas_ferramentas, catho_ferramentas, infojobs_ferramentas

        registro, dicionario = pega_pagina(vagas_ferramentas,"vagas.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "vagas.com", "ferramentas-vagas","#00cc66","Ferramenta de Devops");

        registro, dicionario = pega_pagina(catho_ferramentas,"catho.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "catho.com", "ferramentas-catho","#ff0066","Ferramenta de Devops");

        registro, dicionario = pega_pagina(infojobs_ferramentas,"infojobs.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "infojobs.com", "ferramentas-infojobs","#003399","Ferramenta de Devops");

        png_files = adiciona(png_files,["ferramentas-vagas.png","ferramentas-catho.png","ferramentas-infojobs.png"]);

    if args.estados or args.completo:
        print("\n---- Extraindo informações sobre Estados ----\n");
        
        from variables import estados_vagas, estados_infojobs, estados_catho

        registro, dicionario_1 = pega_pagina(estados_vagas,"vagas.com");
        registra_no_csv(registro);
        plot_histogram(dicionario_1, "vagas.com", "estado-vagas","#00cc66","Estados");
        
        registro, dicionario_2 = pega_pagina(estados_catho,"catho.com");
        registra_no_csv(registro);
        plot_histogram(dicionario_2, "catho.com", "estado-catho","#ff0066","Estados");

        registro, dicionario_3 = pega_pagina(estados_infojobs,"infojobs.com");
        registra_no_csv(registro);
        plot_histogram(dicionario_3, "infojobs.com", "estado-infojobs","#003399","Estados");

        total = soma_dicionarios(dicionario_1, dicionario_2, dicionario_3);
        plot_histogram(total, "total", "total-estados","#ff0000","Estados");

        dicionario_de_regioes = soma_regioes(total);
        plot_donut_graph(dicionario_de_regioes,'total-regiao','Vagas por Região')

        png_files = adiciona(png_files,["estado-vagas.png","estado-catho.png","estado-infojobs.png", "total-estados.png",'total-regiao.png']);

    if args.completo or args.pdf:
        from variables import arquivos_pdf
        carrossel(png_files,f"{arquivos_pdf}carrossel-temp.pdf");
        combine_pdfs([f"{arquivos_pdf}Capa.pdf",f"{arquivos_pdf}carrossel-temp.pdf",f"{arquivos_pdf}fim.pdf"],f"{arquivos_pdf}carrossel.pdf")