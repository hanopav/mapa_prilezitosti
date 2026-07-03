import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import pandas as pd

# Nastavení stránky na široké zobrazení
st.set_page_config(layout="wide", page_title="Mapa příležitostí v ČR")

st.title("🧠 Interaktivní mapa příležitostí v ČR")
st.write("Brainstorming session přenesená do interaktivní síťové mapy s filtrováním.")

# 1. NAČTENÍ DAT (Zcela neprůstřelné čtení)
# 1. NAČTENÍ DAT (Zapsáno přímo v kódu, bez nutnosti externího CSV)
def load_data():
    raw_data = [
        {"Zdroj": "Příležitosti", "Cil": "Posuny v medicíně", "Oblast": "Zdravotnictví", "Popisek": "Hlavní technologický a procesní posun v lékařské péči."},
        {"Zdroj": "Posuny v medicíně", "Cil": "Rozvoj telemedicíny", "Oblast": "Zdravotnictví", "Popisek": "Podpora distanční péče a diagnostiky na dálku."},
        {"Zdroj": "Příležitosti", "Cil": "Budování zdravé odolnosti zal. na empatii", "Oblast": "Zdravotnictví", "Popisek": "Zaměření na psychické zdraví a bezpečné vztahy ve společnosti."},
        {"Zdroj": "Příležitosti", "Cil": "Zelená transformace", "Oblast": "Ekologie", "Popisek": "Udržitelný rozvoj a dekarbonizace."},
        {"Zdroj": "Příležitosti", "Cil": "Dětství včasná péče", "Oblast": "Sociální oblast", "Popisek": "Klíčová fáze vývoje dítěte se zaměřením na odolnost a skautské hodnoty."},
        {"Zdroj": "Dětství včasná péče", "Cil": "Rodičovské kompetence", "Oblast": "Sociální oblast", "Popisek": "Posilování dovedností rodičů při výchově."},
        {"Zdroj": "Příležitosti", "Cil": "Oceňovat hodnotu péče", "Oblast": "Sociální oblast", "Popisek": "Kvalitní sociální služba není levná. Je nutné nastavit nový způsob financování."},
        {"Zdroj": "Oceňovat hodnotu péče", "Cil": "Využití technologií pro šetření času", "Oblast": "Sociální oblast", "Popisek": "Nasazení digitálních nástrojů pro snížení administrativy pečovatelů."}
    ]
    return pd.DataFrame(raw_data)

df = load_data()

# Vyčištění textů od neviditelných mezer
for col in df.columns:
    df[col] = df[col].astype(str).str.strip()

# --- KONTROLNÍ TABULKA ---
st.write("### Kontrola načtených dat (Nyní musí být ve 4 sloupcích):", df)
# --------------------------

# 2. Sidebar (Boční panel) pro filtrování
st.sidebar.header("Filtry a nastavení")
vsechny_oblasti = df["Oblast"].unique().tolist()
vybrane_oblasti = st.sidebar.multiselect(
    "Vyberte oblasti k zobrazení:", 
    options=vsechny_oblasti, 
    default=vsechny_oblasti
)

# Filtrování dat na základě výběru
if vybrane_oblasti:
    df_filtered = df[df["Oblast"].isin(vybrane_oblasti)]
else:
    df_filtered = df

# 3. PŘÍPRAVA UZLŮ (Nodes) A PROPOJENÍ (Edges)
nodes = []
edges = []

# Vytvoříme slovník pro mapování popisků k uzlům
popisky_uzlu = {}
for _, row in df_filtered.iterrows():
    popisky_uzlu[row["Zdroj"]] = ""
    popisky_uzlu[row["Cil"]] = row["Popisek"]

# Unikátní seznam všech uzlů (Zdroj + Cíl)
vsechny_uzly = set(df_filtered["Zdroj"].tolist() + df_filtered["Cil"].tolist())

for uzlik in vsechny_uzly:
    if uzlik == "Příležitosti":
        color = "#FF4B4B"
        size = 35
        tooltip_text = "Centrální bod brainstormingové session"
    else:
        color = "#00A0A0"
        size = 20
        tooltip_text = popisky_uzlu.get(uzlik, "")
        
    nodes.append(Node(
        id=uzlik, 
        label=uzlik, 
        title=tooltip_text,  
        size=size,
        color=color
    ))

# Vytvoření propojení
for _, row in df_filtered.iterrows():
    edges.append(Edge(
        source=row["Zdroj"], 
        target=row["Cil"], 
        type="STRAIGHT"
    ))

# 4. Konfigurace a zobrazení grafu
config = Config(
    width=1000, 
    height=600, 
    directed=True, 
    physics=True, 
    hierarchical=False
)

st.subheader("Mapa vazeb")
st.write("💡 *Tip: Najetím myší na uzel zobrazíte detailní poznámku. Graf můžete přibližovat a uzly posouvat.*")

agraph(nodes=nodes, edges=edges, config=config)