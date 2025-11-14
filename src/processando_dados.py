# %%
import pandas as pd

# %%
data = pd.read_parquet('../data/dados_artilheiros.parquet')
# %%
data['Posição'] = data['Jogadores'].str[1]
data['Jogadores'] = data['Jogadores'].str[0]

data['Nacionalidade 1'] = data['Nac.'].str[0]
data['Nacionalidade 2'] = data['Nac.'].str[1]
data.drop(columns='Nac.', inplace=True)

data['Minutos em campo'] = data['Minutos em campo'].str.replace("'", "").str.replace(".", "").astype(int)
data['Minutos por gol'] = data['Minutos por gol'].str.replace("'", "").str.replace(".", "").astype(int)
data['Assistências'] = data['Assistências'].astype(int)
data['Gols'] = data['Gols'].astype(int)
data['Jogos'] = data['Jogos'].astype(int)

data['Participações em Gols'] = data['Assistências'] + data['Gols']
data['Participações por Jogo'] = data['Participações em Gols'] / data['Jogos']
data['Minutos por participação'] = data['Minutos em campo'] / data['Participações em Gols']
data['Minutos por participação'] = data['Minutos por participação'].astype(int)

# %%

# Esse bloco faz o tratamento de caracteres e espaçamentos especiais usados no HTML do site
data['Idade (hoje)'] = (
    data['Idade (hoje)']
    .str.replace('\xa0', ' ', regex=False)
    .str.replace(r'[^0-9()\s]', 'Morto ', regex=True)
    .str.replace('\s+', ' ', regex=True)
    .str.strip()
)

for idx, row in data.iterrows():

    if len(row['Idade (hoje)']) > 2:

        data.at[idx, 'Idade Campeonato'] = data.at[idx, 'Idade (hoje)'].split(" ")[0]

        if data.at[idx, 'Idade (hoje)'].split(" ")[1] == "(Morto":
            data.at[idx, 'Em Vida'] = "Não"
            data.at[idx, 'Idade Atual'] = data.at[idx, 'Idade (hoje)'].split(" ")[2].replace('(', '').replace(')', '')
        else:
            data.at[idx, 'Em Vida'] = "Sim"
            data.at[idx, 'Idade Atual'] = data.at[idx, 'Idade (hoje)'].split(" ")[1].replace('(', '').replace(')', '')

    else:
        data.at[idx, 'Idade Campeonato'] = data.at[idx, 'Idade (hoje)']
        data.at[idx, 'Idade Atual'] = data.at[idx, 'Idade (hoje)']
        data.at[idx, 'Em Vida'] = "Sim"

data.drop(columns='Idade (hoje)', inplace=True)

# %%

data = (data.rename(columns={'#': 'Posição - Ano',
                            'Jogadores': 'Jogador',
                            'Penalti': 'Gols de Penalti'})
                            [['Posição - Ano', 
                            'Ano',
                            'Jogador',
                            'Clube',
                            'Nacionalidade 1', 
                            'Nacionalidade 2',
                            'Idade Atual',
                            'Idade Campeonato',
                            'Em Vida',
                            'Posição',
                            'Jogos',
                            'Gols',
                            'Gols por jogo',
                            'Assistências',
                            'Participações em Gols',
                            'Participações por Jogo',
                            'Gols de Penalti',
                            'Minutos em campo',
                            'Minutos por gol',
                            'Minutos por participação'
                            ]]
)
# %%
