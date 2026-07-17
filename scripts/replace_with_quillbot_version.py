#!/usr/bin/env python3
"""
Replace Google Doc body with the Quillbot-humanized text from serote.pdf
Doc ID: 1LQTqcm_k-4R91DhZqy_cpNTNxEvWtnC76rIfoo3w8Dk
Taiwan data corrected from 18.1 Mt → 8.1 Mt
"""
import json, os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

DOC_ID = "1LQTqcm_k-4R91DhZqy_cpNTNxEvWtnC76rIfoo3w8Dk"
NAVY  = {"red": 0.1059, "green": 0.1647, "blue": 0.2902}
BLACK = {"red": 0.1,    "green": 0.1,    "blue": 0.1}

# ── Full text from serote.pdf (Quillbot humanized) ────────────────────────────
# Taiwan corrected: 18.1 → 8.1 Mt (source data: IEEFA 2023)

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

Australia exports around two-thirds of its energy production. Some of the largest volumes of production come from coal, LNG, and uranium. Australia's production and exports reach the industrial centers of East and South Asia. Estimations for the 2023-24 financial year report a total primary energy production of 19,232 petajoules (PJ) placing Australia among the highest output energy countries (DCCEEW, 2025). Australia is the world's third-largest exporter of LNG, second-largest for coal, and has roughly 32% of the world's uranium reserves (Geoscience Australia, 2024).

The energy production and consumption of Australia is dominated by fossil fuels. The largest production of energy in Australia comes from black coal, followed by gas and oil. The largest share of the primary energy mix in Australia is oil products, making up around 40.7%. This is a result of the size of Australia's continent, which covers 7.7 million square kilometers. In the 2023-24 financial year, renewables made up around 9.3% of primary energy consumption. This reflects a growth rate of 4.9% for the last decade (DCCEEW, 2025). Uranium is produced, but not consumed in Australia. As a stable OECD democracy in the Indo-Pacific region, Australia has become a de facto energy security anchor for import dependant economies in Japan, South Korea, and Taiwan.

Long-term supply contracts dominate the LNG trade and the relationships involved have political significance that extends beyond typical trade relationships. Complicating this are the legacies of Australia's coal and LNG exports and dwindling long-term demand. They align with the structural problem facing Australia with the clean energy transition. There is some promise with critical minerals like lithium, nickel, and cobalt, but the shift is far from complete.

Using the frameworks of international economics, this paper investigates Australia's energy position. Production, consumption, trade and physical infrastructure fall within the bounds of economics and are the focus of analysis in Section 2. In Section 3, Australia's energy exports' comparative advantage is explained with a focus on the winners and losers. Section 4 focuses on three market distorting policies: the Australian Domestic Gas Security Mechanism, the 2020-2023 China trade dispute and the Safeguard Mechanism reforms of 2023. Section 5 discusses the security trade-offs of globalization. Section 6 offers a conclusion and summary of the findings.

"""

SECTION2 = """\
2. Australia in the Global Energy Market

2.1 Production and Consumption

Australia's energy production is large and dominated by fossil fuels. In 2023-24, 11,398.4 PJ of black coal were produced, recovering from La Nina years of mine closures in Queensland and New South Wales. Brown coal output was 416.4 PJ, with 738.5 PJ of oil and LPG, 6,122.0 PJ of natural gas, and 557.1 PJ produced from renewables (DCCEEW, 2025). Table 1 depicts the five-year production trends by fuel source.

Table 1: Australia's Primary Energy Production by Source, 2019-2024 (Petajoules)
Source: DCCEEW, Australian Energy Statistics National Data 2025.

Fuel Source | 2019-20 | 2020-21 | 2021-22 | 2022-23 | 2023-24
Black Coal | 12,316.8 | 11,359.6 | 11,215.7 | 11,084.4 | 11,398.4
Brown Coal | 425.4 | 430.0 | 415.7 | 400.9 | 416.4
Natural Gas | 5,993.9 | 5,730.0 | 5,830.5 | 6,198.6 | 6,122.0
Oil and LPG | 799.0 | 718.0 | 723.0 | 771.4 | 738.5
Renewables | 418.8 | 464.6 | 513.0 | 551.7 | 557.1
TOTAL | 19,953.9 | 18,702.2 | 18,697.9 | 20,007.0 | 19,232.4

Domestic energy consumption is much less than total energy production. In 2023-24, Australia consumed 5,976.7 PJ of energy, which is a 0.5% increase from the previous year, and fossil fuels constituted 91% of the total consumption. Of that total, oil constituted 40.7%, coal 25.3%, and gas 24.7%. Oil dominates energy consumption due to the high demand of road and air transport within Australia, with very limited progress made on the electrification of transport. Renewables represented 9.3% of total primary energy consumption in 2023-24. Their share is steadily increasing due to the growing use of rooftop solar and increasing wind and solar utility-scale projects (DCCEEW, 2025).

The net export position is the most significant aspect of Australian energy economics, with Australia exporting around 67% of total primary energy production. At the peak of the global commodity price spike in 2022-23, export earnings from the energy commodities reached an all-time high of AUD 238.7 billion (Geoscience Australia, 2024).

2.2 Exports, Imports, and Trade Partners

Most valuable in 2022-23 were exported LNG (AUD 92.2 billion, approximately USD 61 billion), followed by thermal coal (AUD 65.5 billion), metallurgical coal (AUD 61.9 billion), as well as crude oil and feedstocks (AUD 13.2 billion). In terms of volumes traded in 2023-24, black coal recorded the highest at 10,056.9 PJ (approximately 356 million tonnes), followed by LNG which was 4,508.5 PJ (approximately 81 million tonnes), comprising 29.5% of total energy export volume (DCCEEW, 2025). LNG export revenues from 2015 to 2023 are shown in Figure 1.

[CHART: Figure 1 — LNG Revenue]

Australia's energy business is focused on North-East Asia. In the case of LNG, Japan imported 32.1 million tonnes, China 23.3 Mt, South Korea 12.7 Mt and Taiwan 8.1 Mt (Institute for Energy Economics and Financial Analysis [IEEFA], 2023). LNG volumes by destination over the past five years are recorded in Table 3.

Table 3: Australian LNG Export Volumes by Destination Country, 2018-2022 (Million Tonnes)
Source: IEEFA, Global LNG Outlook, 2023.

Destination | 2018 | 2019 | 2020 | 2021 | 2022
Japan | 31.0 | 31.5 | 30.6 | 28.3 | 32.1
China | 25.1 | 30.6 | 31.4 | 33.8 | 23.3
South Korea | 8.5 | 8.3 | 8.7 | 10.1 | 12.7
Taiwan | 2.8 | 4.5 | 4.9 | 6.5 | 8.1
Other | 4.9 | 5.5 | 6.2 | 5.2 | 7.5
TOTAL | 72.3 | 76.4 | 81.8 | 81.9 | 83.7

Despite having a primary energy surplus, Australia imports around 90% of its refined petroleum. In 2024, refined petroleum became Australia's largest import by value, totaling USD 31.6 billion, which came from South Korea, Singapore, Malaysia, and India (Observatory of Economic Complexity, 2024). Australia's inability to refine sufficient energy to even meet the demands of its transportation system is not just an irony; it is a security vulnerability, particularly for scenarios in which Asian supply chains would be disrupted.

2.3 Companies and Infrastructure

The Australian energy sector has a concentrated group of multinationals and domestic firms. Woodside Energy is the sole operator of the Pluto LNG terminal (4.9 Mtpa capacity) and a joint venture of the North West Shelf facility (16.9 Mtpa) in WA. Chevron Australia is the operator of Gorgon (15.6 Mtpa) and Wheatstone (8.9 Mtpa). Shell is the operator of Prelude Floating LNG (3.6 Mtpa) in offshore WA and QCLNG (8.5 Mtpa) in Curtis Island, Queensland. Santos manages the GLNG terminal, ConocoPhillips manages APLNG, and Inpex is in charge of the Ichthys project (8.9 Mtpa) alongside Darwin LNG (3.7 Mtpa) in the Northern Territory. BHP and Glencore control coal extraction in Bowen Basin, Queensland, and Hunter Valley, New South Wales (Australian Energy Regulator [AER], 2024).

Australia exports coal through some of the highest capacity export ports in the world. The Port of Newcastle exports more than 150 million tonnes per year, while Hay Point, Dalrymple Bay, and Abbot Point in Queensland are the primary ports for metallurgical coal (National Competition Council, 2019). Domestic gas flows through the Dampier to Bunbury Natural Gas Pipeline in Western Australia (895 TJ/day) and the Moomba Sydney Pipeline on the eastern seaboard (590 TJ/day) (APA Group, 2024).

Figure 2: Australia's LNG Terminals and Major Coal Export Ports
(Geographic concentration: LNG terminals in Western Australia [Gorgon, Wheatstone, Pluto, North West Shelf, Prelude], Northern Territory [Darwin, Ichthys], Queensland [QCLNG, APLNG, GLNG on Curtis Island] and Coal Ports in New South Wales [Newcastle] and Queensland [Hay Point, Dalrymple Bay, Abbot Point].)
Source: The Energy Consulting Group / EIA, Australia Oil and Gas Overview.

Only two refineries remain in Australia. Ampol's Lytton refinery in Brisbane (with a capacity of 109,000 b/d) and Viva Energy's Geelong refinery (at 120,000 b/d) are both funded by the Australian federally funded Fuel Security Services Payment program to 2030 to avoid total reliance on imported liquid fuels (Argus Media, 2024).

Figure 3: Australian Energy Export Mix by Value, 2022-23
Source: Geoscience Australia, AECR 2025.

[CHART: Figure 3 — Export Mix by Value]

The contribution of the oil and gas segment to the macroeconomic context is significant, representing 3.7% of total GDP, and contributing an estimated AUD 21.9 billion in federal and state taxes and royalties in 2024-25 (Australian Energy Producers, 2024). Australia is the third largest exporter of LNG, the second largest of coal, and the fourth largest of uranium (Geoscience Australia, 2024).

"""

SECTION3 = """\
3. Comparative Advantage and International Trade

3.1 Factor Endowments and the Source of Advantage

Classical theory holds that countries benefit from specializing in goods which, relative to their trading partners, they can produce at the lowest opportunity cost, even if they do not have an absolute cost advantage (Krugman, Obstfeld & Melitz, 2023). The specialization of Australia in the exports of fossil fuels and uranium is built upon three factors: geological endowment, geographical position, and the reliability of its institutions.

When considering geology, Australia contains the world's third largest proven reserves of coal, 105,148 PJ of assessed resources of natural gas, and almost 32% of the world's estimated uranium resources at an extraction cost of below USD 130 per kg. Coal seams and gas fields cannot be artificially constructed by investing capital or changing policies; they only exist because of geologic time scales (Geoscience Australia, 2024).

Cost benchmarks are directly related to market position. The average cost of thermal coal production for Australia in 2025 is set to be close to USD 50 per tonne, compared to USD 59 for Colombia and USD 18 for Indonesia's low-grade coal (IEA, 2025). Australia will not compete on price for thermal coal with Indonesia, but it will compete on coal quality, the reliability of delivery, and proximity to markets for steel in Japan and South Korea.

In the case of LNG, the picture gets more complicated. Qatar's cost of breakeven delivery for LNG into Asia is near USD 3.00 per MMBtu, a function of large scale production, revenues from associated liquids, and a centralized low-wage labor structure. US Gulf Coast LNG sells for USD 5.50-6.00 per MMBtu due to Henry Hub pricing and flexible contracts. Australia's operational LNG facilities have a competitive edge, but forecasted greenfield expansions have breakeven costs of USD 6.00-9.00 per MMBtu (IEEFA, 2024). Cost comparisons are summarized in Table 2.

Table 2: LNG Production and Delivery Cost Benchmarks — Selected Producers
Source: IEEFA, Global LNG Outlook 2024-2028; World Bank, 2022.

Producer | Estimated Breakeven (USD/MMBtu) | Key Competitive Factor
Qatar | ~$3.00 | Economies of scale; liquids-rich fields; low-cost labor
USA (Gulf Coast) | ~$5.50-$6.00 | Liquid domestic market; flexible destination contracts
Australia (New Projects) | ~$6.00-$9.00 | Proximity to Asia; offset by higher labor and capital costs

3.2 Geographic and Institutional Advantages

Geography reinforces the resource advantage. Shipping routes from Pilbara LNG terminals or Queensland coal ports to Tokyo, Busan, or Taipei are shorter than those from the US Gulf Coast or Colombia. This difference in freight costs and delivery time has a significant impact on long-term supply contracts, where reliability is preferred over flexible spot market contracts.

Institutional factors are as important as geography. Australia is a stable democracy, with transparent legal systems, strong contract enforcement, and independent regulators. For energy companies with projects that run 20-30 years with multi-billion dollar investments, this sovereign risk premium is not insignificant. Key bilateral free trade agreements support this, with the Japan-Australia Economic Partnership Agreement (JAEPA) having a dedicated chapter for energy and mineral resources, and the Korea-Australia FTA having specific energy investment clauses (Department of Foreign Affairs and Trade [DFAT], 2024).

To offset labor costs, which are a genuine disadvantage when compared to Indonesia or Qatar, the Australian sector has focused on automation. Automated haulage systems have a strong presence in Pilbara coal and iron ore operations, as well as remote-operated export terminals that reduce staff at port facilities. This replacement of capital for labor maintains cost competitiveness even with Australian wages being much higher than most other economies (Australian Energy Producers, 2025).

3.3 Who Gains and Who Loses

While the benefits of Australia's energy trade are apparent, they are not equally distributed. The largest profits are made by multinational energy companies and the resource-rich state governments of Western Australia and Queensland, who use the royalties to fund their budgets; Western Australia has had fiscal surpluses because of these resource royalties. The reliable energy and resources of Australia are available to Asian industrial consumers, and the remote and regional Australian miners are paid better than the Australian average.

The negative impacts of Australia's energy trade are also apparent. The uncompetitive international gas prices sold to energy-intensive Australian manufacturers, particularly those in aluminium, glass, and chemicals, puts Australia's manufacturers at a disadvantage to manufacturers in countries with subsidised energy (IEEFA, 2024). Coal-dependent communities in Queensland and New South Wales that rely on coal for employment face long-run structural decline, with limited economic alternatives. The most impacted are Australia's Pacific neighbours, who experience rising sea levels and worsening cyclones as the climate deteriorates due to the emissions from Australian fossil fuel exports, with no international legal mechanism to recover these damages.

3.4 An Eroding Advantage and an Emerging One

Australia will no longer enjoy an unchallenged competitive edge in fossil fuel exports. Capital expenditure overruns on the Gorgon, Ichthys, and Prelude LNG projects have made global capital markets hesitant about future Australian offshore projects. Coal mines face rising rehabilitation costs combined with constrained access to project financing due to ESG compliance requirements (IEEFA, 2024).

However, a competitive advantage may be emerging. CSIRO's GenCost 2024-25 analysis shows that in Australia, a coal-fired or nuclear electricity generation system will be significantly more expensive than building a solar and wind-based electricity system, even coupled with battery storage (CSIRO, 2025). Australia, with its abundant lithium, cobalt, nickel, and rare earth elements, has the potential to become a major player in the international clean energy supply chain. This will depend on Australia's investment in downstream processing capacity, as compared to remaining a raw material supplier.

"""

SECTION4 = """\
4. Trade Policies and Market Distortions

4.1 The Australia-China Trade Dispute, 2020-2023

The Morrison Government's call for an international independent investigation into the origins of COVID-19, in early 2020, saw China resort to targeted economic retaliation. In the months that followed, Beijing instituted a series of informal bans, anti-dumping measures, and tariffs on Australian goods, of which coal was the most significant. A number of bulk carriers arrived off Chinese ports and were left unable to unload for weeks (International Journal of Multicultural and Multireligious Understanding, 2023).

The economic mechanism that followed is based on the critical distinction of diversion of trade versus destruction of trade. Coal is a global commodity that is highly fungible. With transportation costs included, the main difference that sets coal apart is its grade. The ban China issued on Australian coal did not abolish the demand for it, but changed where it was sold. Australian exporters initially had to accept discounts to find alternate buyers, and coal was redirected to India, Japan, and South Korea, and then to Europe, where the Russia-Ukraine War had begun to cause energy shortages. Chinese coal-fired power stations had to find alternate supplies of Indonesian and Russian coal, and these supplies were of longer supply chains, poorer quality and less cost competitive.

Instead of Australian coal prices collapsing, they surged as the global market for energy was driven to crisis. The Newcastle coal futures for 2022 surpassed USD 400 per tonne. During this time, China was forced to accept higher coal costs and lower industrial efficiency. The policy had substituted political goals for market efficiency signals, and the market set the cost for the initiating party (Xiang, Kuang & Li, 2017). In 2023, with domestic electricity shortages mounting, China quietly lifted the trade ban. Trade resumed.

However, the episode taught a lasting lesson to Australian exporters: the concentration of export revenue in a single, state-controlled market represents a geopolitical risk that typical corporate risk management fails to sufficiently cover (Export Finance Australia, 2024).

4.2 The Australian Domestic Gas Security Mechanism

Australia's worst domestic energy policy problem is not its exposure to foreign trading bloc embargoes. What is more troubling is that a country that produces 6,122 PJ of natural gas each year is unable to provide affordable gas to its own manufacturers and citizens. This is not a problem of natural resources. It is a problem of market structure.

Queensland's Curtis Island LNG terminals — QCLNG, APLNG, and GLNG — are contractually linked with international oil-indexed netback pricing. When Asian LNG spot prices increase, gas producers on Queensland's east coast are offered better prices for export than for domestic sales, because exporters will sell to the highest bidder. Domestic manufacturers are in competition with buyers in Japan and South Korea. Australian factories are forced to buy Australian gas at inflated global prices.

The Australian Domestic Gas Security Mechanism (ADGSM), created in 2017, aimed to resolve this by allowing the Minister for Resources to limit LNG exports if there was an anticipated annual domestic shortfall, in effect prioritizing domestic contracts over exports (DCCEEW, 2024). In response to the 2022 global energy crisis, where gas prices in the east made some manufacturing operations untenable, the ADGSM's annual trigger mechanism proved insufficient, and reforms were made for 2023. The main reforms were an automatic quarterly trigger, an emergency 12-month price cap of AUD 12 per gigajoule on new domestic wholesale contracts, and the introduction of a mandatory code of conduct in the domestic gas market enforced by the ACCC (Australian National Audit Office, 2024; Treasury, 2022).

There is a clear trade-off. For domestic users and manufacturers, the price cap provides much-needed relief. For LNG producers, it creates greater regulatory uncertainty and a higher risk for investors. The ADGSM was created to address a market failure — the externalization of domestic gas costs onto households. However, it risks creating a second-order failure by reducing the investment signals needed to expand the upstream supply that would ultimately resolve the structural shortage. Determining whether this efficiency cost is justified depends on whether higher domestic prices would have actually created new supply within a commercially viable timeframe, which is unlikely given the capital requirements and lead times of offshore gas development.

4.3 The Safeguard Mechanism and Renewable Energy Policy

Australia's 2023 Safeguard Mechanism reforms have been the greatest changes to Australia's energy regulatory framework in a decade. The mechanism was introduced in 2016 and created largely nominal emissions baselines for the 215 largest industrial facilities, each emitting over 100,000 tonnes of CO2-equivalent per year. These facilities include all the major LNG export terminals and coal mines and make up roughly 30% of Australia's total emissions. Initially, most facilities were not at risk of any real emissions targets enforcement (HopgoodGanim, 2023).

The 2023 reforms changed this materially. They created a system in which emissions baselines had to be decreased by 4.9% a year, the total emissions for the scheme were capped, and any new gas fields for LNG export had to demonstrate "zero reservoir carbon" upon commencement. The new gas fields had to either implement Carbon Capture and Storage technology or buy high-quality carbon offsets from the outset (DLA Piper, 2023). For current participants, costs for compliance increase each year. For future participants, the zero-carbon requirement changes the economics of the entire project.

In conjunction, the federal government initiated the AUD 4 billion Hydrogen Headstart program to fund early-stage green hydrogen projects and bridge the gap between existing costs and future market viability (DCCEEW, 2024). Projects include the 1.5 GW Murchison Green Hydrogen development in Western Australia and the Hunter Valley Hydrogen Hub in New South Wales, alongside an 82% national renewable electricity target by 2030 and a legislated Net Zero by 2050 trajectory.

These policies result in the internal shift of capital from the fossil fuel sector to the clean energy sector. The existing LNG operators will deal with higher costs of doing business and a more uncertain investment climate. Meanwhile, renewable energy and green hydrogen developers benefit from direct subsidies and a more favorable regulatory stance. Determining if net efficiency has improved or worsened is a matter of weighing the interference of subsidies against the prior distortion of unregulated carbon externalities. The Pigouvian case for carbon pricing, with its assertion that a tax set at the social cost of emissions increases overall efficiency, supports the direction of these reforms, even if the specific mechanisms are also distortive.

"""

SECTION5 = """\
5. Globalization and Energy Security

Globalization has connected Australia to the world economy such that large external disturbances now transmit to the domestic economy in a very short time. The outcome is a strategic contradiction where Australia, one of the largest energy exporters in the world, has critical problems of energy security of its own.

Liquid fuel imports exemplify this issue. While Australia produces extensive primary energy, around 90% of transport fuels — petrol, diesel, and jet fuel — are imported from South Korean, Singaporean, and Malaysian refineries (The Guardian, 2026). Supported by federal funding, the remaining domestic refineries number only two. Historically, strategic reserve holdings were insufficient for the International Energy Agency's 90-day net import requirement. Under the 2023 Minimum Stockholding Obligation, Australia must keep only 20-32 days of diesel and 24-27 days of petrol and jet fuel (DCCEEW, 2024). This reserve would run out quickly during a substantial interruption of the Asian maritime supply chain. A South China Sea conflict, or significant disruption to South Korean or Singaporean refining, would immediately affect Australian transport and logistics.

The Russia-Ukraine war illustrated the speed at which an offshore geopolitical event can impact local energy markets. In 2022, as European buyers scrambled to fill the gap of sanctioned Russian pipeline gas, global LNG spot prices surged, and Australia, as an alternative supplier, benefited. Woodside Energy contracted to supply around 0.8 million tonnes per year to Germany's Uniper through 2039 (Woodside Energy, 2022). But the same price increases transmitted immediately into the Australian east coast gas market, threatening the viability of Australian manufacturing and triggering the emergency AUD 12/GJ price cap. Being tied to international commodity markets means exposure to international commodity volatility in both directions.

China represents the most acute geopolitical concern. China accounted for almost 40% of Australian goods exports prior to the 2020 dispute. By 2023, even with significant diversification efforts, that number had only dropped to 32% (Export Finance Australia, 2024). This is due to China's continuing reliance on Australian iron ore, for which no viable alternative has been found. The AUKUS security alliance brings Australia, the UK, and the US closer together in defense and technology. It creates a security dependence on the US and an economic dependence on China that is difficult to balance simultaneously.

The energy transition will create a more structural issue for Australia's export model. The IEA's Net Zero Emissions scenario shows a 69% drop in coal demand by 2035 and 95% by 2050 (Queensland Competition Authority, 2024). For regional economies in New South Wales and Queensland, this means stranded assets on a substantial scale — mines, rail networks, port infrastructure, and communities built around thermal coal with no obvious economic alternative. Critical minerals offer a partial solution. In 2023, Australia exported AUD 19 billion in lithium. The Reserve Bank of Australia expects that the country's exports of lithium, copper, and nickel could reach 10% of total resource exports by 2030 (RBA, 2025). The US Inflation Reduction Act will create additional demand for Australian critical minerals through the US-Australia Free Trade Agreement, but will simultaneously draw downstream processing investment toward the US rather than Australian manufacturing capacity.

The question is whether three decades of sustained commodity demand from Asia and the associated wealth creation can still be seen as net positive in light of the shifting geopolitical foundations of that interdependence. The composition of what Australia sells, to whom it sells, and under what security conditions is changing. Managing the transition from fossil fuel exporter to clean energy supply chain partner is the central economic challenge of the coming generation, and Australia does not yet have a settled answer for how it will do so.

"""

SECTION6 = """\
6. Conclusion

Australia's place in the global energy economy presents an analytical challenge, as it complicates conventional frameworks. Australia is a major primary energy exporter and yet cannot sustain its own transport system in energy terms. It enjoys a comparative advantage due to fossil fuels; however, the world is witnessing diminishing demand for these very resources. It is a stable democracy that has built deep economic interdependence with a geopolitical rival.

Comparative advantages in energy exports are the result of considerable geological endowment, geographic proximity to the world's most rapidly growing energy demand, a reliable institutional framework, and decades of capital investment in infrastructure that competitors cannot quickly replicate. These advantages have generated coal and LNG export revenues that funded state government services, enriched shareholders, and supported regional employment across multiple decades. In the short and medium term, Asian industrial economies still need Australian coal and gas to keep power grids running and steel mills operating.

However, the longer-term structural situation is increasingly complex. Competing with LNG sources in Qatar and the United States presents a real challenge due to breakeven costs on new projects. Following cost overruns associated with Gorgon, Ichthys, and Prelude, investors have become increasingly risk-averse. Australia's current fuel reserve situation is inadequate and would be deemed critically low in most other countries. China is Australia's most significant trading partner, accounting for 32% of total exports, and has demonstrated willingness to utilize trade as a political weapon.

The 2023 policy reforms — the Safeguard Mechanism revisions, the Hydrogen Headstart program, and the 82% renewables target — intentionally make fossil fuel investment less attractive while directing capital toward clean energy. Whether Australia successfully converts from fossil fuel exporter to clean energy supply chain partner depends on choices not yet made: whether it develops domestic capacity to process lithium and nickel rather than exporting raw ore, whether it builds the hydrogen infrastructure to compete internationally, and whether its security alliances can be leveraged into economic partnerships that reduce exposure to a single dominant customer. The analytical tools from this course — comparative advantage, trade policy distortions, deadweight loss, and the costs and benefits of globalization — do not answer those questions, but they make the implications of each choice legible.

"""

REFERENCES = """\
References

Argus Media. (2024). Australia extends subsidy plan for refiners to 2030. https://www.argusmedia.com/en/news-and-insights/latest-market-news/2803693-australia-extends-subsidy-plan-for-refiners-to-2030

APA Group. (2024). Moomba Sydney Pipeline and MSEP. https://www.apa.com.au/operations-and-projects/gas/gas-transmission/moomba-sydney-pipeline-and-msep

Australian Energy Producers. (2024). Media release: Australian oil and gas industry delivers record $22 billion in taxes and royalties. https://energyproducers.au/news/all_news/media-release-australian-oil-gas-industry-delivers-record-22-billion-in-taxes-and-royalties-to-government-revenues-in-2024-25

Australian Energy Producers. (2025). Australia's natural gas investment competitiveness. https://energyproducers.au/wp-content/uploads/2025/05/AEP-Australias-Natural-Gas-Investment-Competitiveness-Final.pdf

Australian Energy Regulator (AER). (2024). State of the energy market 2024: Gas markets in eastern Australia. https://www.aer.gov.au/system/files/2024-11/State%20of%20the%20energy%20market%202024%20-%20Chapter%204%20-%20Gas%20markets%20in%20eastern%20Australia.pdf

Australian National Audit Office (ANAO). (2024). Design of the Energy Price Relief Plan. https://www.anao.gov.au/work/performance-audit/design-of-the-energy-price-relief-plan

CSIRO. (2025). GenCost 2024-25 final report. https://www.csiro.au/en/research/technology-space/energy/electricity-transition/gencost

Department of Climate Change, Energy, the Environment and Water (DCCEEW). (2024). Gas market review report. https://www.dcceew.gov.au/sites/default/files/documents/gas-market-review-report.pdf

Department of Climate Change, Energy, the Environment and Water (DCCEEW). (2024). Hydrogen Headstart program. https://www.dcceew.gov.au/energy/hydrogen/hydrogen-headstart-program

Department of Climate Change, Energy, the Environment and Water (DCCEEW). (2024). Minimum stockholding obligation. https://www.dcceew.gov.au/energy/security/australias-fuel-security/minimum-stockholding-obligation

Department of Climate Change, Energy, the Environment and Water (DCCEEW). (2025). Australian Energy Update 2025. https://www.energy.gov.au/sites/default/files/2025-08/australian_energy_update_2025.pdf

Department of Foreign Affairs and Trade (DFAT). (2024). Summary of JAEPA chapters and annexes. https://www.dfat.gov.au/trade/agreements/in-force/jaepa/full-text/Pages/summary-of-jaepa-chapters-and-annexes

DLA Piper. (2023). Safeguard mechanism reform: Legislative cap on emissions. https://www.dlapiper.com/insights/publications/2023/03/safeguard-mechanism-reform-legislative-cap-on-emissions-changes-agreed-by-the-australian-government

Export Finance Australia. (2024). China: Record imports from Australia but economic headwinds mount. https://www.exportfinance.gov.au/resources/world-risk-developments/2024/july/china-record-imports-from-australia-but-economic-headwinds-mount/

Geoscience Australia. (2024). Australia's Energy Commodity Resources (AECR) 2025. https://www.ga.gov.au/aecr2025/production-and-trade

HopgoodGanim Lawyers. (2023). Safeguard mechanism reforms: What you need to know. https://www.hopgoodganim.com.au/news-insights/safeguard-mechanism-reforms/

Institute for Energy Economics and Financial Analysis (IEEFA). (2023). Global LNG Outlook 2024-2028. https://www.energy.gov.au/sites/default/files/2023-06/Ex%20L%20IEEFA%2C%20Global%20LNG%20Outlook.pdf

Institute for Energy Economics and Financial Analysis (IEEFA). (2024). The hidden costs of the LNG boom. https://ieefa.org/resources/hidden-costs-lng-boom

International Energy Agency (IEA). (2023). Coal 2023: Analysis and forecast to 2026. https://iea.blob.core.windows.net/assets/a72a7ffa-c5f2-4ed8-a2bf-eb035931d95c/Coal_2023.pdf

International Energy Agency (IEA). (2025). Coal 2025: Prices and costs. https://www.iea.org/reports/coal-2025/prices-and-costs

International Journal of Multicultural and Multireligious Understanding. (2023). Australia-China trade tensions during the COVID-19 pandemic. https://ijmmu.com/index.php/ijmmu/article/download/4293/3790

Krugman, P., Obstfeld, M., & Melitz, M. (2023). International economics: Theory and policy (12th ed.). Pearson.

National Competition Council. (2019). Dalrymple Bay Coal Terminal master plan. https://ncc.gov.au/images/uploads/CECTQlAp-006.pdf

Observatory of Economic Complexity (OEC). (2024). Refined petroleum in Australia. https://oec.world/en/profile/bilateral-product/refined-petroleum/reporter/aus

Queensland Competition Authority (QCA). (2024). Depreciation approaches at UT6: NERA report. https://www.qca.org.au/wp-content/uploads/2025/12/attachment-c-nera-report-depreciation-approaches.pdf

Reserve Bank of Australia (RBA). (2025). The global energy transition and critical minerals. https://www.rba.gov.au/publications/bulletin/2025/oct/the-global-energy-transition-and-critical-minerals.html

The Guardian. (2026, March 24). Seven charts that reveal how unprepared Australia was for the fuel crisis. https://www.theguardian.com/business/2026/mar/24/seven-charts-that-reveal-how-unprepared-australia-was-for-the-fuel-crisis

Treasury, Australian Government. (2022). Energy Price Relief Plan. https://www.pm.gov.au/media/energy-price-relief-plan

Woodside Energy. (2022). Third quarter 2022 report. https://www.woodside.com/docs/default-source/asx-announcements/2022/third-quarter-2022-report.pdf

World Bank. (2022). Analytical foundation for increased Pan-Arab regional gas trade. https://ppp.worldbank.org/sites/default/files/2022-06/Analytical_Foundation_for_Increased_Pan-Arab_Regional_Gas_Trade.pdf

Xiang, H., Kuang, Y., & Li, C. (2017). Impact of the China-Australia FTA on global coal production and trade. Journal of Policy Modeling, 39(1), 65-78. https://ideas.repec.org/a/eee/jpolmo/v39y2017i1p65-78.html
"""

# ── auth ─────────────────────────────────────────────────────────────────────

def get_creds():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(base, "token.json")) as f: td = json.load(f)
    with open(os.path.join(base, "credentials.json")) as f: cd = json.load(f)
    ci = cd.get("installed") or cd.get("web", {})
    creds = Credentials(
        token=td.get("token"), refresh_token=td.get("refresh_token"),
        token_uri=ci.get("token_uri"), client_id=ci.get("client_id"), client_secret=ci.get("client_secret"),
    )
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(os.path.join(base, "token.json"), "w") as f: f.write(creds.to_json())
    return creds


def find_para(body, prefix):
    for e in body:
        if "paragraph" not in e: continue
        txt = "".join(r.get("textRun",{}).get("content","") for r in e["paragraph"].get("elements",[])).strip()
        if txt.startswith(prefix):
            return e.get("startIndex",0), e.get("endIndex",0)
    return None

def find_all(body, search):
    res = []
    for e in body:
        if "paragraph" not in e: continue
        txt = "".join(r.get("textRun",{}).get("content","") for r in e["paragraph"].get("elements",[])).strip()
        if search in txt:
            res.append((e.get("startIndex",0), e.get("endIndex",0)))
    return res

def find_text_idx(body, search):
    for e in body:
        if "paragraph" not in e: continue
        txt = "".join(r.get("textRun",{}).get("content","") for r in e["paragraph"].get("elements",[]))
        if search in txt:
            return e.get("startIndex",0) + txt.find(search)
    return None


def main():
    print("Connecting...", flush=True)
    creds = get_creds()
    docs  = build("docs",  "v1", credentials=creds)
    drive = build("drive", "v3", credentials=creds)

    # Get current doc end
    doc = docs.documents().get(documentId=DOC_ID).execute()
    body = doc.get("body",{}).get("content",[])
    end_idx = body[-1].get("endIndex", 2) - 1

    full_text = (COVER + "\n" + INTRO + SECTION2 + SECTION3 + SECTION4 + SECTION5 + SECTION6 + REFERENCES)

    # Delete and re-insert
    print("Replacing body...", flush=True)
    docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": [
        {"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end_idx}}}
    ]}).execute()
    docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": [
        {"insertText": {"location": {"index": 1}, "text": full_text}}
    ]}).execute()

    # Re-read
    print("Applying formatting...", flush=True)
    doc2 = docs.documents().get(documentId=DOC_ID).execute()
    body2 = doc2.get("body",{}).get("content",[])
    doc_end = body2[-1].get("endIndex", 2) - 1

    reqs = []

    # Base: Times New Roman 12pt, 1.5 spacing, black
    reqs.append({"updateTextStyle": {
        "range": {"startIndex": 1, "endIndex": doc_end},
        "textStyle": {
            "weightedFontFamily": {"fontFamily": "Times New Roman"},
            "fontSize": {"magnitude": 12, "unit": "PT"},
            "bold": False, "italic": False,
            "foregroundColor": {"color": {"rgbColor": BLACK}},
        },
        "fields": "weightedFontFamily,fontSize,bold,italic,foregroundColor"
    }})
    reqs.append({"updateParagraphStyle": {
        "range": {"startIndex": 1, "endIndex": doc_end},
        "paragraphStyle": {"lineSpacing": 150, "spaceBelow": {"magnitude": 6, "unit": "PT"}},
        "fields": "lineSpacing,spaceBelow"
    }})

    # Cover: center + navy
    for search, size, bold in [
        ("Australia: Energy, Trade", 18, True),
        ("World Economy", 13, False),
        ("Max Herman", 13, False),
        ("Professor: Luisa", 12, False),
        ("Universidad Europea", 12, False),
        ("May 29, 2026", 12, False),
    ]:
        hits = find_all(body2, search)
        for (s, e) in hits:
            reqs.append({"updateParagraphStyle": {
                "range": {"startIndex": s, "endIndex": e},
                "paragraphStyle": {"alignment": "CENTER", "spaceBelow": {"magnitude": 14, "unit": "PT"}, "lineSpacing": 150},
                "fields": "alignment,spaceBelow,lineSpacing"
            }})
            reqs.append({"updateTextStyle": {
                "range": {"startIndex": s, "endIndex": e - 1},
                "textStyle": {
                    "weightedFontFamily": {"fontFamily": "Times New Roman"},
                    "fontSize": {"magnitude": size, "unit": "PT"},
                    "bold": bold,
                    "foregroundColor": {"color": {"rgbColor": NAVY}},
                },
                "fields": "weightedFontFamily,fontSize,bold,foregroundColor"
            }})

    # Main section headings: navy bold 13pt
    for h in ["1. Introduction","2. Australia in the Global","3. Comparative Advantage",
              "4. Trade Policies","5. Globalization and Energy Security","6. Conclusion","References"]:
        r = find_para(body2, h)
        if r:
            s, e = r
            reqs.append({"updateTextStyle": {
                "range": {"startIndex": s, "endIndex": e - 1},
                "textStyle": {"weightedFontFamily": {"fontFamily": "Times New Roman"},
                              "fontSize": {"magnitude": 13, "unit": "PT"}, "bold": True,
                              "foregroundColor": {"color": {"rgbColor": NAVY}}},
                "fields": "weightedFontFamily,fontSize,bold,foregroundColor"
            }})
            reqs.append({"updateParagraphStyle": {
                "range": {"startIndex": s, "endIndex": e},
                "paragraphStyle": {"spaceAbove": {"magnitude": 14, "unit": "PT"}, "spaceBelow": {"magnitude": 6, "unit": "PT"}},
                "fields": "spaceAbove,spaceBelow"
            }})

    # Sub-headings: navy bold 12pt
    for sh in ["2.1 Production","2.2 Exports","2.3 Companies",
               "3.1 Factor","3.2 Geographic","3.3 Who Gains","3.4 An Eroding",
               "4.1 The Australia-China","4.2 The Australian Domestic","4.3 The Safeguard"]:
        r = find_para(body2, sh)
        if r:
            s, e = r
            reqs.append({"updateTextStyle": {
                "range": {"startIndex": s, "endIndex": e - 1},
                "textStyle": {"bold": True, "foregroundColor": {"color": {"rgbColor": NAVY}}},
                "fields": "bold,foregroundColor"
            }})
            reqs.append({"updateParagraphStyle": {
                "range": {"startIndex": s, "endIndex": e},
                "paragraphStyle": {"spaceAbove": {"magnitude": 8, "unit": "PT"}},
                "fields": "spaceAbove"
            }})

    # Table/figure captions: navy bold
    for cap in ["Table 1:","Table 2:","Table 3:","Figure 1:","Figure 2:","Figure 3:"]:
        r = find_para(body2, cap)
        if r:
            s, e = r
            reqs.append({"updateTextStyle": {
                "range": {"startIndex": s, "endIndex": e - 1},
                "textStyle": {"bold": True, "italic": False, "foregroundColor": {"color": {"rgbColor": NAVY}}},
                "fields": "bold,italic,foregroundColor"
            }})

    # Source lines: italic
    for (s, e) in find_all(body2, "Source: "):
        reqs.append({"updateTextStyle": {
            "range": {"startIndex": s, "endIndex": e - 1},
            "textStyle": {"italic": True}, "fields": "italic"
        }})

    # Send in chunks
    print(f"Sending {len(reqs)} formatting requests...", flush=True)
    for i in range(0, len(reqs), 50):
        docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": reqs[i:i+50]}).execute()

    # Re-insert charts
    print("Re-inserting charts...", flush=True)
    LNG_ID    = "1vEvlU3n-8HrlO8buaFWZU62P2b5uQAYw"
    EXPORT_ID = "1uNVj8abadlwWd25rx1UvtrLLeHp00Hep"

    doc3  = docs.documents().get(documentId=DOC_ID).execute()
    body3 = doc3.get("body",{}).get("content",[])

    idx1 = find_text_idx(body3, "[CHART: Figure 1")
    if idx1:
        docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": [{"insertInlineImage": {
            "location": {"index": idx1},
            "uri": f"https://drive.google.com/uc?export=view&id={LNG_ID}",
            "objectSize": {"width": {"magnitude": 430, "unit": "PT"}, "height": {"magnitude": 240, "unit": "PT"}}
        }}]}).execute()
        print("  Chart 1 inserted.", flush=True)

    doc4  = docs.documents().get(documentId=DOC_ID).execute()
    body4 = doc4.get("body",{}).get("content",[])
    idx3  = find_text_idx(body4, "[CHART: Figure 3")
    if idx3:
        docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": [{"insertInlineImage": {
            "location": {"index": idx3},
            "uri": f"https://drive.google.com/uc?export=view&id={EXPORT_ID}",
            "objectSize": {"width": {"magnitude": 400, "unit": "PT"}, "height": {"magnitude": 240, "unit": "PT"}}
        }}]}).execute()
        print("  Chart 3 inserted.", flush=True)

    print(f"\nDone. URL: https://docs.google.com/document/d/{DOC_ID}/edit", flush=True)


if __name__ == "__main__":
    main()
