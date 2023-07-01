import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import argparse

def carrossel(png_files, output_file):
    from variables import diretorio_de_imagens
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter;

    for png_file in png_files:
        #c.drawImage(png_file, 0, 0.2*height, width, 0.8*height)
        c.drawImage(f"{diretorio_de_imagens}{png_file}", 0, 0.2*height, width, 0.75*width)
        c.showPage()

    c.save()


def plot_histogram(data, site, figura,color,competencia):
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
    plt.title(f"Vagas por {competencia} no '{site}'")

    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.savefig(f"{diretorio_de_imagens}{figura}.png")
    plt.close();

def parse_page(url):
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


def vagas_com(vetor):
    basic_url = "https://www.vagas.com.br/vagas-de-";
    total_urls = len(vetor);
    dicionario = {};
    i = 0;

    for elemento in vetor:
        temp = parse_page(basic_url+elemento);
        if temp != None:
            dicionario[elemento]=temp;

        i+=1;
        print(f"Status: {format((100*i)/total_urls, '.2f')}%", end='\r')

    temp = ""

    for key, value in dicionario.items():
        temp = temp + f"{datetime.now()},vagas.com,{key}, {value}\n";

    return temp, dicionario

def catho_com(vetor):
    total_urls = len(vetor);
    dicionario = {};
    i = 0;

    for elemento in vetor:
        temp = parse_page(f"https://www.catho.com.br/vagas/{elemento.lower()}/?q={elemento.upper()}");

        temp = temp.replace(".","");

        if temp != None and temp != "Ops!":
            dicionario[elemento]=temp;

        i+=1;
        print(f"Status: {format((100*i)/total_urls, '.2f')}%", end='\r')

    temp = ""

    for key, value in dicionario.items():
        temp = temp + f"{datetime.now()},catho.com,{key}, {value}\n";

    return temp, dicionario

def infojobs_com(vetor):
    total_urls = len(vetor);
    dicionario = {};
    i = 0;
    
    for elemento in vetor:
        x = parse_info_jobs(f"https://www.infojobs.com.br/empregos.aspx?palabra={elemento}")
        
        temp = x.split('Vagas de Emprego')[0];
        
        if temp != "":
            dicionario[elemento] = int(temp);

        i+=1;
        print(f"Status: {format((100*i)/total_urls, '.2f')}%", end='\r')

    temp = ""

    for key, value in dicionario.items():
        temp = temp + f"{datetime.now()},infojobs.com,{key}, {value}\n";

    return temp, dicionario

def write_file(name,text):
    file = open(name,"a");
    file.write(text);
    file.close();

def execute(to_print,vector,file_name,site_name,figura,competencia):
    print(to_print);

    if to_print.find("Catho") > 0:
        temp, dicionario = catho_com(vector);
        color = "#ff0066";

    if to_print.find("vagas") > 0:
        temp, dicionario = vagas_com(vector);
        color = "#00cc66";

    if to_print.find("infojobs") > 0:
        temp, dicionario = infojobs_com(vector);
        color = "#003399";

    write_file(file_name,temp);

    plot_histogram(dicionario,site_name,figura,color,competencia);

parser = argparse.ArgumentParser(description='Gerador de relatório sobre competências mais demandadas na área de TI');
parser.add_argument('--certs',action="store_true",default=False, help='Gera relatório sobre certificados');
parser.add_argument('--langs',action="store_true",default=False, help='Gera relatório sobre linguagens de programação');
parser.add_argument('--databases',action="store_true",default=False, help='Gera relatório sobre bancos de dados');
parser.add_argument('--servers',action="store_true",default=False, help='Gera relatório sobre servidores web');

args = parser.parse_args();


if __name__ == "__main__":
    png_files = [];

    if args.certs:
        from variables import certs
        
        execute("===  vagas.com: Certificados ===",certs,"registro.csv","vagas.com","certificados-vagas","Certificação");
        execute("===  Catho.com: Certificados ===",certs,"registro.csv","catho.com","certificados-catho","Certificação");
        execute("===  infojobs.com: Certificados ===",certs,"registro.csv","infojobs.com","certificados-infojobs","Certificação");

        png_files.append('certificados-vagas.png');
        png_files.append('certificados-catho.png');
        png_files.append('certificados-infojobs.png');
    
    if args.langs:
        from variables import langs
        
        execute("===  vagas.com: Linguagens   ===",langs,"registro.csv","vagas.com","linguagens-vagas","Linguagem");
        execute("===  Catho.com: Linguagens   ===",langs,"registro.csv","catho.com","linguagens-catho","Linguagem");
        execute("===  infojobs.com: Linguagens   ===",langs,"registro.csv","infojobs.com","linguagens-infojobs","Linguagem");

        png_files.append('linguagens-vagas.png');
        png_files.append('linguagens-catho.png');
        png_files.append('linguagens-infojobs.png');
    
    if args.databases:
        from variables import databases
        
        execute("===  vagas.com: Banco de Dados ===",databases,"registro.csv","vagas.com","databases-vagas","Banco de Dados");
        execute("===  Catho.com: Banco de Dados ===",databases,"registro.csv","catho.com","databases-catho","Banco de Dados");
        execute("===  infojobs.com: Banco de Dados ===",databases,"registro.csv","infojobs.com","databases-infojobs","Banco de Dados");

        png_files.append('databases-vagas.png');
        png_files.append('databases-catho.png');
        png_files.append('databases-infojobs.png');
    
    
    if args.servers:
        from variables import servers
        
        execute("===  vagas.com: Servidores   ===",servers,"registro.csv","vagas.com","servidores-vagas","Servidores");
        execute("===  Catho.com: Servidores   ===",servers,"registro.csv","catho.com","servidores-catho","Servidores");
        execute("===  infojobs.com: Servidores   ===",servers,"registro.csv","infojobs.com","servidores-infojobs","Servidores");

        png_files.append('servidores-vagas.png');
        png_files.append('servidores-catho.png');
        png_files.append('servidores-infojobs.png');

    carrossel(png_files,"carrossel.pdf");