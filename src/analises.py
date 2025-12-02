# %%

import pandas as pd

dados = pd.read_parquet('../data/tb_artilheiros_brasileirao.parquet')

# %%

dados

# %%
ranking_1 = dados[dados['Posição - Ano'] == 1].copy()

idade_min = ranking_1['Idade Campeonato'].min()
idade_max = ranking_1['Idade Campeonato'].max()

artilheiro_mais_jovem = ranking_1[ranking_1['Idade Campeonato'] == idade_min]['Jogador'].reset_index(drop=True)
artilheiro_mais_velho = ranking_1[ranking_1['Idade Campeonato'] == idade_max]['Jogador'].reset_index(drop=True)

max_gols = ranking_1['Gols'].max()
maior_artilharia = ranking_1[ranking_1['Gols'] == max_gols]['Jogador'].reset_index(drop=True)

max_eficiencia = ranking_1['Gols por jogo'].max()
artilharia_eficiente = ranking_1[ranking_1['Gols por jogo'] == max_eficiencia]['Jogador'].reset_index(drop=True)

df_ranking_1 = pd.DataFrame({
    'Artilheiro mais jovem': artilheiro_mais_jovem,
    'Artilheiro mais velho': artilheiro_mais_velho,
    'Artilheiro com mais gols': maior_artilharia,
    'Artilheiro mais eficiente': artilharia_eficiente,

})

df_ranking_1
# %%

top_5_gols = (dados.groupby(by='Jogador', as_index=False)
              .agg(
                  {
                      'Gols': 'sum',
                      'Jogos': 'sum',
                      'Minutos em campo': 'sum'
                    }
                ).sort_values(by='Gols', ascending=False).iloc[0:5]
).reset_index(drop=True).copy()

top_5_gols['Minutos p/ Gol'] = round(top_5_gols['Minutos em campo'] / top_5_gols['Gols'], 1)
top_5_gols['Gols p/ Jogo'] = round(top_5_gols['Gols'] / top_5_gols['Jogos'], 1)
string_df = top_5_gols.to_string(index=False)

print(f"O top 5 goleadores do campeonato artilheiro em toda série histórica são:\n {string_df}")

# %%

# %%

from matplotlib import pyplot as plt

aux_idades = dados[['Idade Campeonato', 'Posição - Ano']].sort_values(by=['Idade Campeonato', 'Posição - Ano'], ascending=[True, True])
eixo_idade = aux_idades['Idade Campeonato']
eixo_posicao = aux_idades['Posição - Ano']

plt.title('Posições por idades')

plt.xlabel('Idades')
plt.ylabel('Posição')

plt.scatter(eixo_idade, eixo_posicao)

plt.show()

# %%

gols_por_clubes = dados.groupby(by='Clube', as_index=False)['Gols'].sum()
gols_por_clubes = gols_por_clubes.sort_values(by='Gols', ascending=False)
gols_por_clubes = gols_por_clubes.iloc[0:5]

eixo_gols = gols_por_clubes['Gols']
eixo_clubes = gols_por_clubes['Clube']

plt.bar(eixo_clubes, eixo_gols, width=0.35)
plt.title('Clubes com maior total de gols')

# %%
### Tratamento dos outliers para cálculo do clube com melhor média de gols por artilheiro

aux_outliers_clubes = dados.groupby(by='Clube').size().reset_index(name='num_aparicoes')

Q1 = aux_outliers_clubes['num_aparicoes'].quantile(0.25)

clubes_sem_outliers = aux_outliers_clubes[aux_outliers_clubes['num_aparicoes'] >= Q1]['Clube']
dados_sem_outliers = dados[dados['Clube'].isin(clubes_sem_outliers)]

media_gols_por_clube = dados_sem_outliers.groupby(by='Clube', as_index=False)['Gols'].mean()
media_gols_por_clube = media_gols_por_clube.sort_values(by='Gols', ascending=False)
media_gols_por_clube = media_gols_por_clube.iloc[0:5]

eixo_gols = media_gols_por_clube['Gols']
eixo_clubes = media_gols_por_clube['Clube']

plt.bar(eixo_clubes, eixo_gols)
plt.title('Maiores médias de gols p/ artilheiro')


clube_melhores_artilharias = dados_sem_outliers[dados_sem_outliers['Clube'] == media_gols_por_clube.iloc[0]['Clube']][['Clube', 'Jogador', 'Gols', 'Ano', 'Posição - Ano']]
clube_melhores_artilharias.sort_values(by='Gols', ascending=False, inplace=True)
print(f'Artilheiros do {clube_melhores_artilharias.iloc[0]['Clube']} e suas participações nas artilharias:')
for idx, row in clube_melhores_artilharias.iterrows():
    jogador = row['Jogador']
    gols = row['Gols']
    ano = row['Ano']
    posicao_ano = row['Posição - Ano']

    print(f'{jogador} com {gols} gols ficou na posição {posicao_ano} dos artilheiros em {ano}')

# %%
