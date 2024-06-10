import requests
from bs4 import BeautifulSoup
import re


def consultardados(nome, linguagem, localidade, contpag):
    resultados = []
    if " " in nome:             #Se nome tiver espaço
        nome = nome.replace(" ","+") #Substituir por +

    if " " in localidade:       #Se localidade tiver espaço
        localidade = localidade.replace(" ","+")  #Substituir por +

    if "C++" in linguagem:      #Se linguagem tiver C++
        linguagem = linguagem.replace("C++","C%2B%2B")  #Substituir por C%2B%2B 

    if "C#" in linguagem:      #Se linguagem tiver C++
        linguagem = linguagem.replace("C#","C%23")  #Substituir por C%2B%2B  

    if " " in linguagem:     #Se linguagem tiver espaço
        linguagens = linguagem.split(" ") #Quebrar a string depois do espaço
        for lang in linguagens: 
            linguagem = "+".join(f"language%3A{lang}") #unir as strings quebradas com a estrutura da url


    def entrarsite(localidade, linguagem, nome, contpag): #função de construir a url, entrar no site, interpretar as informações 
        link = f"https://github.com/search?q=location%3A{localidade}+language%3A{linguagem}+fullname%3A{nome}&type=users&p={contpag}"
        res = requests.get(link)   #fazer requisição
        if res.status_code == 200: #Verifica se a conexão foi bem sucedida.
            dados = BeautifulSoup(res.text, 'html.parser') #Organizar e ler HTML
            dados = dados.get_text()  #Remover a parte HTML
        else:
            print("Falha ao acessar o site:", res.status_code)
            dados, link = entrarsite(localidade, linguagem, nome, contpag)
        return dados, link #Retornar os dados

    dados, link = entrarsite(localidade, linguagem, nome, contpag) #definir as variáveis 
    
    avatar = re.findall(r'"avatar_url":"(.*?)"', dados)
    logins = re.findall(r'"display_login":"(.*?)"', dados)
    for login, avatar  in zip(logins, avatar):
        resultados.append(f"https://github.com/{login}, {avatar}")
            
    return resultados
