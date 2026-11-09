# **Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor** 

**Hrithik Lokhande** 

Data Science Intern (March 2026 – August 2026) | Unified Mentor Private Limited 

GitHub: | LinkedIn: 

## **Abstract** 

This study provides an empirical evaluation of domestic distribution networks to identify systemic transit delays, channel performance variances, and spatial bottlenecks. Analysing transactional shipment records across US shipping lanes, this paper measures fulfillment timelines using descriptive statistics, dynamic route normalization, and dispersion metrics. The analysis reveals tri-modal lead-time distributions, significant regional performance disparities, and trade-offs between shipping modes. We present an end-to-end framework incorporating exploratory data analysis (EDA), state-level performance indexing, and operational strategies to enhance supply chain resilience and minimize logistical friction. 

## **1. Introduction** 

Modern supply chain management relies on predictable fulfillment cycles. Delays in transit increase safety stock requirements, elevate holding costs, and diminish customer trust. Nassau Candy's national distribution network operates across diverse geographic destinations and logistics providers. However, systemic transit variances—exacerbated by infrastructure bottlenecks and carrier inconsistencies—lead to unpredictable fulfillment lead times. 

This research analyses transactional shipping data to identify the structural drivers of fulfillment latency. By establishing standardized operational metrics, evaluating transit lane efficiency, and conducting spatial performance profiling, this paper provides an evidence- 

based roadmap for optimizing freight scheduling and carrier allocation. 

## **2. Research Objectives** 

1. **Quantify Operational Latency:** Calculate fulfillment lead times across all historical orders and assess the underlying distribution profile. 

2. **Develop a Normalized Efficiency Metric:** Formulate a Route Efficiency Score ( _Er_ ) to benchmark performance across heterogeneous transit lanes. 

3. **Identify Regional Bottlenecks:** Isolate states and geographic corridors experiencing disproportionate fulfillment delays. 

4. **Evaluate Carrier & Channel Reliability:** Compare average transit times and variability (standard deviation) across shipping channels. 

5. **Formulate Strategic Interventions:** Provide actionable recommendations for inventory allocation, carrier management, and infrastructure planning. 

## **4. Methodology** 

#### **4.1 Data Preprocessing & Validation** 

1. **Temporal Standardization:** Raw order and ship dates were converted into standardized datetime64 objects. 

2. **Target Variable Engineering:** Individual fulfillment lead times ( _Li_ ) were calculated as: 



## **3. Dataset Description** 

The analysis utilizes transactional shipment records capturing key fulfillment parameters. 

- **Order Reference (Order ID):** Unique identifier for each customer transaction. 

- **Temporal Attributes (Order Date, Ship Date):** Timestamps marking order placement and factory dispatch. 

- **Geographic Attributes (Customer State, Customer Region, Factory Location):** Spatial origindestination metadata. 

- **Fulfillment Attributes (Ship Mode):** Logistics service channel (e.g., Standard, Second Class, Same Day, Expedited). 

- **Target Metric (Shipping Lead Time):** Calculated continuous variable representing transit duration in days. 

- **Composite Category (Route_State/Province):** Engineered lane identifier linking origin plants to destination states. 

where _T_ ship _,i_ is the dispatch date and _T_ order _,i_ is the order placement date. 

3. **Missing Value Handling & Geographic Normalization:** Data records were validated to ensure completeness, and state/province fields were standardized using twoletter postal codes for spatial mapping. 

#### **4.2 Mathematical Normalization & Metrics Formulation** 

To evaluate routes of varying volumes and distances, the **Route Efficiency Score (** _Er_ **)** was engineered to bound performance on a scale of [ 0,100 ]: 



Where: 

- _Lr_ is the mean lead time for a given route _r_ : 



- _Lmin_ and _Lmax_ represent the global minimum and maximum average lead times across all lanes in the active evaluation set. 

- _N r_ represents the total order volume for route _r_ . 



To measure channel stability, the sample standard deviation ( _σ r_ ) was computed for each shipping mode: 

## **5. EDA & Key Insights** 

The exploratory data analysis evaluates national distribution performance across temporal, geographic, and channel dimensions. By analysing shipment transaction records, this section isolates structural lead-time patterns, regional bottleneck corridors, and trade-offs between delivery speed and operational consistency. 

### **5.1 Multi-Modal Lead-Time Distribution** 



Figure 1: Distribution of National Freight Transit Lead Times Showing Tri-Modal Latency Clusters. 

As illustrated in **Figure 1** , the national fulfillment latency distribution exhibits strong rightskewness and distinct **tri-modal clustering** . Rather than displaying a uniform bell-curve distribution around the network mean (1287.7 days), order lead times split into three isolated operational tiers: 

- **Baseline Cluster (~900–950 Days):** Rapid-dispatch orders operating under optimal transit conditions without operational friction. 

- **Primary Volume Peak (~1250–1300 Days):** The structural centre of gravity representing standard transit workflows across primary industrial lanes. 

- **Acute Latency Outliers (~1600–1650 Days):** Long-tail delays driven by severe systemic interruptions, customs holds, or port backlogs. 

**Key Takeaway:** The broad data gaps between clusters indicate that extreme transit delays are not caused by marginal day-to-day variances. Instead, shipments undergo distinct, categorical delays (adding 350 to 700 days of fixed latency). 

### **5.2 Spatial Bottlenecks & Regional Disparities** 



Figure 2: Route Efficiency Score (Er) – Top 10 vs. Bottom 10 Destination States. 

Aggregating performance by destination state via the normalized **Route Efficiency Score (** _Er_ **)** uncovers substantial geographic performance gaps ( **Figure 2** ): 

- **High-Efficiency Corridors (** _Er ≥_ 73.9 **):** Destination regions located adjacent to central manufacturing and logistics hubs (e.g., Maine, Newfoundland and Labrador) consistently maintain high efficiency scores and low average lead times. 

- **Bottleneck Destinations (** _Er_ <39.7 **):** Outlying states and remote territories (e.g., Vermont, New Mexico, Saskatchewan, West Virginia and North Dakota) exhibit significant fulfillment friction, with average lead times dragging efficiency scores down near zero. 

|Region Category|Avg Efficiency<br>Score (Er)|Operational Profile|Primary Driver|
|---|---|---|---|
|Top 10 States|73.9 – 100.0|High Speed, Low Var.|Proximity to Origin|
|Middle Tier|40.0 – 73.8|Baseline Delivery|Standard Surface Lanes|
|Bottom 10 Bottlenecks|0.0–39.7|ChronicDelayRisk|Intermodal Transfer|



The breakdown of regional performance tiers demonstrates that fulfillment efficiency is governed by structural logistics mechanics. While high-scoring states benefit from direct proximity to dispatch hubs, the acute friction in bottom-tier bottleneck states ( _Er_ <40.0) is primarily driven by intermodal transfer delays—where cargo handoffs across rail-to-truck junctions and regional sorting facilities create severe operational lag. 

**Key Takeaway:** Transit latency is heavily concentrated in specific destination zones rather than origin dispatch operations, pointing to localized intermodal transfer bottlenecks and regional carrier capacity limits. 

**Note:** The raw dataset includes both US states and Canadian provinces (e.g., Newfoundland & Labrador, Ontario, Manitoba, Saskatchewan). 

### **5.3 Shipping Mode Speed vs. Reliability Trade-Offs** 



Figure 3: Lead-Time Dispersion (σ) and Median Durations Across Fulfillment Channels. 

A cross-channel evaluation ( **Figure 3** ) demonstrates the operational trade-off between baseline delivery speed and channel stability across fulfillment modes: 

- **Median Durations:** All four shipping channels (First Class, Same Day, Second Class, and Standard Class) exhibit an identical median lead time of approximately **1,270 days** (indicated by the red line). 

- **Dispersion & Outliers:** Each channel shares identical lower bounds (~900 days), upper quartiles (~1,630 days), and maximum whiskers (~1,640 days). 

**Key Takeaway:** Premium shipping modes provide **zero operational speed or reliability advantage** over standard surface modes. The network suffers from structural carrier neutralisation, where expedited freight is processed through the exact same congested transit pipelines as standard freight. 

### **5.4 Synthesis of Analytical Insights** 

1. **Network Skewness:** Mean lead times are heavily inflated by tail anomalies (1600 + days) rather than general operational slowness. 

2. **Geographic Heterogeneity:** Shipping performance cannot be evaluated as a single national metric; regional destination performance varies by up to 100.0 efficiency points. 

3. **Variance Over Mean:** Inconsistent delivery windows ( _σ_ ) in standard transit channels present a higher operational risk to customer SLAs than absolute transit duration. 

## **6. Correlation Analysis** 

To evaluate structural dependencies within the distribution network, Pearson correlation coefficients ( _r_ ) were calculated across primary transactional metrics: 

Correlation Matrix 

|Metric|Lead<br>Time<br>(Days)|Shipment<br>Volume|Efficiency<br>Score|
|---|---|---|---|
|Lead Time<br>(Days)|1.00|+0.12|-0.96|
|Shipment<br>Volume|+0.12|1.00|-0.10|
|Route<br>Efficiency<br>(Er)|-0.96|-0.10|1.00|



- **Lead Time vs. Efficiency Score (** _r_ =-0.96 **):** Strong inverse linear correlation, validating _Er_ as a standardized metric for network friction. 

- **Shipment Volume vs. Lead Time (** _r_ =+0.12 **):** Weak positive 

correlation, confirming that volume surges alone do not drive fulfillment delays. Network latency is governed by regional infrastructure constraints rather than order density. 

- **Ship Mode Tier vs. Lead Time (** _r ≈_ 0.00 **):** Negligible correlation, statistically proving the modal invariance observed in Figure 3. 

## **7. Recommendations** 

Based on the empirical findings, strategic interventions must address destination friction and carrier contract structures: 

1. **Restructure Carrier Contracts & Audit Premium Tiers:** Re-evaluate service level agreements (SLAs) for expedited shipping modes. Because Same Day and First-Class modes deliver identical lead-time distributions to Standard Class (Figure 3), premium shipping surcharges should be suspended until carriers guarantee distinct speed tiers. 

2. **Regional Safety Stock Allocation:** Deploy buffer inventory in distribution hubs servicing the bottom 10 bottleneck states ( _Er ≤_ 39.7, including West Virginia, North Dakota, and Saskatchewan) to absorb chronic long-tail delivery delays (1600+ days). 

3. **Variance-Based SLA Enforcement:** Shift carrier performance monitoring from mean delivery times to standard deviation ( _σ_ ) and long-tail cluster boundaries, penalizing carriers when shipments cross into the 1600day delay tier. 

## **8. Future Scope** 

- **Predictive ETA Modelling:** Train supervised machine learning models (e.g., XGBoost, Random Forest) to predict long-tail delay probability at order entry based on destination state and temporal features. 

- **Intermodal Telemetry Integration:** Incorporate GPS and container tracking data across intermodal transit hubs to pinpoint exact geographic handoff points responsible for the 350-to-700-day latency spikes. 

- **Dynamic Re-Routing Algorithms:** Develop prescriptive inventory management systems that dynamically re-route orders from 

secondary plants when primary destination lanes cross critical latency thresholds. 

## **9. Conclusion** 

This research demonstrates that national freight transit latency is driven by spatial bottlenecks and structural system friction rather than order volume surges. The empirical analysis reveals a tri-modal leadtime distribution, a 100-point efficiency disparity across destination states, and complete modal parity across fulfillment channels. By targeting regional distribution bottlenecks and aligning carrier contracts with true transit reliability, logistics operators can reduce network variance, improve SLA compliance, and build supply chain resilience. 

