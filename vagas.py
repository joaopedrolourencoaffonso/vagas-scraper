import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime

def plot_histogram(data):
    names = list(data.keys())
    values = list(data.values());

    values = list(map(int, data.values()))

    # Ordenando os valores
    sorted_indices = sorted(range(len(values)), key=lambda i: values[i])
    sorted_names = [names[i] for i in sorted_indices]
    sorted_values = [values[i] for i in sorted_indices]
    
    plt.bar(range(len(data)), sorted_values, tick_label=sorted_names);
    plt.xticks(rotation=90);
    plt.ylim(0, max(values));
    
    # Titulo dos eixos e do gráfico
    plt.xlabel('Certificado') 
    plt.ylabel('Nº de vagas') 
    plt.title("Vagas por certificado no 'vagas.com'")

    #plt.show()
    #Salvando o gráfico
    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.savefig('vagas.png');

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

basic_url = "https://www.vagas.com.br/vagas-de-";
urls = ["MTCNA","CCNA","HCIA","JNCIA","ACMA","NSE","ITIL","COBIT","AZURE","MCSE","AWS","COMPTIA","UniFi","CISSP","GCP","OCI","PMP","VMware"];
total_urls = len(urls);
dicionario = {'':0};
i = 0;

for url in urls:
    temp = parse_page(basic_url+url);
    if temp != None:
        dicionario[url]=temp;

    i+=1;
    print(f"Status: {format((100*i)/total_urls, '.2f')}%", end='\r')

temp = ""

for key, value in dicionario.items():
    temp = temp + f"{datetime.now()}, {key}, {value}\n";

file = open("vagas.csv","a");
file.write(temp);
file.close()

plot_histogram(dicionario)