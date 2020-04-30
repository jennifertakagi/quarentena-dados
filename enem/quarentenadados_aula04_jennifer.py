# -*- coding: utf-8 -*-
"""QuarentenaDados - Aula04 - Jennifer

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LnVizlkCuNIP2XTXtse4t_6WJ503adXK
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd

# %precision %.2f
pd.options.display.float_format = '{:,.2f}'.format

uri = "https://github.com/guilhermesilveira/enem-2018/blob/master/MICRODADOS_ENEM_2018_SAMPLE_43278.csv?raw=true"
dados = pd.read_csv(uri)
dados.head()

print(dados.columns.values)

dados.describe()

colunas_de_notas = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
dados_notas = dados[colunas_de_notas].dropna()
dados_notas.columns = ["ciencias_naturais", "ciencias_humanas", "linguagem_codigo", "matematica", "redacao"]
dados_notas.head()

len(dados_notas)

corr = dados_notas.corr()
corr

from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=np.bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

sns.heatmap(corr)

sns.pairplot(dados_notas)

"""## Desafio 1 da [Thais André](https://twitter.com/thais_tandre)

Se a pessoa não teve presença, preencha a nota dela com algum número. A nota 0? A nota média? A mediana?
"""

faltou = 0
presente = 1
eliminado = 2

dados_nota = dados.copy()

dados_nota.loc[dados["TP_PRESENCA_CN"].isin([faltou, eliminado]), "NU_NOTA_CN"] = 0
dados_nota.loc[dados["TP_PRESENCA_CH"].isin([faltou, eliminado]), "NU_NOTA_CH"] = 0
dados_nota.loc[dados["TP_PRESENCA_LC"].isin([faltou, eliminado]), "NU_NOTA_LC"] = 0
dados_nota.loc[dados["TP_PRESENCA_MT"].isin([faltou, eliminado]), "NU_NOTA_MT"] = 0

dados_nota[colunas_de_notas].head()

"""## Desafio 2 do [Thiago Gonçalves](https://twitter.com/tgcsantos)

A matriz de correlação está feiosa, vamos deixar mais bonita? :) Não se esqueça de manter os valores dentro delas.
"""

sns.set(font_scale=1.2)

labels = ["Ciências da Natureza", "Ciências Humanas", "Linguagens e Códigos", "Matemática", "Redação"]

plt.figure(figsize=(6, 6))
ax = sns.heatmap(
    corr,
    annot=True,
    cmap="YlGnBu",
    cbar=False,
    xticklabels=labels,
    yticklabels=labels,
)

plt.show()

sns.set()

"""## Desafio 3 do [Paulo Silveira](https://twitter.com/paulo_caelum)


Pairplot dos acertos de cada categoria (CN, CH, MT, LC, nota pura da redação). Usar o gabarito e as respostas
"""

def contar_acertos(aluno, materia):
    respostas = aluno.get(f"TX_RESPOSTAS_{materia}")
    gabarito = aluno.get(f"TX_GABARITO_{materia}")

    if (type(respostas) != str or type(gabarito) != str):
        return 0

    return sum(a==b for a, b in zip(respostas, gabarito))

dados_nota_2 = dados_nota.copy()

dados_nota_2["NU_RESPOSTAS_CORRETAS_CN"] = dados_nota_2.apply(contar_acertos, materia="CN", axis=1)
dados_nota_2["NU_RESPOSTAS_CORRETAS_CH"] = dados_nota_2.apply(contar_acertos, materia="CH", axis=1)
dados_nota_2["NU_RESPOSTAS_CORRETAS_LC"] = dados_nota_2.apply(contar_acertos, materia="LC", axis=1)
dados_nota_2["NU_RESPOSTAS_CORRETAS_MT"] = dados_nota_2.apply(contar_acertos, materia="MT", axis=1)

num_questoes_acertadas = dados_nota_2[["NU_RESPOSTAS_CORRETAS_CN", "NU_RESPOSTAS_CORRETAS_CH", "NU_RESPOSTAS_CORRETAS_LC", "NU_RESPOSTAS_CORRETAS_MT", "NU_NOTA_REDACAO"]]
num_questoes_acertadas.columns = ["Ciências da Natureza", "Ciências Humana", "Linguagens e Códigos", "Matemática", "Redação"]

sns.set()
sns.pairplot(num_questoes_acertadas)

"""## Desafio 4 do [Guilherme Silveira](https://twitter.com/guilhermecaelum)

Remover todos os zeros. Tomar o cuidado que no desafio 1 já tomamos decisões ligadas a limpeza dos dados também. Você também pode exportar para outro CSV se quiser.
"""

import numpy as np

dados_nota_sem_0 = dados_nota_2.copy()

dados_nota_sem_0["NU_NOTA_CN"] = dados_nota_2["NU_NOTA_CN"].replace(0., np.NAN)
dados_nota_sem_0["NU_NOTA_CH"] = dados_nota_2["NU_NOTA_CH"].replace(0., np.NAN)
dados_nota_sem_0["NU_NOTA_LC"] = dados_nota_2["NU_NOTA_LC"].replace(0., np.NAN)
dados_nota_sem_0["NU_NOTA_MT"] = dados_nota_2["NU_NOTA_MT"].replace(0., np.NAN)

dados_nota_sem_0.dropna(subset=["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT"], inplace=True)

dados_nota_sem_0[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT"]].head()

"""## Desafio 5 do [Thiago Gonçalves](https://twitter.com/tgcsantos)

Quais questões tiveram mais erros (análise sobre o gabarito x acertos x erros)
"""

def corrigir_questoes(aluno, materia):
    respostas = aluno.get(f"TX_RESPOSTAS_{materia}")
    gabarito = aluno.get(f"TX_GABARITO_{materia}")
    
    return pd.Series([int(a==b) for a, b in zip(respostas, gabarito)])

prova_cn_azul = dados.query("CO_PROVA_CN == 447")

matriz_acertos = prova_cn_azul.apply(corrigir_questoes, materia="CN", axis=1)
matriz_acertos