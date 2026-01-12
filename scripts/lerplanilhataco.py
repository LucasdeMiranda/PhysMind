import os
import sys
import django
import pandas as pd
import math  # necessário para checar NaN

# 1️⃣ Adiciona a raiz do projeto ao Python path
project_root = r"C:\Users\miran\OneDrive\Documentos\GitHub\PhysMind"
sys.path.insert(0, project_root)

# 2️⃣ Configura Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# 3️⃣ Importa o modelo
from alimentos.models import AlimentoBase

# 4️⃣ Lista para armazenar os objetos antes de salvar
alimentos = []

# 5️⃣ Função para normalizar valores
def normaliza(valor):
    if valor in ("NA", "Tr") or valor is None:
        return None
    try:
        f = float(valor)
        if math.isnan(f):  # ignora NaN
            return None
        return f
    except (ValueError, TypeError):
        return None

# 6️⃣ Lê a planilha
df = pd.read_excel(r"C:\Users\miran\Downloads\Taco-4a-Edicao.xlsx", header=None)

# 7️⃣ Loop para processar cada linha
for _, linha in df.iterrows():
    # pula linhas cujo primeiro campo não é número (ex: cabeçalho)
    if not isinstance(linha[0], (int, float)):
        continue

    nome = linha[1]
    if pd.isna(nome):
        continue  # pula linhas sem nome

    nome = str(nome)[:30]  # garante string e respeita max_length

    calorias = normaliza(linha[3])
    proteinas = normaliza(linha[5])
    colesterol = normaliza(linha[7])
    carboidratos = normaliza(linha[8])
    fibra = normaliza(linha[9])
    sodio = normaliza(linha[17])

    # pula se não tiver calorias válidas
    if calorias is None:
        continue

    # cria objeto e adiciona à lista
    alimentos.append(
        AlimentoBase(
            nome=nome,
            calorias=int(calorias),
            proteinas=proteinas,
            carboidratos=carboidratos,
            colesterol=colesterol,
            fibra=fibra,
            sodio=sodio,
        )
    )

# 8️⃣ Salva cada alimento individualmente para evitar problemas no SQLite
contador = 0
for alimento in alimentos:
    alimento.save()
    contador += 1

print(f"{contador} alimentos foram adicionados ao banco.")
