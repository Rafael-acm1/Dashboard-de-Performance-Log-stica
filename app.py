import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Performance Logística",
    layout="wide",
    initial_sidebar_state="expanded",
)


ACCENT       = "#2563EB"
ACCENT_DARK  = "#1D4ED8"
ACCENT_LIGHT = "#DBEAFE"
SUCCESS      = "#16A34A"
DANGER       = "#DC2626"
WARNING      = "#D97706"
NEUTRAL      = "#64748B"
TEXT_DARK    = "#0F172A"

HUB_COORDS = {
    "São Paulo":      {"lat": -23.55, "lon": -46.63},
    "Curitiba":       {"lat": -25.43, "lon": -49.27},
    "Belo Horizonte": {"lat": -19.92, "lon": -43.93},
    "Salvador":       {"lat": -12.97, "lon": -38.51},
    "Recife":         {"lat":  -8.05, "lon": -34.88},
}

COLOR_TRANSPORT = {
    "Correios":   "#2563EB",
    "Jadlog":     "#7C3AED",
    "Loggi":      "#0891B2",
    "Azul Cargo": "#059669",
}

CHART_LAYOUT = dict(
    template="plotly_white",
    font=dict(family="Inter, sans-serif", color="#1E293B", size=13),
    paper_bgcolor="white",
    plot_bgcolor="#FAFBFC",
    margin=dict(l=40, r=24, t=64, b=40),
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter", font_color="#1E293B"),
    title_font=dict(size=16, color="#0F172A", family="Inter, sans-serif"),
    legend=dict(font=dict(size=12, color="#1E293B")),
    coloraxis_colorbar=dict(tickfont=dict(color="#334155"), title_font=dict(color="#1E293B")),
    separators=",.",
)

AXIS_STYLE = dict(
    tickfont=dict(color="#334155", size=12),
    title_font=dict(color="#1E293B", size=13),
)

def _apply_axis_style(fig):
    """Aplica cores escuras nos eixos X e Y de um gráfico."""
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig

def fmt_brl(val, decimals=2):
    """Formata valor em Reais: R$ 1.234,56"""
    s = f"{val:,.{decimals}f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$&nbsp;{s}"


def fmt_num(val, decimals=0):
    """Formata número com separador de milhar: 1.234"""
    s = f"{val:,.{decimals}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def _icon(name, size=18, color="#F4B433"):
    """Retorna SVG inline (estilo Lucide) pelo nome."""
    svgs = {
        "check-circle": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>'
            '<polyline points="22 4 12 14.01 9 11.01"/></svg>'
        ),
        "dollar-sign": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<line x1="12" y1="1" x2="12" y2="23"/>'
            '<path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>'
        ),
        "package": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/>'
            '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8'
            'a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>'
            '<polyline points="3.27 6.96 12 12.01 20.73 6.96"/>'
            '<line x1="12" y1="22.08" x2="12" y2="12"/></svg>'
        ),
        "alert-triangle": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>'
            '<line x1="12" y1="9" x2="12" y2="13"/>'
            '<line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
        ),
        "truck": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/>'
            '<path d="M15 18H9"/>'
            '<path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/>'
            '<circle cx="7" cy="18" r="2"/><circle cx="21" cy="18" r="2"/></svg>'
        ),
        "clock": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="12" cy="12" r="10"/>'
            '<polyline points="12 6 12 12 16 14"/></svg>'
        ),
        "map-pin": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/>'
            '<circle cx="12" cy="10" r="3"/></svg>'
        ),
        "bar-chart": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<line x1="18" y1="20" x2="18" y2="10"/>'
            '<line x1="12" y1="20" x2="12" y2="4"/>'
            '<line x1="6" y1="20" x2="6" y2="14"/></svg>'
        ),
        "trending-up": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>'
            '<polyline points="16 7 22 7 22 13"/></svg>'
        ),
        "activity": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
        ),
        "target": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/>'
            '<circle cx="12" cy="12" r="2"/></svg>'
        ),
        "filter": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>'
        ),
        "zap": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
        ),
    }
    return svgs.get(name, "")


def kpi_card(icon_name, label, value, sub="", icon_color=NEUTRAL):
    """Retorna HTML de um card de KPI."""
    return f"""
    <div class="kpi-card">
        <div class="kpi-header">
            {_icon(icon_name, 16, icon_color)}
            <span class="kpi-label">{label}</span>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""


def section_title(icon_name, text):
    """Título de seção com ícone."""
    return f'<div class="section-title">{_icon(icon_name, 18, "#F4B433")} {text}</div>'


def insight_card(title, text, variant="default"):
    """Card de insight com borda lateral colorida."""
    cls = {"success": "success", "danger": "danger", "warning": "warning"}.get(variant, "")
    return f"""
    <div class="insight-card {cls}">
        <div class="insight-title">{title}</div>
        <div class="insight-text">{text}</div>
    </div>"""


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 0;
        max-width: 100%;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        border-right: 1px solid #334155;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] label {
        color: #CBD5E1 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stDateInput label {
        color: #94A3B8 !important;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ── Ocultar elementos padrão ── */
    #MainMenu, footer, header {visibility: hidden;}

    /* ── KPI Cards ── */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 1px 3px 0 rgba(0,0,0,0.04);
        transition: box-shadow 0.2s;
    }
    .kpi-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);
    }
    .kpi-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.2;
        margin-bottom: 4px;
    }
    .kpi-sub {
        font-size: 12px;
        color: #94A3B8;
        font-weight: 500;
    }

    /* ── Header ── */
    .dash-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 4px;
    }
    .dash-title {
        font-size: 26px;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
    }
    .dash-badge {
        background: #DBEAFE;
        color: #2563EB;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .dash-subtitle {
        font-size: 14px;
        color: #F4B433;
        margin-bottom: 20px;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 2px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 13px;
        color: #64748B;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        color: #2563EB !important;
    }

    /* ── Seções & Insights ── */
    .section-title {
        font-size: 16px;
        font-weight: 600;
        color: #F4B433;
        margin: 16px 0 12px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .insight-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #2563EB;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .insight-card.warning { border-left-color: #D97706; }
    .insight-card.danger  { border-left-color: #DC2626; }
    .insight-card.success { border-left-color: #16A34A; }
    .insight-title {
        font-size: 14px;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 4px;
    }
    .insight-text {
        font-size: 13px;
        color: #475569;
        line-height: 1.6;
    }

    /* ── Plotly wrapper ── */
    .stPlotlyChart {
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        overflow: hidden;
    }

    hr { border: none; border-top: 1px solid #E2E8F0; margin: 16px 0; }

    /* ── Force Plotly text to dark ── */
    .stPlotlyChart text {
        fill: #1E293B !important;
    }
    .stPlotlyChart .gtitle {
        fill: #0F172A !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Carrega, valida e enriquece o dataset logístico."""
    try:
        df = pd.read_csv("FCD_logistica.csv", sep=";", encoding="utf-8")
    except FileNotFoundError:
        st.error("Arquivo **FCD_logistica.csv** não encontrado na raiz do projeto.")
        st.stop()
    except Exception as exc:
        st.error(f"Erro ao carregar dados: {exc}")
        st.stop()

    # Conversão de tipos
    df["data_pedido"]  = pd.to_datetime(df["data_pedido"],  format="%d/%m/%Y", errors="coerce")
    df["data_entrega"] = pd.to_datetime(df["data_entrega"], format="%d/%m/%Y", errors="coerce")
    for col in ("prazo_estimado_dias", "prazo_real_dias", "custo_transporte"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Métricas derivadas
    df["atraso_dias"] = df["prazo_real_dias"] - df["prazo_estimado_dias"]
    df["no_prazo"]    = df["prazo_real_dias"] <= df["prazo_estimado_dias"]
    df["atrasado"]    = df["prazo_real_dias"] >  df["prazo_estimado_dias"]
    df["mes"]         = df["data_pedido"].dt.to_period("M").dt.to_timestamp()

    # Limpeza
    df = df.dropna(subset=["data_pedido", "prazo_real_dias", "custo_transporte"])
    return df


df_raw = load_data()


with st.sidebar:
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:24px;'
        f'padding-bottom:16px;border-bottom:1px solid #334155;">'
        f'{_icon("truck", 28, "#60A5FA")}'
        f'<div><div style="font-size:18px;font-weight:700;color:#F1F5F9;">Dashboard</div>'
        f'<div style="font-size:11px;color:#64748B;font-weight:500;">Performance Logística</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:12px;">'
        f'{_icon("filter", 14, "#94A3B8")}'
        f'<span style="font-size:11px;font-weight:700;color:#94A3B8;'
        f'text-transform:uppercase;letter-spacing:1px;">Filtros</span></div>',
        unsafe_allow_html=True,
    )

    min_date = df_raw["data_pedido"].min().date()
    max_date = df_raw["data_pedido"].max().date()
    cd1, cd2 = st.columns(2)
    with cd1:
        data_inicio = st.date_input("De", value=min_date, min_value=min_date, max_value=max_date)
    with cd2:
        data_fim = st.date_input("Até", value=max_date, min_value=min_date, max_value=max_date)

    transportadoras = sorted(df_raw["transportadora"].dropna().unique())
    sel_transp = st.multiselect("Transportadora", transportadoras, default=transportadoras)

    hubs = sorted(df_raw["cidade_origem"].dropna().unique())
    sel_hubs = st.multiselect("Hub de Origem", hubs, default=hubs)

    statuses = sorted(df_raw["status_entrega"].dropna().unique())
    sel_status = st.multiselect("Status", statuses, default=statuses)

    st.markdown("---")
    st.markdown(
        f'<div style="font-size:11px;color:#475569;text-align:center;">'
        f'Base: {fmt_num(len(df_raw))} registros</div>',
        unsafe_allow_html=True,
    )

df = df_raw.copy()
df = df[
    (df["data_pedido"].dt.date >= data_inicio)
    & (df["data_pedido"].dt.date <= data_fim)
    & (df["transportadora"].isin(sel_transp))
    & (df["cidade_origem"].isin(sel_hubs))
    & (df["status_entrega"].isin(sel_status))
]

if df.empty:
    st.warning("Nenhum registro encontrado com os filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

total_pedidos = len(df)
custo_total   = df["custo_transporte"].sum()
custo_medio   = df["custo_transporte"].mean()
otd_pct       = df["no_prazo"].mean() * 100
tempo_medio   = df["prazo_real_dias"].mean()
atraso_medio  = df.loc[df["atrasado"], "atraso_dias"].mean() if df["atrasado"].any() else 0
pct_atrasados = df["atrasado"].mean() * 100


st.markdown(
    f'<div class="dash-header">{_icon("activity", 28, ACCENT)}'
    f'<h1 class="dash-title">Dashboard de Performance Logística</h1>'
    f'<span class="dash-badge">Live</span></div>'
    f'<p class="dash-subtitle">'
    f'Monitoramento de eficiência, prazos e custos &middot; '
    f'{data_inicio.strftime("%d/%m/%Y")} a {data_fim.strftime("%d/%m/%Y")} &middot; '
    f'{fmt_num(total_pedidos)} pedidos</p>',
    unsafe_allow_html=True,
)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    _c = SUCCESS if otd_pct >= 70 else (WARNING if otd_pct >= 50 else DANGER)
    st.markdown(
        kpi_card(
            "check-circle", "Entregas no Prazo (OTD)",
            f"{otd_pct:.1f}%".replace(".", ","),
            f"{fmt_num(df['no_prazo'].sum())} de {fmt_num(total_pedidos)} pedidos",
            _c,
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:10px;color:#94A3B8;margin-top:-8px;padding-left:12px;">' 
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:10px;color:#94A3B8;margin-top:-8px;padding-left:12px;">' 
        '<i>% de pedidos entregues no prazo</i></div>',
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        kpi_card(
            "dollar-sign", "Custo Total de Frete",
            fmt_brl(custo_total, 0),
            f"Médio: {fmt_brl(custo_medio)} / pedido",
            ACCENT,
        ),
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        kpi_card(
            "package", "Volume de Pedidos",
            fmt_num(total_pedidos),
            f"{fmt_num(df['cidade_destino'].nunique())} destinos únicos",
            ACCENT,
        ),
        unsafe_allow_html=True,
    )

with k4:
    st.markdown(
        kpi_card(
            "clock", "Tempo Médio de Entrega",
            f"{tempo_medio:.1f} dias".replace(".", ","),
            f"Prazo estimado médio: {df['prazo_estimado_dias'].mean():.1f} dias".replace(".", ","),
            WARNING,
        ),
        unsafe_allow_html=True,
    )

with k5:
    _c = DANGER if pct_atrasados > 30 else (WARNING if pct_atrasados > 15 else SUCCESS)
    st.markdown(
        kpi_card(
            "alert-triangle", "Taxa de Atraso",
            f"{pct_atrasados:.1f}%".replace(".", ","),
            f"Atraso médio: {atraso_medio:.1f} dias (quando atrasa)".replace(".", ","),
            _c,
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:10px;color:#94A3B8;margin-top:-8px;padding-left:12px;">' 
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:10px;color:#94A3B8;margin-top:-8px;padding-left:12px;">' 
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)


tab_perf, tab_mapa, tab_custo, tab_decisao = st.tabs([
    "  Performance  ",
    "  Mapa & Fluxos  ",
    "  Análise de Custos  ",
    "  Decisões para Gestão  ",
])

with tab_perf:
    col_a, col_b = st.columns(2)

    with col_a:
        df_tempo = (
            df.groupby("transportadora")["prazo_real_dias"]
            .mean().reset_index()
            .sort_values("prazo_real_dias", ascending=True)
        )
        fig = px.bar(
            df_tempo, x="prazo_real_dias", y="transportadora",
            orientation="h",
            text=df_tempo["prazo_real_dias"].apply(lambda v: f"{v:.1f} dias".replace(".", ",")),
            color="transportadora", color_discrete_map=COLOR_TRANSPORT,
        )
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(
            **CHART_LAYOUT,
            title="Tempo Médio de Entrega por Transportadora",
            xaxis_title="Dias", yaxis_title="",
            showlegend=False, height=350,
        )
        _apply_axis_style(fig)
        st.plotly_chart(fig, width='stretch', theme=None)

    with col_b:
        df_otd = (
            df.groupby("transportadora")["no_prazo"]
            .mean().mul(100).reset_index()
            .rename(columns={"no_prazo": "otd"})
            .sort_values("otd", ascending=True)
        )
        fig = px.bar(
            df_otd, x="otd", y="transportadora",
            orientation="h",
            text=df_otd["otd"].apply(lambda v: f"{v:.1f}%".replace(".", ",")),
            color="transportadora", color_discrete_map=COLOR_TRANSPORT,
        )
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(
            **CHART_LAYOUT,
            title="Taxa de Entrega no Prazo (OTD) por Transportadora<br><sub style='font-size:11px;color:#94A3B8;font-weight:400;'>OTD = On-Time Delivery (% de pedidos entregues no prazo ou antes)</sub>",
            xaxis_title="OTD (%)", yaxis_title="",
            showlegend=False, height=350,
        )
        fig.update_xaxes(range=[0, max(df_otd["otd"].max() * 1.15, 100)])
        _apply_axis_style(fig)
        st.plotly_chart(fig, width='stretch', theme=None)

    # ── Evolução Mensal do OTD ──
    st.markdown(section_title("trending-up", "Evolução Mensal do OTD (% de pedidos entregues no prazo)"), unsafe_allow_html=True)

    df_trend = (
        df.groupby([df["mes"], "transportadora"])["no_prazo"]
        .mean().mul(100).reset_index()
        .rename(columns={"no_prazo": "otd"})
    )
    fig = px.line(
        df_trend, x="mes", y="otd", color="transportadora",
        color_discrete_map=COLOR_TRANSPORT, markers=True,
    )
    fig.update_layout(
        **CHART_LAYOUT,
        title="Evolução da Taxa OTD ao Longo do Tempo",
        xaxis_title="", yaxis_title="OTD (%)", height=360,
        legend_title="Transportadora", hovermode="x unified",
    )
    fig.update_traces(line_width=2.5)
    _apply_axis_style(fig)
    st.plotly_chart(fig, width='stretch', theme=None)

    st.markdown(section_title("map-pin", "Performance por Hub de Origem"), unsafe_allow_html=True)

    df_hub = (
        df.groupby("cidade_origem")
        .agg(
            volume=("pedido_id", "count"),
            otd=("no_prazo", "mean"),
            tempo=("prazo_real_dias", "mean"),
            custo=("custo_transporte", "mean"),
        )
        .reset_index()
        .sort_values("volume", ascending=False)
    )

    hub_cols = st.columns(len(df_hub))
    for i, (_, r) in enumerate(df_hub.iterrows()):
        otd_val = r["otd"] * 100
        otd_c = SUCCESS if otd_val >= 70 else (WARNING if otd_val >= 50 else DANGER)
        with hub_cols[i]:
            st.markdown(
                f"""<div class="kpi-card" style="text-align:center;">
                <div style="font-size:14px;font-weight:700;color:#1E293B;margin-bottom:8px;">
                    {r['cidade_origem']}</div>
                <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748B;margin-bottom:4px;">
                    <span>Volume</span><span style="font-weight:600;color:#1E293B;">{fmt_num(r['volume'])}</span></div>
                <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748B;margin-bottom:4px;">
                    <span>OTD</span><span style="font-weight:600;color:{otd_c};">{otd_val:.1f}%</span></div>
                <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748B;margin-bottom:4px;">
                    <span>Tempo</span><span style="font-weight:600;color:#1E293B;">{r['tempo']:.1f} dias</span></div>
                <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748B;">
                    <span>Custo</span><span style="font-weight:600;color:#1E293B;">{fmt_brl(r['custo'], 0)}</span></div>
                </div>""",
                unsafe_allow_html=True,
            )


with tab_mapa:

    # ── Função auxiliar: gerar coordenada determinística para cidade fictícia ──
    # Fronteira LESTE (costa) e OESTE (divisa) simplificadas (lat → lon)
    _COAST_EAST = [
        (-33.0, -52.5), (-30.0, -50.2), (-28.0, -48.6), (-26.0, -48.5),
        (-25.3, -48.3), (-24.0, -46.3), (-23.0, -43.5), (-22.0, -41.0),
        (-20.0, -40.0), (-18.0, -39.5), (-16.0, -39.0), (-14.0, -38.9),
        (-13.0, -38.5), (-10.0, -36.5), (-8.0,  -34.9), (-5.0,  -35.2),
        (-3.0,  -38.5), (-1.0,  -44.0), (0.0,   -48.0), (2.0,   -50.0),
        (4.5,   -51.5),
    ]
    _BORDER_WEST = [
        (-33.0, -57.5), (-30.0, -57.0), (-28.0, -56.0), (-26.0, -54.5),
        (-24.0, -54.5), (-22.0, -55.0), (-20.0, -57.5), (-18.0, -58.0),
        (-16.0, -59.0), (-14.0, -60.0), (-12.0, -62.0), (-10.0, -65.5),
        (-8.0,  -67.0), (-6.0,  -69.5), (-4.0,  -70.0), (-2.0,  -70.0),
        (0.0,   -69.5), (2.0,   -64.0), (4.5,   -60.5),
    ]

    def _interp_border(lat, border_pts):
        """Interpola longitude de uma fronteira para dada latitude."""
        lats = [p[0] for p in border_pts]
        lons = [p[1] for p in border_pts]
        if lat <= lats[0]:
            return lons[0]
        if lat >= lats[-1]:
            return lons[-1]
        for i in range(len(lats) - 1):
            if lats[i] <= lat <= lats[i + 1]:
                t = (lat - lats[i]) / (lats[i + 1] - lats[i])
                return lons[i] + t * (lons[i + 1] - lons[i])
        return -47.0

    @st.cache_data
    def _dest_coords(cidade_destino, cidade_origem):
        """Gera lat/lon simulada para destino, dentro do território brasileiro."""
        hub = HUB_COORDS.get(cidade_origem, {"lat": -15.0, "lon": -47.0})

        # Hash determinístico
        h = int(hashlib.md5(cidade_destino.encode()).hexdigest(), 16)
        h2 = int(hashlib.md5((cidade_destino + "_v2").encode()).hexdigest(), 16)

        # Espalhar: lat ±5 graus, lon até -10 graus para oeste
        lat_offset = ((h % 1000) / 1000 - 0.5) * 10.0       # -5 a +5 graus
        lon_offset = -((h2 % 10000) / 10000 * 9.0 + 1.0)    # -1 a -10 graus (sempre oeste)

        lat = hub["lat"] + lat_offset
        lon = hub["lon"] + lon_offset

       
        lat = np.clip(lat, -32.5, 4.0)

        
        east_lon = _interp_border(lat, _COAST_EAST)
        west_lon = _interp_border(lat, _BORDER_WEST)

        east_limit = east_lon - 0.8
        west_limit = west_lon + 0.8

        if lon > east_limit:
            frac = (h % 5000) / 5000
            lon = west_limit + frac * (east_limit - west_limit)
        elif lon < west_limit:
            frac = (h2 % 5000) / 5000
            lon = west_limit + frac * (east_limit - west_limit)

        return lat, lon

    st.markdown(section_title("map-pin", "Mapa Interativo — Fluxos Origem → Destino"), unsafe_allow_html=True)

    df_routes = (
        df.groupby(["cidade_origem", "cidade_destino"])
        .agg(
            volume=("pedido_id", "count"),
            atraso_medio=("atraso_dias", "mean"),
            atrasado_pct=("atrasado", "mean"),
            custo_total=("custo_transporte", "sum"),
        )
        .reset_index()
    )
    avg_atraso_global = df_routes["atraso_medio"].mean()

    dest_coords = df_routes.apply(
        lambda r: _dest_coords(r["cidade_destino"], r["cidade_origem"]), axis=1
    )
    df_routes["dest_lat"] = [c[0] for c in dest_coords]
    df_routes["dest_lon"] = [c[1] for c in dest_coords]
    df_routes["orig_lat"] = df_routes["cidade_origem"].map(lambda x: HUB_COORDS[x]["lat"])
    df_routes["orig_lon"] = df_routes["cidade_origem"].map(lambda x: HUB_COORDS[x]["lon"])
    df_routes["is_delayed"] = df_routes["atraso_medio"] > avg_atraso_global

    total_routes = len(df_routes)
    top_n = st.slider(
        "Rotas exibidas (por volume)", min_value=10, max_value=total_routes,
        value=max(10, total_routes // 2), step=10,
        help=f"Total de rotas: {total_routes}. Exibe as top N por volume. Arraste até o fim para ver todas.",
    )
    df_top = df_routes.nlargest(top_n, "volume")

    fig = go.Figure()

    df_ok = df_top[~df_top["is_delayed"]]
    for _, r in df_ok.iterrows():
        fig.add_trace(go.Scattergeo(
            lat=[r["orig_lat"], r["dest_lat"]],
            lon=[r["orig_lon"], r["dest_lon"]],
            mode="lines",
            line=dict(width=max(0.5, r["volume"] / df_top["volume"].max() * 3), color="rgba(37,99,235,0.3)"),
            hoverinfo="text",
            text=f"<b>{r['cidade_origem']} → {r['cidade_destino']}</b><br>"
                 f"Volume: {r['volume']}<br>"
                 f"Atraso médio: {r['atraso_medio']:.1f} dias<br>"
                 f"Custo total: {fmt_brl(r['custo_total'], 0)}",
            showlegend=False,
        ))

    df_delay = df_top[df_top["is_delayed"]]
    for _, r in df_delay.iterrows():
        fig.add_trace(go.Scattergeo(
            lat=[r["orig_lat"], r["dest_lat"]],
            lon=[r["orig_lon"], r["dest_lon"]],
            mode="lines",
            line=dict(width=max(0.8, r["volume"] / df_top["volume"].max() * 3.5), color="rgba(220,38,38,0.4)"),
            hoverinfo="text",
            text=f"<b>{r['cidade_origem']} → {r['cidade_destino']}</b><br>"
                 f"Volume: {r['volume']}<br>"
                 f"Atraso médio: {r['atraso_medio']:.1f} dias ⚠<br>"
                 f"Custo total: {fmt_brl(r['custo_total'], 0)}",
            showlegend=False,
        ))

    fig.add_trace(go.Scattergeo(
        lat=df_top["dest_lat"], lon=df_top["dest_lon"],
        mode="markers",
        marker=dict(
            size=4, color=df_top["is_delayed"].map({True: DANGER, False: "#93C5FD"}),
            opacity=0.6, line=dict(width=0),
        ),
        hoverinfo="skip", showlegend=False,
    ))

    df_hub_map = (
        df.groupby("cidade_origem")
        .agg(volume=("pedido_id", "count"), otd=("no_prazo", "mean"))
        .reset_index()
    )
    df_hub_map["lat"] = df_hub_map["cidade_origem"].map(lambda x: HUB_COORDS[x]["lat"])
    df_hub_map["lon"] = df_hub_map["cidade_origem"].map(lambda x: HUB_COORDS[x]["lon"])

    fig.add_trace(go.Scattergeo(
        lat=df_hub_map["lat"], lon=df_hub_map["lon"],
        text=df_hub_map.apply(
            lambda r: f"<b>Hub: {r['cidade_origem']}</b><br>"
                      f"Volume: {fmt_num(r['volume'])}<br>"
                      f"OTD: {r['otd']*100:.1f}%", axis=1
        ),
        hoverinfo="text",
        marker=dict(
            size=df_hub_map["volume"] / df_hub_map["volume"].max() * 30 + 14,
            color="#1E40AF", opacity=0.95,
            line=dict(width=3, color="white"), sizemode="diameter",
            symbol="circle",
        ),
        showlegend=False,
    ))

    
    fig.add_trace(go.Scattergeo(
        lat=df_hub_map["lat"] + 1.0, lon=df_hub_map["lon"],
        text=df_hub_map["cidade_origem"], mode="text",
        textfont=dict(size=12, color="#0F172A", family="Inter"),
        hoverinfo="skip", showlegend=False,
    ))

    fig.update_geos(
        scope="south america",
        showland=True, landcolor="#F1F5F9",
        showocean=True, oceancolor="#EFF6FF",
        showcountries=True, countrycolor="#CBD5E1",
        showcoastlines=True, coastlinecolor="#94A3B8",
        showframe=False,
        lonaxis_range=[-58, -28], lataxis_range=[-34, 2],
        bgcolor="white",
    )
    fig.update_layout(
        **CHART_LAYOUT, height=600, showlegend=False,
        title="Fluxos de Entrega — Origem (Hubs) → Destinos",
        geo=dict(bgcolor="white"),
    )
    st.markdown(
        '<div style="font-size:12px;color:#475569;padding:10px 14px;margin-top:8px;'
        'background:#FFFBEB;border-radius:6px;border:1px solid #FDE68A;line-height:1.7;">'
        '<span style="font-weight:600;color:#92400E;">Sobre a representação do mapa</span><br>'
        'As <b>posições geográficas das cidades de destino são simuladas</b>, pois os nomes '
        'das cidades são fictícios. Os pontos são distribuídos dentro do território brasileiro '
        'apenas para fins de visualização dos fluxos. '
        'No entanto, os <b>dados exibidos ao passar o mouse (hover) são reais</b>, '
        'extraídos diretamente da base de dados:<br>'
        '<span style="color:#1E40AF;font-weight:500;">• Rota</span> (origem → destino) · '
        '<span style="color:#1E40AF;font-weight:500;">• Volume</span> de entregas · '
        '<span style="color:#1E40AF;font-weight:500;">• Atraso médio</span> (dias) · '
        '<span style="color:#1E40AF;font-weight:500;">• Custo total</span> da rota<br>'
        'Os <b>hubs de origem</b> (São Paulo, Curitiba, Belo Horizonte, Salvador, Recife) '
        'estão posicionados em suas <b>coordenadas reais</b>.'
        '</div>',
        unsafe_allow_html=True,
    )
    
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    _apply_axis_style(fig)
    st.plotly_chart(fig, width='stretch', theme=None)

    
    st.markdown(
        f'<div style="font-size:11px;color:#94A3B8;padding:8px 12px;'
        f'background:#F8FAFC;border-radius:6px;border:1px solid #E2E8F0;line-height:1.8;">'
        f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;'
        f'background:#1E40AF;margin-right:4px;vertical-align:middle;"></span>'
        f'<span style="color:#1E40AF;font-weight:600;">Azul escuro</span> = Hub de origem (tamanho = volume) &nbsp;&middot;&nbsp; '
        f'<span style="display:inline-block;width:18px;height:2px;'
        f'background:#2563EB;margin-right:4px;vertical-align:middle;"></span>'
        f'<span style="color:#2563EB;font-weight:600;">Linha azul</span> = rota no prazo &nbsp;&middot;&nbsp; '
        f'<span style="display:inline-block;width:18px;height:2px;'
        f'background:#DC2626;margin-right:4px;vertical-align:middle;"></span>'
        f'<span style="color:#DC2626;font-weight:600;">Linha vermelha</span> = rota com atraso acima da média ({avg_atraso_global:.1f} dias) &nbsp;&middot;&nbsp; '
        f'Espessura = volume de entregas'
        f'</div>',
        unsafe_allow_html=True,
    )
    
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    col_sk, col_heat = st.columns([1, 1])

    with col_sk:
        st.markdown(section_title("activity", "Fluxo: Origem → Transportadora"), unsafe_allow_html=True)

        df_flow = (
            df.groupby(["cidade_origem", "transportadora"])
            .agg(volume=("pedido_id", "count"), taxa_atraso=("atrasado", "mean"))
            .reset_index()
        )
        origins  = sorted(df_flow["cidade_origem"].unique())
        transps  = sorted(df_flow["transportadora"].unique())
        nodes    = origins + transps
        node_idx = {n: i for i, n in enumerate(nodes)}

        avg_delay_rate = df_flow["taxa_atraso"].mean()

        fig = go.Figure(go.Sankey(
            node=dict(
                pad=20, thickness=22,
                line=dict(color="white", width=2),
                label=nodes,
                color=["#1E40AF"] * len(origins) + [COLOR_TRANSPORT.get(t, ACCENT) for t in transps],
            ),
            link=dict(
                source=[node_idx[r["cidade_origem"]] for _, r in df_flow.iterrows()],
                target=[node_idx[r["transportadora"]] for _, r in df_flow.iterrows()],
                value=df_flow["volume"].tolist(),
                color=[
                    "rgba(220,38,38,0.25)" if r["taxa_atraso"] > avg_delay_rate
                    else "rgba(37,99,235,0.12)"
                    for _, r in df_flow.iterrows()
                ],
            ),
        ))
        fig.update_layout(
            **CHART_LAYOUT, height=450,
            title=dict(text="Fluxo de Pedidos por Rota", font=dict(size=16, color="#0F172A")),
        )
        _apply_axis_style(fig)
        st.plotly_chart(fig, width='stretch', theme=None)

        st.markdown(
            f'<div style="font-size:11px;color:#94A3B8;padding:8px 12px;'
            f'background:#F8FAFC;border-radius:6px;border:1px solid #E2E8F0;">'
            f'{_icon("alert-triangle", 12, DANGER)} '
            f'<span style="color:#DC2626;font-weight:600;">Vermelho</span> = taxa de atraso acima da média '
            f'({avg_delay_rate*100:.1f}%) &nbsp;&middot;&nbsp; '
            f'{_icon("check-circle", 12, ACCENT)} '
            f'<span style="color:#2563EB;font-weight:600;">Azul</span> = dentro da média</div>',
            unsafe_allow_html=True,
        )

    with col_heat:
        st.markdown(
            section_title("target", "Mapa de Calor — Atraso Médio (dias)"),
            unsafe_allow_html=True,
        )

        df_heat = df.pivot_table(
            index="cidade_origem", columns="transportadora",
            values="atraso_dias", aggfunc="mean",
        ).round(1)

        fig = px.imshow(
            df_heat, text_auto=True,
            color_continuous_scale=["#DBEAFE", "#2563EB", "#DC2626"],
            aspect="auto",
        )
        fig.update_layout(
            **CHART_LAYOUT,
            title="Hub × Transportadora",
            xaxis_title="Transportadora", yaxis_title="Hub de Origem",
            height=450, coloraxis_colorbar_title="Dias",
        )
        _apply_axis_style(fig)
        st.plotly_chart(fig, width='stretch', theme=None)


with tab_custo:
    col_tree, col_bar = st.columns([3, 2])

    with col_tree:
        st.markdown(
            section_title("bar-chart", "Custo Logístico por Hub e Transportadora"),
            unsafe_allow_html=True,
        )
        df_tree = (
            df.groupby(["cidade_origem", "transportadora"])["custo_transporte"]
            .sum().reset_index()
        )
        fig = px.treemap(
            df_tree, path=["cidade_origem", "transportadora"],
            values="custo_transporte", color="custo_transporte",
            color_continuous_scale=["#DBEAFE", "#2563EB", "#1E40AF"],
        )
        fig.update_layout(
            **CHART_LAYOUT, title="Distribuição do Custo Total de Frete",
            height=460, coloraxis_colorbar_title="Custo (R$)",
        )
        fig.update_traces(
            textinfo="label+value",
            texttemplate="%{label}<br>R$ %{value:,.0f}",
            textfont=dict(size=12, color="#FFFFFF"),
        )
        _apply_axis_style(fig)
        st.plotly_chart(fig, width='stretch', theme=None)

    with col_bar:
        st.markdown(
            section_title("truck", "Custo Médio por Transportadora"),
            unsafe_allow_html=True,
        )
        df_ct = (
            df.groupby("transportadora")["custo_transporte"]
            .mean().reset_index()
            .sort_values("custo_transporte", ascending=True)
        )
        fig = px.bar(
            df_ct, x="custo_transporte", y="transportadora",
            orientation="h",
            text=df_ct["custo_transporte"].apply(lambda v: fmt_brl(v)),
            color="transportadora", color_discrete_map=COLOR_TRANSPORT,
        )
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(
            **CHART_LAYOUT, title="Custo Médio por Entrega",
            xaxis_title="R$", yaxis_title="",
            showlegend=False, height=460,
        )
        _apply_axis_style(fig)
        st.plotly_chart(fig, width='stretch', theme=None)

    st.markdown(
        section_title("trending-up", "Evolução Mensal do Custo de Frete"),
        unsafe_allow_html=True,
    )
    df_cm = (
        df.groupby([df["mes"], "transportadora"])["custo_transporte"]
        .sum().reset_index()
    )
    fig = px.area(
        df_cm, x="mes", y="custo_transporte",
        color="transportadora", color_discrete_map=COLOR_TRANSPORT,
    )
    fig.update_layout(
        **CHART_LAYOUT,
        title="Custo Total de Frete por Mês",
        xaxis_title="", yaxis_title="R$", height=360,
        legend_title="Transportadora", hovermode="x unified",
    )
    _apply_axis_style(fig)
    st.plotly_chart(fig, width='stretch', theme=None)

    st.markdown(section_title("target", "Eficiência de Custo por Hub"), unsafe_allow_html=True)

    df_eff = (
        df.groupby("cidade_origem")
        .agg(
            custo_total=("custo_transporte", "sum"),
            custo_medio=("custo_transporte", "mean"),
            volume=("pedido_id", "count"),
            otd=("no_prazo", "mean"),
        )
        .reset_index()
    )
    df_eff["custo_por_entrega_otd"] = df_eff["custo_total"] / (df_eff["otd"] * df_eff["volume"])
    df_eff["otd"]                   = (df_eff["otd"] * 100).round(1)
    df_eff["custo_medio"]           = df_eff["custo_medio"].round(2)
    df_eff["custo_total"]           = df_eff["custo_total"].round(2)
    df_eff["custo_por_entrega_otd"] = df_eff["custo_por_entrega_otd"].round(2)
    df_eff.columns = [
        "Hub", "Custo Total (R$)", "Custo Médio (R$)",
        "Volume", "OTD (%)", "Custo / Entrega no Prazo (R$)",
    ]
    st.dataframe(df_eff, width='stretch', hide_index=True)


with tab_decisao:
    st.markdown(
        section_title("zap", "Insights Automáticos para Tomada de Decisão"),
        unsafe_allow_html=True,
    )

    grp_transp_otd   = df.groupby("transportadora")["no_prazo"].mean()
    grp_transp_custo = df.groupby("transportadora")["custo_transporte"].mean()
    grp_hub_otd      = df.groupby("cidade_origem")["no_prazo"].mean()

    best_t   = grp_transp_otd.idxmax()
    best_tv  = grp_transp_otd.max() * 100
    worst_t  = grp_transp_otd.idxmin()
    worst_tv = grp_transp_otd.min() * 100

    cheap_t  = grp_transp_custo.idxmin()
    cheap_v  = grp_transp_custo.min()
    expen_t  = grp_transp_custo.idxmax()
    expen_v  = grp_transp_custo.max()

    best_h   = grp_hub_otd.idxmax()
    best_hv  = grp_hub_otd.max() * 100
    worst_h  = grp_hub_otd.idxmin()
    worst_hv = grp_hub_otd.min() * 100

    df_combo = (
        df.groupby(["cidade_origem", "transportadora"])
        .agg(otd=("no_prazo", "mean"), volume=("pedido_id", "count"), atraso=("atraso_dias", "mean"))
        .reset_index()
    )
    worst_combo = df_combo.loc[df_combo["otd"].idxmin()]
    best_combo  = df_combo.loc[df_combo["otd"].idxmax()]

    ci1, ci2 = st.columns(2)

    with ci1:
        st.markdown(
            f'<div style="font-size:15px;font-weight:700;color:#0F69F2;margin-bottom:12px;">'
            f'{_icon("truck", 18, "#0F69F2")} Eficiência das Transportadoras</div>',
            unsafe_allow_html=True,
        )
        st.markdown(insight_card(
            f"Melhor Transportadora: {best_t}",
            f"Taxa OTD de <b>{best_tv:.1f}%</b> — a mais alta entre todas. "
            f"Considere priorizá-la para rotas críticas e de alto valor.",
            "success",
        ), unsafe_allow_html=True)

        st.markdown(insight_card(
            f"Maior Taxa de Atraso: {worst_t}",
            f"Taxa OTD de apenas <b>{worst_tv:.1f}%</b>. Recomenda-se reunião de "
            f"alinhamento para renegociar SLAs ou avaliar alternativas.",
            "danger",
        ), unsafe_allow_html=True)

        st.markdown(insight_card(
            "Análise de Custo-Benefício",
            f"<b>{cheap_t}</b> tem o menor custo médio ({fmt_brl(cheap_v)}/entrega), enquanto "
            f"<b>{expen_t}</b> custa {fmt_brl(expen_v)}/entrega. "
            f"Diferença de <b>{fmt_brl(expen_v - cheap_v)}</b> por pedido.",
        ), unsafe_allow_html=True)

    with ci2:
        st.markdown(
            f'<div style="font-size:15px;font-weight:700;color:#0F69F2;margin-bottom:12px;">'
            f'{_icon("map-pin", 18, "#0F69F2")}  Gargalos Logísticos</div>',
            unsafe_allow_html=True,
        )
        st.markdown(insight_card(
            f"Hub com Pior Performance: {worst_h}",
            f"OTD de <b>{worst_hv:.1f}%</b>. Investigue causas: capacidade operacional, "
            f"infraestrutura viária ou distância média dos destinos.",
            "warning",
        ), unsafe_allow_html=True)

        st.markdown(insight_card(
            f"Pior Rota: {worst_combo['cidade_origem']} via {worst_combo['transportadora']}",
            f"OTD de apenas <b>{worst_combo['otd']*100:.1f}%</b> com "
            f"{fmt_num(worst_combo['volume'])} pedidos e atraso médio de "
            f"<b>{worst_combo['atraso']:.1f} dias</b>. "
            f"Esta é a combinação hub-transportadora mais problemática.",
            "danger",
        ), unsafe_allow_html=True)

        st.markdown(insight_card(
            f"Melhor Rota: {best_combo['cidade_origem']} via {best_combo['transportadora']}",
            f"OTD de <b>{best_combo['otd']*100:.1f}%</b> com "
            f"{fmt_num(best_combo['volume'])} pedidos. "
            f"Use como benchmark para otimizar as demais rotas.",
            "success",
        ), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:15px;font-weight:700;color:#0F69F2;margin-bottom:12px;">'
        f'{_icon("target", 18, "#0F69F2")} Recomendações para Reduzir Custos e Melhorar Prazos</div>',
        unsafe_allow_html=True,
    )

    r1, r2, r3 = st.columns(3)

    with r1:
        st.markdown(insight_card(
            f"{_icon('dollar-sign', 14, ACCENT)} Redução de Custos",
            f"Renegociar contratos com <b>{expen_t}</b> ou redistribuir volume para "
            f"<b>{cheap_t}</b> nas rotas em comum. Economia potencial: "
            f"<b>{fmt_brl(expen_v - cheap_v)}</b> por pedido.",
        ), unsafe_allow_html=True)

    with r2:
        st.markdown(insight_card(
            f"{_icon('clock', 14, WARNING)} Melhoria de Prazos",
            f"Focar na rota <b>{worst_combo['cidade_origem']} → {worst_combo['transportadora']}</b>. "
            f"Considere trocar a transportadora nesta rota ou ajustar os prazos prometidos "
            f"ao cliente para refletir a realidade operacional.",
            "warning",
        ), unsafe_allow_html=True)

    with r3:
        st.markdown(insight_card(
            f"{_icon('trending-up', 14, SUCCESS)} Otimização de Rotas",
            f"Replicar o modelo operacional de <b>{best_combo['cidade_origem']}</b> "
            f"(melhor hub) nos demais centros. Investigar práticas e processos "
            f"que contribuem para o OTD de {best_hv:.1f}%.",
            "success",
        ), unsafe_allow_html=True)


st.markdown("---")
st.markdown("<p style='text-align: center; color: #808080;'>Dashboard de Performance Logística | Desenvolvido para a cadeira de Fundamentos em Ciência da Dados 2025.2</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #808080;'>2026 - Rafael Alves</p>", unsafe_allow_html=True)