import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
import PyPDF2
import argparse
from tqdm import tqdm

def carrossel(png_files, output_file):
    from variables import diretorio_de_imagens
    
    c = canvas.Canvas(output_file, pagesize=landscape(letter))
    width, height = letter;

    for png_file in png_files:
        c.drawImage(f"{diretorio_de_imagens}{png_file}", 0.15*width, 0.15*height, width, 0.75*width)
        c.showPage()

    c.save()


def plot_histogram(data, site, figura,color,caracteristica):
    from variables import diretorio_de_imagens
    
    names = list(data.keys())
    values = list(data.values())

    values = list(map(int, values))  # Convert values to integers

    # Ordenando os valores
    sorted_indices = sorted(range(len(values)), key=lambda i: values[i])
    sorted_names = [names[i] for i in sorted_indices]
    sorted_values = [values[i] for i in sorted_indices]
    
    plt.bar(range(len(data)), sorted_values, tick_label=sorted_names,color=color)
    plt.xticks(rotation=90)
    plt.ylim(0, (1.1)*max(values));
    
    # Titulo dos eixos e do gráfico
    plt.ylabel('Nº de vagas') 
    plt.title(f"Vagas por {caracteristica} no '{site}'")

    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.savefig(f"{diretorio_de_imagens}{figura}.png")
    plt.close();

def parse_catho_com(url):
    # GET a página
    response = requests.get(url)

    if response.status_code == 200:
        # Parseando a página
        soup = BeautifulSoup(response.content, "html.parser")

        # Cada página tem único h1 onde tem o número de vagas encontradas
        h1_elements = soup.find_all("h1")

        # Retorna o número de vagas
        for h1 in h1_elements:
            return h1.text.split(" ")[0]
    else:
        print("Failed to retrieve the web page. Error code:", response.status_code)
        
def parse_vagas_com(url):
    # GET a página
    response = requests.get(url)

    # Checando se o get foi bem sucedido
    if response.status_code == 200:
        # Parseando a página
        soup = BeautifulSoup(response.content, "html.parser")

        # Cada página tem único h1 onde tem o número de vagas encontradas
        h1_elements = soup.find_all("h1")

        # Retorna o número de vagas
        for h1 in h1_elements:
            return h1.text.split(" ")[0]
    else:
        print("Failed to retrieve the web page. Error code:", response.status_code)

def parse_info_jobs(url):
    response = requests.get(url);
    soup = BeautifulSoup(response.content, 'html.parser')
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    if meta_tag:
        description = meta_tag.get('content')
        temp = description.split('Vagas de Emprego')[0];
        return temp
    else:
        return None

def pega_pagina(catalogo,site):
    total_urls = len(catalogo);
    dicionario = {};
    i = 0;

    progress_bar = tqdm(total=total_urls, unit='%', ncols=80)

    for elemento in catalogo:
        if site == "catho.com":
            temp = parse_catho_com(catalogo[elemento]);
            progress_bar.set_description(f'Catho.com');

        if site == "vagas.com":
            temp = parse_vagas_com(catalogo[elemento]);
            progress_bar.set_description(f'Vagas.com');

        if site == "infojobs.com":
            temp = parse_info_jobs(catalogo[elemento]);
            progress_bar.set_description(f'infojobs.com');
            
        if temp != None and temp != 'Ops!' and temp != "":
            temp = temp.replace(".","");
            dicionario[elemento] = int(temp);

        i+=1;
        
        progress_bar.update(1);

    progress_bar.close();

    registro = ""

    for key, value in dicionario.items():
        if site == "catho.com":
            registro = registro + f"{datetime.now()},catho.com,{key}, {value}\n";
        
        if site == "vagas.com":
            registro = registro + f"{datetime.now()},vagas.com,{key}, {value}\n";
        
        if site == "infojobs.com":
            registro = registro + f"{datetime.now()},infojobs.com,{key}, {value}\n";

    return registro, dicionario

def registra_no_csv(text):
    file = open("registro.csv","a");
    file.write(text);
    file.close();


def combine_pdfs(input_files, output_file):
    pdf_writer = PyPDF2.PdfWriter()

    # Iterate through each input PDF file
    for file in input_files:
        with open(file, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            # Merge each page of the input PDF into the output PDF writer
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)

    # Write the combined PDF to the output file
    with open(output_file, 'wb') as output:
        pdf_writer.write(output)

    #print(f"Combined PDF files into '{output_file}'.")

def adiciona(png_files, lista):
    png_files.append(lista[0]);
    png_files.append(lista[1]);
    png_files.append(lista[2]);

    return png_files


parser = argparse.ArgumentParser(description='Gerador de relatório sobre área de TI');
parser.add_argument('--certs',action="store_true",default=False, help='Gera relatório sobre certificados');
parser.add_argument('--langs',action="store_true",default=False, help='Gera relatório sobre linguagens');
parser.add_argument('--databases',action="store_true",default=False, help='Gera relatório sobre bancos de dados');
parser.add_argument('--webframeworks',action="store_true",default=False, help='Gera relatório sobre frameworks web');
parser.add_argument('--ferramentas',action="store_true",default=False, help='Gera relatório sobre ferramentas de Devops');
parser.add_argument('--completo',action="store_true",default=False, help='Gera relatório pdf completo');

args = parser.parse_args();


if __name__ == "__main__":
    png_files = [];

    if args.certs:
        print("---- Extraindo informações sobre certificados ----\n");
        
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

    if args.langs:
        print("---- Extraindo informações sobre Linguagens de Programação ----\n");
        
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

    if args.databases:
        print("---- Extraindo informações sobre Bancos de Dados ----\n");
        
        from variables import vagas_databases, catho_databases, infojobs_databases

        registro, dicionario = pega_pagina(vagas_databases,"catho.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "vagas.com", "databases-vagas","#00cc66","Banco de Dados");

        registro, dicionario = pega_pagina(catho_databases,"catho.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "catho.com", "databases-catho","#ff0066","Banco de Dados");

        registro, dicionario = pega_pagina(infojobs_databases,"infojobs.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "infojobs.com", "databases-infojobs","#003399","Banco de Dados");

        png_files = adiciona(png_files,["databases-vagas.png","databases-catho.png","databases-infojobs.png"]);

    if args.webframeworks:
        print("---- Extraindo informações sobre Frameworks Web ----\n");
        
        from variables import vagas_webframeworks, catho_webframeworks, infojobs_webframeworks

        registro, dicionario = pega_pagina(vagas_webframeworks,"catho.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "vagas.com", "webframeworks-vagas","#00cc66","Frameworks Web");

        registro, dicionario = pega_pagina(catho_webframeworks,"catho.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "catho.com", "webframeworks-catho","#ff0066","Frameworks Web");

        registro, dicionario = pega_pagina(infojobs_webframeworks,"infojobs.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "infojobs.com", "webframeworks-infojobs","#003399","Frameworks Web");

        png_files = adiciona(png_files,["webframeworks-vagas.png","webframeworks-catho.png","webframeworks-infojobs.png"]);

    if args.ferramentas:
        print("---- Extraindo informações sobre DevOps ----\n");
        
        from variables import vagas_ferramentas, catho_ferramentas, infojobs_ferramentas

        registro, dicionario = pega_pagina(vagas_ferramentas,"catho.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "vagas.com", "ferramentas-vagas","#00cc66","Ferramentas de Devops");

        registro, dicionario = pega_pagina(catho_ferramentas,"catho.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "catho.com", "ferramentas-catho","#ff0066","Ferramentas de Devops");

        registro, dicionario = pega_pagina(infojobs_ferramentas,"infojobs.com");
        registra_no_csv(registro);
        plot_histogram(dicionario, "infojobs.com", "ferramentas-infojobs","#003399","Ferramentas de Devops");

        png_files = adiciona(png_files,["ferramentas-vagas.png","ferramentas-catho.png","ferramentas-infojobs.png"]);

    if args.completo:
        from variables import arquivos_pdf
        carrossel(png_files,f"{arquivos_pdf}carrossel-temp.pdf");
        combine_pdfs([f"{arquivos_pdf}Capa.pdf",f"{arquivos_pdf}carrossel-temp.pdf",f"{arquivos_pdf}fim.pdf"],f"{arquivos_pdf}carrossel.pdf")