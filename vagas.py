import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def carrossel(png_files, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter;

    for png_file in png_files:
        #c.drawImage(png_file, 0, 0.2*height, width, 0.8*height)
        c.drawImage(png_file, 0, 0.2*height, width, 0.75*width)
        c.showPage()

    c.save()


def plot_histogram(data, site, figura):
    names = list(data.keys())
    values = list(data.values())

    values = list(map(int, values))  # Convert values to integers

    # Ordenando os valores
    sorted_indices = sorted(range(len(values)), key=lambda i: values[i])
    sorted_names = [names[i] for i in sorted_indices]
    sorted_values = [values[i] for i in sorted_indices]
    
    plt.bar(range(len(data)), sorted_values, tick_label=sorted_names)
    plt.xticks(rotation=90)
    plt.ylim(0, (1.1)*max(values));
    
    # Titulo dos eixos e do gráfico
    plt.ylabel('Nº de vagas') 
    plt.title(f"Vagas por competência no '{site}'")

    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.savefig(f"{figura}.png")
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
        temp = temp + f"{datetime.now()}, {key}, {value}\n";

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
        temp = temp + f"{datetime.now()}, {key}, {value}\n";

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
        temp = temp + f"{datetime.now()}, {key}, {value}\n";

    return temp, dicionario

def write_file(name,text):
    file = open(name,"a");
    file.write(text);
    file.close();

def execute(to_print,vector,file_name,site_name,figura):
    print(to_print);

    if to_print.find("Catho") > 0:
        temp, dicionario = catho_com(vector)

    if to_print.find("vagas") > 0:
        temp, dicionario = vagas_com(vector);

    if to_print.find("infojobs") > 0:
        temp, dicionario = infojobs_com(vector);

    write_file(file_name,temp);

    plot_histogram(dicionario,site_name,figura);

certs = ["PCNSA","MTCNA","CCNA","HCIA","JNCIA","ACMA","NSE","ITIL","COBIT","AZURE","MCSE","AWS","COMPTIA","UniFi","CISSP","GCP","OCI","PMP","VMware"];
langs = ['python','Linguagem C++','Linguagem C#','JavaScript','TypeScript','PHP','Swift','Kotlin','Java','Linguagem Go','Ruby','shellscript','Rust','Pearl','linguagem R']


if __name__ == "__main__":
    execute("===  vagas.com: Certificados ===",certs,"vagas.csv","vagas.com","certificados-vagas");
    execute("===  vagas.com: Linguagens   ===",langs,"vagas.csv","vagas.com","linguagens-vagas");
    execute("===  Catho.com: Certificados ===",certs,"catho.csv","catho.com","certificados-catho");
    execute("===  Catho.com: Linguagens   ===",langs,"catho.csv","catho.com","linguagens-catho");
    execute("===  infojobs.com: Certificados ===",certs,"infojobs.csv","infojobs.com","certificados-infojobs");
    execute("===  infojobs.com: Linguagens   ===",langs,"infojobs.csv","infojobs.com","linguagens-infojobs");

    carrossel(['certificados-catho.png','certificados-vagas.png','certificados-infojobs.png','linguagens-vagas.png','linguagens-catho.png','linguagens-infojobs.png'],"carrossel.pdf")