import json
import textwrap

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Mapa příležitostí v ČR")

st.title("Interaktivní mapa příležitostí v ČR")
st.caption(
    "tmavě zelené kruhy = hlavní příležitosti, světle zelené kruhy = navazující příležitosti."
)


@st.cache_data
def load_map_data():
    nodes = []
    edges = []

    def add_node(node_id, nazev, typ, oblast, popisek, x, y, size=None):
        nodes.append(
            {
                "id": node_id,
                "Nazev": nazev,
                "Typ": typ,
                "Oblast": oblast,
                "Popisek": popisek,
                "x": x,
                "y": y,
                "size": size,
            }
        )

    def add_edge(source, target, vazba=""):
        edges.append({"source": source, "target": target, "vazba": vazba})

    # Centrum
    add_node(
        "root",
        "Příležitosti",
        "Centrum",
        "Centrum",
        "Centrální uzel celé mapy příležitostí.",
        0,
        0,
        62,
    )

    # Hlavní příležitosti – tmavě zelené uzly v původní mapě
    add_node(
        "tech_ai",
        "Posuny v technologiích, AI, výzkumu",
        "Hlavní příležitost",
        "Technologie a výzkum",
        "Technologické změny, AI, výzkum a digitalizace jako průřezový zdroj inovací.",
        -720,
        -230,
        50,
    )
    add_node(
        "community",
        "Podpora komunit",
        "Hlavní příležitost",
        "Komunity a vztahy",
        "Rozvoj komunit, lokální ekonomiky a vztahů mezi lidmi a generacemi.",
        -420,
        -330,
        47,
    )
    add_node(
        "school",
        "Školství",
        "Hlavní příležitost",
        "Vzdělávání",
        "Škola jako prostředí rozvoje dětí, učitelů a zájmových organizací.",
        0,
        -350,
        47,
    )
    add_node(
        "migration",
        "Migrace",
        "Hlavní příležitost",
        "Migrace",
        "Začleňování migrantů, práce se školami, komunitami a vstupem na trh práce.",
        650,
        -330,
        46,
    )
    add_node(
        "childhood",
        "Dětství",
        "Hlavní příležitost",
        "Děti a mladí",
        "Včasná péče, rodičovské kompetence a odolnost v dětství.",
        820,
        -150,
        42,
    )
    add_node(
        "youth_power",
        "Práce s dospívajícími, dát jim moc rozhodovat a měnit věci",
        "Hlavní příležitost",
        "Děti a mladí",
        "Posilování agency dospívajících: důvěra, sebevědomí a reálný prostor ovlivňovat věci.",
        760,
        80,
        44,
    )
    add_node(
        "care_value",
        "Oceňovat hodnotu péče, kvalitní služba není levná",
        "Hlavní příležitost",
        "Sociální služby a péče",
        "Prestiž péče, financování kvalitních služeb a využití technologií pro šetření času.",
        600,
        285,
        44,
    )
    add_node(
        "public_admin",
        "Veřejná správa",
        "Hlavní příležitost",
        "Veřejná správa",
        "Strategické řízení, prevence a implementace koncepcí ve veřejné správě.",
        280,
        520,
        45,
    )
    add_node(
        "green",
        "Zelená transformace",
        "Hlavní příležitost",
        "Ekologie",
        "Zelená transformace jako průřezová příležitost pro kvalitu života, energetiku a komunity.",
        -120,
        390,
        38,
    )
    add_node(
        "aging",
        "Stárnutí",
        "Hlavní příležitost",
        "Stárnutí",
        "Stárnutí populace jako příležitost k age managementu, aktivnímu stárnutí a podpoře péče.",
        -420,
        420,
        46,
    )
    add_node(
        "collab",
        "Podpora spolupráce",
        "Hlavní příležitost",
        "Spolupráce",
        "Rozvoj spolupráce mezi institucemi, sektory, obcemi, regiony a veřejností.",
        -900,
        20,
        46,
    )
    add_node(
        "housing",
        "Bydlení",
        "Hlavní příležitost",
        "Bydlení",
        "Dostupnější a komunitnější formy bydlení.",
        -930,
        330,
        42,
    )

    for target in [
        "tech_ai",
        "community",
        "school",
        "migration",
        "childhood",
        "youth_power",
        "care_value",
        "public_admin",
        "green",
        "aging",
        "collab",
        "housing",
    ]:
        add_edge("root", target)

    # Navazující příležitosti – světle zelené uzly v původní mapě
    add_node(
        "medicine",
        "Posuny v medicíně",
        "Navazující příležitost",
        "Zdravotnictví",
        "Technologický a procesní posun v medicíně.",
        -1050,
        -410,
        40,
    )
    add_node(
        "resilience",
        "Budování zdravé odolnosti zal. na empatii",
        "Navazující příležitost",
        "Komunity a vztahy",
        "Bezpečné vztahy, dialog a psychická/komunitní odolnost založená na empatii.",
        -560,
        -610,
        40,
    )
    add_node(
        "tech_fields",
        "Podpora technologických oborů",
        "Navazující příležitost",
        "Vzdělávání",
        "Podpora technologických oborů v návaznosti na vzdělávání a budoucí pracovní trh.",
        -190,
        -600,
        40,
    )
    add_node(
        "interest_orgs",
        "Podpora zájmových organizací",
        "Navazující příležitost",
        "Vzdělávání",
        "Zájmové organizace jako prostředí rozvoje dětí, kompetencí a vztahů.",
        40,
        -600,
        38,
    )
    add_node(
        "inequality",
        "Odstraňování nerovností",
        "Navazující příležitost",
        "Vzdělávání",
        "Snižování nerovností ve vzdělávání a životních šancích.",
        280,
        -600,
        40,
    )
    add_node(
        "intersector",
        "Meziresortní/multidisciplinární/mezinárodní spolupráce",
        "Navazující příležitost",
        "Spolupráce",
        "Propojování aktérů napříč resorty, disciplínami a zeměmi.",
        -1180,
        -110,
        46,
    )
    add_node(
        "cross_sector_rel",
        "Vytvářet prostor na budování vztahů napříč sektory",
        "Navazující příležitost",
        "Spolupráce",
        "Budování vztahů a důvěry mezi veřejným, neziskovým, soukromým a komunitním sektorem.",
        -1180,
        160,
        44,
    )
    add_node(
        "informal_care",
        "Podpora neformální péče",
        "Navazující příležitost",
        "Sociální služby a péče",
        "Podpora rodinných a dalších neformálních pečujících, včetně dostupnosti služeb a technologií.",
        -620,
        680,
        39,
    )
    add_node(
        "active_aging",
        "Aktivní stárnutí",
        "Navazující příležitost",
        "Stárnutí",
        "Aktivní zapojení starších lidí, dobrovolnictví a komunitní práce.",
        -250,
        730,
        42,
    )

    add_edge("tech_ai", "medicine")
    add_edge("community", "resilience")
    add_edge("school", "tech_fields")
    add_edge("school", "interest_orgs")
    add_edge("school", "inequality")
    add_edge("collab", "intersector")
    add_edge("collab", "cross_sector_rel")
    add_edge("aging", "informal_care")
    add_edge("aging", "active_aging")

    return pd.DataFrame(nodes), pd.DataFrame(edges)


nodes_df, edges_df = load_map_data()

# Sidebar
st.sidebar.header("Filtry")
areas = sorted([a for a in nodes_df["Oblast"].unique().tolist() if a != "Centrum"])
selected_areas = st.sidebar.multiselect("Oblasti", areas, default=areas)

types = ["Hlavní příležitost", "Navazující příležitost"]
selected_types = st.sidebar.multiselect("Typ uzlu", types, default=types)

search = st.sidebar.text_input("Vyhledat v názvu nebo popisku", "")
show_arrows = st.sidebar.toggle("Zobrazit směrové šipky", value=False)
show_table = st.sidebar.toggle("Zobrazit kontrolní tabulku", value=False)

mask = (
    ((nodes_df["Oblast"].isin(selected_areas)) | (nodes_df["Oblast"] == "Centrum"))
    & ((nodes_df["Typ"].isin(selected_types)) | (nodes_df["Typ"] == "Centrum"))
)

if search.strip():
    q = search.strip().casefold()
    search_mask = (
        nodes_df["Nazev"].str.casefold().str.contains(q, regex=False)
        | nodes_df["Popisek"].str.casefold().str.contains(q, regex=False)
        | nodes_df["Oblast"].str.casefold().str.contains(q, regex=False)
    )
    mask = mask & ((search_mask) | (nodes_df["Typ"] == "Centrum"))

selected_ids = set(nodes_df.loc[mask, "id"].tolist())
selected_ids.add("root")

# Přidej rodičovské uzly, aby vyhledaný uzel nezůstal bez kontextu.
changed = True
while changed:
    before = len(selected_ids)
    parents = set(edges_df.loc[edges_df["target"].isin(selected_ids), "source"].tolist())
    selected_ids |= parents
    changed = len(selected_ids) > before

nodes_view = nodes_df[nodes_df["id"].isin(selected_ids)].copy()
edges_view = edges_df[edges_df["source"].isin(selected_ids) & edges_df["target"].isin(selected_ids)].copy()

# Vizuální nastavení uzlů
STYLE = {
    "Centrum": {
        "bg": "#087B2C",
        "border": "#065F22",
        "font": "#FFFFFF",
        "font_size": 26,
        "shape": "circle",
        "width": 18,
    },
    "Hlavní příležitost": {
        "bg": "#2FCB5F",
        "border": "#25AE50",
        "font": "#FFFFFF",
        "font_size": 16,
        "shape": "circle",
        "width": 20,
    },
    "Navazující příležitost": {
        "bg": "#A8EFC5",
        "border": "#8ADDB0",
        "font": "#1F3D2C",
        "font_size": 15,
        "shape": "circle",
        "width": 20,
    },
}


def wrap_label(text, width):
    return "\n".join(textwrap.wrap(str(text), width=width, break_long_words=False))


vis_nodes = []
for _, row in nodes_view.iterrows():
    style = STYLE[row["Typ"]]
    size = int(row["size"] if pd.notna(row["size"]) else 25)
    vis_nodes.append(
        {
            "id": row["id"],
            "label": wrap_label(row["Nazev"], style["width"]),
            "x": int(row["x"]),
            "y": int(row["y"]),
            "size": size,
            "shape": style["shape"],
            "color": {
                "background": style["bg"],
                "border": style["border"],
                "highlight": {"background": style["bg"], "border": "#0B3D1E"},
            },
            "font": {
                "color": style["font"],
                "size": style["font_size"],
                "face": "Inter, Arial, sans-serif",
                "bold": row["Typ"] in ["Centrum", "Hlavní příležitost"],
            },
            "margin": 8,
            "borderWidth": 1,
            # Metadata for tooltip and click panel. Deliberately no native `title`,
            # because Streamlit/Vis sometimes renders HTML title content as raw text.
            "nazev": row["Nazev"],
            "typ": row["Typ"],
            "oblast": row["Oblast"],
            "popisek": row["Popisek"],
        }
    )

vis_edges = []
for _, row in edges_view.iterrows():
    vis_edges.append(
        {
            "from": row["source"],
            "to": row["target"],
            "color": {"color": "#B8B8B8", "highlight": "#777777"},
            "width": 1.4,
            "smooth": {"enabled": True, "type": "cubicBezier", "roundness": 0.22},
        }
    )

nodes_json = json.dumps(vis_nodes, ensure_ascii=False)
edges_json = json.dumps(vis_edges, ensure_ascii=False)
arrows_json = "true" if show_arrows else "false"

html_graph = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    body {{ margin: 0; font-family: Inter, Arial, sans-serif; background: #ffffff; }}
    .wrap {{ display: grid; grid-template-columns: minmax(0, 1fr) 330px; gap: 14px; height: 780px; }}
    .network-shell {{ position: relative; width: 100%; height: 780px; }}
    #network {{ width: 100%; height: 780px; border: 1px solid #E5E7EB; border-radius: 14px; background: #fff; }}
    #custom-tooltip {{
      display: none;
      position: absolute;
      z-index: 10;
      max-width: 330px;
      padding: 12px 13px;
      border: 1px solid #D0D5DD;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.97);
      box-shadow: 0 12px 28px rgba(16, 24, 40, 0.16);
      pointer-events: none;
      color: #1D2939;
    }}
    .tooltip-title {{ font-weight: 750; font-size: 14px; line-height: 1.25; margin-bottom: 6px; }}
    .tooltip-meta {{ font-size: 12px; color: #667085; margin-bottom: 8px; }}
    .tooltip-text {{ font-size: 13px; line-height: 1.38; color: #344054; }}
    #panel {{ border: 1px solid #E5E7EB; border-radius: 14px; padding: 16px; background: #FAFAFA; overflow: auto; }}
    .eyebrow {{ color: #667085; font-size: 12px; text-transform: uppercase; letter-spacing: .06em; font-weight: 700; }}
    h3 {{ margin: 8px 0 10px 0; font-size: 20px; line-height: 1.25; }}
    .pill {{ display: inline-block; padding: 4px 8px; border-radius: 999px; background: #E9F8EE; color: #126B35; font-size: 12px; margin: 2px 4px 8px 0; }}
    .text {{ color: #344054; font-size: 14px; line-height: 1.45; white-space: pre-wrap; }}
    .hint {{ color: #667085; font-size: 13px; line-height: 1.4; margin-top: 14px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="network-shell">
      <div id="network"></div>
      <div id="custom-tooltip">
        <div class="tooltip-title" id="tooltip-title"></div>
        <div class="tooltip-meta" id="tooltip-meta"></div>
        <div class="tooltip-text" id="tooltip-text"></div>
      </div>
    </div>
    <aside id="panel">
      <div class="eyebrow">Detail uzlu</div>
      <h3 id="detail-title">Klikněte na uzel v mapě</h3>
      <div id="detail-meta"></div>
      <div class="text" id="detail-text">Po kliknutí se zde zobrazí popis a zařazení. Při najetí myší se zobrazuje krátký tooltip přímo v mapě.</div>
      <div class="hint">Tip: Uzly lze posouvat.</div>
    </aside>
  </div>

  <script type="text/javascript">
    const nodes = new vis.DataSet({nodes_json});
    const edges = new vis.DataSet({edges_json});
    const container = document.getElementById("network");
    const shell = document.querySelector(".network-shell");
    const tooltip = document.getElementById("custom-tooltip");
    const data = {{ nodes: nodes, edges: edges }};
    const options = {{
      autoResize: true,
      layout: {{ improvedLayout: false }},
      physics: {{ enabled: false }},
      interaction: {{
        hover: true,
        dragNodes: true,
        dragView: true,
        zoomView: true,
        navigationButtons: true,
        keyboard: true
      }},
      nodes: {{
        chosen: true,
        borderWidthSelected: 3
      }},
      edges: {{
        arrows: {{ to: {{ enabled: {arrows_json}, scaleFactor: 0.55 }} }},
        selectionWidth: 2
      }}
    }};

    const network = new vis.Network(container, data, options);
    network.moveTo({{ position: {{ x: 0, y: 80 }}, scale: 0.58 }});

    function setText(id, value) {{
      document.getElementById(id).textContent = value || "";
    }}

    function setPanel(node) {{
      setText("detail-title", node.nazev || node.label);
      document.getElementById("detail-meta").innerHTML = "";
      const typ = document.createElement("span");
      typ.className = "pill";
      typ.textContent = node.typ || "";
      const oblast = document.createElement("span");
      oblast.className = "pill";
      oblast.textContent = node.oblast || "";
      document.getElementById("detail-meta").appendChild(typ);
      document.getElementById("detail-meta").appendChild(oblast);
      setText("detail-text", node.popisek || "Bez doplňující poznámky.");
    }}

    function setTooltip(node) {{
      setText("tooltip-title", node.nazev || node.label);
      setText("tooltip-meta", `${{node.typ || ""}} · ${{node.oblast || ""}}`);
      setText("tooltip-text", node.popisek || "Bez doplňující poznámky.");
    }}

    function positionTooltip(event) {{
      const rect = shell.getBoundingClientRect();
      let left = event.clientX - rect.left + 16;
      let top = event.clientY - rect.top + 16;

      const tooltipRect = tooltip.getBoundingClientRect();
      if (left + tooltipRect.width > rect.width - 10) {{
        left = event.clientX - rect.left - tooltipRect.width - 16;
      }}
      if (top + tooltipRect.height > rect.height - 10) {{
        top = event.clientY - rect.top - tooltipRect.height - 16;
      }}

      tooltip.style.left = `${{Math.max(8, left)}}px`;
      tooltip.style.top = `${{Math.max(8, top)}}px`;
    }}

    network.on("hoverNode", function(params) {{
      const node = nodes.get(params.node);
      setTooltip(node);
      tooltip.style.display = "block";
    }});

    network.on("blurNode", function() {{
      tooltip.style.display = "none";
    }});

    container.addEventListener("mousemove", function(event) {{
      if (tooltip.style.display === "block") {{
        positionTooltip(event);
      }}
    }});

    network.on("click", function(params) {{
      if (params.nodes.length > 0) {{
        const node = nodes.get(params.nodes[0]);
        setPanel(node);
      }}
    }});
  </script>
</body>
</html>
"""

st.subheader("Mapa vazeb")
st.write(
    "Najetí myší zobrazí tooltip. Kliknutí otevře detail v pravém panelu. "
    "Uzly lze přesouvat."
)
components.html(html_graph, height=805, scrolling=False)

if show_table:
    st.write("### Kontrolní tabulka uzlů")
    st.dataframe(
        nodes_view[["Nazev", "Typ", "Oblast", "Popisek"]].sort_values(["Typ", "Oblast", "Nazev"]),
        use_container_width=True,
    )
    st.write("### Kontrolní tabulka vazeb")
    edges_named = edges_view.merge(
        nodes_df[["id", "Nazev"]], left_on="source", right_on="id", how="left"
    ).rename(columns={"Nazev": "Zdroj"})
    edges_named = edges_named.merge(
        nodes_df[["id", "Nazev"]], left_on="target", right_on="id", how="left"
    ).rename(columns={"Nazev": "Cíl"})
    st.dataframe(edges_named[["Zdroj", "Cíl", "vazba"]], use_container_width=True)
