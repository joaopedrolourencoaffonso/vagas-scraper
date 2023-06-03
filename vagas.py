import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime

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
    plt.ylim(0, max(values))
    
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

def vagas_com(vetor):
    basic_url = "https://www.vagas.com.br/vagas-de-";
    total_urls = len(vetor);
    dicionario = {'':0};
    i = 0;

    for elemento in vetor:
        temp = parse_page(basic_url+elemento);
        if temp != None:
            dicionario[elemento]=temp;

        i+=1;
        #print(f"Status: {format((100*i)/total_urls, '.2f')}%", end='\r')

    temp = ""

    for key, value in dicionario.items():
        temp = temp + f"{datetime.now()}, {key}, {value}\n";

    return temp, dicionario

def catho_com(vetor):
    total_urls = len(vetor);
    dicionario = {'':0};
    i = 0;

    for elemento in vetor:
        temp = parse_page(f"https://www.catho.com.br/vagas/{elemento.lower()}/?q={elemento.upper()}");

        temp = temp.replace(".","");

        if temp != None and temp != "Ops!":
            dicionario[elemento]=temp;

        i+=1;
        #print(f"Status: {format((100*i)/total_urls, '.2f')}%", end='\r')

    temp = ""

    for key, value in dicionario.items():
        temp = temp + f"{datetime.now()}, {key}, {value}\n";

    return temp, dicionario

def write_file(name,text):
    file = open(name,"a");
    file.write(text);
    file.close();

def execute(to_print,vector,file_name,site_name,figura):
    #print(to_print);

    if to_print.find("Catho") > 0:
        temp, dicionario = catho_com(vector)

    if to_print.find("vagas") > 0:
        temp, dicionario = vagas_com(vector)

    write_file(file_name,temp);

    plot_histogram(dicionario,site_name,figura);

certs = ["PCNSA","MTCNA","CCNA","HCIA","JNCIA","ACMA","NSE","ITIL","COBIT","AZURE","MCSE","AWS","COMPTIA","UniFi","CISSP","GCP","OCI","PMP","VMware"];
langs = ['python','Linguagem C++','Linguagem C#','JavaScript','TypeScript','PHP','Swift','Kotlin','Java','Linguagem Go','Ruby','shellscript','Rust','Pearl','linguagem R']


if __name__ == "__main__":
    execute("===  vagas.com: Certificados ===",certs,"vagas.csv","vagas.com","certificados-vagas");
    execute("===  vagas.com: Linguagens   ===",langs,"vagas.csv","vagas.com","linguagens-vagas");
    execute("===  Catho.com: Certificados ===",certs,"catho.csv","catho.com","certificados-catho");
    execute("===  Catho.com: Linguagens   ===",langs,"catho.csv","catho.com","linguagens-catho");
