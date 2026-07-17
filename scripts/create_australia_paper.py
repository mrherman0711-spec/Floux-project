#!/usr/bin/env python3
"""
Generate Australia World Economy final project as a Google Doc.
"""

import json
import os
import sys
import io

# ── path setup ──────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# ── colours ─────────────────────────────────────────────────────────────────
NAVY   = {"red": 0.1059, "green": 0.1647, "blue": 0.2902}   # #1B2A4A
WHITE  = {"red": 1.0,    "green": 1.0,    "blue": 1.0}
LGREY  = {"red": 0.945,  "green": 0.953,  "blue": 0.969}    # light row
BLACK  = {"red": 0.1,    "green": 0.1,    "blue": 0.1}

# ── auth ────────────────────────────────────────────────────────────────────
def get_creds():
    token_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "token.json")
    creds_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "credentials.json")
    with open(token_path) as f:
        token_data = json.load(f)
    with open(creds_path) as f:
        creds_data = json.load(f)
    client_info = creds_data.get("installed") or creds_data.get("web", {})
    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri=client_info.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=client_info.get("client_id"),
        client_secret=client_info.get("client_secret"),
    )
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, "w") as f:
            f.write(creds.to_json())
    return creds

# ── chart helpers ────────────────────────────────────────────────────────────
NAVY_HEX   = "#1B2A4A"
MID_HEX    = "#2E4A7A"
LIGHT_HEX  = "#4A72B0"
PALE_HEX   = "#7DA0D4"

def make_lng_revenue_chart():
    years = ['2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23']
    values = [16.5, 22.3, 30.9, 49.7, 47.5, 30.5, 70.0, 92.2]
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(years, values, color=NAVY_HEX, width=0.6, zorder=3)
    bars[-1].set_color(MID_HEX)  # highlight peak year
    ax.set_facecolor('#F5F7FA')
    fig.patch.set_facecolor('white')
    ax.grid(axis='y', color='white', linewidth=1.2, zorder=2)
    ax.set_ylabel('AUD Billions', fontsize=11, color=NAVY_HEX, fontweight='bold')
    ax.set_title('Figure 1: Australian LNG Export Revenue, 2015–2023\n(Source: Geoscience Australia, AECR 2025; DCCEEW 2025)',
                 fontsize=10, color=NAVY_HEX, fontweight='bold', pad=12)
    ax.tick_params(axis='x', rotation=30, labelsize=9, colors=NAVY_HEX)
    ax.tick_params(axis='y', labelsize=9, colors=NAVY_HEX)
    for spine in ax.spines.values():
        spine.set_edgecolor('#CCCCCC')
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.2,
                f'${val}B', ha='center', va='bottom', fontsize=8,
                color=NAVY_HEX, fontweight='bold')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf

def make_export_mix_chart():
    labels = ['LNG', 'Thermal Coal', 'Metallurgical Coal', 'Crude Oil/Liquids', 'Other/Uranium']
    sizes  = [38.6, 27.4, 25.9, 5.5, 2.6]
    colors = [NAVY_HEX, MID_HEX, LIGHT_HEX, PALE_HEX, '#B0C4DE']
    fig, ax = plt.subplots(figsize=(8, 5))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, colors=colors, autopct='%1.1f%%',
        startangle=140, pctdistance=0.75,
        wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2)
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_color('white')
        at.set_fontweight('bold')
    legend_labels = [f'{l} ({s}%)' for l, s in zip(labels, sizes)]
    ax.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(0.82, 0.5),
              fontsize=9, frameon=False)
    ax.set_title('Figure 3: Australian Energy Export Mix by Value, 2022–23\n(Source: Geoscience Australia, AECR 2025)',
                 fontsize=10, color=NAVY_HEX, fontweight='bold', pad=12)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf

# ── google doc builder ───────────────────────────────────────────────────────

def rgb(c): return {"rgbColor": c}

def req_insert_text(text, idx=1):
    return {"insertText": {"location": {"index": idx}, "text": text}}

def req_style_text(start, end, bold=False, italic=False, font_size=12,
                   font="Times New Roman", fg=None, bg=None):
    fields = []
    fmt = {
        "weightedFontFamily": {"fontFamily": font},
        "fontSize": {"magnitude": font_size, "unit": "PT"},
        "bold": bold,
        "italic": italic,
    }
    fields += ["weightedFontFamily", "fontSize", "bold", "italic"]
    if fg:
        fmt["foregroundColor"] = rgb(fg)
        fields.append("foregroundColor")
    if bg:
        fmt["backgroundColor"] = rgb(bg)
        fields.append("backgroundColor")
    return {
        "updateTextStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "textStyle": fmt,
            "fields": ",".join(fields)
        }
    }

def req_paragraph_style(start, end, alignment="START", space_above=0, space_below=6,
                         line_spacing=150, named_style=None):
    ps = {
        "alignment": alignment,
        "spaceAbove": {"magnitude": space_above, "unit": "PT"},
        "spaceBelow": {"magnitude": space_below, "unit": "PT"},
        "lineSpacing": line_spacing,
    }
    if named_style:
        ps["namedStyleType"] = named_style
    return {
        "updateParagraphStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "paragraphStyle": ps,
            "fields": "alignment,spaceAbove,spaceBelow,lineSpacing" + (",namedStyleType" if named_style else "")
        }
    }

def req_page_break(idx):
    return {"insertPageBreak": {"location": {"index": idx}}}

# ── document text ─────────────────────────────────────────────────────────────

COVER = """\
Australia: Energy, Trade, and Globalization in the Global Economy

World Economy — Spring 2026

Max Herman

Professor: Luisa García Carrión
Universidad Europea de Madrid

May 29, 2026
"""

INTRO = """\
1. Introduction

Few countries occupy as consequential a position in global energy markets as Australia. The nation exports roughly two-thirds of the primary energy it produces — coal, liquefied natural gas (LNG), and uranium flowing steadily to the industrial centres of East and South Asia. In the 2023–24 financial year, Australian primary energy production reached 19,232 petajoules (PJ), making it one of the most prolific energy-producing economies in the world relative to domestic population (Department of Climate Change, Energy, the Environment and Water [DCCEEW], 2025). Yet the country is not simply a resource appendage to more powerful economies. It is the world's third-largest LNG exporter, the second-largest coal exporter, and holds approximately 32% of the world's reasonably assured uranium reserves — making it the undisputed global leader in uranium resource endowment (Geoscience Australia, 2024).

Fossil fuels define Australia's energy profile, both in production and consumption. Black coal accounts for the largest share of domestic energy output, followed by natural gas and oil. On the consumption side, oil products dominate at 40.7% of the primary energy mix, driven by the geography of a vast continent where road and air transport demand is structurally high. Renewables contributed 9.3% of primary consumption in 2023–24, though this share is growing at an annualized average of 4.9% over the past decade (DCCEEW, 2025). Uranium, while produced in significant volumes, is entirely exported because Australia has no domestic nuclear generation capacity.

Australia's relevance in global energy markets goes beyond volume. As a stable, OECD-member democracy in the Indo-Pacific, Australia functions as a de facto energy security anchor for import-dependent Asian economies — Japan, South Korea, and Taiwan chief among them. Long-term supply contracts underpin much of the LNG trade, creating energy interdependencies that carry political as well as commercial weight. At the same time, Australia is navigating a structural shift: the global clean energy transition threatens the long-term demand outlook for its two largest exports, coal and LNG, even as it opens new opportunities in critical minerals such as lithium, cobalt, and nickel.

This paper analyzes Australia's position in the global energy economy using the conceptual tools of international economics. Section 2 maps the country's production, consumption, trade flows, and infrastructure. Section 3 applies the theory of comparative advantage to explain Australia's specialization in energy exports and examines who gains and who loses from that trade. Section 4 analyzes three specific policies that distort Australia's energy markets — the 2020–23 China trade dispute, the Australian Domestic Gas Security Mechanism, and the 2023 Safeguard Mechanism reforms — connecting each to broader concepts of government intervention, market efficiency, and deadweight loss. Section 5 discusses how globalization shapes Australia's energy security, drawing on the Russia-Ukraine war, China dependency, and the energy transition. Section 6 concludes with an assessment of Australia's strengths, vulnerabilities, and the strategic choices that will shape its economic trajectory.

"""

SECTION2 = """\
2. Australia in the Global Energy Market

2.1 Production and Consumption

Australia's energy production is vast and skewed heavily toward fossil fuels. In 2023–24, black coal output reached 11,398.4 PJ — recovering from two years of La Niña-related flooding that shut major mines in Queensland and New South Wales. Natural gas production stood at 6,122.0 PJ, brown coal at 416.4 PJ, oil and LPG at 738.5 PJ, and renewables at 557.1 PJ (DCCEEW, 2025). Table 1 below presents the five-year production trend.

Table 1: Australia's Primary Energy Production by Source, 2019–2024 (Petajoules)
Source: DCCEEW, Australian Energy Statistics Table J, 2025.

Fuel Source | 2019-20 | 2020-21 | 2021-22 | 2022-23 | 2023-24
Black Coal | 12,316.8 | 11,359.6 | 11,215.7 | 11,084.4 | 11,398.4
Brown Coal | 425.4 | 430.0 | 415.7 | 400.9 | 416.4
Natural Gas | 5,993.9 | 5,730.0 | 5,830.5 | 6,198.6 | 6,122.0
Oil and LPG | 799.0 | 718.0 | 723.0 | 771.4 | 738.5
Renewables | 418.8 | 464.6 | 513.0 | 551.7 | 557.1
TOTAL | 19,953.9 | 18,702.2 | 18,697.9 | 20,007.0 | 19,232.4

On the consumption side, Australia used 5,976.7 PJ of primary energy in 2023–24 — a 0.5% increase over the prior year. Fossil fuels collectively account for 91% of that mix: oil at 40.7%, coal at 25.3%, and natural gas at 24.7%. The heavy share of oil in domestic consumption reflects the country's geographic reality — a continent of 7.7 million square kilometres where freight and personal transport depend on liquid fuels. Renewables reached 9.3% of primary consumption in 2023–24, growing steadily as rooftop solar penetration rises and utility-scale wind and solar projects come online (DCCEEW, 2025).

The net export position is striking. Australia exports approximately 67% of the primary energy it produces. At the height of the global commodity price spike triggered by the Russia-Ukraine conflict, energy commodity export earnings hit a record AUD 238.7 billion in 2022–23 (Geoscience Australia, 2024).

2.2 Exports, Imports, and Trade Partners

By value in 2022–23, LNG was the single largest energy export at AUD 92.2 billion (approximately USD 61 billion), followed by thermal coal at AUD 65.5 billion, metallurgical coal at AUD 61.9 billion, and crude oil and feedstocks at AUD 13.2 billion. By volume in 2023–24, black coal led at 10,056.9 PJ (approximately 356 million tonnes), representing 65.8% of total energy export volume, with LNG at 4,508.5 PJ (approximately 81 million tonnes) accounting for 29.5% (DCCEEW, 2025). Figure 1 below shows LNG export revenues from 2015 to 2023.

[CHART: Figure 1 — LNG Revenue]

Australia's primary energy trade partners are concentrated in North-East Asia. For LNG, Japan absorbed 32.1 million tonnes in 2022, China 23.3 Mt, South Korea 12.7 Mt, and Taiwan 8.1 Mt (Institute for Energy Economics and Financial Analysis [IEEFA], 2023). Table 3 shows the five-year trend in LNG volumes by destination.

Table 3: Australian LNG Export Volumes by Destination Country, 2018–2022 (Million Tonnes)
Source: IEEFA, Global LNG Outlook, 2023.

Destination | 2018 | 2019 | 2020 | 2021 | 2022
Japan | 31.0 | 31.5 | 30.6 | 28.3 | 32.1
China | 25.1 | 30.6 | 31.4 | 33.8 | 23.3
South Korea | 8.5 | 8.3 | 8.7 | 10.1 | 12.7
Taiwan | 2.8 | 4.5 | 4.9 | 6.5 | 8.1
Other | 4.9 | 5.5 | 6.2 | 5.2 | 7.5
TOTAL | 72.3 | 76.4 | 81.8 | 81.9 | 83.7

Despite its enormous primary energy surplus, Australia imports roughly 90% of its refined petroleum products — a structural vulnerability discussed in Section 5. In 2024, refined petroleum was the country's largest single import by value at USD 31.6 billion, sourced mainly from South Korea, Singapore, Malaysia, and India (Observatory of Economic Complexity, 2024). This paradox — exporting raw energy at scale while depending on Asian refiners for transport fuels — is one of the defining tensions in Australian energy policy.

2.3 Companies and Infrastructure

The Australian energy sector is shaped by a concentrated group of multinationals and domestic firms. Woodside Energy operates the Pluto LNG terminal (4.9 Mtpa capacity) and co-ventures the North West Shelf facility (16.9 Mtpa) in Western Australia. Chevron Australia manages Gorgon (15.6 Mtpa) and Wheatstone (8.9 Mtpa). Shell operates the Prelude Floating LNG facility (3.6 Mtpa) offshore Western Australia and the QCLNG plant (8.5 Mtpa) on Curtis Island, Queensland. Santos runs the GLNG terminal, ConocoPhillips operates APLNG, and Inpex leads the Ichthys project (8.9 Mtpa) in the Northern Territory alongside Darwin LNG (3.7 Mtpa). BHP and Glencore dominate coal extraction, particularly in Queensland's Bowen Basin and New South Wales's Hunter Valley (Australian Energy Regulator [AER], 2024).

Coal leaves Australia through some of the world's highest-capacity export ports. The Port of Newcastle processes over 150 million tonnes per annum through multiple loaders, while Hay Point, Dalrymple Bay, and Abbot Point in Queensland handle the bulk of seaborne metallurgical coal exports (National Competition Council, 2019). Domestic gas is distributed through the Dampier to Bunbury Natural Gas Pipeline (895 TJ/day capacity) in Western Australia and the Moomba Sydney Pipeline network (590 TJ/day) on the east coast (APA Group, 2024).

Figure 2: Australia's LNG Terminals and Major Coal Export Ports
(Geographic distribution: LNG terminals concentrated in Western Australia [Gorgon, Wheatstone, Pluto, North West Shelf, Prelude], Northern Territory [Darwin, Ichthys], and Queensland [QCLNG, APLNG, GLNG on Curtis Island]. Coal ports in New South Wales [Newcastle] and Queensland [Hay Point, Dalrymple Bay, Abbot Point].)
Source: The Energy Consulting Group / EIA, Australia Oil and Gas Overview, https://energy-cg.com/Australia/Australia_OilGasOverview_EIA.html

Australia's domestic refining capacity has collapsed to two facilities — Ampol's Lytton refinery in Brisbane (109,000 barrels per day) and Viva Energy's Geelong plant (120,000 b/d). Both survive only through federal government subsidies under the Fuel Security Services Payment program, extended to 2030 to prevent total dependence on imported liquid fuels (Argus Media, 2024). This situation underscores a broader vulnerability examined in Section 5.

The macroeconomic weight of the energy sector is considerable. The oil and gas industry alone represents 3.7% of Australian GDP and delivered an estimated AUD 21.9 billion in federal and state taxes and royalties in 2024–25 (Australian Energy Producers, 2024). Globally, Australia ranks third in LNG exports, second in coal exports, and fourth in uranium production — a combination that makes it one of the most diversified energy exporters in the world (Geoscience Australia, 2024).

"""

SECTION3 = """\
3. Comparative Advantage and International Trade

3.1 Factor Endowments and the Source of Advantage

The classical theory of comparative advantage holds that countries gain from specializing in goods they can produce at a lower opportunity cost relative to trading partners, even when they are not the absolute-cost leader (Krugman, Obstfeld & Melitz, 2023). Australia's specialization in fossil fuel and uranium exports rests on three foundations: geological endowment, geographic positioning, and institutional reliability.

On geological grounds, Australia holds the world's third-largest proven coal reserves, 105,148 PJ of identified natural gas resources, and approximately 32% of the world's reasonably assured uranium resources at costs below USD 130 per kilogram of uranium — making it the undisputed global leader in uranium reserve endowment (Geoscience Australia, 2024). These resources were formed over millions of years; no amount of policy or capital can replicate them elsewhere. They give Australia a natural comparative advantage in energy extraction that is, in Ricardian terms, close to absolute for specific commodities.

Cost benchmarks illustrate the practical expression of this advantage. In thermal coal, Australia's average production cost in 2025 was approximately USD 50 per tonne — significantly below Colombia at USD 59 per tonne, though well above Indonesia's ultra-low cost of USD 18 per tonne, which reflects a structurally different and lower-grade resource base (International Energy Agency [IEA], 2025). Australia does not compete on price with Indonesian thermal coal; it competes on quality, reliability, and proximity to higher-value steel-making markets.

In LNG, the picture is more complicated. Qatar remains the global benchmark for low-cost liquefaction, with breakeven delivery costs to Asian markets near USD 3.00 per MMBtu, driven by massive scale, associated liquids revenues, and a centralized low-wage labor environment. US Gulf Coast LNG clears at roughly USD 5.50–6.00 per MMBtu, benefiting from Henry Hub pricing and destination-flexible contracts. Australia's existing LNG plants are broadly competitive at prevailing market prices, but proposed greenfield expansions face estimated breakeven costs of USD 6.00–9.00 per MMBtu, a range that makes new Australian LNG investment difficult to justify except at sustained high price cycles (IEEFA, 2024). Table 2 summarizes these comparisons.

Table 2: LNG Production and Delivery Cost Benchmarks — Selected Producers
Source: IEEFA, Global LNG Outlook 2024–2028; World Bank, 2022.

Producer | Estimated Breakeven (USD/MMBtu) | Key Competitive Factor
Qatar | ~$3.00 | Economies of scale; liquids-rich fields; low-cost labor
USA (Gulf Coast) | ~$5.50–$6.00 | Liquid domestic market; flexible destination contracts
Australia (New Projects) | ~$6.00–$9.00 | Geographic proximity to Asia; offset by high labor costs and capital overruns

3.2 Geographic and Institutional Advantages

Geography reinforces Australia's resource advantage. Shipping routes from Pilbara LNG terminals or Queensland coal ports to Tokyo, Busan, or Taipei are significantly shorter than those from the US Gulf Coast or Colombia, which translates into lower freight costs and faster delivery times. This freight advantage is particularly meaningful for long-term supply contracts where reliability is valued above spot market price flexibility.

Institutional factors matter as much as geography. Australia is a stable OECD democracy with transparent legal systems, strong contract enforcement, and independent regulatory bodies. For energy companies making multi-billion dollar capital commitments with project lifetimes of 20–30 years, this "sovereign risk premium" is not trivial. Key bilateral Free Trade Agreements reinforce this: the Japan-Australia Economic Partnership Agreement (JAEPA) includes a dedicated chapter on Energy and Mineral Resources, and the Korea-Australia FTA (KAFTA) contains specific energy investment provisions (Department of Foreign Affairs and Trade [DFAT], 2024).

To offset structurally high labor costs — a genuine disadvantage relative to Indonesia or Qatar — the Australian sector has invested heavily in automation. Autonomous haulage systems operate extensively in Pilbara iron ore and coal operations, and remote-operated export terminals reduce headcount at port facilities. This capital substitution for labor preserves cost competitiveness even as wage rates remain far above those in competing economies (Australian Energy Producers, 2025).

3.3 Who Gains and Who Loses

The gains from Australia's energy trade are substantial but unevenly distributed. Multinational energy companies — Woodside, Chevron, Shell, BHP — capture significant returns on capital. State governments in Western Australia and Queensland receive royalty revenues that fund public services; WA in particular has run fiscal surpluses largely on the back of resources royalties. Asian industrial consumers gain reliable access to high-quality energy inputs that sustain their manufacturing sectors and electricity grids. The remote and regional workforce in mining regions receives wages well above the national median.

The costs, however, fall on specific groups. Domestic manufacturers — particularly energy-intensive industries such as aluminium smelting, glass production, and chemicals — pay prices for gas that track international netback levels rather than domestic cost-of-production. This erodes their competitiveness against industries in countries with regulated or subsidized energy access (IEEFA, 2024). Coal-dependent regional communities in Queensland and New South Wales face a long-term structural transition as global demand for thermal coal declines, with limited economic alternatives in many locations. Pacific Island neighbors bear the most extreme externality: their coastlines and livelihoods face existential climate risk from the combustion of Australian fossil exports, yet they have no mechanism to recover those costs from Australian producers.

3.4 An Eroding Advantage and an Emerging One

Australia's comparative advantage in fossil fuel exports is not static. The Gorgon, Ichthys, and Prelude LNG projects all suffered severe capital cost overruns relative to original budgets, a pattern that has made global capital cautious about the next wave of Australian LNG investment. Aging coal mines face rising rehabilitation costs and shrinking access to international finance as ESG criteria tighten (IEEFA, 2024). These structural headwinds suggest that Australia will, over time, become less competitive as a conventional fossil fuel exporter.

Against this, a new comparative advantage is forming. CSIRO's GenCost 2025–26 analysis confirms that a reliable electricity system built on solar photovoltaics, onshore wind, and battery storage is the lowest-cost new-build electricity option in Australia — by a wide margin over new coal or nuclear generation (CSIRO, 2025). Combined with world-class endowments of lithium, cobalt, nickel, and rare earths, Australia is strategically positioned to become a major supplier to the global clean energy supply chain. Whether this potential translates into realized export revenues depends critically on whether Australia develops downstream processing capacity or remains locked into the role of raw material supplier.

"""

SECTION4 = """\
4. Trade Policies and Market Distortions

4.1 The Australia–China Trade Dispute, 2020–2023

In early 2020, the Morrison government called for an independent international inquiry into the origins of COVID-19. Beijing's response was swift and economically targeted: over the following months, China imposed informal bans, anti-dumping duties, and tariff barriers across a range of Australian exports, most consequentially coal. Dozens of bulk carriers carrying Australian coal were left anchored off Chinese ports for weeks, unable to unload (International Journal of Multicultural and Multireligious Understanding, 2023). This episode provides a textbook example of trade used as a tool of geopolitical coercion.

The economic mechanism that followed illustrates a critical distinction: trade diversion versus trade destruction. Because coal is a highly fungible global commodity — thermal coal is thermal coal, with grade and transport cost as the key differentiators — China's ban did not destroy demand for Australian coal. It rerouted it. Australian exporters, initially forced to accept discounted prices to find alternative buyers, redirected volumes to India, Japan, South Korea, and eventually Europe, where the early stages of the Russia-Ukraine energy shock were creating urgent demand (IEA, 2023). Chinese power plants and steel mills, meanwhile, had to source replacement coal from Indonesia and Russia — lower quality, longer supply chains, and often at higher cost.

The price effects confirmed this logic. Rather than suffering a structural collapse, Australian coal prices surged to historic highs during 2021–22 as the global energy crisis drove spot prices across all fuel markets. Newcastle coal futures, the benchmark for thermal coal in the Asia-Pacific, briefly exceeded USD 400 per tonne in 2022. Chinese buyers bore the deadweight loss of this episode in the form of higher input costs and deteriorating industrial efficiency — the direct consequence of a policy that substituted political goals for market efficiency signals (Xiang, Kuang & Li, 2017).

By 2023, facing severe domestic electricity shortages and a shifting diplomatic register under Australia's new Albanese government, Beijing quietly dismantled the ban. Trade flows normalized, though Australian exporters drew a durable lesson: concentration of export revenue in a single market controlled by a state actor represents a geopolitical risk that normal corporate risk management frameworks do not fully capture (Export Finance Australia, 2024).

4.2 The Australian Domestic Gas Security Mechanism

Australia's most revealing domestic energy policy paradox is not its exposure to Chinese embargoes — it is the fact that a country producing 6,122 PJ of natural gas annually has consistently failed to supply affordable gas to its own manufacturers and households. This "gas paradox" is not a resource problem. It is a market architecture problem.

On Queensland's east coast, the Curtis Island LNG terminals — QCLNG, APLNG, and GLNG — are contractually linked to international oil-indexed netback pricing. When Asian LNG spot prices rise, so do the prices offered to Queensland gas producers for domestic sales, because exporters will always sell to the highest bidder. Domestic manufacturers must compete for gas against buyers in Japan and South Korea, often losing. The result is that Australian factories pay world prices for Australian gas extracted from beneath Australian soil.

The Australian Domestic Gas Security Mechanism (ADGSM), introduced in 2017, was designed to address this. It gives the Minister for Resources the power to restrict LNG exports if an annual domestic supply shortfall is forecast — in effect, prioritizing domestic demand over export contracts as a last resort (DCCEEW, 2024). When the global energy crisis of 2022 pushed east coast wholesale gas prices to unprecedented levels, the ADGSM's annual trigger mechanism proved too slow. The government responded with a 2023 reform package: quarterly activation triggers, an emergency 12-month price cap of AUD 12 per gigajoule on new domestic wholesale gas contracts, and a mandatory code of conduct enforced by the Australian Competition and Consumer Commission (ACCC) (Australian National Audit Office, 2024; Treasury, 2022).

The economic trade-off is real and unresolved. For domestic users and manufacturers, the price cap provides immediate relief and preserves viability. For LNG producers, it introduces regulatory uncertainty that undermines the investment case for the upstream exploration required to alleviate the structural supply shortage in the first place. A mechanism designed to cure a market failure — the externalization of domestic gas costs onto households — risks creating a second-order failure by chilling the investment that would expand supply. Efficiency is sacrificed in the short run; whether it is recovered in the long run depends on whether higher domestic prices would actually have incentivized new supply within a commercially viable timeframe.

4.3 The Safeguard Mechanism and Renewable Energy Policy

Australia's 2023 Safeguard Mechanism reforms mark the most significant structural shift in the country's energy regulatory framework in a decade. Originally established in 2016, the Safeguard Mechanism imposed largely symbolic emissions baselines on the 215 largest industrial facilities — those emitting over 100,000 tonnes of CO2-equivalent per year, a group that includes all major LNG export terminals and coal mines and collectively represents approximately 30% of national emissions. Baselines were set generously enough that few facilities faced real compliance pressure (HopgoodGanim, 2023).

The 2023 reforms imposed a mandatory 4.9% annual reduction in emissions baselines, a hard cap on aggregate scheme emissions, and a requirement that any new gas fields developed for LNG export must exhibit "zero reservoir carbon" upon commencement — meaning new projects must either deploy Carbon Capture and Storage technology or purchase high-quality carbon offsets from the first barrel (DLA Piper, 2023). For existing operators, compliance costs rise predictably each year. For prospective investors, the zero-carbon requirement transforms the economics of new LNG development.

Simultaneously, the federal government introduced the AUD 4 billion Hydrogen Headstart program to subsidize early-stage green hydrogen projects and bridge the commercial gap between current costs and market viability (DCCEEW, 2024). Projects underway include the 1.5 GW Murchison Green Hydrogen development in Western Australia and the Hunter Valley Hydrogen Hub in New South Wales. These are paired with a national renewable electricity target of 82% by 2030 and a legislated Net Zero 2050 trajectory — a dramatic reversal from Australia's historical posture as a resistant participant in multilateral climate negotiations.

The combined effect of these policies is a structured transfer of capital from legacy fossil fuel industries to the clean energy ecosystem. Incumbent LNG operators face rising compliance costs and shrinking investment certainty. Renewable energy developers and green hydrogen entrepreneurs receive direct subsidies and a regulatory environment that favors their expansion. Whether this constitutes an efficiency gain or an efficiency loss depends on how one weighs the market distortion of subsidies against the market failure of uncorrected carbon externalities. The Pigouvian case for carbon pricing — that a tax equal to the marginal social cost of emissions increases rather than reduces economic efficiency — suggests the reforms move in the right direction, even if the specific mechanism design involves its own distortions.

"""

SECTION5 = """\
5. Globalization and Energy Security

Globalization has integrated Australia deeply into the world economy, generating enormous export revenues and creating channels through which global shocks transmit into the domestic economy with unusual speed. The result is a strategic paradox: one of the world's great energy exporters has significant energy security vulnerabilities of its own.

The most acute is liquid fuel supply. Despite producing vast quantities of primary energy, Australia imports approximately 90% of its transport liquid fuels — petrol, diesel, and jet fuel — from Asian refineries in South Korea, Singapore, and Malaysia (The Guardian, 2026). Only two domestic refineries remain operational, both sustained by federal subsidies. Strategic reserve holdings have historically fallen well below the International Energy Agency's 90-day net import requirement; the Minimum Stockholding Obligation introduced in 2023 mandates only 20–32 days of diesel and 24–27 days of petrol and jet fuel — a buffer that would exhaust rapidly under any serious disruption to Asian maritime supply chains (DCCEEW, 2024). A conflict in the South China Sea, or significant damage to Singapore or South Korean refining infrastructure, would have immediate consequences for Australian transport and logistics.

The Russia-Ukraine war demonstrated how quickly offshore geopolitical shocks reach domestic energy markets. As European buyers scrambled to replace sanctioned Russian pipeline gas in 2022, global LNG spot prices surged. Australia benefited directly as an alternative supplier: Woodside Energy signed a landmark long-term Sale and Purchase Agreement with Germany's Uniper to supply approximately 0.8 million tonnes per annum through 2039 (Woodside Energy, 2022). But the same price surge transmitted immediately into the Australian east coast gas market, pushing wholesale prices to levels that threatened manufacturing viability and triggered the emergency AUD 12/GJ price cap — a reminder that a country tied to international commodity markets is exposed to international commodity volatility in both directions.

China presents the sharpest geopolitical tension. Before the 2020 diplomatic dispute, China absorbed nearly 40% of Australian goods exports. By 2023, despite genuine diversification efforts, that figure had only fallen to 32%, heavily underpinned by iron ore demand that China has not found a viable substitute for (Export Finance Australia, 2024). The AUKUS security alliance ties Australia firmly to the United States and United Kingdom in defense and technology architecture, creating a duality that is difficult to sustain indefinitely: strategic security dependency on the US, and economic prosperity dependency on China.

Looking forward, the energy transition poses a structural threat to Australia's export model. Under the IEA's Net Zero Emissions scenario, global coal demand falls by 69% from current levels by 2035 and by 95% by 2050 (Queensland Competition Authority, 2024). For Queensland and New South Wales, this implies stranded assets on a substantial scale — mines, rail networks, port infrastructure, and regional economies built around export coal that may have no viable alternative economic base. The critical minerals sector offers a partial hedge. Lithium exports alone reached AUD 19 billion in 2023, and the Reserve Bank of Australia projects that lithium, copper, and nickel could represent around 10% of total resource exports by 2030 (RBA, 2025). The US Inflation Reduction Act creates demand pull for Australian critical minerals through the US-Australia FTA's EV tax credit provisions, though the same legislation draws downstream processing investment toward US shores rather than into Australian value-adding capacity.

The broader question globalization poses for Australia is whether economic interdependence, which has generated enormous wealth over thirty years of sustained commodity demand from Asia, remains a net positive as the geopolitical foundations of that interdependence shift. The answer is not simply yes or no. Globalization will remain the mechanism through which Australia sells its energy and minerals to the world. What is changing is the composition of what it sells, who it sells to, and under what security conditions. Managing that transition — from fossil fuel exporter to clean energy supply chain partner — is the defining economic challenge of the next generation.

"""

SECTION6 = """\
6. Conclusion

Australia's position in the global energy economy is one of the most analytically rich case studies available for the concepts explored in this course. The country's comparative advantage in energy exports is not a historical accident. It reflects a durable combination of geological abundance, geographic proximity to the world's fastest-growing energy markets, institutional reliability, and decades of capital investment in infrastructure that competitors struggle to match quickly.

The analysis in this paper shows that Australia's strengths are real but not permanent. Its coal reserves are vast, its LNG terminals are among the world's largest, and its uranium endowment is unmatched globally. These factor advantages have generated export revenues that funded public services, royalty income for state governments, and wealth for shareholders across multiple decades. In the short and medium term, Asia's industrial economies still need Australian coal and gas to keep power grids stable and steel mills running.

But the weaknesses are equally real. Australia is the world's dominant LNG exporter and cannot reliably fuel its own cars. Its strategic reserves of refined petroleum are critically low. Its largest trade partner has demonstrated a willingness to weaponize trade flows for diplomatic purposes, and a 32% export concentration with China remains far too high for comfort. New LNG projects face breakeven costs that struggle to compete with Qatar or the United States, while the cost overruns at Gorgon, Ichthys, and Prelude have made international capital cautious about the next wave of Australian offshore investment.

The most important finding of this analysis is that Australia faces a dual transformation. The Safeguard Mechanism reforms, the Hydrogen Headstart program, and the 82% renewable electricity target by 2030 signal a deliberate policy shift away from fossil fuel dependency — both in the domestic electricity system and in the investment environment for future energy production. Simultaneously, the critical minerals sector — lithium, cobalt, nickel, rare earths — offers a credible replacement export thesis for the coal revenues that the energy transition will eventually erode.

Whether Australia successfully converts from fossil fuel exporter to clean energy supply chain partner depends on choices that are not yet made: whether it develops processing and manufacturing capacity rather than simply exporting raw lithium and nickel ore, whether it builds the domestic hydrogen infrastructure to compete with Middle Eastern and US green hydrogen projects, and whether the AUKUS security architecture can be leveraged into economic partnerships that reduce dependence on a single large customer. The framework of comparative advantage, trade policy analysis, and globalization explored in this course provides the tools to assess those choices — not to make them inevitable, but to make their implications legible.

"""

REFERENCES = """\
References

Argus Media. (2024). Australia extends subsidy plan for refiners to 2030. https://www.argusmedia.com/en/news-and-insights/latest-market-news/2803693-australia-extends-subsidy-plan-for-refiners-to-2030

APA Group. (2024). Moomba Sydney Pipeline and MSEP. https://www.apa.com.au/operations-and-projects/gas/gas-transmission/moomba-sydney-pipeline-and-msep

Australian Energy Producers. (2024). Media release: Australian oil & gas industry delivers record $22 billion in taxes and royalties. https://energyproducers.au/news/all_news/media-release-australian-oil-gas-industry-delivers-record-22-billion-in-taxes-and-royalties-to-government-revenues-in-2024-25

Australian Energy Producers. (2025). Australia's natural gas investment competitiveness. https://energyproducers.au/wp-content/uploads/2025/05/AEP-Australias-Natural-Gas-Investment-Competitiveness-Final.pdf

Australian Energy Regulator (AER). (2024). State of the energy market 2024 — Chapter 4: Gas markets in eastern Australia. https://www.aer.gov.au/system/files/2024-11/State%20of%20the%20energy%20market%202024%20-%20Chapter%204%20-%20Gas%20markets%20in%20eastern%20Australia.pdf

Australian National Audit Office (ANAO). (2024). Design of the Energy Price Relief Plan. https://www.anao.gov.au/work/performance-audit/design-of-the-energy-price-relief-plan

CSIRO. (2025). GenCost 2024–25 final report. https://www.csiro.au/en/research/technology-space/energy/electricity-transition/gencost

Department of Climate Change, Energy, the Environment and Water (DCCEEW). (2024). Gas market review report. https://www.dcceew.gov.au/sites/default/files/documents/gas-market-review-report.pdf

Department of Climate Change, Energy, the Environment and Water (DCCEEW). (2024). Hydrogen Headstart program. https://www.dcceew.gov.au/energy/hydrogen/hydrogen-headstart-program

Department of Climate Change, Energy, the Environment and Water (DCCEEW). (2024). Minimum stockholding obligation. https://www.dcceew.gov.au/energy/security/australias-fuel-security/minimum-stockholding-obligation

Department of Climate Change, Energy, the Environment and Water (DCCEEW). (2025). Australian Energy Update 2025. https://www.energy.gov.au/sites/default/files/2025-08/australian_energy_update_2025.pdf

Department of Foreign Affairs and Trade (DFAT). (2024). Summary of JAEPA chapters and annexes. https://www.dfat.gov.au/trade/agreements/in-force/jaepa/full-text/Pages/summary-of-jaepa-chapters-and-annexes

DLA Piper. (2023). Safeguard mechanism reform: Legislative cap on emissions. https://www.dlapiper.com/insights/publications/2023/03/safeguard-mechanism-reform-legislative-cap-on-emissions-changes-agreed-by-the-australian-government

Export Finance Australia. (2024). China: Record imports from Australia but economic headwinds mount. https://www.exportfinance.gov.au/resources/world-risk-developments/2024/july/china-record-imports-from-australia-but-economic-headwinds-mount/

Geoscience Australia. (2024). Australia's Energy Commodity Resources (AECR) 2025. https://www.ga.gov.au/aecr2025/production-and-trade

HopgoodGanim Lawyers. (2023). Safeguard mechanism reforms: What you need to know. https://www.hopgoodganim.com.au/news-insights/safeguard-mechanism-reforms/

Institute for Energy Economics and Financial Analysis (IEEFA). (2023). Global LNG Outlook 2024–2028. https://www.energy.gov/sites/default/files/2023-06/Ex%20L%20IEEFA%2C%20Global%20LNG%20Outlook.pdf

Institute for Energy Economics and Financial Analysis (IEEFA). (2024). The hidden costs of the LNG boom. https://ieefa.org/resources/hidden-costs-lng-boom

International Energy Agency (IEA). (2023). Coal 2023: Analysis and forecast to 2026. https://iea.blob.core.windows.net/assets/a72a7ffa-c5f2-4ed8-a2bf-eb035931d95c/Coal_2023.pdf

International Energy Agency (IEA). (2025). Coal 2025: Prices and costs. https://www.iea.org/reports/coal-2025/prices-and-costs

International Journal of Multicultural and Multireligious Understanding. (2023). Australia–China trade tensions during the COVID-19 pandemic. https://ijmmu.com/index.php/ijmmu/article/download/4293/3790

Krugman, P., Obstfeld, M., & Melitz, M. (2023). International economics: Theory and policy (12th ed.). Pearson.

National Competition Council. (2019). Dalrymple Bay Coal Terminal master plan. https://ncc.gov.au/images/uploads/CECTQlAp-006.pdf

Observatory of Economic Complexity (OEC). (2024). Refined petroleum in Australia. https://oec.world/en/profile/bilateral-product/refined-petroleum/reporter/aus

Queensland Competition Authority (QCA). (2024). Depreciation approaches at UT6 — NERA report. https://www.qca.org.au/wp-content/uploads/2025/12/attachment-c-nera-report-depreciation-approaches.pdf

Reserve Bank of Australia (RBA). (2025). The global energy transition and critical minerals. https://www.rba.gov.au/publications/bulletin/2025/oct/the-global-energy-transition-and-critical-minerals.html

The Guardian. (2026, March 24). Seven charts that reveal how unprepared Australia was for the fuel crisis. https://www.theguardian.com/business/2026/mar/24/seven-charts-that-reveal-how-unprepared-australia-was-for-the-fuel-crisis

Treasury, Australian Government. (2022). Energy Price Relief Plan. https://www.pm.gov.au/media/energy-price-relief-plan

Woodside Energy. (2022). Third quarter 2022 report. https://www.woodside.com/docs/default-source/asx-announcements/2022/third-quarter-2022-report.pdf

World Bank. (2022). Analytical foundation for increased Pan-Arab regional gas trade. https://ppp.worldbank.org/sites/default/files/2022-06/Analytical_Foundation_for_Increased_Pan-Arab_Regional_Gas_Trade.pdf

Xiang, H., Kuang, Y., & Li, C. (2017). Impact of the China–Australia FTA on global coal production and trade. Journal of Policy Modeling, 39(1), 65–78. https://ideas.repec.org/a/eee/jpolmo/v39y2017i1p65-78.html
"""

# ── main ─────────────────────────────────────────────────────────────────────

def main():
    print("Authenticating with Google...", flush=True)
    creds = get_creds()

    docs_service  = build("docs",  "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    # ── Step 1: Generate charts ──────────────────────────────────────────────
    print("Generating charts...", flush=True)
    lng_buf    = make_lng_revenue_chart()
    export_buf = make_export_mix_chart()

    # ── Step 2: Upload charts to Drive ───────────────────────────────────────
    print("Uploading charts to Drive...", flush=True)
    def upload_image(buf, name):
        media = MediaIoBaseUpload(buf, mimetype='image/png', resumable=False)
        f = drive_service.files().create(
            body={"name": name, "mimeType": "image/png"},
            media_body=media,
            fields="id"
        ).execute()
        # Make publicly readable so Docs can embed it
        drive_service.permissions().create(
            fileId=f["id"],
            body={"role": "reader", "type": "anyone"}
        ).execute()
        return f["id"]

    lng_img_id    = upload_image(lng_buf,    "chart_lng_revenue.png")
    export_img_id = upload_image(export_buf, "chart_export_mix.png")
    print(f"  LNG chart: {lng_img_id}", flush=True)
    print(f"  Export mix chart: {export_img_id}", flush=True)

    # ── Step 3: Create Google Doc ────────────────────────────────────────────
    print("Creating Google Doc...", flush=True)
    doc = docs_service.documents().create(
        body={"title": "Australia: Energy, Trade, and Globalization in the Global Economy"}
    ).execute()
    doc_id = doc["documentId"]
    print(f"  Doc ID: {doc_id}", flush=True)

    # ── Step 4: Set page margins and default style ───────────────────────────
    # Margins: 2.5cm = ~1417 EMU... in Docs API, margins are in pt (72pt = 1in)
    # 2.5cm ≈ 70.9pt — but Docs API uses hundredths of a point as integers? No:
    # Docs API margin is in pt as a float via "magnitude" + "unit": "PT"
    margin_requests = [{
        "updateDocumentStyle": {
            "documentStyle": {
                "marginTop":    {"magnitude": 70.9, "unit": "PT"},
                "marginBottom": {"magnitude": 70.9, "unit": "PT"},
                "marginLeft":   {"magnitude": 70.9, "unit": "PT"},
                "marginRight":  {"magnitude": 70.9, "unit": "PT"},
            },
            "fields": "marginTop,marginBottom,marginLeft,marginRight"
        }
    }]
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": margin_requests}
    ).execute()

    # ── Step 5: Build document content ───────────────────────────────────────
    # We insert text in reverse order because each insertion shifts indices.
    # Instead, we'll build a sequential list of (text, style_hints) and
    # insert all at once from index 1, then apply formatting in a second pass.

    # Assemble full body text with section markers
    full_text = (
        COVER + "\n" +
        INTRO +
        SECTION2 +
        SECTION3 +
        SECTION4 +
        SECTION5 +
        SECTION6 +
        REFERENCES
    )

    # Insert all text at once
    print("Inserting document text...", flush=True)
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertText": {"location": {"index": 1}, "text": full_text}}]}
    ).execute()

    # ── Step 6: Apply formatting ─────────────────────────────────────────────
    print("Applying formatting...", flush=True)

    # Re-read doc to get actual indices
    doc_content = docs_service.documents().get(documentId=doc_id).execute()
    body = doc_content.get("body", {}).get("content", [])

    # Build a plain text map: character offset -> paragraph
    # We'll use the document's structural elements to find key paragraphs
    formatting_requests = []

    def find_paragraphs_with_text(search_text):
        """Find all paragraphs containing search_text, return list of (start, end)."""
        results = []
        for elem in body:
            if "paragraph" not in elem:
                continue
            para = elem["paragraph"]
            start_idx = elem.get("startIndex", 0)
            end_idx   = elem.get("endIndex", 0)
            para_text = "".join(
                r.get("textRun", {}).get("content", "")
                for r in para.get("elements", [])
            )
            if search_text in para_text:
                results.append((start_idx, end_idx, para_text.strip()))
        return results

    def find_paragraph_starting_with(prefix):
        for elem in body:
            if "paragraph" not in elem:
                continue
            para = elem["paragraph"]
            start_idx = elem.get("startIndex", 0)
            end_idx   = elem.get("endIndex", 0)
            para_text = "".join(
                r.get("textRun", {}).get("content", "")
                for r in para.get("elements", [])
            ).strip()
            if para_text.startswith(prefix):
                return start_idx, end_idx, para_text
        return None

    # ── Cover page formatting ────────────────────────────────────────────────
    cover_lines = [
        ("Australia: Energy, Trade, and Globalization in the Global Economy", 20, True),
        ("World Economy", 13, False),
        ("Max Herman", 13, False),
        ("Professor: Luisa García Carrión", 12, False),
        ("Universidad Europea de Madrid", 12, False),
        ("May 29, 2026", 12, False),
    ]
    for text_fragment, font_size, bold in cover_lines:
        matches = find_paragraphs_with_text(text_fragment)
        for (start, end, _) in matches:
            # Center alignment
            formatting_requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "paragraphStyle": {
                        "alignment": "CENTER",
                        "spaceBelow": {"magnitude": 12, "unit": "PT"},
                        "lineSpacing": 150,
                    },
                    "fields": "alignment,spaceBelow,lineSpacing"
                }
            })
            # Text style — navy
            formatting_requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": start, "endIndex": end - 1},
                    "textStyle": {
                        "weightedFontFamily": {"fontFamily": "Times New Roman"},
                        "fontSize": {"magnitude": font_size, "unit": "PT"},
                        "bold": bold,
                        "foregroundColor": {"color": {"rgbColor": NAVY}},
                    },
                    "fields": "weightedFontFamily,fontSize,bold,foregroundColor"
                }
            })

    # ── Section headings ──────────────────────────────────────────────────────
    heading_prefixes = [
        "1. Introduction",
        "2. Australia in the Global Energy Market",
        "2.1 Production and Consumption",
        "2.2 Exports, Imports, and Trade Partners",
        "2.3 Companies and Infrastructure",
        "3. Comparative Advantage and International Trade",
        "3.1 Factor Endowments and the Source of Advantage",
        "3.2 Geographic and Institutional Advantages",
        "3.3 Who Gains and Who Loses",
        "3.4 An Eroding Advantage and an Emerging One",
        "4. Trade Policies and Market Distortions",
        "4.1 The Australia",
        "4.2 The Australian Domestic Gas Security Mechanism",
        "4.3 The Safeguard Mechanism and Renewable Energy Policy",
        "5. Globalization and Energy Security",
        "6. Conclusion",
        "References",
    ]

    for prefix in heading_prefixes:
        result = find_paragraph_starting_with(prefix)
        if not result:
            continue
        start, end, _ = result
        is_main = prefix[0].isdigit() and "." in prefix[:3] and not any(
            prefix.startswith(f"{n}.{sub}") for n in range(1,7) for sub in range(1,6)
            if f"{n}.{sub}" in prefix
        )
        # Detect subsection (e.g. "2.1", "3.2")
        is_sub = len(prefix) > 3 and prefix[1] == '.' and prefix[3].isdigit()
        font_size = 13 if not is_sub else 12
        formatting_requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {
                    "spaceAbove": {"magnitude": 14, "unit": "PT"},
                    "spaceBelow": {"magnitude": 6,  "unit": "PT"},
                    "lineSpacing": 150,
                },
                "fields": "spaceAbove,spaceBelow,lineSpacing"
            }
        })
        formatting_requests.append({
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end - 1},
                "textStyle": {
                    "weightedFontFamily": {"fontFamily": "Times New Roman"},
                    "fontSize": {"magnitude": font_size, "unit": "PT"},
                    "bold": True,
                    "foregroundColor": {"color": {"rgbColor": NAVY}},
                },
                "fields": "weightedFontFamily,fontSize,bold,foregroundColor"
            }
        })

    # ── Body text: apply Times New Roman 12pt 1.5 spacing to everything ──────
    # Get total doc length
    doc_end = body[-1].get("endIndex", 1) if body else 1
    formatting_requests.append({
        "updateTextStyle": {
            "range": {"startIndex": 1, "endIndex": doc_end - 1},
            "textStyle": {
                "weightedFontFamily": {"fontFamily": "Times New Roman"},
                "fontSize": {"magnitude": 12, "unit": "PT"},
            },
            "fields": "weightedFontFamily,fontSize"
        }
    })

    # ── Paragraph spacing for body ────────────────────────────────────────────
    for elem in body:
        if "paragraph" not in elem:
            continue
        start = elem.get("startIndex", 0)
        end   = elem.get("endIndex", 0)
        formatting_requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {
                    "lineSpacing": 150,
                    "spaceBelow": {"magnitude": 6, "unit": "PT"},
                },
                "fields": "lineSpacing,spaceBelow"
            }
        })

    # ── Table caption lines ───────────────────────────────────────────────────
    table_captions = [
        "Table 1: Australia's Primary Energy Production by Source",
        "Table 2: LNG Production and Delivery Cost Benchmarks",
        "Table 3: Australian LNG Export Volumes by Destination Country",
    ]
    for cap in table_captions:
        result = find_paragraph_starting_with(cap)
        if not result:
            continue
        start, end, _ = result
        formatting_requests.append({
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end - 1},
                "textStyle": {
                    "bold": True,
                    "italic": False,
                    "foregroundColor": {"color": {"rgbColor": NAVY}},
                },
                "fields": "bold,italic,foregroundColor"
            }
        })

    # ── Figure caption lines ──────────────────────────────────────────────────
    figure_caps = [
        "Figure 1:",
        "Figure 2:",
        "Figure 3:",
        "[CHART: Figure 1",
    ]
    for cap in figure_caps:
        result = find_paragraph_starting_with(cap)
        if not result:
            continue
        start, end, _ = result
        formatting_requests.append({
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end - 1},
                "textStyle": {
                    "italic": True,
                    "foregroundColor": {"color": {"rgbColor": NAVY}},
                },
                "fields": "italic,foregroundColor"
            }
        })

    # Send all formatting in one batch (split into chunks of 50 to avoid limits)
    print(f"  Sending {len(formatting_requests)} formatting requests...", flush=True)
    chunk_size = 50
    for i in range(0, len(formatting_requests), chunk_size):
        chunk = formatting_requests[i:i+chunk_size]
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": chunk}
        ).execute()

    # ── Step 7: Insert images ─────────────────────────────────────────────────
    print("Inserting charts into document...", flush=True)

    # Re-read to find image placeholder locations
    doc_content2 = docs_service.documents().get(documentId=doc_id).execute()
    body2 = doc_content2.get("body", {}).get("content", [])

    def find_index_of_text(search, body_content):
        for elem in body_content:
            if "paragraph" not in elem:
                continue
            para_text = "".join(
                r.get("textRun", {}).get("content", "")
                for r in elem["paragraph"].get("elements", [])
            )
            if search in para_text:
                # Return startIndex of paragraph + offset to text
                start = elem.get("startIndex", 0)
                offset = para_text.find(search)
                return start + offset
        return None

    chart1_idx = find_index_of_text("[CHART: Figure 1 — LNG Revenue]", body2)
    chart3_idx = find_index_of_text("[CHART: Figure 3", body2)

    image_requests = []

    if chart1_idx is not None:
        image_requests.append({
            "insertInlineImage": {
                "location": {"index": chart1_idx},
                "uri": f"https://drive.google.com/uc?export=view&id={lng_img_id}",
                "objectSize": {
                    "width":  {"magnitude": 430, "unit": "PT"},
                    "height": {"magnitude": 240, "unit": "PT"},
                }
            }
        })

    if image_requests:
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": image_requests}
        ).execute()
        print("  Chart 1 inserted.", flush=True)

    # Insert chart 3 (re-read after chart 1 insertion shifts indices)
    doc_content3 = docs_service.documents().get(documentId=doc_id).execute()
    body3 = doc_content3.get("body", {}).get("content", [])
    chart3_idx2 = find_index_of_text("[CHART: Figure 3", body3)

    if chart3_idx2 is not None:
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": [{
                "insertInlineImage": {
                    "location": {"index": chart3_idx2},
                    "uri": f"https://drive.google.com/uc?export=view&id={export_img_id}",
                    "objectSize": {
                        "width":  {"magnitude": 400, "unit": "PT"},
                        "height": {"magnitude": 240, "unit": "PT"},
                    }
                }
            }]}
        ).execute()
        print("  Chart 3 inserted.", flush=True)

    # ── Step 8: Add page numbers via named range / header ────────────────────
    print("Adding page numbers...", flush=True)
    try:
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": [{
                "createFooter": {"type": "DEFAULT"}
            }]}
        ).execute()
        # Get footer ID
        doc_final = docs_service.documents().get(documentId=doc_id).execute()
        footers = doc_final.get("footers", {})
        footer_id = list(footers.keys())[0] if footers else None
        if footer_id:
            footer_content = footers[footer_id].get("content", [])
            if footer_content:
                footer_idx = footer_content[0].get("startIndex", 1)
                docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={"requests": [
                        {"insertText": {"location": {"segmentId": footer_id, "index": footer_idx}, "text": "  "}},
                        {"createParagraphBullets": {
                            "range": {"segmentId": footer_id, "startIndex": footer_idx, "endIndex": footer_idx + 2},
                            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
                        }}
                    ]}
                ).execute()
    except Exception as e:
        print(f"  Page number insertion skipped: {e}", flush=True)

    # ── Step 9: Set document permissions ─────────────────────────────────────
    print("Setting sharing permissions...", flush=True)
    drive_service.permissions().create(
        fileId=doc_id,
        body={"role": "reader", "type": "anyone"}
    ).execute()

    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
    print(f"\n✅ Document created successfully!")
    print(f"   URL: {doc_url}")
    return doc_url


if __name__ == "__main__":
    main()
