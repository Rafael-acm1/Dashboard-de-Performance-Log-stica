# Dashboard de Performance Logística 🚚

Dashboard interativo para análise de eficiência logística, permitindo aos gestores monitorar entregas, identificar gargalos e avaliar custos de transporte por região.

Sistema desenvolvido para gerenciamento estratégico de operações logísticas, oferecendo visão completa de transportadoras, performance de hubs e otimização de rotas.

**Disciplina:** Fundamentos em Ciência de Dados  
**Professor:** Assuero Ximenes  
**Período:** 2025.2

## 🚀 Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit** - Framework para interface web interativa
- **Pandas** - Manipulação e análise de dados
- **Plotly Express & Graph Objects** - Visualizações interativas e mapas
- **NumPy** - Operações numéricas
- **Hashlib** - Geração determinística de coordenadas simuladas

## 📦 Instalação

### 1. Instalar Python
Certifique-se de ter o Python 3.8 ou superior instalado.

### 2. Instalar Dependências

**Opção 1 - Usando requirements.txt:**
```powershell
pip install -r requirements.txt
```

**Opção 2 - Instalação manual:**
```powershell
pip install streamlit pandas plotly numpy
```

## 🎯 Execução

No diretório do projeto, execute:

```powershell
streamlit run app.py
```

O dashboard será aberto automaticamente no navegador em `http://localhost:8501`

Para encerrar, pressione `Ctrl+C` no terminal.

## 📁 Estrutura de Arquivos

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

## 🎨 Design

- **Layout**: Wide mode com sidebar
- **Tema**: Profissional com fundo branco
- **Cores**:
  - Azul (#2563EB): Destaque principal
  - Verde (#16A34A): Sucesso/No prazo
  - Vermelho (#DC2626): Crítico/Atrasado
  - Amarelo (#D97706): Atenção
- **Tipografia**: Inter, sans-serif
- **Ícones**: SVG inline (estilo Lucide)
- **Responsivo**: Colunas adaptáveis

## 📊 Estrutura da Base de Dados

**Arquivo**: `FCD_logistica.csv`  
**Separador**: Ponto-e-vírgula (;)  
**Encoding**: UTF-8  
**Registros**: 8.001 linhas

### Colunas:
- `pedido_id`: Identificador único do pedido
- `data_pedido`: Data do pedido (formato: dd/mm/yyyy)
- `data_entrega`: Data da entrega (formato: dd/mm/yyyy)
- `transportadora`: Nome da transportadora (Correios, Jadlog, Loggi, Azul Cargo)
- `cidade_origem`: Hub de origem (São Paulo, Curitiba, Belo Horizonte, Salvador, Recife)
- `cidade_destino`: Cidade de destino (446 cidades fictícias)
- `prazo_estimado_dias`: Prazo previsto em dias
- `prazo_real_dias`: Prazo real em dias
- `custo_transporte`: Custo do frete (float)
- `status_entrega`: Status (Entregue, Devolvido, Em trânsito)

### Colunas Derivadas (calculadas no código):
- `atraso_dias`: `prazo_real_dias - prazo_estimado_dias`
- `no_prazo`: Booleano (True se atraso ≤ 0)
- `atrasado`: Booleano (True se atraso > 0)
- `mes`: Mês de referência (formato: YYYY-MM)

## 🎯 Objetivo do Projeto

Fornecer aos gestores logísticos uma ferramenta de **Business Intelligence** que permita:

1. **Avaliar a eficiência das transportadoras**
   - Comparar OTD, tempo médio e custos
   - Identificar parcerias mais vantajosas

2. **Identificar gargalos logísticos**
   - Hubs com maior taxa de atraso
   - Rotas problemáticas
   - Períodos críticos

3. **Planejar ações para reduzir custos**
   - Otimizar distribuição entre hubs
   - Negociar melhores tarifas
   - Redirecionar rotas

4. **Melhorar prazos de entrega**
   - Focar em transportadoras eficientes
   - Revisar estimativas de prazo
   - Implementar melhorias operacionais

## 📝 Observações Técnicas

- **Cache**: Função `load_data()` usa `@st.cache_data` para performance
- **Parsing de datas**: Formato brasileiro `%d/%m/%Y`
- **Tratamento de dados**: Remoção de valores nulos em colunas críticas
- **Visualizações**: Todas com `theme=None` para evitar conflito com tema dark do Streamlit
- **Template Plotly**: `plotly_white` para melhor legibilidade
- **Responsividade**: Uso de `width='stretch'` em todos os gráficos

## 🏆 Componentes Implementados

Todos os requisitos do projeto foram atendidos:

✅ **a) KPI de Entregas no Prazo (%)** - Card de OTD com cor dinâmica  
✅ **b) Tempo Médio de Entrega por Transportadora** - Gráfico de barras comparativo  
✅ **c) Mapa Interativo com Fluxos Origem-Destino** - Mapa geográfico com rotas e volume  
✅ **d) Custos Logísticos por Região** - TreeMap, gráficos e tabela de eficiência  
✅ **e) Decisões para Gestores** - Tab completa com insights e recomendações automáticas

## 📞 Suporte

Para dúvidas sobre execução ou funcionalidades, consulte:
- Esta documentação (README.md)
- Comentários no código-fonte (app.py)
- Professor da disciplina

---

**Desenvolvido para**: Fundamentos em Ciência de Dados - 2025.2  
**Tecnologia**: Python + Streamlit + Plotly
