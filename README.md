# Dashboard de Performance Logística 🚚

Dashboard interativo para análise de eficiência logística, desenvolvido para monitorar entregas, identificar gargalos e avaliar custos de transporte.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.8+** - Linguagem de programação
- **Streamlit 1.28.0+** - Framework para interface web interativa
- **Pandas 2.0.0+** - Manipulação e análise de dados
- **Plotly 5.18.0+** - Visualizações interativas e mapas geográficos
- **NumPy** - Operações numéricas e cálculos
- **Hashlib** (biblioteca padrão Python) - Geração determinística de coordenadas simuladas

### 📌 Instalação Manual de Dependências (sem requirements.txt)

Caso não utilize o arquivo `requirements.txt`, execute os seguintes comandos para instalar todas as bibliotecas necessárias:

```powershell
pip install streamlit>=1.28.0
pip install pandas>=2.0.0
pip install plotly>=5.18.0
pip install numpy
```

**Ou instale todas de uma vez:**
```powershell
pip install streamlit>=1.28.0 pandas>=2.0.0 plotly>=5.18.0 numpy
```

---

## 📋 Pré-requisitos

1. **Python 3.8 ou superior** instalado no sistema
   - Verificar versão: `python --version`
   - Download: [python.org](https://www.python.org/downloads/)

2. **Pip** (gerenciador de pacotes Python) atualizado
   - Geralmente vem instalado com Python
   - Atualizar: `python -m pip install --upgrade pip`

3. **Git** (opcional, para clonar o repositório)
   - Download: [git-scm.com](https://git-scm.com/)

---

## 📦 Instalação e Configuração

### Passo 1: Obter o Projeto

**Opção A - Clonar o repositório (se estiver no GitHub):**
```bash
git clone <URL_DO_REPOSITORIO>
cd dashboardPerformanceLogística
```

**Opção B - Download manual:**
1. Baixe o projeto como ZIP
2. Extraia para uma pasta de sua preferência
3. Abra o terminal/prompt na pasta do projeto

### Passo 2: Criar Ambiente Virtual (Recomendado)

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

> **Nota:** O ambiente virtual isola as dependências do projeto. Você saberá que está ativo quando aparecer `(.venv)` no início da linha do terminal.

### Passo 3: Instalar Dependências

Com o ambiente virtual ativado, execute:

```powershell
pip install -r requirements.txt
```

**Instalação manual (alternativa):**
```powershell
pip install streamlit>=1.28.0 pandas>=2.0.0 plotly>=5.18.0 numpy
```

### Passo 4: Verificar Arquivos Necessários

Certifique-se de que os seguintes arquivos estão presentes na pasta do projeto:

```
dashboardPerformanceLogística/
├── app.py                    # Código principal do dashboard
├── requirements.txt          # Lista de dependências
├── FCD_logistica.csv        # Base de dados (8001 registros)
└── README.md                # Este arquivo
```

---

## ▶️ Execução do Projeto

### Passo 1: Ativar o Ambiente Virtual (se não estiver ativo)

**Windows:**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### Passo 2: Executar o Dashboard

No diretório do projeto, execute:

```powershell
streamlit run app.py
```

### Passo 3: Acessar o Dashboard

- O Streamlit abrirá automaticamente o navegador padrão
- Caso não abra, acesse manualmente: **http://localhost:8501**
- O dashboard estará pronto para uso

### Passo 4: Encerrar a Aplicação

- No terminal, pressione `Ctrl + C`
- Para desativar o ambiente virtual: `deactivate`

---

## 🎯 Como Usar o Dashboard

### 1. Filtros (Barra Lateral)

Ao abrir o dashboard, você verá filtros na barra lateral esquerda:

- **Período (De/Até)**: Selecione o intervalo de datas para análise
  - Padrão: Todo o período disponível (01/01/2024 a 28/12/2024)
  
- **Transportadora**: Escolha uma ou mais transportadoras
  - Opções: Correios, Jadlog, Loggi, Azul Cargo
  - Padrão: Todas selecionadas
  
- **Hub de Origem**: Selecione os hubs de distribuição
  - Opções: São Paulo, Curitiba, Belo Horizonte, Salvador, Recife
  - Padrão: Todos selecionados
  
- **Status**: Filtre por status da entrega
  - Opções: Entregue, Devolvido, Em trânsito
  - Padrão: Todos selecionados

### 2. Indicadores Principais (KPIs)

No topo da página, você verá 5 indicadores-chave:

- **Entregas no Prazo (OTD)**: Percentual de entregas pontuais
- **Custo Total de Frete**: Soma dos custos de transporte
- **Volume de Pedidos**: Total de pedidos e destinos únicos
- **Tempo Médio de Entrega**: Prazo real médio em dias
- **Taxa de Atraso**: Percentual e tempo médio de atrasos

### 3. Abas de Análise

#### **Aba 1: Performance**
- Gráficos de tempo médio por transportadora
- Taxa de entrega no prazo (OTD) comparativa
- Evolução mensal do OTD
- Cards de performance por hub

#### **Aba 2: Mapa & Fluxos**
- Mapa interativo com rotas de entrega
- Controle de visualização por slider
- Diagrama de fluxo Origem → Transportadora
- Mapa de calor Hub × Transportadora

#### **Aba 3: Análise de Custos**
- TreeMap de custos por região
- Custo total por hub
- Evolução mensal dos custos
- Tabela de eficiência (Top 15 combinações)

#### **Aba 4: Decisões para Gestão**
- Insights automáticos sobre transportadoras
- Oportunidades de otimização de custos
- Identificação de gargalos
- Recomendações estratégicas

### 4. Interação com Gráficos

- **Hover**: Passe o mouse sobre elementos para ver detalhes
- **Zoom**: Clique e arraste no mapa para aproximar/afastar
- **Legenda**: Clique nos itens da legenda para ocultar/mostrar séries
- **Slider**: No mapa, ajuste o número de rotas exibidas

---

## 🔧 Solução de Problemas

### Erro: "streamlit: comando não encontrado"

**Solução:**
1. Certifique-se de que o ambiente virtual está ativado
2. Reinstale o Streamlit: `pip install streamlit`
3. Verifique a instalação: `streamlit --version`

### Erro: "No module named 'pandas'" (ou plotly, numpy)

**Solução:**
```powershell
pip install pandas plotly numpy
```

### Erro: "FileNotFoundError: FCD_logistica.csv"

**Solução:**
1. Verifique se o arquivo CSV está na mesma pasta que `app.py`
2. Certifique-se de estar executando o comando no diretório correto
3. Use `cd` para navegar até a pasta do projeto

### Dashboard não abre no navegador

**Solução:**
1. Copie o endereço mostrado no terminal (geralmente `http://localhost:8501`)
2. Cole no navegador manualmente
3. Verifique se nenhuma outra aplicação está usando a porta 8501

### Erro de porta em uso

**Solução:**
Execute com porta alternativa:
```powershell
streamlit run app.py --server.port 8502
```

---

## 📊 Estrutura da Base de Dados

**Arquivo:** `FCD_logistica.csv`  
**Separador:** Ponto-e-vírgula (;)  
**Encoding:** UTF-8  
**Registros:** 8.001 entregas

**Colunas:**
- `pedido_id`: Identificador único
- `data_pedido`: Data do pedido (dd/mm/yyyy)
- `data_entrega`: Data da entrega (dd/mm/yyyy)
- `transportadora`: Nome da transportadora
- `cidade_origem`: Hub de origem (5 cidades)
- `cidade_destino`: Cidade de destino (446 cidades)
- `prazo_estimado_dias`: Prazo previsto
- `prazo_real_dias`: Prazo real
- `custo_transporte`: Valor do frete
- `status_entrega`: Status da entrega

---

## 📝 Observações Finais

- O dashboard utiliza **cache** para melhor performance após o primeiro carregamento
- Todas as visualizações são **interativas** e responsivas
- Os dados são **filtrados em tempo real** conforme seleção na sidebar
- O mapa utiliza **coordenadas simuladas** para cidades fictícias (dados reais no hover)

---

## 🎓 Informações Acadêmicas

**Projeto:** Dashboard de Performance Logística  
**Disciplina:** Fundamentos em Ciência de Dados  
**Professor:** Assuero Ximenes  
**Período:** 2025.2

**Objetivo:** O objetivo deste projeto é desenvolver um Dashboard de performance logística, permitindo aos gestores monitorar a eficiência das entregas, identificar gargalos e avaliar os custos logísticos por região. O foco é fornecer informações que apoiem decisões estratégicas sobre transportadoras, prazos e otimização de rotas.

```
dashboardPerformanceLogística/
├── app.py                    # Código principal do dashboard
├── requirements.txt          # Dependências do projeto
├── FCD_logistica.csv        # Base de dados de entregas
└── README.md                # Documentação (este arquivo)
```

## ✨ Funcionalidades

### 🎛️ Filtros Interativos (Sidebar)

- **📅 Período**: Filtro por intervalo de datas (De/Até)
  - Padrão: Todo o período da base (2024/01/01 a 2024/12/28)
- **🚛 Transportadora**: Seleção múltipla (Correios, Jadlog, Loggi, Azul Cargo)
- **🏢 Hub de Origem**: Seleção múltipla (São Paulo, Curitiba, Belo Horizonte, Salvador, Recife)
- **📋 Status**: Seleção múltipla (Entregue, Devolvido, Em trânsito)

### 📊 Indicadores Principais (KPIs)

Linha de 5 cards com métricas consolidadas:

1. **✅ Entregas no Prazo (OTD)**
   - Percentual de pedidos entregues no prazo
   - Cor dinâmica: Verde (≥70%), Amarelo (50-70%), Vermelho (<50%)
   - Tooltip explicativo: "OTD = On-Time Delivery (% no prazo)"

2. **💰 Custo Total de Frete**
   - Soma total de custos de transporte
   - Custo médio por pedido

3. **📦 Volume de Pedidos**
   - Total de pedidos no período
   - Número de destinos únicos atendidos

4. **⏱️ Tempo Médio de Entrega**
   - Prazo real médio em dias
   - Comparação com prazo estimado médio

5. **⚠️ Taxa de Atraso**
   - Percentual de pedidos atrasados
   - Atraso médio quando ocorre
   - Tooltip: "Pedidos entregues após o prazo estimado"

### 📈 Aba 1: Performance

#### Análise de Tempo Médio
- **Gráfico de Barras**: Tempo médio de entrega por transportadora
- Comparação visual entre transportadoras
- Identificação de eficiência no tempo de entrega

#### Taxa de Entrega no Prazo (OTD)
- **Gráfico de Barras Horizontal**: OTD % por transportadora
- Cores distintas por transportadora
- Tooltip explicativo do termo "OTD"

#### Evolução Mensal do OTD
- **Gráfico de Linhas**: Tendência temporal do OTD
- Comparação entre transportadoras ao longo do tempo
- Marcadores interativos

#### Performance por Hub de Origem
- **5 Cards Comparativos** (um para cada hub):
  - Volume de entregas
  - OTD % (com cor dinâmica)
  - Tempo médio de entrega
  - Custo médio por entrega
- Identificação visual de hubs críticos

### 🗺️ Aba 2: Mapa & Fluxos

#### Mapa Interativo - Fluxos Origem → Destino
- **Visualização geográfica** das rotas de entrega
- **Características**:
  - Hubs de origem com coordenadas reais (SP, CWB, BH, SSA, REC)
  - Destinos com posições simuladas dentro do território brasileiro
  - Linhas azuis: rotas no prazo
  - Linhas vermelhas: rotas com atraso acima da média
  - Espessura propproporcional ao volume
  - Bolhas azuis nos hubs (tamanho = volume)

- **Slider interativo**: Controle de quantas rotas exibir (10 até todas)
- **Legenda visual**: Explicação das cores e símbolos
- **Nota explicativa**: Esclarecimento sobre coordenadas simuladas vs. dados reais no hover

#### Diagrama de Fluxo: Origem → Transportadora
- **Sankey Diagram**: Visualização de fluxo de pedidos
- Tooltip: Explicação do diagrama
- Nós coloridos por hub/transportadora
- Links com opacidade suave

#### Mapa de Calor: Hub × Transportadora
- **Heatmap**: Volume de pedidos cruzando hubs e transportadoras
- Identificação de parcerias mais fortes
- Cores em escala de blues

### 💰 Aba 3: Análise de Custos

#### TreeMap de Custos por Região
- **Visualização hierárquica**: Cidade de Origem → Transportadora
- Tamanho proporcional ao custo total
- Cores por transportadora
- Identificação rápida de maiores custos

#### Custo Total por Hub
- **Gráfico de Barras**: Soma de custos por cidade de origem
- Comparação entre hubs
- Formato monetário brasileiro (R$)

#### Evolução Mensal dos Custos
- **Gráfico de Área**: Tendência de custos ao longo do tempo
- Empilhamento por transportadora
- Identificação de picos de gastos

#### Tabela de Eficiência
- **Ranking**: Melhores combinações Hub × Transportadora
- Métricas:
  - Volume de entregas
  - OTD %
  - Tempo médio
  - Custo médio
  - Custo total
- Top 15 combinações mais eficientes

### 🎯 Aba 4: Decisões para Gestão

**Insights automáticos baseados em análise de dados:**

#### 🏆 Performance de Transportadoras
- Melhor transportadora (maior OTD)
- Pior transportadora (menor OTD)
- Volume transportado por cada
- Justificativa com dados quantitativos

#### 💡 Oportunidades de Otimização de Custos
- Hub mais econômico
- Hub mais caro
- Diferença percentual entre eles
- Sugestão de redistribuição de rotas

#### ⚠️ Gargalos Identificados
- Hubs com maior taxa de atraso
- Volume de pedidos atrasados
- Recomendações: revisão de rotas, negociação com transportadoras

#### 📋 Recomendações Estratégicas
- **Renegociação de contratos**: Transportadoras com baixo OTD
- **Expansão de parcerias**: Transportadoras eficientes
- **Otimização de hubs**: Redistribuição para hubs mais eficientes
- **Análise de sazonalidade**: Identificação de meses críticos

## 📖 Como Usar

### 1. Configure os Filtros (Barra Lateral)
- **Período**: Defina data de início e fim (padrão: todo o período)
- **Transportadora**: Selecione uma ou múltiplas (padrão: todas)
- **Hub de Origem**: Escolha os hubs de interesse (padrão: todos)
- **Status**: Filtre por status de entrega (padrão: todos)

### 2. Analise os KPIs Principais
Veja métricas consolidadas no topo:
- OTD % (On-Time Delivery)
- Custo Total e Médio
- Volume e Destinos
- Tempo Médio e Taxa de Atraso

### 3. Explore as Abas de Análise

**Performance**: Identifique transportadoras mais eficientes e hubs críticos

**Mapa & Fluxos**: Visualize rotas geográficas e fluxos de distribuição

**Análise de Custos**: Descubra onde estão os maiores gastos e oportunidades

**Decisões**: Consulte insights automáticos e recomendações estratégicas

### 4. Interaja com os Gráficos
- **Hover**: Passe o mouse para ver detalhes
- **Zoom**: Clique e arraste no mapa
- **Filtros**: Use o slider de rotas no mapa
- **Legenda**: Clique para ocultar/mostrar séries

## ⚙️ Regras de Negócio

### Cálculo de OTD (On-Time Delivery)
- **Critério**: Pedido é "no prazo" quando `prazo_real_dias ≤ prazo_estimado_dias`
- **Cálculo**: `(pedidos_no_prazo / total_pedidos) × 100`
- **Cor do indicador**:
  - 🟢 Verde: OTD ≥ 70%
  - 🟡 Amarelo: 50% ≤ OTD < 70%
  - 🔴 Vermelho: OTD < 50%

### Classificação de Atraso
- **Pedido Atrasado**: `prazo_real_dias > prazo_estimado_dias`
- **Atraso em Dias**: `prazo_real_dias - prazo_estimado_dias`
- **Rota com Atraso** (no mapa): Atraso médio acima da média global

### Custos Logísticos
- **Custo Total**: Soma de todos os `custo_transporte` no período
- **Custo Médio**: `custo_total / quantidade_pedidos`
- **Formato**: R$ (moeda brasileira)

### Coordenadas do Mapa
- **Hubs de Origem**: Coordenadas geográficas reais das 5 cidades
- **Destinos**: Posições simuladas (hash determinístico) dentro do território brasileiro
  - Respeitam fronteiras leste (costa) e oeste (divisas)
  - Distribuídas uniformemente para visualização
  - **Dados reais no hover**: Volume, Atraso médio, Custo total

### Agregação de Dados
- **Por Transportadora**: Agrupamento por `transportadora`
- **Por Hub**: Agrupamento por `cidade_origem`
- **Por Rota**: Combinação `cidade_origem` + `cidade_destino`
- **Temporal**: Agregação mensal para gráficos de tendência

**Desenvolvido para**: Fundamentos em Ciência de Dados - 2025.2  
**Tecnologia**: Python + Streamlit + Plotly
