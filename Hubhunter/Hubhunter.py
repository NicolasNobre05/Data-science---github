import requests
from bs4 import BeautifulSoup
import re
import time


nome = ""
localidade = ""
linguagem = "Python"

if " " in nome:
    nome = nome.replace(" ","+")


if " " in localidade:
    localidade = localidade.replace(" ","+") 


if " " in linguagem:
    linguagens = linguagem.split(" ")
    linguagem = "+".join([f"language%3A{lang}" for lang in linguagens])

link= f"https://github.com/search?q=location%3A{localidade}+language%3A{linguagem}+fullname%3A{nome}&type=users&p=1"

res = requests.get(link)

if res.status_code == 200:      
    dados = BeautifulSoup(res.text, 'html.parser')
    dados = dados.get_text()
    pagina = re.findall(r'"page_count":(\d+)', dados) 
    pagina = int(pagina[0])

    for contpag in range(pagina + 1):
        link= f"https://github.com/search?q=location%3A{localidade}+language%3A{linguagem}+fullname%3A{nome}&type=users&p={contpag}"
        res = requests.get(link) 
        if res.status_code == 200:
            dados = BeautifulSoup(res.text, 'html.parser') 
            dados = dados.get_text() 
            logins = re.findall(r'"display_login":"(.*?)"', dados)        #Encontrar o padrão display login, 
            for cont in logins: 
                print(f"https://github.com/{cont}")
            print(link)
            time.sleep(1)    
        else:
            print(f"Falha ao acessar o site: {res.status_code}")
        time.sleep(1)   
else:
    print(f"Falha ao acessar o site: {res.status_code}") 
