# PhysMind
Projeto feito em django e flutter para cutting e bulking.

# PhysMind 🧠💪  
**Inteligência aplicada ao corpo e à mente**

PhysMind é um **gerenciador inteligente de cutting e bulking**, focado em controle, adaptação e consistência.  
Diferente de aplicativos tradicionais de dieta, o PhysMind não apenas registra dados — ele **analisa, ajusta e orienta decisões**.

O sistema foi pensado para quem treina sério e entende que a rotina nem sempre é perfeita. Aqui, erros não são punições, são **dados para ajuste**.

---

## 🚀 Principais funcionalidades

- Cálculo ou inserção manual de **calorias, macronutrientes e BF**
- Planejamento de **dieta, hidratação e cardio**
- Acompanhamento diário da execução
- **Correção inteligente de desvios alimentares** (diferencial do projeto)
- Estrutura modular, escalável e orientada a dados

---

## 🧩 Estrutura da aplicação

### 🔹 Módulo 1 – Perfil do usuário
Centraliza os dados base para personalização e cálculos:

- Sexo  
- Idade  
- Altura  
- Peso atual  
- Objetivo:  
  - Cutting  
  - Bulking  
  - Manutenção  
- Nível de atividade física  

---

### 🔹 Módulo 2 – Gordura corporal (BF)

O usuário pode escolher entre:

- 📐 **Estimativa pela Fórmula da Marinha**, usando circunferências corporais  
- ✍️ **Inserção manual do BF**, para quem já realizou avaliação física profissional  

Essa abordagem garante flexibilidade e maior precisão.

---

### 🔹 Módulo 3 – Calorias e macronutrientes

O PhysMind oferece duas rotas independentes:

#### ✔️ Rota A – Usuário já possui dieta definida
- Calorias diárias
- Proteína mínima (g/kg ou valor absoluto)
- Gordura mínima
- Carboidratos livres ou calculados

#### ✔️ Rota B – Cálculo automático pelo sistema
- TMB (Mifflin-St Jeor ou Harris-Benedict)
- Gasto energético total (TDEE)
- Déficit ou superávit configurável
- Proteína baseada em massa magra
- Gordura mínima voltada à saúde hormonal
- Carboidratos como principal variável de ajuste

---

### 🔹 Módulo 4 – Água e retenção hídrica

Recomendações inteligentes de hidratação:

- Cálculo de ingestão mínima de água (ml/kg)
- Ajustes com base em:
  - Consumo de sódio
  - Fibras
  - Potássio (opcional)
- Alertas educativos, como:
  > “Baixa ingestão de água associada a alto consumo de sódio pode aumentar retenção hídrica.”

---

### 🔹 Módulo 5 – Alimentos e refeições

Sistema flexível e personalizável:

- Cadastro livre de alimentos
- Quantidades em gramas, ml ou unidades
- Cálculo automático de macronutrientes
- Edição completa dos alimentos cadastrados

Foco em simplicidade e usabilidade.

---

### 🔹 Módulo 6 – Atividade física

Registro e acompanhamento de gasto energético:

- Cardio (com estimativa de calorias gastas)
- Passos diários (com conversão opcional)
- Treino de força (registro informativo)

---

## 🔥 Diferencial do PhysMind  
### Módulo 7 – Correção inteligente de desvios alimentares

Quando o usuário consome algo fora da dieta planejada, o sistema:

1. Calcula:
   - Calorias excedentes
   - Proteína ingerida
   - Diferença no saldo energético diário
2. Oferece **três estratégias claras de correção**:

#### ✅ Opção A – Abater da dieta
Sugestões práticas, por exemplo:
- Reduzir 120 g de arroz  
- OU reduzir 30 g de aveia  

#### ✅ Opção B – Ajustar o cardio
- +20 minutos de caminhada  
- +12 minutos de bicicleta  

#### ✅ Opção C – Compensar nos dias seguintes
- Distribuir o excedente em 2 dias  
  - Ex: -120 kcal/dia  

> Enquanto a maioria dos apps apenas informa que o limite foi ultrapassado, o PhysMind **ensina o que fazer depois**.

---

## 🏗️ Arquitetura do projeto

O projeto é dividido em dois componentes principais:

Lucas Lucas123@