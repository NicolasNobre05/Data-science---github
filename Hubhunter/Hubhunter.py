import requests
from bs4 import BeautifulSoup
import re

user = ""            #Colocar usuário  que deseja encontrar
nome ="Nicolas"             #Colocar Nome do usuário
local ="São Paulo"            #Colocar Cidade/Estado/Pais
linguagem ="PHP java python"        #Colocar Linguagem de programação
pagina = "1"          #Colocar página


if " " in nome:
    nome = nome.replace(" ","+")

if " " in local:
    local = local.replace(" ","+") 

if "c++" in linguagem:
    linguagem = "C%2B&2B"

if " " in linguagem:
    linguagens = linguagem.split(" ")
    linguagem_url = "+".join([f"language%3A{lang}" for lang in linguagens])

link= f"https://github.com/search?q={user}+location%3A{local}+language%3A{linguagem_url}+fullname%3A{nome}&type=users&p={pagina}"

res = requests.get(link) 

#Fazer requisição ao servidor HTTPS.
if res.status_code == 200:                                        #Verifica se a conexão foi bem sucedida.
    dados = BeautifulSoup(res.text, 'html.parser')                #Organizar e ler HTML
    dados = dados.get_text()                                      #Remover a parte HTML
    logins = re.findall(r'"display_login":"(.*?)"', dados)        #Encontrar o padrão display login, 
    print(link)
    print("Quantidade de usuários:",dados.count("display_login")) #contar quantidade de usuários.

    for cont in logins:                                           #Contador para gerar as url
        print(f"https://github.com/search?q={cont}")

else:
    print(f"Falha ao acessar o site: {res.status_code}") 