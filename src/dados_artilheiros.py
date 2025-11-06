# %%

import pandas as pd
import requests
from bs4 import BeautifulSoup
# %%

def acesso_pagina(url):
    
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "referer": "https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/torschuetzenliste/wettbewerb/BRA1",
        "sec-ch-ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    }

    cookies = {
        "_sp_v1_ss": "1:H4sIAAAAAAAAAItWqo5RKimOUbKKxs_IAzEMamN1YpRSQcy80pwcILsErKC6lpoSSrEA-EAOLpYAAAA=",
        "_sp_v1_p": "186",
        "_sp_v1_data": "746454",
        "_sp_su": "false",
        "euconsent-v2": "CQaXJQAQaXJQAAGABCENCCFsAP_gAELAAAKIIzQIQAFAANAAqABwAEAAJwAWgAyABoAEUAJgAUgAxABvADmAIQARwAmgBSAEIAKGAe0BDYCNQEyALaAXmAxkBkgDQgGogQuAjMAhEAMABQAjgCEADhIBgAFQAOAAggBkAGgATAA3gCEAE0Ae0BeYDJAIXDoBgAFQAOAAggBkAGgATAAxABvAE0Ae0BMgC8wGSEIAQAYgA3koAoAHAAmABiAXmAyQpAJAAqABwAEAANAAmABiAPaAvMBkhUACAAooABABkAAA.YAAAAAAAAAAA",
        "consentUUID": "1eba8321-31b7-40cb-b943-14f9c5ff6559_49",
        "pbjs-unifiedid": '{"TDID":"dcabce63-55b5-4b7f-b116-417ee6427bc9","TDID_LOOKUP":"TRUE","TDID_CREATED_AT":"2025-10-04T19:05:32"}',
        "pbjs-unifiedid_cst": "Kyw6LMgsDw==",
        "nadz_dailyVisits": "1",
        "panoramaId_expiry": "1762369532460",
        "kndctr_B21B678254F601E20A4C98A5_AdobeOrg_identity": "CiY2ODcwOTg1Nzc5NTYzNDcwMzcyMDI1MTI5NDI0Mjk5ODM4MzEzNVIQCOesioKlMxgBKgNWQTYwAfAB56yKgqUz",
        "AMCV_B21B678254F601E20A4C98A5@AdobeOrg": "MCMID|68709857795634703720251294242998383135",
        "SA": "1",
        "cuukie": "U0psR19sWWlfYzJzZXhlR0swbUxLZnhmeVJRMkRqM28ZD_ZCRYxgNxV9V3Q3-ZIDiWmZp6icLh8Ul96SvKjS-A==",
        "kndctr_B21B678254F601E20A4C98A5_AdobeOrg_cluster": "va6",
        "cto_bundle": "rHKaPl9GVkpjcTVDNEYxWWdIbGtHbmR4UlRnVGk2UkpneEJ2aWxMV2hJeWk0ejlVNE4lMkZMWjlicU1mVVY4RlRWM0xEMkI2YTk0cTh1TlFHMU9rSnMzUWNBZTl6bG9oJTJGRXBWN3l6eHBkdWV1JTJCMUZab2t2YnNWTlhRaWhNSyUyRiUyRjZZN0U1STh3Nmx6T2RxMFg4RER5VWJkRFV0OHVpMVFNbHAlMkZPcmZCZWhWcXMzUHRTZTAlM0Q",
        "__gads": "ID=b0621c86a1f05e8a:T=1762283133:RT=1762368906:S=ALNI_MYmu9SfW9q-AaycGeOEh9humai4iw",
        "__gpi": "UID=000012a5bcdb0ee9:T=1762283133:RT=1762368906:S=ALNI_MbWf3Nddwy-RjF-LdDY-m9yfVM9bQ",
        "__eoi": "ID=d937620dceffb0ea:T=1762283133:RT=1762368906:S=AA-Afja8ev_f8fOEyCR5O11d_raf",
        "clever-last-tracker-61227": "232"
    }

    resp = requests.get(url, headers=headers, cookies=cookies)
    return resp



def coleta_colunas(soup):

    div = soup.find('div', class_='responsive-table')
    tabela = div.find('table', class_ = "items")
    colunas = tabela.find_all('th')

    lista_colunas = []
    for i in colunas:
        if i.find('span'):
            descricao_coluna = i.find('span')['title']
        elif i.find('div'):
            descricao_coluna = i.find('div')['title']
        else:
            descricao_coluna = i.text

        lista_colunas.append(descricao_coluna)
    
    return lista_colunas



def coleta_dados(soup):

    lista_dados = []

    div = soup.find('div', class_='responsive-table')
    dados_tabela = div.find('tbody')
    dados_jogador = dados_tabela.find_all('tr', class_ = 'odd') + dados_tabela.find_all('tr', class_ = 'even')
    for dado in dados_jogador:
        indice = dado.find_all('td')[0].text
        nome = dado.find_all('td')[1].find('img')['title']
        posicao = dado.find_all('td')[1].find_all('td')[-1].text

        lista_nacionalidades = []
        nacionalidades = dado.find_all('td')[5].find_all('img')
        for i in range(0, len(nacionalidades)):
            nacionalidade = nacionalidades[i]['title']
            lista_nacionalidades.append(nacionalidade)

        idade = dado.find_all('td')[6].text
        try:
            clube = dado.find_all('td')[7].find('a')['title']
        except:
            clube = None

        jogos = dado.find_all('td')[8].text
        assistencias = dado.find_all('td')[9].text
        penaltis = dado.find_all('td')[10].text
        minutos_em_campo = dado.find_all('td')[11].text
        minutos_por_gol = dado.find_all('td')[12].text
        gols_por_jogo = dado.find_all('td')[13].text
        gols = dado.find_all('td')[14].text

        lista_dados.append([indice, 
                            (nome, 
                            posicao), 
                            lista_nacionalidades, 
                            idade, 
                            clube, 
                            jogos, 
                            assistencias,
                            penaltis,
                            minutos_em_campo,
                            minutos_por_gol,
                            gols_por_jogo,
                            gols])
        
    return lista_dados


# %%
total_anos = (2025 - 2000) + 1

lista_urls = []
lista_dfs = []
ano = 2024

for i in range(total_anos):
    
    url = f"https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/torschuetzenliste/wettbewerb/BRA1/saison_id/{ano}/altersklasse/alle/detailpos//plus/1"

    resp = acesso_pagina(url)

    if resp.status_code != 200:
        print('O acesso a url retornou algum erro. Verifique')
    else:
        soup = BeautifulSoup(resp.text, 'html.parser')
        lista_colunas = coleta_colunas(soup)
        lista_dados = coleta_dados(soup)

    lista_dicts = [dict(zip(lista_colunas, linha)) for linha in lista_dados]

    df = pd.DataFrame(lista_dicts)

    df['#'] = df['#'].astype(int)
    df = df.sort_values(by='#', ascending=True).reset_index(drop=True)
    
    lista_dfs.append(df)

    ano -= 1

df_geral = pd.concat(lista_dfs, ignore_index=True).reset_index(drop=True)
