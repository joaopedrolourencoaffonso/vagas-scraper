import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from tqdm import tqdm
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
import PyPDF2

def carrossel(png_files, output_file):
    from variables import diretorio_de_imagens
    
    c = canvas.Canvas(output_file, pagesize=landscape(letter))
    width, height = letter;

    for png_file in png_files:
        c.drawImage(f"{diretorio_de_imagens}{png_file}", 0.15*width, 0.15*height, width, 0.75*width)
        c.showPage()

    c.save()

def nada_encontrado(site, figura,caracteristica):
    from variables import diretorio_de_imagens
    
    plt.figure(figsize=(8, 4))
    plt.text(0.5, 0.5, f"Sem vagas envolvendo {caracteristica} no {site}", ha='center', va='center', fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f"{diretorio_de_imagens}{figura}.png")
    plt.close()

def plot_histogram(data, site, figura,color,caracteristica):
    if not data:
        nada_encontrado(site, figura,caracteristica);
        return

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


def plot_donut_graph(data,figura,titulo):
    from variables import diretorio_de_imagens
    labels = list(data.keys())
    values = list(data.values())

    fig, ax = plt.subplots()

    # Plotando o gráfico
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})

    # Circulo branco no centro para criar a impressão de um 'donut'
    center_circle = plt.Circle((0, 0), 0.7, fc='white')
    fig.gca().add_artist(center_circle)

    # Ajustando 'aspect ratio'
    ax.set_aspect('equal')

    # Título do gráfico
    ax.set_title(titulo)

    # Salvando o gráfico
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
        
def soma_regioes(dicionario):
    dicionario_de_regioes = {};
    dicionario_de_regioes['Sul'] = dicionario['PR'] + dicionario['SC'] + dicionario['RS'];
    dicionario_de_regioes['Sudeste'] = dicionario['RJ'] + dicionario['SP'] + dicionario['ES'] + dicionario['MG'];
    dicionario_de_regioes['Centro-Oeste'] = dicionario['MT'] + dicionario['MS'] + dicionario['GO'] + dicionario['DF'];
    dicionario_de_regioes['Norte'] = dicionario['AC'] + dicionario['RO'] + dicionario['AM'] + dicionario['TO'] + dicionario['PA'] + dicionario['AP'] + dicionario['RR'];
    dicionario_de_regioes['Nordeste'] = dicionario['MA'] + dicionario['PI'] + dicionario['CE'] + dicionario['RN'] + dicionario['PB'] + dicionario['PE'] + dicionario['AL'] + dicionario['SE'] + dicionario['BH'];

    return dicionario_de_regioes

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
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    span_tag = soup.find('span', class_='small text-medium')
    if span_tag:
        number = span_tag.text.strip()
        return number
    else:
        return None

def parse_gupy(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    p_element = soup.find('p', attrs={'data-testid': 'result-total-text'});
    # Check if the <p> element was found
    if p_element:
        result_text = p_element.get_text()
        result = result_text.split(" ")[0];
        return result
        
    else:
        return None;

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

        if site == "gupy.io":
            temp = parse_gupy(catalogo[elemento]);
            progress_bar.set_description(f'gupy.io');
            
        if temp != None and temp != 'Ops!' and temp != '':
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
        
        if site == "gupy.io":
            registro = registro + f"{datetime.now()},gupy.io,{key}, {value}\n";

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
    for item in lista:
        png_files.append(item);
    
    return png_files

def soma_dicionarios(*dicionarios):
    result = {}
    for dicionario in dicionarios:
        for key, value in dicionario.items():
            result[key] = result.get(key, 0) + value
    return result