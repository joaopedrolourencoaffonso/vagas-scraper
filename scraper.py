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
        return description
    else:
        return None

def pega_infojobs_com(catalogo):
    total_urls = len(catalogo);
    dicionario = {};
    i = 0;
    
    #print("====Infojobs.com====");
    progress_bar = tqdm(total=total_urls, unit='%', ncols=80)

    for elemento in catalogo:
        x = parse_info_jobs(catalogo[elemento])
        
        temp = x.split('Vagas de Emprego')[0];
        
        if temp != None and temp != 'Ops!' and temp != "":
            temp = temp.replace(".","");
            dicionario[elemento] = int(temp);

        i+=1;
        
        #print(f"Status: {format((100*i)/total_urls, '.2f')}%", end='\r')
        progress_bar.set_description(f'Infojobs.com: {i}/{total_urls}');
        progress_bar.update(1);

    progress_bar.close();

    temp = ""

    for key, value in dicionario.items():
        temp = temp + f"{datetime.now()},infojobs.com, {key}, {value}\n";

    return temp, dicionario

def pega_vagas_com(catalogo):
    total_urls = len(catalogo);
    dicionario = {};
    i = 0;

    #print("====Vagas.com====");
    progress_bar = tqdm(total=total_urls, unit='%', ncols=80)

    for elemento in catalogo:
        temp = parse_vagas_com(catalogo[elemento]);
        
        if temp != None and temp != 'Ops!' and temp != "":
            temp = temp.replace(".","");
            dicionario[elemento]=int(temp);

        i+=1;
        
        #print(f"Status: {format((100*i)/total_urls, '.2f')}%", end='\r')
        progress_bar.set_description(f'Vagas.com: {i}/{total_urls}');
        progress_bar.update(1);

    progress_bar.close();

    registro = ""

    for key, value in dicionario.items():
        registro = registro + f"{datetime.now()},vagas.com,{key}, {value}\n";

    return registro, dicionario

def pega_catho_com(catalogo):
    total_urls = len(catalogo);
    dicionario = {};
    i = 0;

    #print("====Catho.com====");
    progress_bar = tqdm(total=total_urls, unit='%', ncols=80)

    for elemento in catalogo:
        temp = parse_catho_com(catalogo[elemento]);
        
        if temp != None and temp != 'Ops!' and temp != "":
            temp = temp.replace(".","");
            dicionario[elemento]=int(temp);

        i+=1;
        
        #print(f"Status: {format((100*i)/total_urls, '.2f')}%", end='\r')
        progress_bar.set_description(f'Catho.com: {i}/{total_urls}');
        progress_bar.update(1);

    progress_bar.close();

    registro = ""

    for key, value in dicionario.items():
        registro = registro + f"{datetime.now()},catho.com,{key}, {value}\n";

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



parser = argparse.ArgumentParser(description='Gerador de relatório sobre área de TI');
parser.add_argument('--certs',action="store_true",default=False, help='Gera relatório sobre certificados');
parser.add_argument('--langs',action="store_true",default=False, help='Gera relatório sobre linguagens');
parser.add_argument('--completo',action="store_true",default=False, help='Gera relatório pdf completo');

args = parser.parse_args();


if __name__ == "__main__":
    png_files = [];

    if args.certs:
        print("---- Extraindo informações sobre certificados ----\n");
        
        from variables import vagas_certs, catho_certs, infojobs_certs

        registro, dicionario = pega_vagas_com(vagas_certs);
        registra_no_csv(registro);
        plot_histogram(dicionario, "vagas.com", "certificados-vagas","#00cc66","Certificação");

        registro, dicionario = pega_catho_com(catho_certs);
        registra_no_csv(registro);
        plot_histogram(dicionario, "catho.com", "certificados-catho","#ff0066","Certificação");

        registro, dicionario = pega_infojobs_com(infojobs_certs);
        registra_no_csv(registro);
        plot_histogram(dicionario, "infojobs.com", "certificados-infojobs","#003399","Certificação");

        png_files.append("certificados-vagas.png")
        png_files.append("certificados-catho.png")
        png_files.append("certificados-infojobs.png")

    if args.langs:
        print("---- Extraindo informações sobre Linguagens de Programação ----\n");
        
        from variables import vagas_langs, catho_langs, infojobs_langs

        registro, dicionario = pega_vagas_com(vagas_langs);
        registra_no_csv(registro);
        plot_histogram(dicionario, "vagas.com", "languages-vagas","#00cc66","Linguagem de Programação");

        registro, dicionario = pega_catho_com(catho_langs);
        registra_no_csv(registro);
        plot_histogram(dicionario, "catho.com", "languages-catho","#ff0066","Linguagem de Programação");

        registro, dicionario = pega_infojobs_com(infojobs_langs);
        registra_no_csv(registro);
        plot_histogram(dicionario, "infojobs.com", "languages-infojobs","#003399","Linguagem de Programação");

        png_files.append("languages-vagas.png")
        png_files.append("languages-catho.png")
        png_files.append("languages-infojobs.png")

    if args.completo:
        from variables import arquivos_pdf
        carrossel(png_files,f"{arquivos_pdf}carrossel-temp.pdf");
        combine_pdfs([f"{arquivos_pdf}Capa.pdf",f"{arquivos_pdf}carrossel-temp.pdf",f"{arquivos_pdf}fim.pdf"],f"{arquivos_pdf}carrossel.pdf")