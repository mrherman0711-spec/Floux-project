#!/usr/bin/env python3
"""
Replace the body text in the existing Australia Google Doc with humanized content.
Doc ID: 1LQTqcm_k-4R91DhZqy_cpNTNxEvWtnC76rIfoo3w8Dk
"""

import json, os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

DOC_ID = "1LQTqcm_k-4R91DhZqy_cpNTNxEvWtnC76rIfoo3w8Dk"

NAVY = {"red": 0.1059, "green": 0.1647, "blue": 0.2902}
WHITE = {"red": 1.0, "green": 1.0, "blue": 1.0}
LGREY = {"red": 0.945, "green": 0.953, "blue": 0.969}
BLACK = {"red": 0.1, "green": 0.1, "blue": 0.1}

# ── humanized section text ────────────────────────────────────────────────────

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

Australia exports roughly two-thirds of the primary energy it produces. Coal, liquefied natural gas (LNG), and uranium move from its mines and terminals to the industrial centers of East and South Asia in volumes that few countries can match. In the 2023-24 financial year, total primary energy production reached 19,232 petajoules (PJ), placing Australia among the highest-output energy economies in the world on a per-capita basis (Department of Climate Change, Energy, the Environment and Water [DCCEEW], 2025). It is the world's third-largest LNG exporter, the second-largest coal exporter, and holds approximately 32% of the world's reasonably assured uranium reserves (Geoscience Australia, 2024).

Fossil fuels dominate both production and consumption. Black coal accounts for the largest share of domestic energy output, followed by natural gas and oil. On the consumption side, oil products represent 40.7% of the primary energy mix, driven by the logistics demands of a continent spanning 7.7 million square kilometres. Renewables reached 9.3% of primary consumption in 2023-24, growing at around 4.9% annually over the previous decade (DCCEEW, 2025). Uranium is produced but not used domestically; Australia has no nuclear power generation capacity, so all uranium output goes to export.

The country's relevance in global energy markets is not purely about volume. As a stable OECD democracy in the Indo-Pacific, it has become a de facto energy security anchor for import-dependent economies in Japan, South Korea, and Taiwan. Long-term supply contracts underpin much of the LNG trade, which means the relationships carry political weight that goes beyond standard commercial arrangements. At the same time, the clean energy transition presents a structural problem: the two largest Australian exports, coal and LNG, face declining long-run demand prospects. Critical minerals like lithium, nickel, and cobalt offer a potential alternative, but that transition is far from complete.

This paper works through Australia's energy position using standard tools from international economics. Section 2 maps production, consumption, trade flows, and physical infrastructure. Section 3 examines the sources of Australia's comparative advantage in energy exports and asks who benefits and who bears the costs. Section 4 analyzes three policies that distort Australia's energy markets: the 2020-23 China trade dispute, the Australian Domestic Gas Security Mechanism, and the 2023 Safeguard Mechanism reforms. Section 5 addresses the energy security vulnerabilities that globalization has created alongside the wealth it has generated. Section 6 draws the analysis together.

"""

SECTION2 = """\
2. Australia in the Global Energy Market

2.1 Production and Consumption

Australia's energy production is large and skewed heavily toward fossil fuels. In 2023-24, black coal output reached 11,398.4 PJ, recovering from two years of La Nina-related flooding that had shut major mines in Queensland and New South Wales. Natural gas production stood at 6,122.0 PJ, brown coal at 416.4 PJ, oil and LPG at 738.5 PJ, and renewables at 557.1 PJ (DCCEEW, 2025). Table 1 shows the five-year production trend by fuel source.

Table 1: Australia's Primary Energy Production by Source, 2019-2024 (Petajoules)
Source: DCCEEW, Australian Energy Statistics Table J, 2025.

Fuel Source | 2019-20 | 2020-21 | 2021-22 | 2022-23 | 2023-24
Black Coal | 12,316.8 | 11,359.6 | 11,215.7 | 11,084.4 | 11,398.4
Brown Coal | 425.4 | 430.0 | 415.7 | 400.9 | 416.4
Natural Gas | 5,993.9 | 5,730.0 | 5,830.5 | 6,198.6 | 6,122.0
Oil and LPG | 799.0 | 718.0 | 723.0 | 771.4 | 738.5
Renewables | 418.8 | 464.6 | 513.0 | 551.7 | 557.1
TOTAL | 19,953.9 | 18,702.2 | 18,697.9 | 20,007.0 | 19,232.4

Domestic consumption is far smaller than production. Australia used 5,976.7 PJ in 2023-24, a 0.5% increase over the prior year, with fossil fuels accounting for 91% of that total: oil at 40.7%, coal at 25.3%, and gas at 24.7%. The dominance of oil in consumption reflects the country's continental geography, where road and air freight demand is structurally high and electrification of transport has barely started. Renewables reached 9.3% of primary consumption in 2023-24, growing steadily as rooftop solar penetration rises and utility-scale wind and solar projects come online (DCCEEW, 2025).

The net export position is the defining feature of Australia's energy economy. The country exports approximately 67% of its primary energy production. At the height of the global commodity price spike in 2022-23, energy commodity export earnings reached a record AUD 238.7 billion (Geoscience Australia, 2024).

2.2 Exports, Imports, and Trade Partners

By value in 2022-23, LNG was the largest energy export at AUD 92.2 billion (approximately USD 61 billion), followed by thermal coal at AUD 65.5 billion, metallurgical coal at AUD 61.9 billion, and crude oil and feedstocks at AUD 13.2 billion. By volume in 2023-24, black coal led at 10,056.9 PJ (approximately 356 million tonnes), with LNG at 4,508.5 PJ (approximately 81 million tonnes) accounting for 29.5% of total energy export volume (DCCEEW, 2025). Figure 1 shows LNG export revenues from 2015 to 2023.

[CHART: Figure 1 — LNG Revenue]

Australia's energy trade is concentrated in North-East Asia. For LNG, Japan absorbed 32.1 million tonnes in 2022, China 23.3 Mt, South Korea 12.7 Mt, and Taiwan 8.1 Mt (Institute for Energy Economics and Financial Analysis [IEEFA], 2023). Table 3 shows the five-year breakdown of LNG volumes by destination.

Table 3: Australian LNG Export Volumes by Destination Country, 2018-2022 (Million Tonnes)
Source: IEEFA, Global LNG Outlook, 2023.

Destination | 2018 | 2019 | 2020 | 2021 | 2022
Japan | 31.0 | 31.5 | 30.6 | 28.3 | 32.1
China | 25.1 | 30.6 | 31.4 | 33.8 | 23.3
South Korea | 8.5 | 8.3 | 8.7 | 10.1 | 12.7
Taiwan | 2.8 | 4.5 | 4.9 | 6.5 | 8.1
Other | 4.9 | 5.5 | 6.2 | 5.2 | 7.5
TOTAL | 72.3 | 76.4 | 81.8 | 81.9 | 83.7

Despite its primary energy surplus, Australia imports roughly 90% of its refined petroleum products. In 2024, refined petroleum was the country's largest single import by value at USD 31.6 billion, sourced mainly from South Korea, Singapore, Malaysia, and India (Observatory of Economic Complexity, 2024). A country that produces enormous volumes of raw energy but cannot refine enough of it to fuel its own transport network is not simply an irony; it is a security vulnerability that becomes relevant in any scenario where Asian supply chains are disrupted.

2.3 Companies and Infrastructure

The Australian energy sector is dominated by a concentrated group of multinationals and domestic firms. Woodside Energy operates the Pluto LNG terminal (4.9 Mtpa capacity) and co-ventures the North West Shelf facility (16.9 Mtpa) in Western Australia. Chevron Australia manages Gorgon (15.6 Mtpa) and Wheatstone (8.9 Mtpa). Shell operates Prelude Floating LNG (3.6 Mtpa) offshore Western Australia and QCLNG (8.5 Mtpa) on Curtis Island, Queensland. Santos runs the GLNG terminal, ConocoPhillips operates APLNG, and Inpex leads the Ichthys project (8.9 Mtpa) in the Northern Territory alongside Darwin LNG (3.7 Mtpa). BHP and Glencore dominate coal extraction, particularly in Queensland's Bowen Basin and New South Wales's Hunter Valley (Australian Energy Regulator [AER], 2024).

Coal leaves Australia through some of the world's highest-capacity export ports. The Port of Newcastle processes over 150 million tonnes per annum, while Hay Point, Dalrymple Bay, and Abbot Point in Queensland handle most seaborne metallurgical coal exports (National Competition Council, 2019). Domestic gas is distributed through the Dampier to Bunbury Natural Gas Pipeline (895 TJ/day capacity) in Western Australia and the Moomba Sydney Pipeline network (590 TJ/day) on the east coast (APA Group, 2024).

Figure 2: Australia's LNG Terminals and Major Coal Export Ports
(Geographic distribution: LNG terminals concentrated in Western Australia [Gorgon, Wheatstone, Pluto, North West Shelf, Prelude], Northern Territory [Darwin, Ichthys], and Queensland [QCLNG, APLNG, GLNG on Curtis Island]. Coal ports in New South Wales [Newcastle] and Queensland [Hay Point, Dalrymple Bay, Abbot Point].)
Source: The Energy Consulting Group / EIA, Australia Oil and Gas Overview.

Australia's domestic refining capacity has collapsed to two facilities: Ampol's Lytton refinery in Brisbane (109,000 barrels per day) and Viva Energy's Geelong plant (120,000 b/d). Both survive through federal government subsidies under the Fuel Security Services Payment program, extended to 2030 to prevent complete dependence on imported liquid fuels (Argus Media, 2024).

Figure 3: Australian Energy Export Mix by Value, 2022-23
Source: Geoscience Australia, AECR 2025.

[CHART: Figure 3 — Export Mix by Value]

The energy sector's macroeconomic contribution is considerable: the oil and gas industry represents 3.7% of GDP and delivered an estimated AUD 21.9 billion in federal and state taxes and royalties in 2024-25 (Australian Energy Producers, 2024). Australia ranks third in LNG exports, second in coal exports, and fourth in uranium production (Geoscience Australia, 2024).

"""

SECTION3 = """\
3. Comparative Advantage and International Trade

3.1 Factor Endowments and the Source of Advantage

The classical theory of comparative advantage holds that countries gain from specializing in goods they can produce at lower opportunity cost relative to trading partners, even without an absolute cost advantage (Krugman, Obstfeld & Melitz, 2023). Australia's specialization in fossil fuel and uranium exports rests on three foundations: geological endowment, geographic position, and institutional reliability.

On geological grounds, Australia holds the world's third-largest proven coal reserves, 105,148 PJ of identified natural gas resources, and approximately 32% of the world's reasonably assured uranium resources at extraction costs below USD 130 per kilogram. These are not reproducible advantages. No policy decision or capital injection can create the coal seams of Queensland's Bowen Basin or the gas fields of the North West Shelf; they formed over geological timescales (Geoscience Australia, 2024).

Cost benchmarks show how geological advantage translates into market position. In thermal coal, Australia's average production cost in 2025 was approximately USD 50 per tonne. That is below Colombia at USD 59 per tonne, though well above Indonesia's ultra-low USD 18 per tonne, which reflects a structurally different and lower-grade resource base (IEA, 2025). Australia does not compete on price with Indonesian thermal coal; it competes on coal quality, delivery reliability, and proximity to steel-making markets in Japan and South Korea.

In LNG, the cost picture is more complicated. Qatar's breakeven delivery cost to Asian markets runs near USD 3.00 per MMBtu, built on massive scale, associated liquids revenues, and a centralized low-wage labor environment. US Gulf Coast LNG clears at roughly USD 5.50-6.00 per MMBtu, benefiting from Henry Hub domestic pricing and destination-flexible contracts. Australia's existing LNG plants are broadly competitive at prevailing market prices, but proposed greenfield expansions face estimated breakeven costs of USD 6.00-9.00 per MMBtu, making new investment difficult to justify except during sustained high price cycles (IEEFA, 2024). Table 2 summarizes these cost comparisons.

Table 2: LNG Production and Delivery Cost Benchmarks — Selected Producers
Source: IEEFA, Global LNG Outlook 2024-2028; World Bank, 2022.

Producer | Estimated Breakeven (USD/MMBtu) | Key Competitive Factor
Qatar | ~$3.00 | Economies of scale; liquids-rich fields; low-cost labor
USA (Gulf Coast) | ~$5.50-$6.00 | Liquid domestic market; flexible destination contracts
Australia (New Projects) | ~$6.00-$9.00 | Geographic proximity to Asia; offset by high labor costs and capital overruns

3.2 Geographic and Institutional Advantages

Geography reinforces the resource advantage. Shipping routes from Pilbara LNG terminals or Queensland coal ports to Tokyo, Busan, or Taipei are shorter than those from the US Gulf Coast or Colombia. That difference in freight cost and delivery time matters considerably in long-term supply contracts where reliability is valued above spot market flexibility.

Institutional factors matter as much as geography. Australia is a stable democracy with transparent legal systems, strong contract enforcement, and independent regulatory bodies. For energy companies making multi-billion dollar capital commitments on projects that run 20-30 years, this sovereign risk premium is not trivial. Key bilateral free trade agreements reinforce this: the Japan-Australia Economic Partnership Agreement (JAEPA) includes a dedicated chapter on energy and mineral resources, and the Korea-Australia FTA contains specific energy investment provisions (Department of Foreign Affairs and Trade [DFAT], 2024).

To offset structurally high labor costs, a genuine disadvantage relative to Indonesia or Qatar, the Australian sector has invested in automation. Autonomous haulage systems operate extensively in Pilbara coal and iron ore operations, and remote-operated export terminals reduce headcount at port facilities. This substitution of capital for labor preserves cost competitiveness even as Australian wages remain well above those in competing economies (Australian Energy Producers, 2025).

3.3 Who Gains and Who Loses

The gains from Australia's energy trade are real but uneven. Multinational energy companies capture significant returns on capital. State governments in Western Australia and Queensland receive royalty revenues that fund public services; WA in particular has run fiscal surpluses largely on the back of resource royalties. Asian industrial consumers get reliable access to high-quality energy inputs. The remote and regional mining workforce earns wages well above the national median.

The costs fall on specific groups. Domestic manufacturers, particularly energy-intensive industries like aluminium smelting, glass production, and chemicals, pay gas prices that track international netback levels rather than domestic cost of production. This erodes their competitiveness against industries in countries with regulated or subsidized energy access (IEEFA, 2024). Coal-dependent regional communities in Queensland and New South Wales face long-run structural decline as global thermal coal demand drops, with limited economic alternatives in many locations. Pacific Island neighbors bear the most direct external cost: rising sea levels and intensifying cyclones linked to global emissions from the combustion of Australian fossil exports, without any legal mechanism to recover those damages from Australian producers.

3.4 An Eroding Advantage and an Emerging One

Australia's comparative advantage in fossil fuel exports is not fixed. The Gorgon, Ichthys, and Prelude LNG projects all suffered severe capital cost overruns relative to original budgets, a pattern that has made global capital cautious about the next wave of Australian offshore investment. Aging coal mines face rising rehabilitation costs and shrinking access to international project finance as ESG criteria tighten in major lending institutions (IEEFA, 2024).

Against this, a new cost advantage is forming. CSIRO's GenCost 2024-25 analysis confirms that a reliable electricity system built on solar photovoltaics, onshore wind, and battery storage is the lowest-cost new-build electricity option in Australia by a wide margin over coal or nuclear generation (CSIRO, 2025). Combined with world-class lithium, cobalt, nickel, and rare earth endowments, Australia is well placed to become a major supplier to the global clean energy supply chain. Whether that potential converts into actual export revenues depends on whether Australia builds downstream processing capacity or remains a raw material supplier.

"""

SECTION4 = """\
4. Trade Policies and Market Distortions

4.1 The Australia-China Trade Dispute, 2020-2023

In early 2020, the Morrison government called for an independent international inquiry into the origins of COVID-19. China's response was economically targeted: over the following months, Beijing imposed informal bans, anti-dumping duties, and tariff barriers across a range of Australian exports, most consequentially coal. Dozens of bulk carriers arrived off Chinese ports and were left anchored for weeks, unable to unload (International Journal of Multicultural and Multireligious Understanding, 2023).

The economic mechanism that followed turns on a critical distinction: trade diversion versus trade destruction. Coal is a highly fungible global commodity. Grade and transport cost are the key differentiators, but thermal coal is ultimately thermal coal. China's ban did not destroy demand for Australian coal; it rerouted it. Australian exporters, initially forced to accept discounted prices while finding alternative buyers, redirected volumes to India, Japan, South Korea, and eventually Europe, where early-stage energy shortages from the Russia-Ukraine conflict were creating urgent demand (IEA, 2023). Chinese power plants and steel mills sourced replacement coal from Indonesia and Russia: lower quality, longer supply chains, and often at higher cost.

The price effects confirmed this logic. Rather than collapsing, Australian coal prices surged to historic highs during 2021-22 as the global energy crisis drove spot prices across all fuel markets. Newcastle coal futures, the Asia-Pacific benchmark, briefly exceeded USD 400 per tonne in 2022. Chinese buyers bore the deadweight loss of this episode in the form of higher input costs and deteriorating industrial efficiency. The policy substituted diplomatic goals for market efficiency signals, and the market imposed the costs on the initiating party (Xiang, Kuang & Li, 2017).

By 2023, facing domestic electricity shortages and a shifting diplomatic register under Australia's Albanese government, Beijing quietly lifted the ban. Trade flows normalized. But the episode left a durable lesson for Australian exporters: concentration of export revenue in a single state-controlled market is a geopolitical risk that standard corporate risk management does not adequately price (Export Finance Australia, 2024).

4.2 The Australian Domestic Gas Security Mechanism

Australia's most acute domestic energy policy problem is not its exposure to foreign embargoes. It is the fact that a country producing 6,122 PJ of natural gas annually has consistently failed to supply affordable gas to its own manufacturers and households. This is not a resource problem. It is a market architecture problem.

On Queensland's east coast, the Curtis Island LNG terminals, QCLNG, APLNG, and GLNG, are contractually linked to international oil-indexed netback pricing. When Asian LNG spot prices rise, gas producers on Queensland's east coast are offered higher prices for export sales than for domestic sales, because exporters sell to the highest bidder. Domestic manufacturers must compete directly with buyers in Japan and South Korea. Australian factories pay world prices for Australian gas extracted from Australian soil.

The Australian Domestic Gas Security Mechanism (ADGSM), introduced in 2017, was designed to address this. It gives the Minister for Resources the power to restrict LNG exports if an annual domestic supply shortfall is forecast, in effect prioritizing domestic demand over export contracts as a last resort (DCCEEW, 2024). When the global energy crisis of 2022 pushed east coast wholesale gas prices to levels that threatened manufacturing viability, the ADGSM's annual trigger mechanism proved too slow. The government responded with a 2023 reform package: quarterly activation triggers, an emergency 12-month price cap of AUD 12 per gigajoule on new domestic wholesale gas contracts, and a mandatory code of conduct enforced by the Australian Competition and Consumer Commission (ACCC) (Australian National Audit Office, 2024; Treasury, 2022).

The trade-off here is real and not yet resolved. For domestic users and manufacturers, the price cap provides immediate relief. For LNG producers, it introduces regulatory uncertainty that undermines the investment case for the upstream exploration needed to expand supply in the first place. A mechanism designed to correct a market failure, the externalization of domestic gas costs onto households, risks creating a second-order failure by depressing the investment signals that would eventually alleviate the underlying shortage. Whether that efficiency cost is justified depends on whether higher domestic prices would have actually incentivized new supply within a commercially viable timeframe, which is far from guaranteed given the capital requirements and long lead times of offshore gas development.

4.3 The Safeguard Mechanism and Renewable Energy Policy

Australia's 2023 Safeguard Mechanism reforms are the most significant structural shift in the country's energy regulatory framework in a decade. Originally established in 2016, the mechanism imposed largely nominal emissions baselines on the 215 largest industrial facilities, those emitting over 100,000 tonnes of CO2-equivalent per year. This group includes all major LNG export terminals and coal mines and collectively accounts for approximately 30% of national emissions. Baselines were initially set generously enough that few facilities faced real compliance pressure (HopgoodGanim, 2023).

The 2023 reforms changed this materially. They imposed a mandatory 4.9% annual reduction in emissions baselines, a hard cap on aggregate scheme emissions, and a requirement that any new gas fields developed for LNG export must demonstrate "zero reservoir carbon" upon commencement, meaning new projects must either deploy Carbon Capture and Storage technology or purchase high-quality carbon offsets from the outset (DLA Piper, 2023). For existing operators, compliance costs rise predictably each year. For prospective investors in new LNG development, the zero-carbon requirement transforms the economics of the project.

Simultaneously, the federal government introduced the AUD 4 billion Hydrogen Headstart program to subsidize early-stage green hydrogen projects and bridge the commercial gap between current costs and market viability (DCCEEW, 2024). Projects include the 1.5 GW Murchison Green Hydrogen development in Western Australia and the Hunter Valley Hydrogen Hub in New South Wales. These are paired with a national renewable electricity target of 82% by 2030 and a legislated Net Zero 2050 trajectory.

The combined effect of these policies is a structured transfer of capital from fossil fuel industries to the clean energy sector. Incumbent LNG operators face rising compliance costs and a less certain investment environment. Renewable energy developers and green hydrogen producers receive direct subsidies and a regulatory framework that favors their expansion. Whether this constitutes a net efficiency gain or a net efficiency loss depends on how one weighs the distortion of subsidies against the prior market failure of uncorrected carbon externalities. The Pigouvian case for carbon pricing argues that a tax set at the marginal social cost of emissions increases rather than reduces aggregate economic efficiency, which suggests the reforms move in the right direction even if the specific mechanism involves its own distortions.

"""

SECTION5 = """\
5. Globalization and Energy Security

Globalization has tied Australia into the world economy deeply enough that large offshore shocks now reach the domestic economy fast. The result is a strategic paradox: one of the world's largest energy exporters has serious energy security vulnerabilities of its own.

The most acute of these is liquid fuel. Despite producing vast quantities of primary energy, Australia imports approximately 90% of its transport fuels, petrol, diesel, and jet fuel, from Asian refineries in South Korea, Singapore, and Malaysia (The Guardian, 2026). Only two domestic refineries remain, both sustained by federal subsidies. Strategic reserve holdings have historically fallen well below the International Energy Agency's 90-day net import requirement. The Minimum Stockholding Obligation introduced in 2023 mandates only 20-32 days of diesel and 24-27 days of petrol and jet fuel (DCCEEW, 2024). That is a buffer that would exhaust rapidly under any serious disruption to Asian maritime supply chains. A conflict in the South China Sea or significant damage to Singapore or South Korean refining infrastructure would have immediate consequences for Australian transport and logistics.

The Russia-Ukraine war showed how quickly an offshore geopolitical shock reaches domestic energy markets. As European buyers scrambled to replace sanctioned Russian pipeline gas in 2022, global LNG spot prices surged. Australia benefited directly as an alternative supplier: Woodside Energy signed a long-term sales agreement with Germany's Uniper to supply approximately 0.8 million tonnes per annum through 2039 (Woodside Energy, 2022). But the same price surge transmitted immediately into the Australian east coast gas market, pushing wholesale prices to levels that threatened manufacturing viability and triggered the emergency AUD 12/GJ price cap. Being tied to international commodity markets means exposure to international commodity volatility in both directions.

China is the sharpest geopolitical tension. Before the 2020 dispute, China absorbed nearly 40% of Australian goods exports. By 2023, despite genuine diversification efforts, that share had only fallen to 32%, heavily underpinned by iron ore demand that China has not found a viable substitute for (Export Finance Australia, 2024). The AUKUS security alliance ties Australia to the United States and United Kingdom in defense and technology architecture, creating a duality that is difficult to sustain indefinitely: security dependency on Washington, economic prosperity dependency on Beijing.

Looking forward, the energy transition poses a structural threat to Australia's export model. Under the IEA's Net Zero Emissions scenario, global coal demand falls by 69% from current levels by 2035 and by 95% by 2050 (Queensland Competition Authority, 2024). For Queensland and New South Wales, that implies stranded assets on a substantial scale: mines, rail networks, port infrastructure, and regional economies built around thermal coal that may have no economically viable alternative function. Critical minerals offer a partial offset. Lithium exports alone reached AUD 19 billion in 2023, and the Reserve Bank of Australia projects that lithium, copper, and nickel could account for around 10% of total resource exports by 2030 (RBA, 2025). The US Inflation Reduction Act creates demand for Australian critical minerals through the US-Australia FTA's electric vehicle tax credit provisions, though the same legislation pulls downstream processing investment toward US rather than Australian manufacturing capacity.

The broader question is whether economic interdependence, which has generated enormous wealth over thirty years of sustained commodity demand from Asia, remains a net positive as the geopolitical foundations of that interdependence shift. The composition of what Australia sells, to whom it sells it, and under what security conditions is changing. Managing that transition from fossil fuel exporter to clean energy supply chain partner is the central economic challenge of the next generation, and Australia does not yet have a settled answer for how it will do so.

"""

SECTION6 = """\
6. Conclusion

Australia's position in the global energy economy is analytically useful precisely because it complicates the usual narratives. A massive exporter of primary energy that cannot reliably fuel its own transport network. A country with comparative advantage in fossil fuels facing a structural shift in global demand for those fuels. A stable democracy that has become economically dependent on a geopolitical rival.

The comparative advantage in energy exports is real and not accidental. It rests on geological abundance, geographic proximity to the world's fastest-growing energy demand, institutional reliability, and decades of capital investment in infrastructure that competitors cannot quickly replicate. These advantages have generated coal and LNG export revenues that funded state government services, enriched shareholders, and sustained regional workforces across multiple decades. In the short and medium term, Asian industrial economies still need Australian coal and gas to keep power grids running and steel mills operating.

But the structural picture is more complicated. New LNG projects face breakeven costs that struggle to compete with Qatar or the United States. Capital cost overruns at Gorgon, Ichthys, and Prelude have made international investors cautious. Domestic refined fuel security is critically thin by any standard measure. China represents 32% of goods export revenue and has already shown willingness to use trade as a diplomatic tool.

The 2023 policy reforms, the Safeguard Mechanism revisions, the Hydrogen Headstart program, and the 82% renewable electricity target, signal a deliberate shift away from fossil fuel dependency. Whether these translate into a new comparative advantage in clean energy depends on choices not yet made: whether Australia processes lithium and nickel domestically or exports raw ore, whether it builds the domestic hydrogen infrastructure to compete internationally, and whether its security alliances can be leveraged into economic partnerships that reduce exposure to a single large customer. The analytical framework from this course, comparative advantage, trade policy distortions, deadweight loss, globalization's costs and benefits, does not answer those questions. But it makes their economic implications legible.

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
    with open(os.path.join(base, "token.json")) as f:
        token_data = json.load(f)
    with open(os.path.join(base, "credentials.json")) as f:
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
        with open(os.path.join(base, "token.json"), "w") as f:
            f.write(creds.to_json())
    return creds


def main():
    print("Connecting to Google Docs...", flush=True)
    creds = get_creds()
    docs = build("docs", "v1", credentials=creds)

    # Step 1: Get current doc to find body bounds
    doc = docs.documents().get(documentId=DOC_ID).execute()
    body = doc.get("body", {}).get("content", [])

    # Find last body index (just before the end)
    end_index = body[-1].get("endIndex", 2) - 1  # subtract 1 for the trailing newline
    print(f"Current doc end index: {end_index}", flush=True)

    # Step 2: Delete all body content and re-insert humanized text
    # We delete from index 1 to end_index (exclusive of final newline)
    new_text = (
        COVER + "\n" +
        INTRO +
        SECTION2 +
        SECTION3 +
        SECTION4 +
        SECTION5 +
        SECTION6 +
        REFERENCES
    )

    print("Deleting existing body content...", flush=True)
    docs.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": [
            {"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end_index}}}
        ]}
    ).execute()

    print("Inserting humanized text...", flush=True)
    docs.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": [
            {"insertText": {"location": {"index": 1}, "text": new_text}}
        ]}
    ).execute()

    # Step 3: Apply formatting
    print("Re-applying formatting...", flush=True)
    doc2 = docs.documents().get(documentId=DOC_ID).execute()
    body2 = doc2.get("body", {}).get("content", [])

    def find_paragraphs_with_text(search_text):
        results = []
        for elem in body2:
            if "paragraph" not in elem:
                continue
            para_text = "".join(
                r.get("textRun", {}).get("content", "")
                for r in elem["paragraph"].get("elements", [])
            )
            if search_text in para_text:
                results.append((elem.get("startIndex", 0), elem.get("endIndex", 0), para_text.strip()))
        return results

    def find_paragraph_starting_with(prefix):
        for elem in body2:
            if "paragraph" not in elem:
                continue
            para_text = "".join(
                r.get("textRun", {}).get("content", "")
                for r in elem["paragraph"].get("elements", [])
            ).strip()
            if para_text.startswith(prefix):
                return elem.get("startIndex", 0), elem.get("endIndex", 0), para_text
        return None

    fmt_requests = []

    # Set all body text: Times New Roman 12pt, 1.5 spacing
    doc_end = body2[-1].get("endIndex", 2) - 1
    fmt_requests.append({
        "updateTextStyle": {
            "range": {"startIndex": 1, "endIndex": doc_end},
            "textStyle": {
                "weightedFontFamily": {"fontFamily": "Times New Roman"},
                "fontSize": {"magnitude": 12, "unit": "PT"},
                "bold": False,
                "italic": False,
                "foregroundColor": {"color": {"rgbColor": BLACK}},
            },
            "fields": "weightedFontFamily,fontSize,bold,italic,foregroundColor"
        }
    })
    fmt_requests.append({
        "updateParagraphStyle": {
            "range": {"startIndex": 1, "endIndex": doc_end},
            "paragraphStyle": {
                "lineSpacing": 150,
                "spaceBelow": {"magnitude": 6, "unit": "PT"},
            },
            "fields": "lineSpacing,spaceBelow"
        }
    })

    # Cover page: center + large title
    cover_lines = [
        ("Australia: Energy, Trade, and Globalization", 18, True),
        ("World Economy", 13, False),
        ("Max Herman", 13, False),
        ("Professor: Luisa", 12, False),
        ("Universidad Europea", 12, False),
        ("May 29, 2026", 12, False),
    ]
    for search, size, bold in cover_lines:
        matches = find_paragraphs_with_text(search)
        for (s, e, _) in matches:
            fmt_requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": s, "endIndex": e},
                    "paragraphStyle": {"alignment": "CENTER", "spaceBelow": {"magnitude": 12, "unit": "PT"}, "lineSpacing": 150},
                    "fields": "alignment,spaceBelow,lineSpacing"
                }
            })
            fmt_requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": s, "endIndex": e - 1},
                    "textStyle": {
                        "weightedFontFamily": {"fontFamily": "Times New Roman"},
                        "fontSize": {"magnitude": size, "unit": "PT"},
                        "bold": bold,
                        "foregroundColor": {"color": {"rgbColor": NAVY}},
                    },
                    "fields": "weightedFontFamily,fontSize,bold,foregroundColor"
                }
            })

    # Section headings: bold, navy, 13pt
    section_headings = [
        "1. Introduction",
        "2. Australia in the Global Energy Market",
        "3. Comparative Advantage and International Trade",
        "4. Trade Policies and Market Distortions",
        "5. Globalization and Energy Security",
        "6. Conclusion",
        "References",
    ]
    for heading in section_headings:
        result = find_paragraph_starting_with(heading)
        if result:
            s, e, _ = result
            fmt_requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": s, "endIndex": e - 1},
                    "textStyle": {
                        "weightedFontFamily": {"fontFamily": "Times New Roman"},
                        "fontSize": {"magnitude": 13, "unit": "PT"},
                        "bold": True,
                        "foregroundColor": {"color": {"rgbColor": NAVY}},
                    },
                    "fields": "weightedFontFamily,fontSize,bold,foregroundColor"
                }
            })
            fmt_requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": s, "endIndex": e},
                    "paragraphStyle": {"spaceAbove": {"magnitude": 12, "unit": "PT"}, "spaceBelow": {"magnitude": 6, "unit": "PT"}},
                    "fields": "spaceAbove,spaceBelow"
                }
            })

    # Sub-headings (2.1, 2.2 etc): bold, navy, 12pt
    sub_headings = [
        "2.1 Production", "2.2 Exports", "2.3 Companies",
        "3.1 Factor", "3.2 Geographic", "3.3 Who Gains", "3.4 An Eroding",
        "4.1 The Australia-China", "4.2 The Australian Domestic", "4.3 The Safeguard",
    ]
    for sh in sub_headings:
        result = find_paragraph_starting_with(sh)
        if result:
            s, e, _ = result
            fmt_requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": s, "endIndex": e - 1},
                    "textStyle": {
                        "bold": True,
                        "foregroundColor": {"color": {"rgbColor": NAVY}},
                    },
                    "fields": "bold,foregroundColor"
                }
            })

    # Table and figure captions: bold navy
    captions = [
        "Table 1:", "Table 2:", "Table 3:",
        "Figure 1:", "Figure 2:", "Figure 3:",
    ]
    for cap in captions:
        result = find_paragraph_starting_with(cap)
        if result:
            s, e, _ = result
            fmt_requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": s, "endIndex": e - 1},
                    "textStyle": {
                        "bold": True,
                        "italic": False,
                        "foregroundColor": {"color": {"rgbColor": NAVY}},
                    },
                    "fields": "bold,italic,foregroundColor"
                }
            })

    # Source lines under tables: italic
    source_lines = find_paragraphs_with_text("Source: ")
    for (s, e, txt) in source_lines:
        fmt_requests.append({
            "updateTextStyle": {
                "range": {"startIndex": s, "endIndex": e - 1},
                "textStyle": {"italic": True},
                "fields": "italic"
            }
        })

    # Send formatting in chunks
    print(f"Sending {len(fmt_requests)} formatting requests...", flush=True)
    for i in range(0, len(fmt_requests), 50):
        docs.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": fmt_requests[i:i+50]}
        ).execute()

    # Step 4: Re-insert charts
    print("Re-inserting charts...", flush=True)
    LNG_IMG_ID    = "1vEvlU3n-8HrlO8buaFWZU62P2b5uQAYw"
    EXPORT_IMG_ID = "1uNVj8abadlwWd25rx1UvtrLLeHp00Hep"

    doc3 = docs.documents().get(documentId=DOC_ID).execute()
    body3 = doc3.get("body", {}).get("content", [])

    def find_index_of_text(search, body_content):
        for elem in body_content:
            if "paragraph" not in elem:
                continue
            para_text = "".join(
                r.get("textRun", {}).get("content", "")
                for r in elem["paragraph"].get("elements", [])
            )
            if search in para_text:
                start = elem.get("startIndex", 0)
                offset = para_text.find(search)
                return start + offset
        return None

    chart1_idx = find_index_of_text("[CHART: Figure 1", body3)
    if chart1_idx is not None:
        docs.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": [{
                "insertInlineImage": {
                    "location": {"index": chart1_idx},
                    "uri": f"https://drive.google.com/uc?export=view&id={LNG_IMG_ID}",
                    "objectSize": {
                        "width":  {"magnitude": 430, "unit": "PT"},
                        "height": {"magnitude": 240, "unit": "PT"},
                    }
                }
            }]}
        ).execute()
        print("  Chart 1 inserted.", flush=True)

    # Re-read for chart 3 (index shifted after chart 1)
    doc4 = docs.documents().get(documentId=DOC_ID).execute()
    body4 = doc4.get("body", {}).get("content", [])
    chart3_idx = find_index_of_text("[CHART: Figure 3", body4)
    if chart3_idx is not None:
        docs.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": [{
                "insertInlineImage": {
                    "location": {"index": chart3_idx},
                    "uri": f"https://drive.google.com/uc?export=view&id={EXPORT_IMG_ID}",
                    "objectSize": {
                        "width":  {"magnitude": 400, "unit": "PT"},
                        "height": {"magnitude": 240, "unit": "PT"},
                    }
                }
            }]}
        ).execute()
        print("  Chart 3 inserted.", flush=True)

    print(f"\nDone. Doc URL: https://docs.google.com/document/d/{DOC_ID}/edit", flush=True)


if __name__ == "__main__":
    main()
