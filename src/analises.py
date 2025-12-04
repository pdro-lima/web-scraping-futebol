# %%

import pandas as pd
from matplotlib import pyplot as plt
from time import sleep

dados = pd.read_parquet('../data/tb_artilheiros_brasileirao.parquet')

# %%
ranking_1 = dados[dados['Posição - Ano'] == 1].copy()

mais_vzs_artilheiro = ranking_1.groupby('Jogador', as_index=False)['Posição - Ano'].sum().sort_values(by='Posição - Ano', ascending=False)['Jogador'].iloc[0]

idade_min = ranking_1['Idade Campeonato'].min()
idade_max = ranking_1['Idade Campeonato'].max()

artilheiro_mais_jovem = ranking_1[ranking_1['Idade Campeonato'] == idade_min]['Jogador'].reset_index(drop=True)
artilheiro_mais_velho = ranking_1[ranking_1['Idade Campeonato'] == idade_max]['Jogador'].reset_index(drop=True)

max_gols = ranking_1['Gols'].max()
maior_artilharia = ranking_1[ranking_1['Gols'] == max_gols]['Jogador'].reset_index(drop=True)

max_eficiencia = ranking_1['Gols por jogo'].max()
artilharia_eficiente = ranking_1[ranking_1['Gols por jogo'] == max_eficiencia]['Jogador'].reset_index(drop=True)

df_ranking_1 = pd.DataFrame({
    'Mais jovem|': artilheiro_mais_jovem,
    'Mais velho|': artilheiro_mais_velho,
    'Mais gols|': maior_artilharia,
    'Mais eficiente|': artilharia_eficiente,
    'Mais vezes artilheiro|': mais_vzs_artilheiro
})

print(f"Dados gerais dos artilheiros (atleta com mais gols no ano disputado):\n\n{df_ranking_1.to_string(index=False)}")
sleep(5)
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

print(f"O top 5 goleadores do campeonato brasileiro no período são:\n\n {top_5_gols.to_string(index=False)}\n\n")
sleep(5)
# %%

contagem_max_artilheiros = ranking_1.groupby(by='Clube', as_index=False)['Posição - Ano'].sum().sort_values(by='Posição - Ano', ascending=False)['Posição - Ano'].iloc[0]
clubes_mais_artilheiros = ranking_1.groupby(by='Clube', as_index=False)['Posição - Ano'].sum().sort_values(by='Posição - Ano', ascending=False)
clubes_mais_artilheiros = clubes_mais_artilheiros[clubes_mais_artilheiros['Posição - Ano'] == contagem_max_artilheiros].rename(columns={'Posição - Ano': 'Qtd Artilheiros'})

print(f"Clubes com maior quantidade de jogadores que já foram artilheiros do campeonato no período:\n\n{clubes_mais_artilheiros.to_string(index=False)}\n\n")
sleep(5)
# %%

gols_por_clubes = dados.groupby(by='Clube', as_index=False)['Gols'].sum()
gols_por_clubes = gols_por_clubes.sort_values(by='Gols', ascending=False)
gols_por_clubes = gols_por_clubes.iloc[0:5]

print(f"Top 5 clubes com maior total de gols somados pelos jogadores \n\n{gols_por_clubes.to_string(index=False)}\n\n")

clubes_em_comum = clubes_mais_artilheiros[clubes_mais_artilheiros['Clube'].isin(gols_por_clubes['Clube'])]['Clube'].unique()

string_clubes_em_comum = ""
for i in range(0, len(clubes_em_comum)):
    if i == len(clubes_em_comum) - 2:
        clube = clubes_em_comum[i] + " "
    elif i == len(clubes_em_comum) - 1:
        clube = "e " + clubes_em_comum[i] + " "
    else:
        clube = clubes_em_comum[i] + ", "
    string_clubes_em_comum += clube


print(f"\n\nDos clubes com maior número de artilheiros {string_clubes_em_comum}também estiveram entre os 5 clubes com maior número de gols\n\n")
sleep(5)

# %%

aux_gols_posicao = dados.groupby(by='Posição', as_index=False)['Gols'].sum().sort_values(by='Gols', ascending=False).iloc[0:5]
gols = aux_gols_posicao['Gols']
posicao = aux_gols_posicao['Posição']

share_centroavantes = round(aux_gols_posicao['Gols'].max() / aux_gols_posicao['Gols'].sum() * 100, 0) 

plt.title('Total de gols por posição')
plt.xlabel('Posição')
plt.ylabel('Gols')

plt.bar(posicao, height=gols, width=0.3)
plt.show()

print(f"{share_centroavantes}% do total de gols está concentrado nos centroavantes\n\n")
sleep(5)

# %%

aux_posicoes_mais_gols = dados.groupby(by='Posição', as_index=False)['Gols'].sum().sort_values(by='Gols', ascending=False).iloc[0:5]['Posição']

aux_gols_posicao_ano = dados[dados['Posição'].isin(aux_posicoes_mais_gols)].pivot_table(
                                            index='Década',
                                            columns='Posição',
                                            values='Gols',
                                            aggfunc='sum'
                                        )

for posicao in aux_gols_posicao_ano.columns:

    if "2021-2025" in aux_gols_posicao_ano.index:
        aux_gols_posicao_ano.loc["2021-2025", posicao] *= 2 # Faço uma projeção simples de que na segunda metade dessa década as posições manterão seus ritmos de gols da primeira metade para conseguir comparar com as outras décadas que tem períodos completos

    plt.plot(aux_gols_posicao_ano.index, aux_gols_posicao_ano[posicao], label=posicao)


plt.xlabel('Década')
plt.ylabel('Total de Gols')
plt.legend()
plt.title("Posições mais goleadoras por década")
plt.show()

print("Pelo gráfico podemos observar que existiu um movimento de jogadores das pontas aumentarem seus números de gols, enquanto que meias ofensivos diminuíram\n\n")
sleep(5)
# %%

aux_idades = dados[['Minutos em campo', 'Posição - Ano']].sort_values(by=['Minutos em campo', 'Posição - Ano'], ascending=[True, True])
eixo_minutos = aux_idades['Minutos em campo']
eixo_posicao = aux_idades['Posição - Ano']

plt.title('Posições por Minutos em Campo')

plt.xlabel('Minutos em Campo')
plt.ylabel('Posição')

plt.scatter(eixo_minutos, eixo_posicao)

plt.show()
print("O gráfico de distribuição mostra que não existe uma correlação entre as variáveis.\n\nNão é possível traçar uma curva de comportamento dos dados e identificar que a medida que um jogador tenha mais minutos esse também terá uma melhor posição no ranking.\n\nOu seja, a posição no ranking depende mais da eficiência do jogador nos minutos em que está em campo.\n\n")
sleep(5)

# %%

estado_clubes = pd.DataFrame({
    'Clube': ranking_1['Clube'].unique(),
    'Estado': ['MG', 'SP', 'MG', 'RJ', 'SP', 'RJ', 'SP', 'PE', 'PR', 'RS', 'PR', 'PR', 'GO', 'RJ', 'SP']
})

ranking_1 = ranking_1.merge(
    estado_clubes,
    on='Clube',
    how='left'
)

aux_contagem_ranking_1 = ranking_1.groupby(by='Estado', as_index=False)['Posição - Ano'].sum().sort_values(by='Posição - Ano', ascending=False)
eixo_idade = aux_contagem_ranking_1['Estado']
eixo_contagem = aux_contagem_ranking_1['Posição - Ano']

plt.pie(eixo_contagem, labels=eixo_idade)
plt.title('Contagem de artilharias por UF')
plt.show()

print("O gráfico mostra que existe uma grande concentração de artilheiros nos clubes do Sudeste.\n\nPodemos explicar esse evento através do fato de que o Sudeste é a região com maior número de clubes com alto investimento, tanto nos times principais quanto nas categorias de base.\n\nEsse investimento possibilita a formação do cenário ideal pra artilharia: um time formado com jogadores melhores tecnicamente criando mais oportunidades de gols pra um jogador muitas vezes também mais eficiente\n\n")
sleep(10)
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

plt.bar(eixo_clubes, eixo_gols, width=0.5)
plt.title('Maiores médias de gols p/ jogador no ranking')
plt.show()


clube_melhores_artilharias = dados_sem_outliers[dados_sem_outliers['Clube'] == media_gols_por_clube.iloc[0]['Clube']][['Clube', 'Jogador', 'Gols', 'Ano', 'Posição - Ano']]
clube_melhores_artilharias.sort_values(by='Gols', ascending=False, inplace=True)
print(f'Jogadores do {clube_melhores_artilharias.iloc[0]['Clube']} e suas participações nas artilharias:\n')
for idx, row in clube_melhores_artilharias.iterrows():
    jogador = row['Jogador']
    gols = row['Gols']
    ano = row['Ano']
    posicao_ano = row['Posição - Ano']

    print(f'{jogador} com {gols} gols ficou na posição {posicao_ano} dos artilheiros em {ano}')

print("\nCuriosamente, o top2 clubes com as maiores médias não são do Sudeste e são clubes de menor investimento, visibilidade e torcida.\n\nNesses casos, o cenário não era igual a de seus adversários com jogadores melhores tecnicamente ou mais eficientes individualmente.\n\nEsses times buscaram ao longo de suas campanhas a formação de times melhores conjuntamente, com encaixes bem feitos entre os jogadores e seus pontos fortes, estratégias claras e organização, além de muito treino e dedicação\n\n")
sleep(10)
