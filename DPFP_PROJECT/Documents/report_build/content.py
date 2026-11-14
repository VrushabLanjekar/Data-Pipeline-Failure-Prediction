# -*- coding: utf-8 -*-
"""Report text for DPFP_Project_Report.docx.
Block types: ("h1", title) chapter, ("h2", t), ("h3", t), ("p", text), ("pi", text) indented note,
("num", [items]) numbered list, ("table", caption, header, rows, widths), ("fig", path, caption, width_in),
("pagebreak",). Citations are written {key} and numbered in order of first appearance (IEEE)."""

FIG = "Documents/report_figures/"
OUT = "outputs/"

TITLE = ("Data-Pipeline Failure Prediction: Leakage-Free Next-Day Forecasting of "
         "Failures from Data-Quality Signals")

ABSTRACT = [
    "Data pipelines move data from a source into the tables, reports and models that depend on it. When a run "
    "delivers broken data, the damage often shows up only later, downstream. Most monitoring tools raise an alert "
    "after a check has already failed. This project asks whether the failure of the next pipeline run can be "
    "forecast one day ahead from the pipeline's own data-quality signals, and which kinds of failure can be "
    "forecast at all.",
    "The study uses a real ingestion pipeline that collects hourly air-quality data for Pune and Delhi from the "
    "Open-Meteo API, which serves CAMS model data. The pipeline ran once per day from 5 August 2022, giving 1,557 "
    "daily runs per city up to 8 November 2026. A run counts as a failure only when the data or the API is broken. "
    "Genuinely high pollution is logged as a warning and used as an input signal. From each run the pipeline "
    "records 22 signals covering data quality, infrastructure, failure history and season, including a drift "
    "score based on the Population Stability Index (PSI). Models are trained on a strict chronological split, so "
    "every prediction uses only information available on the day it is made.",
    "On the Delhi test window, a Random Forest reached a PR-AUC of 0.229 against a random baseline of 0.111, "
    "about 2.1 times better than chance. At the alarm threshold chosen on validation data it caught 25 of 43 "
    "failures one day ahead (recall 0.58), with about 6.0 false alarms per month. A model using only data signals "
    "scored 0.217, against 0.116 for infrastructure signals alone. A deliberately leaky model that reads the same "
    "run's columns scored a perfect 1.000, which shows how easily same-run features inflate results. The "
    "per-failure-type map found data-quality failures in Delhi predictable (lift 2.27, with the lower end of its "
    "confidence interval at 1.62). Pune's 8 data-quality failures were not reliably predictable, and API "
    "service-level breaches were too rare to test. The model runs every day through GitHub Actions, retrains "
    "weekly, logs each forecast as it is made, and feeds a public dashboard called Pipeline Radar. The results "
    "are modest but measured honestly, and they show that per-type predictability is a useful way to report "
    "failure forecasting.",
]

KEYWORDS = ("Data-pipeline failure prediction, Data quality, Data observability, Data drift, Population Stability "
            "Index, Random Forest, Class imbalance, Probability calibration, Data leakage, Lead time, SHAP, "
            "Time-series cross-validation, Open-Meteo, Air quality")

DECLARATION_AI = ("An AI writing assistant (Claude, by Anthropic) was used to help draft and edit the text of this "
                  "report. All results, tables and figures come from the project's own code and output files, and "
                  "I have checked them. [Edit this statement to match the university's policy on AI use.]")

CH = []
a = CH.append

# ---------------------------------------------------------------- Chapter 1
a(("h1", "Introduction"))
a(("h2", "1.1 Background"))
a(("p", "Organisations depend on data pipelines to collect data from a source, check it, reshape it and load it into "
        "the tables that reports, dashboards and machine-learning models read. A pipeline can fail loudly, for "
        "example when an API call times out. It can also fail quietly by delivering values that look normal to a "
        "scheduler but are wrong: negative concentrations, readings that do not change for hours, sudden "
        "impossible jumps, or a day with missing hours. Quiet failures are the harder kind, because nobody notices "
        "them until a downstream report or model has already used the bad data."))
a(("p", "Data observability tools address this by checking freshness, volume, schema and value distributions on "
        "every run {P25}{P31}. These checks are useful, but they report a problem after it has happened. The "
        "operator learns that today's load is broken once it is already broken. A forecast that warns a day in "
        "advance would let the team check the source, hold dependent jobs, or add a manual review before the bad "
        "data spreads."))
a(("p", "This report uses the term data pipeline in the sense of an ETL or ingestion pipeline that moves data. It is "
        "a different object from a CI/CD build pipeline, which compiles and tests software. Published work on "
        "\"CI/CD pipeline failure prediction\" studies software build and delivery pipelines "
        "{P3}. The present study forecasts failures of a data-ingestion pipeline from the quality of the "
        "data it handles, so results from the CI/CD literature do not transfer directly."))
a(("h2", "1.2 Why pipeline failures matter"))
a(("p", "A failed run has a cost beyond the run itself. Missing or wrong data can break a dashboard, bias a model "
        "that retrains on it, or trigger a chain of reruns. The reviewed literature reports the same pattern from "
        "several angles. Studies of cloud jobs show that failed tasks waste compute that could have been saved by "
        "acting early {P6}{P40}. Work on data contracts reports fewer downstream failures when violations are "
        "predicted before they occur {P36}. Reliability frameworks for data systems note that silent correctness "
        "failures need data-specific instrumentation that standard site-reliability tooling does not provide {P11}."))
a(("p", "For an operator, the useful question is practical: how likely is tomorrow's run to fail, why, and how many "
        "false alarms will a warning system raise each month? This project tries to answer that question with "
        "measured numbers."))
a(("h2", "1.3 Problem statement"))
a(("p", "Most published failure-prediction work forecasts infrastructure events such as node, job or hardware "
        "failures, using CPU, memory, scheduling or log features {P2}{P9}{P43}. Most data-quality work detects "
        "problems in the current batch {P13}{P14}{P44}. In the 47 papers reviewed for this project, we did not find "
        "a study that forecasts the failure of the next run of a data-ingestion pipeline from its own data-quality "
        "signals, evaluates the forecast without leakage, and reports which failure types can be forecast and how "
        "early. To our knowledge this combination is seldom reported, and it is the gap this project addresses."))
a(("p", "The research question is: which data-pipeline failures can be forecast one day ahead from the pipeline's "
        "own data-quality telemetry, how early, and how much do same-run leakage and infrastructure-only signals "
        "mislead the evaluation?"))
a(("h2", "1.4 Scope"))
a(("p", "The study is built on one real, public ingestion pipeline. Each day it requests 24 hourly records of six "
        "pollutants (PM2.5, PM10, NO2, SO2, CO and ozone) for two Indian cities, Pune and Delhi, from the Open-Meteo "
        "air-quality API. The API serves model data from the Copernicus Atmosphere Monitoring Service "
        "(CAMS). The pipeline validates each day's data, labels the run as a success, a warning or a failure, and "
        "logs a set of quality and infrastructure signals. The data covers 5 August 2022 to 8 November 2026 for "
        "the main analysis."))
a(("p", "The prediction target is a data-quality failure on the next day's run. Delhi, with 130 data-quality "
        "failures, is the main city. Pune, with 8, is used as a second source for a cross-city check. The models "
        "are standard tree ensembles and a logistic regression. The contribution of the project lies in the "
        "signals, the leakage-free evaluation and the per-failure-type analysis. "
        "The project also includes a working daily system: a scheduled job that collects data, retrains weekly, "
        "stores every forecast as it is made and publishes a dashboard (see Annexure A)."))
a(("p", "Out of scope are automatic repair of failures, other data sources and APIs, and pipelines that run more "
        "than once a day."))
a(("h2", "1.5 Structure of the report"))
a(("p", "Chapter 2 reviews the 47 papers and states the research gap. Chapter 3 lists the eight objectives. "
        "Chapter 4 describes the data, tools, failure taxonomy and the 22 signals. Chapter 5 presents the analysis "
        "and results, from the leakage demonstration to the deployed system. Chapter 6 summarises and discusses the "
        "results, and Chapter 7 sets out the limitations and future work. References and annexures follow."))

# ---------------------------------------------------------------- Chapter 2
# -*- coding: utf-8 -*-
# Chapter 2 in the style of the sample report: one paragraph per paper, bold-italic author and year, then [n].
# n = SR.No in Research_Findings_47_Papers.xlsx. Every statement comes from that sheet.
a(("h1", "Literature Review"))
a(("p", "A brief review of the 47 papers on failure prediction, data-quality monitoring and pipeline observability that "
        "were collected for this project is given in this chapter. Each paper is summarised from the project's "
        "research-findings sheet, which records its objective, method, findings and gap. For some papers only "
        "metadata was available, and the summaries for those papers say so."))

_P = [
 ("Hoo Meng Wong et.al.(2026)", "has proposed an end-to-end adaptive pipeline that links data-drift detection with "
  "data-quality validation to decide when a machine-learning model should be retrained. The work addresses "
  "drift-triggered retraining. It does not aim to forecast pipeline failures in general or to measure operational "
  "lead time. The full text was not available for this review", 1),
 ("Panna Das et.al.(2026)", "has studied early prediction of task failure in cloud computing on the Google Borg 2019 "
  "trace, where the probability of failure is estimated right after a resource request. Logistic regression, Random "
  "Forest, XGBoost and a feedforward neural network were compared, together with feature analytics and clustering. "
  "Random Forest performed best, with 85.06% accuracy and 86% failure recall. The study concluded that early "
  "prediction is feasible and can cut wasted resources. Its features describe scheduling and resource requests, and "
  "data-centric signals are not used", 2),
 ("Mokshda N. Kachave et.al.(2026)", "has applied an XGBoost-based classifier to predict failures of CI/CD pipeline "
  "executions. The paper concerns software build and delivery pipelines and not data pipelines. The full text was "
  "not available for this review", 3),
 ("Rahul Chawla et.al.(2026)", "has presented a multi-agent framework for autonomous data-engineering pipelines that "
  "combines predictive modelling, large language models and reinforcement learning. The sheet notes that these "
  "components need stronger validation on realistic failures and on pipelines not seen before", 4),
 ("Ankush Sharma et.al.(2026)", "has proposed a Random-Forest-gated temporal risk model over multivariate telemetry "
  "for cloud infrastructure. It was compared with logistic regression, a decision tree, Random Forest, SVM, gradient "
  "boosting and LSTM models. The gated model performed best on simulated data (ROC-AUC 0.987, F1 about 0.871) and "
  "separates risk prediction from alerting. The results come from simulation only, and data correctness, schema and "
  "freshness are not covered", 5),
 ("Ling He et.al.(2026)", "has studied early job failures in cloud data centres using XGBoost on the Google cluster "
  "trace. Fourteen features were selected with Random Forest importance and Spearman correlation, and an "
  "interpretable rule-based representation learning model was added. The study reports a weighted AUC of 0.9993 and "
  "an F1 of 0.9936. Active cloning of jobs gave a 26% median speed-up for failed jobs at negligible overhead. The "
  "work targets cloud jobs and not data quality or pipeline correctness", 6),
 ("Sridevi A et.al.(2026)", "has applied meta-research analytics and machine-learning classifiers to predict the "
  "failure of research projects. The study shows that project-level failure prediction is feasible in research "
  "management. It predicts project risk and not pipeline execution failures, so it gives little evidence for "
  "observability signals", 7),
 ("Jay Mehta(2026)", "has proposed machine learning for predictive data-quality engineering in distributed data "
  "platforms. The sheet notes that the work needs stronger root-cause localisation, testing across pipelines and "
  "evidence that the predictions reduce operational incidents. Only metadata was available for this review", 8),
 ("Somit Jaiswal et.al.(2026)", "has presented a multi-model ensemble approach to node-failure prediction for cloud "
  "systems reliability. The approach predicts infrastructure failures well, but it leaves out data quality, schema, "
  "lineage and the impact on data products. Only metadata was available for this review", 9),
 ("Eftim Zdravevski et.al.(2026)", "has built a real-time failure-forecasting system for Industry 4.0 using XGBoost on "
  "the Bosch production-line data. Nominal features were encoded with weight of evidence, processing ran on Apache "
  "Spark, and the TabNet deep tabular model was used as a baseline. XGBoost reached an AUC-ROC of 0.966, an MCC of "
  "0.793 and an F1 of 0.929. The study concluded that scalable forecasting is feasible on one benchmark. It deals "
  "with manufacturing and not with data-pipeline failures", 10),
 ("Santoshi Maddali(2026)", "has described a conceptual framework for reliability engineering of data and AI "
  "systems. It combines a site-reliability failure taxonomy, a catalogue of data and model service-level "
  "indicators, data contracts, automated validation, drift monitoring and staged rollout. The paper concluded that "
  "silent correctness failures need data- and model-specific instrumentation. It offers no predictive model or "
  "quantitative validation", 11),
 ("A. Mishra(2026)", "has presented a reliability-first architecture for large-scale batch data pipelines, built on "
  "idempotency with coordination stores, transactional commit protocols, date-scoped dependency graphs and "
  "checkpoint-based recovery. These patterns make failures less severe and reprocessing deterministic. The paper "
  "does not provide a validated predictive model or an evaluation of warning time", 12),
 ("I. Kyrychenko et.al.(2026)", "has researched automated data-quality testing and anomaly-detection methods for "
  "pipeline telemetry. The work detects data-quality and telemetry anomalies but does not fully forecast failures "
  "with several causes or validate useful warning time. Only metadata was available for this review", 13),
 ("Zinkal Thakker et.al.(2026)", "has proposed self-supervised anomaly-detection models for continuous data-quality "
  "monitoring in enterprise platforms, which improve detection when labels are not available. The models do not "
  "connect the anomalies to future pipeline failure, cause, lead time or remediation. Only metadata was available "
  "for this review", 14),
 ("Dillepkumar Pentyala(2025)", "has described a multi-layer AI observability architecture for DataOps that uses "
  "generative AI and machine learning for telemetry analysis, lineage tracing and anomaly detection. The paper "
  "reports that mean time to detect fell to minutes with fewer false positives, and it points towards self-healing "
  "pipelines and autonomous governance. The sheet notes that the vision needs benchmark datasets, time-based "
  "evaluation, calibrated probabilities and independent validation", 15),
 ("Pradeep Kumar Nangunoori(2025)", "has built a machine-learning framework for predictive diagnostics in cloud "
  "database replication systems. A Random Forest, a gradient-boosting model and an LSTM were combined on Oracle "
  "GoldenGate and MySQL metrics and logs and deployed as a microservice. The framework reached 92.4% accuracy and a "
  "37% reduction in downtime, but recall stayed low for rare events such as network partitions and schema "
  "conflicts. The work is specific to database replication", 16),
 ("M. K. et.al.(2025)", "has combined an LSTM, LightGBM, statistical tests and ARIMA for concept-drift detection and "
  "proactive model updating, using heterogeneous and simulated data. Prediction error was up to 40% lower than with "
  "static models. The study focuses on drift detection and model updating and not on forecasting failures with "
  "several causes", 17),
 ("Santosh Kumar Sana(2025)", "has developed a multi-layer anomaly-detection system for cloud data pipelines that "
  "combines statistical profiling, deep learning (transformers, variational autoencoders and graph networks), "
  "semantic detection and adaptive thresholds. It reports 94.3% anomaly accuracy with a 5.2% false-positive rate. "
  "The sheet notes that the paper relies heavily on secondary literature and has limited experiments of its own, "
  "and it does not show failure forecasting or generalisation across pipelines", 18),
 ("M. Thanjaivadivel et.al.(2025)", "has proposed dynamic observability for automated machine-learning pipelines in "
  "predictive maintenance for industrial IoT. The observability is limited to industrial ML pipelines and does not "
  "establish general data-pipeline failure prediction. Only metadata was available for this review", 19),
 ("Preetam Kumar Ojha(2025)", "has proposed hierarchical robust PCA for data-quality monitoring in multi-level "
  "aggregation pipelines. Each level is split into a low-rank and a sparse part with truncated SVD, and anomalies "
  "are detected without labels. On synthetic hierarchical data the method beat rule-based checks and allowed "
  "root-cause localisation. It detects anomalies in aggregated data and does not model operational failure or "
  "lead time", 20),
 ("Rambabu Tangirala(2025)", "has proposed a failure-prevention framework for ETL pipelines that uses AI agents, "
  "retrieval-augmented generation and a vector database for anomaly detection, root-cause analysis and "
  "remediation. It reports 94.7% prediction accuracy, 68% less downtime and 82.4% automatic remediation success, "
  "with 5.3% false negatives remaining. The sheet notes that predictive performance, false-alert burden and safe "
  "deployment are not sufficiently established", 21),
 ("Vineeth Kumar Reddy Mittamidi(2025)", "has designed lightweight predictive models over fused telemetry, integrity "
  "and change signals for change-data-capture pipelines, with graph-based diagnosis over the pipeline topology and "
  "risk-tiered automation. The paper is a prototype design with an evaluation plan that has not yet been "
  "implemented, and it stresses that automation needs policy gating", 22),
 ("B. Vijaya Kumar et.al.(2025)", "has proposed real-time drift detection with deep learning for anomaly-detection "
  "services on multivariate time series inside MLOps pipelines. It detects drift in the services but does not "
  "predict general pipeline failures or quantify how useful the alerts are. Only metadata was available for this "
  "review", 23),
 ("Srinivasa Rao Seetala(2025)", "has reviewed self-healing data pipelines built on predictive monitoring, covering "
  "machine-learning anomaly detection, automated root-cause analysis and remediation within AIOps and DataOps. "
  "Model drift and integration complexity remain open problems. The sheet notes that reproducible real-world "
  "experiments, calibrated risk and lead-time measurement are still needed", 24),
 ("Suman Reddy Gaddam(2024)", "has described a data-observability and self-healing architecture for regulated "
  "enterprises, built on five pillars (freshness, volume, schema, distribution and lineage), anomaly detection on "
  "telemetry, confidence-based escalation and recovery by retries and rollback. The paper describes a shift from "
  "reactive monitoring to proactive reliability. It lacks reproducible model comparisons, warning-time results and "
  "false-alert analysis", 25),
 ("Vineeth Kumar Reddy Mittamidi(2024)", "has proposed a conceptual five-layer architecture for self-healing "
  "pipelines: telemetry and lineage, features and knowledge, detection, causal diagnostic reasoning and "
  "policy-governed remediation. Its central principle is constrained autonomy. The main gap is empirical "
  "validation of precision, calibration, lead time and safe autonomous actions", 26),
 ("S. S et.al.(2024)", "has applied machine learning to workload and infrastructure features of Amazon cloud "
  "systems to predict cloud workloads. The work does not use real pipeline telemetry, data quality, lineage or "
  "causal explanations. Only metadata was available for this review", 27),
 ("Fahd Azouz et.al.(2024)", "has predicted machine failure in data centres using time-series analysis and LSTM "
  "networks. The target is hardware failure, and the paper does not cover data-pipeline semantics, quality or "
  "dependencies. Only metadata was available for this review", 28),
 ("Roopesh Kumar Reddy Ramalinga Reddy(2024)", "has applied LSTM and Transformer sequence models to IoT telemetry "
  "together with observability-first site-reliability practice (service-level indicators, objectives and error "
  "budgets) and event-driven self-healing. A smart-meter case study showed a failure lead time of about 30 minutes "
  "and a lower time to repair, and the sheet notes that broader validation is needed. The paper does not cover "
  "data correctness, schema or lineage", 29),
 ("Sebastian Strasser(2024)", "has proposed model-aware data validation, in which data assertions are built from "
  "training data and weighted by their influence on a downstream model. The work is at an early stage and the "
  "metadata-collection component is not yet implemented. It supports validation but does not predict pipeline "
  "failure or measure warning lead time", 30),
 ("Naveen Edapurath Vijayan(2023)", "has reviewed automated data-quality monitoring in machine-learning pipelines, "
  "combining statistical analysis, machine-learning anomaly detection, rule-based systems and data profiling "
  "across the MLOps stages. Balancing precision and recall to avoid alert fatigue is named as the open challenge. "
  "The paper monitors current data problems and does not forecast future failures", 31),
 ("Adrian-Ioan Tuns et.al.(2023)", "has predicted cloud service failures on Google Borg cluster traces with "
  "traditional machine-learning classifiers. The work addresses task and job failure and not data correctness, "
  "quality degradation or pipeline impact. Only metadata was available for this review", 32),
 ("D. Wani et.al.(2023)", "has proposed drift monitoring for log anomaly-detection pipelines using Bayes factors "
  "with windowing over log-template count vectors, in order to tell drift apart from anomalies. It was validated "
  "on real and simulated log data from a single pipeline. It maintains log-anomaly models under drift and does not "
  "forecast pipeline failure", 33),
 ("Srujana Parepalli(2023)", "has used classical machine-learning models (regression, tree-based estimators and "
  "support-vector methods) with feature engineering on operational logs to predict ETL throughput and resource "
  "use. The forecasts were operationally useful and interpretable, and they improve on reactive static tuning. The "
  "target is throughput and resource use and not failure or data correctness", 34),
 ("Preethi Samantha Bennet et.al.(2023)", "has presented an intelligent machine-failure prediction system for "
  "predictive maintenance, built on a maintenance dataset. The dataset is not from pipeline operations, and "
  "real-time or cross-system generalisation is not established. Only metadata was available for this review", 35),
 ("Koteswara Rao Chirumamilla(2023)", "has predicted data-contract failures using a hybrid model of gradient-boosted "
  "decision trees, temporal drift modules and embedding-based schema representations over historical and real-time "
  "metadata. In finance, e-commerce and healthcare data it reached 79% accuracy, 42% fewer downstream failures and "
  "37% faster triage, with lead times from hours to a day. The model covers contract violations but not resource, "
  "log, freshness, deployment, runtime or semantic failure causes", 36),
 ("Venkata Gummadi(2023)", "has described a log-based framework for enterprise failure forecasting that uses "
  "feature engineering, ensemble learning and model versioning, and validated it in a case study. The framework "
  "improves operational efficiency through forecasting, resource allocation and real-time decisions. The sheet "
  "notes that reproducible evidence on data-quality integration, calibration, lead time and cross-pipeline "
  "deployment is lacking", 37),
 ("Anwesha Das et.al.(2023)", "has proposed Prolego, a method for predicting failures in complex systems from time "
  "series. It uses deep-learning auto-labelling from sparse ground truth, ranks signals by coefficient of "
  "variation and retrains the predictive model frequently. On three real-world systems it reached 86.2% accuracy, "
  "more than 15% improvement over baselines and lead times of up to 8 hours. The method does not combine "
  "data-quality, schema, lineage or remediation signals", 38),
 ("Ghatoth Mishra(2023)", "has described real-time data-quality monitoring and gating in cloud-based data pipelines "
  "through streaming micro quality gates (\"gatelets\") with threshold and severity rules and fast-track or "
  "stop-and-check strategies. The design is rule-driven and cloud-native and is based on service-level "
  "objectives. It uses gating to manage quality issues but does not predict failure risk from several sources "
  "before a gate is breached", 39),
 ("Jie Li et.al.(2023)", "has built two machine-learning models for workload failure prediction in data centres, a "
  "queue-time model used before execution and a runtime model, trained on production cluster traces and integrated "
  "with the job scheduler. Precision was 90.61% for the queue-time model and 97.75% for the runtime model, and "
  "scheduler integration cut CPU time by about 16.7% and memory by about 14.53%. The evidence is strong at "
  "workload level, but it includes no data-quality, schema or pipeline-specific causes", 40),
 ("Srinivasa Rao Seetala(2022)", "has reviewed adaptive machine-learning frameworks for data-quality monitoring, "
  "using Local Outlier Factor, Isolation Forest and concept-drift detection inside continuous ML pipelines. The "
  "paper reports that machine learning moves quality monitoring from reactive to proactive and embeds validation in "
  "production MLOps workflows. Adaptive quality monitoring is not the same as forecasting execution failure", 41),
 ("Rohit Reddy Gaddam(2022)", "has presented hybrid drift detection at scale on Kafka and Spark, combining "
  "statistical tests, embedding-based similarity, ensemble anomaly scoring and adaptive thresholds, with "
  "interpretable drift attribution. The hybrid beat single methods, gave fewer false alarms and scaled to millions "
  "of predictions. The paper does not show whether drift predicts pipeline failure or quantify the operational "
  "benefit", 42),
 ("Mohammad S. Jassas et.al.(2022)", "has analysed job failures in cloud computing and built prediction models on "
  "three public traces (Google cluster, Mustang and Trinity). Random Forest worked best, with high precision, "
  "recall and F1, and the study found a strong correlation between unsuccessful tasks and the resources requested. "
  "It uses public cloud traces and does not model data correctness, schema, quality or observability "
  "integration", 43),
 ("Nagender Yamsani(2022)", "has surveyed machine learning for automated data-quality and anomaly detection in "
  "enterprise data pipelines, covering probabilistic modelling, deep learning and the model-guided cleaning "
  "systems HoloClean and ActiveClean. The survey concluded that machine-learning-driven data quality is viable at "
  "scale, that selective model-guided cleaning beats exhaustive cleaning and that humans are still needed in the "
  "loop. The paper finds and diagnoses data defects but does not forecast integrated pipeline failure with "
  "operational warning time", 44),
 ("Hardik Patel(2022)", "has proposed a resilient data-engineering architecture on enterprise cloud distributed "
  "systems, with adaptive orchestration, fault-tolerant dataflow scheduling, self-healing microservices, "
  "multi-region replication and a learning-enabled reliability manager. Synthetic metrics show 98% availability, "
  "12-second recovery and a resilience health index of 0.94. The sheet notes that the paper lacks a reproducible "
  "predictive benchmark and a calibrated failure-risk evaluation", 45),
 ("R. Rossini et.al.(2022)", "has built a feature-extraction and failure-detection pipeline for log and production "
  "data, with a two-step feature engineering process, binary classification (Random Forest and k-nearest "
  "neighbour) and a time-to-repair severity model, on real data from a drilling machine in woodworking. It "
  "predicts both whether a failure occurs and how severe it is. The method is machine-specific and lacks "
  "data-pipeline, lineage, schema and cross-platform validation", 46),
 ("N. Mangala(2022)", "has described real-time data-quality monitoring and gating in cloud-based data pipelines with "
  "the same gatelet framework as {P39}. The sheet flags it as a likely duplicate or variant of that paper by a "
  "different author. Quality gating can block bad data but does not predict a future technical failure or "
  "estimate actionable lead time", 47),
]
for _who, _txt, _n in _P:
    a(("pbi", _who, _txt, _n))

a(("h2", "2.1 Summary of the reviewed literature"))
a(("p", "The 47 papers fall into six themes (Table 2.1). Infrastructure and job failure prediction is the most "
        "mature group, followed by data-quality monitoring and by architectures for self-healing and observable "
        "pipelines."))
a(("table", "Table 2.1: Themes in the 47 reviewed papers",
   ["Theme", "Papers", "Count"],
   [["Infrastructure, job and node failure prediction", "[P2], [P5], [P6], [P9], [P16], [P27], [P32], [P38], [P40], [P43]", "10"],
    ["CI/CD build-failure prediction", "[P3]", "1"],
    ["Data-quality monitoring and anomaly detection", "[P8], [P13], [P14], [P18], [P20], [P30], [P31], [P34], [P36], [P39], [P41], [P44], [P47]", "13"],
    ["Drift detection and drift-triggered retraining", "[P1], [P17], [P23], [P33], [P42]", "5"],
    ["Self-healing pipelines, observability and reliability architecture", "[P4], [P11], [P12], [P15], [P19], [P21], [P22], [P24], [P25], [P26], [P37], [P45]", "12"],
    ["Failure prediction in other domains", "[P7], [P10], [P28], [P29], [P35], [P46]", "6"]],
   [3.0, 3.4, 0.7]))
a(("h2", "2.2 Research gap"))
a(("p", "Reading the papers together shows a consistent pattern. Studies that forecast failures use infrastructure, "
        "scheduling or hardware signals {P2}{P5}{P6}{P9}{P40}{P43}, and the sheet records for almost all of them that data "
        "quality, schema and lineage are not covered. Studies that use data-quality signals mostly detect problems in "
        "the current batch {P13}{P14}{P18}{P20}{P44}, and studies on drift treat it as something to detect and use as a "
        "trigger for retraining {P1}{P17}{P23}{P33}{P42}. The architecture papers describe predictive and self-healing "
        "pipelines {P21}{P22}{P24}{P25}{P26}, but the sheet repeatedly notes that they lack reproducible experiments, "
        "calibrated risk, measured lead time and false-alarm analysis."))
a(("p", "Lead time is reported by only a few of the papers: about 30 minutes for IoT telemetry {P29}, hours to a day "
        "for data-contract failures {P36} and up to 8 hours for time-series failure prediction {P38}. The papers that "
        "report accuracy above 90% {P6}{P16}{P21} do so on different tasks, and several rely on simulated or synthetic "
        "data {P5}{P17}{P20}{P45}."))
a(("p", "To our knowledge, none of the 47 papers does all of the following for a data-ingestion pipeline: (1) "
        "forecasts the next run's failure from the pipeline's own data-quality signals, (2) evaluates the forecast on "
        "a strict chronological split and shows what leakage does, (3) compares data signals with infrastructure "
        "signals under the same model, (4) reports a measured lead time and false-alarm rate, and (5) reports which "
        "failure types are predictable and which are not. Each element on its own is standard. The contribution of "
        "this project is the combination, applied to a real pipeline and run as a working daily system."))

# ---------------------------------------------------------------- Chapter 3
a(("h1", "Objectives of the Study"))
a(("p", "The eight objectives turn the research gap into steps that can be checked. Objectives 4 and 6 carry the "
        "two headline contributions. Table 3.1 links each objective to the section where it is answered."))
a(("num", [
    "Build a pipeline that logs data-centric leading indicators on every run: drift (PSI), freshness, completeness, "
    "API-latency trend, value stability, the count of values above a hazard threshold, and warning history.",
    "Predict the next run's failure without leakage, using only information available up to the current run.",
    "Test whether data signals predict better than infrastructure signals through a controlled comparison of "
    "infrastructure-only, data-only and combined models on PR-AUC.",
    "Map predictability per failure type: report the score and lift for each failure type and state which types "
    "are predictable and which are not, with reasons (headline).",
    "Quantify the early-warning lead time: report how far ahead failures are flagged and how skill changes as the "
    "warning horizon grows.",
    "Demonstrate the leakage gap: show the inflated same-run model beside the honest next-day model (headline).",
    "Validate across data sources: train on one city's pipeline and test on the other, under a shared schema "
    "(supporting evidence).",
    "Deliver explainable, date-based predictions: for a given date, return a risk score, the likely failure type, "
    "the lead time and the signals that drive the warning.",
]))
a(("table", "Table 3.1: Objectives, contributions and where they are answered",
   ["Objective", "Contribution", "Answered in"],
   [["1. Data-centric signals", "Data signals as predictors", "Sections 4.3, 4.4"],
    ["2. Leakage-free next-run forecast", "Forecasting instead of detection", "Sections 4.5, 5.1"],
    ["3. Data vs infrastructure signals", "Data signals as predictors", "Section 5.4"],
    ["4. Per-failure-type map (headline)", "Per-type predictability", "Section 5.7"],
    ["5. Lead time", "Measured lead time", "Section 5.6"],
    ["6. Leakage gap (headline)", "Leakage demonstration", "Section 5.1"],
    ["7. Cross-city validation", "Supporting check", "Section 5.8"],
    ["8. Explainable date-based prediction", "Usable output", "Sections 5.9, 5.10"]],
   [2.6, 2.4, 2.0]))

# ---------------------------------------------------------------- Chapter 4
a(("h1", "Methodology"))
a(("h2", "4.1 Data description"))
a(("p", "The data comes from the project's own ingestion pipeline. For each city and each day, the pipeline calls "
        "the Open-Meteo air-quality API and requests 24 hourly values of PM2.5, PM10, NO2, SO2, CO and "
        "ozone. The API uses the CAMS global model (domain cams_global). The values are therefore model output, "
        "produced by an atmospheric model, and they do not come from ground sensors. The two locations are Pune "
        "(18.5204 N, 73.8567 E) and Delhi (28.6139 N, 77.2090 E)."))
a(("p", "One row of the run log is one daily run. Each row records when the run started and ended, the API status "
        "and latency, the number of rows received, coverage and missing-value rates, gaps, duplicates, invalid "
        "values, the validation result, the failure type, any warning and the engineered signals. The pipeline was "
        "first run as a historical backfill from 5 August 2022 and then kept current by the daily job. The "
        "analysis uses runs up to 8 November 2026. Table 4.1 gives the audit of both logs."))
a(("table", "Table 4.1: Data audit of the two run logs (outputs/01_data_audit.csv)",
   ["City", "Runs", "From", "To", "Missing days", "Failures", "Failure %", "Data-quality", "API SLA", "Hazard-warning days"],
   [["Delhi", "1,557", "2022-08-05", "2026-11-08", "0", "133", "8.54", "130", "3", "1,252"],
    ["Pune", "1,557", "2022-08-05", "2026-11-08", "0", "11", "0.71", "8", "3", "121"]],
   [0.6, 0.55, 0.85, 0.85, 0.6, 0.65, 0.6, 0.7, 0.55, 0.75]))
a(("p", "Both logs are complete, with no missing days. Delhi has twelve times as many failures as Pune, so it is the "
        "main city for modelling. Hazard warnings are also far more frequent in Delhi (1,252 days against 121), "
        "which reflects real air pollution and not a fault in the data. Figure 4.1 shows how failures are spread "
        "over time."))
a(("fig", FIG + "fig4_1_failures_per_quarter.png",
   "Figure 4.1: Failed runs per quarter for Delhi and Pune, 5 Aug 2022 to 8 Nov 2026 (counted from the run logs; totals 133 and 11 match Table 4.1)", 6.5))
a(("h2", "4.2 Computational tools"))
a(("p", "The project is written in Python. Table 4.2 lists the main tools and what each was used for."))
a(("table", "Table 4.2: Tools used in the project",
   ["Tool", "Use in the project"],
   [["Python 3", "Pipeline, analysis, automation scripts"],
    ["pandas, NumPy", "Run logs, feature construction, splits"],
    ["scikit-learn", "Random Forest, logistic regression, metrics, time-series cross-validation"],
    ["XGBoost", "Gradient-boosted trees, compared in model selection"],
    ["imbalanced-learn (SMOTE)", "Oversampling inside training folds"],
    ["SHAP", "Tree-based explanations of the model"],
    ["Matplotlib", "Figures"],
    ["Jupyter notebook", "DPFP_Phase2_Modelling.ipynb, the full analysis"],
    ["joblib", "Saving the trained model bundles"],
    ["GitHub Actions and GitHub Pages", "Daily job, weekly retrain, dashboard hosting"],
    ["HTML and JavaScript", "Pipeline Radar dashboard"]],
   [2.4, 4.6]))
a(("h2", "4.3 Data pre-processing and validation"))
a(("p", "Each run passes through ingestion, validation, transformation and feature enrichment. The loader keeps one "
        "run per day; if a day was logged more than once, the last run is used. Validation compares the day's data "
        "against rules set in the configuration file and assigns one of three outcomes: success, warning or "
        "failure."))
a(("p", "The central design decision is the failure taxonomy (Table 4.3). A run is a FAILURE only when the data or "
        "the pipeline is broken. High pollution is a real event in the world. When values cross the Central "
        "Pollution Control Board severe limits, the run is marked with a WARNING and the count of such values "
        "becomes an input signal. It is never the label. Treating high pollution as failure would teach the model "
        "to predict dirty air instead of broken data, and in Delhi it would turn 1,252 hazard days into "
        "\"failures\"."))
a(("table", "Table 4.3: Failure and warning taxonomy used by the pipeline",
   ["Outcome", "Type", "Rule (from the configuration)"],
   [["FAILURE", "DATA_QUALITY_FAILURE", "Negative pollutant values or invalid timestamps"],
    ["FAILURE", "DATA_QUALITY_FAILURE", "Sudden jump: PM2.5 changes by more than 50 µg/m³ in one hour"],
    ["FAILURE", "DATA_QUALITY_FAILURE", "Stagnant values: PM2.5 or PM10 identical for 6 or more consecutive hours"],
    ["FAILURE", "DATA_QUALITY_FAILURE", "Coverage below 80% or missing values above 25%"],
    ["FAILURE", "API_SLA_BREACH", "Run duration above the 3.0 s service-level limit"],
    ["WARNING", "HAZARD_THRESHOLD_EXCEEDED", "Values above CPCB severe limits (PM2.5 120, PM10 200, NO2 100, SO2 100, CO 2000 µg/m³)"],
    ["WARNING", "HIGH_RUNTIME", "Run duration above 2.0 s"],
    ["WARNING", "Coverage / missing values", "Coverage below 95% or missing values above 10%"]],
   [1.0, 2.1, 3.9]))
a(("p", "Because the data is model output, a run of identical values is a stagnant value in the served data. The "
        "pipeline's log calls this check SENSOR_STAGNATION, but there is no physical sensor behind it. This report "
        "uses the term stagnant values."))
a(("p", "Columns that never change in the training data carry no information and are dropped before modelling. "
        "Missing values in a feature are filled with the median of the training data, so no statistic from the "
        "validation or test period is used."))
a(("h2", "4.4 Feature engineering"))
a(("p", "All features are computed from the current run and earlier runs only. The notebook builds 22 signals in "
        "four groups (Table 4.4). Two of them, freshness_lag_hours and rows_vs_expected_ratio, are constant in the "
        "Delhi training data and are dropped, so the models use 20 signals."))
a(("table", "Table 4.4: The 22 signals by group",
   ["Group", "Signals", "Count"],
   [["DATA", "max_hourly_jump, drift_psi_mean, drift_psi_max, max_stagnation_run, invalid_value_count, max_hourly_jump_roll7, drift_psi_mean_roll7, freshness_lag_hours*, rows_vs_expected_ratio*, hazard_exceed_count", "10"],
    ["INFRA", "duration_seconds, duration_vs_baseline, api_latency_mean, api_latency_vs_baseline, api_latency_roll7_std, runtime_warn_last7", "6"],
    ["HISTORY", "dq_fail_today, sla_fail_today, fails_last7, days_since_fail", "4"],
    ["CALENDAR", "month_sin, month_cos", "2"]],
   [1.0, 5.3, 0.7]))
a(("pi", "* Constant in the training data and dropped before modelling."))
a(("p", "The DATA group describes the values themselves: the largest hour-to-hour jump, the longest run of "
        "identical values, the count of invalid values, the count of values above a hazard limit, and drift. The "
        "suffix roll7 marks a 7-run rolling mean of a signal. The INFRA group describes how the run behaved: its "
        "duration and API latency, each compared with a recent baseline, and recent high-runtime warnings. The "
        "HISTORY group records whether today's run failed, the number of failures in the last 7 runs and the days "
        "since the last failure. Month is encoded as a sine and cosine pair so that December sits next to "
        "January."))
a(("p", "Drift is measured with the Population Stability Index. For each pollutant, the current day's values "
        "are compared with a reference built from the means of the previous 7 runs, using 10 bins with edges taken "
        "from the reference distribution:"))
a(("p", "PSI = Σ_i (a_i − e_i) × ln(a_i / e_i)"))
a(("p", "where e_i and a_i are the shares of the reference and current samples in bin i. A PSI below 0.1 is usually "
        "read as no real shift, 0.1 to 0.25 as a moderate shift and above 0.25 as a large shift. drift_psi_mean is "
        "the mean over pollutants and drift_psi_max the largest value."))
a(("h2", "4.5 Exploratory analysis and chronological split"))
a(("p", "The target y is 1 when the next day's run is a DATA_QUALITY_FAILURE. Features from day t predict the label "
        "of day t+1. The Delhi log is split in time order: the oldest 50% of days for training, the next 25% for "
        "validation and the newest 25% for testing (Table 4.5, Figure 4.2). The data is never shuffled. The "
        "validation window covers a full year so that it contains enough failures for model choice and for the "
        "alarm threshold. The test window is used once, at the end, and holds 43 failures, above the minimum of 30 "
        "set in advance."))
a(("table", "Table 4.5: Chronological split of the Delhi data (outputs/03_split.csv)",
   ["Split", "From", "To", "Days", "Next-day failures", "Rate %"],
   [["Train", "2022-08-05", "2024-09-20", "778", "56", "7.2"],
    ["Validation", "2024-09-21", "2025-10-14", "389", "31", "8.0"],
    ["Test", "2025-10-15", "2026-11-07", "389", "43", "11.1"]],
   [1.1, 1.2, 1.2, 0.8, 1.4, 0.8]))
a(("fig", FIG + "fig4_2_split.png", "Figure 4.2: Next-day data-quality failures in each split (outputs/03_split.csv)", 4.8))
a(("p", "The failure rate rises from 7.2% in training to 11.1% in testing. A model that does well on the test window "
        "therefore has to cope with a later period that has more failures than it saw during training. All test "
        "results are compared with the test base rate of 0.111, which is the PR-AUC a random model would reach."))
a(("p", "PR-AUC (average precision) is the main metric because failures are rare. ROC-AUC is also reported. Lift is "
        "PR-AUC divided by the base rate; a lift of 1 means no better than chance. Confidence intervals come from "
        "1,000 bootstrap resamples of the test window."))

# ---------------------------------------------------------------- Chapter 5
a(("h1", "Analysis and Result"))
a(("h2", "5.1 Leakage-free next-day setup and the leakage demonstration"))
a(("p", "Every model in this chapter uses features from day t to predict the label of day t+1. Thresholds, "
        "calibration and model choice are fitted on the training and validation windows only. To show why this "
        "matters, the notebook also trains a deliberately invalid model. It predicts a run's failure from columns "
        "logged in that same run, such as invalid_value_count and max_hourly_jump. These columns are what the "
        "validation rules use to declare the failure, so the model is reading the answer."))
a(("table", "Table 5.1: Leaky vs honest model on the Delhi test window (outputs/10_leakage_gap.csv)",
   ["Model", "PR-AUC", "95% CI", "ROC-AUC", "Base rate", "Lift"],
   [["Leaky: same-run features to same-run failure (invalid)", "1.000", "[1.000, 1.000]", "1.000", "0.111", "9.05"],
    ["Honest: today's features to tomorrow's failure", "0.229", "[0.157, 0.347]", "0.695", "0.111", "2.07"]],
   [2.9, 0.7, 1.1, 0.7, 0.8, 0.6]))
a(("fig", FIG + "fig5_1_leakage_gap.png", "Figure 5.1: Same-run leakage gives a perfect score; the honest next-day model scores 0.229 (outputs/10_leakage_gap.csv)", 5.4))
a(("p", "The leaky model scores a perfect 1.000; the honest model scores 0.229. The difference of 0.771 is entirely "
        "an artefact of evaluation. A result of this kind looks impressive in a paper and is useless in practice, "
        "because the columns it relies on exist only after the run has failed. This project applies a known "
        "pitfall demonstration to data-pipeline failure forecasting, where same-run features are an easy trap. "
        "All later results use the honest setup."))
a(("h2", "5.2 Model and class-imbalance selection"))
a(("p", "Three algorithms were compared: Random Forest, XGBoost and logistic regression as a "
        "linear reference. Each was combined with four ways of handling imbalance: none, class weights, SMOTE "
        " and both together. SMOTE was applied only inside the training data, never to validation or test "
        "rows. All twelve combinations were trained on the training window and ranked by validation PR-AUC "
        "(Table 5.2, Figure 5.2). The test window was not used."))
a(("table", "Table 5.2: Model x imbalance ablation on the validation window (outputs/04_imbalance_ablation.csv)",
   ["Rank", "Model", "Imbalance", "Validation PR-AUC", "Validation ROC-AUC"],
   [["1", "Random Forest", "none", "0.171", "0.726"],
    ["2", "Logistic Regression", "weights", "0.161", "0.637"],
    ["3", "Random Forest", "weights", "0.141", "0.706"],
    ["4", "XGBoost", "none", "0.140", "0.707"],
    ["5", "Logistic Regression", "none", "0.118", "0.609"],
    ["6", "Random Forest", "smote", "0.114", "0.655"],
    ["7", "Random Forest", "both", "0.114", "0.656"],
    ["8", "XGBoost", "smote", "0.112", "0.647"],
    ["9", "XGBoost", "both", "0.112", "0.647"],
    ["10", "XGBoost", "weights", "0.110", "0.652"],
    ["11", "Logistic Regression", "smote", "0.110", "0.570"],
    ["12", "Logistic Regression", "both", "0.110", "0.570"]],
   [0.6, 1.8, 1.1, 1.6, 1.6]))
a(("fig", FIG + "fig5_2_imbalance_ablation.png", "Figure 5.2: Validation PR-AUC for each model and imbalance strategy; dashed line = validation base rate 0.080 (outputs/04_imbalance_ablation.csv)", 6.2))
a(("p", "Random Forest without resampling ranked first, with a validation PR-AUC of 0.171, and was selected. SMOTE "
        "lowered the score for every algorithm. With only 56 training failures, synthetic points made between "
        "neighbouring failures seem to add noise more than signal. XGBoost was planned as the primary model in the "
        "methodology document, but the validation result favoured Random Forest, so the data decided. This suggests "
        "that, on small tabular data like this, the features and the evaluation matter more than the choice among "
        "tree ensembles."))
a(("h2", "5.3 Probability calibration"))
a(("p", "A risk score is more useful when 0.40 means about a 40% chance. Platt scaling was fitted "
        "on the validation window, which SMOTE never touches. Isotonic calibration was not used because it "
        "over-fits at this data size. Table 5.3 shows the effect on the test window."))
a(("table", "Table 5.3: Calibration on the test window (outputs/05_calibration.csv)",
   ["", "Brier score (lower is better)", "PR-AUC"],
   [["Before calibration", "0.0945", "0.2291"],
    ["After Platt calibration", "0.0931", "0.2291"]],
   [2.2, 2.4, 1.4]))
a(("fig", OUT + "fig05_reliability.png", "Figure 5.3: Reliability diagram on the test window, raw and Platt-calibrated risk (outputs/fig05_reliability.png, from the notebook)", 3.9))
a(("p", "Calibration lowered the Brier score from 0.0945 to 0.0931. PR-AUC did not change, because Platt scaling "
        "keeps the order of the scores and PR-AUC depends only on that order. The benefit is in how the number "
        "reads: the calibrated risk shown to an operator is closer to an observed failure rate."))
a(("h2", "5.4 Baselines and the data-vs-infrastructure ablation"))
a(("p", "To test whether data signals carry the predictive value, the same algorithm was retrained on each feature "
        "group, with its own calibration and threshold from validation. Two simple baselines set the floor: a "
        "dummy model that always predicts the base rate, and a persistence rule that warns tomorrow whenever "
        "today failed. All rows use the same test window (Table 5.4, Figure 5.4)."))
a(("table", "Table 5.4: Baselines and feature-group models on the test window (outputs/06_baselines_and_ablation.csv)",
   ["Model", "PR-AUC", "95% CI", "ROC-AUC", "Lift", "Precision", "Recall", "F1"],
   [["Dummy (base rate)", "0.111", "[0.085, 0.141]", "0.500", "1.00", "-", "-", "-"],
    ["Rule: persistence (today failed)", "0.169", "[0.111, 0.253]", "0.608", "1.52", "0.302", "0.302", "0.302"],
    ["ML: INFRA only", "0.116", "[0.078, 0.196]", "0.482", "1.05", "0.112", "0.674", "0.192"],
    ["ML: HISTORY only", "0.196", "[0.126, 0.308]", "0.593", "1.77", "0.346", "0.209", "0.261"],
    ["ML: DATA only", "0.217", "[0.144, 0.340]", "0.664", "1.97", "0.219", "0.488", "0.302"],
    ["ML: DATA + HISTORY", "0.220", "[0.147, 0.330]", "0.678", "1.99", "0.233", "0.488", "0.316"],
    ["ML: ALL (data + infra + history)", "0.229", "[0.157, 0.347]", "0.695", "2.07", "0.248", "0.581", "0.347"]],
   [2.2, 0.65, 1.1, 0.7, 0.55, 0.75, 0.65, 0.55]))
a(("fig", FIG + "fig5_4_baselines_ablation.png", "Figure 5.4: Test PR-AUC with 95% bootstrap intervals for baselines and feature groups (outputs/06_baselines_and_ablation.csv)", 6.5))
a(("p", "The infrastructure-only model scored 0.116, almost the same as the dummy's 0.111, and its ROC-AUC of 0.482 "
        "is below 0.5. Run duration and API latency carry almost no information about tomorrow's data-quality "
        "failure. The data-only model scored 0.217, close to the full model's 0.229. The full model also beat the "
        "persistence rule (0.169). The confidence intervals are wide and overlap, because the test window holds "
        "only 43 failures, so the ranking between the data-only and the full model is not certain. The gap between "
        "data-only and infrastructure-only is clearer, and it supports the second objective. The full model is "
        "used from here on."))
a(("h2", "5.5 Operating point: alerts and false alarms"))
a(("p", "An operator needs a yes or no alarm. The threshold was chosen on the validation window by maximising F1, "
        "giving 0.116, and then applied unchanged to the test window (Table 5.5)."))
a(("table", "Table 5.5: Operating point on the test window (outputs/07_operating_point.csv)",
   ["Threshold", "Test failures", "Caught (TP)", "Missed (FN)", "False alarms (FP)", "Recall", "Precision", "False alarms / month", "Alarms / month"],
   [["0.116", "43", "25", "18", "76", "0.581", "0.248", "5.95", "7.91"]],
   [0.75, 0.75, 0.7, 0.7, 0.85, 0.6, 0.7, 0.9, 0.75]))
a(("fig", OUT + "fig07_pr_curve.png", "Figure 5.5: Precision-recall curve on the test window with the chosen threshold marked (outputs/fig07_pr_curve.png, from the notebook)", 4.0))
a(("fig", FIG + "fig5_6_operating_point.png", "Figure 5.6: Test outcomes at the chosen threshold (outputs/07_operating_point.csv)", 4.8))
a(("p", "At this threshold the model caught 25 of the 43 test failures one day ahead and missed 18. It raised about "
        "7.9 alarms a month, of which about 6.0 were false. Roughly one alarm in four was followed by a real "
        "failure. For a daily pipeline this is about two checks a week in exchange for advance notice of more "
        "than half the failures. A team that wants fewer false alarms can "
        "raise the threshold and accept a lower recall, moving along the curve in Figure 5.5."))
a(("h2", "5.6 Lead time and the 3-day outlook"))
a(("p", "Each run is one day, so the basic lead time of the model is one day. The notebook looks at lead time in two "
        "ways. The horizon curve retrains the model for a wider target: a failure on any of the next k days, for k "
        "from 1 to 7 (Table 5.6). The alarm run-up counts, for each test failure, how many consecutive days the "
        "alarm had already been on before it (Figure 5.7)."))
a(("table", "Table 5.6: Horizon curve, target = a failure within the next k days (outputs/08_horizon_curve.csv)",
   ["k (days)", "Test PR-AUC", "95% CI", "Base rate", "Lift", "ROC-AUC"],
   [["1", "0.229", "[0.157, 0.347]", "0.111", "2.07", "0.695"],
    ["2", "0.273", "[0.208, 0.378]", "0.188", "1.45", "0.589"],
    ["3", "0.341", "[0.266, 0.447]", "0.254", "1.34", "0.562"],
    ["4", "0.410", "[0.341, 0.508]", "0.316", "1.30", "0.573"],
    ["5", "0.487", "[0.415, 0.573]", "0.369", "1.32", "0.566"],
    ["6", "0.470", "[0.403, 0.560]", "0.412", "1.14", "0.525"],
    ["7", "0.480", "[0.415, 0.562]", "0.454", "1.06", "0.496"]],
   [0.9, 1.1, 1.4, 1.0, 0.8, 1.0]))
a(("fig", FIG + "fig5_7_lead_time.png", "Figure 5.7: Left, horizon curve with lift at each k (outputs/08_horizon_curve.csv). Right, share of the 43 test failures for which the alarm was already on 1, 2 or 3 days before (notebook Section 8 output)", 6.5))
a(("p", "PR-AUC rises with k, but the base rate rises faster, so lift falls from 2.07 at one day to 1.06 at seven "
        "days. At seven days the model is close to guessing. The alarm run-up gives a similar picture: the alarm "
        "was on at least one day before 58% of test failures, at least two days before 40% and at least three "
        "days before 30%."))
a(("p", "The dashboard uses a different target for its 3-day outlook. horizon_models.py trains one model per exact "
        "day: will the run on day t+2 fail, and will the run on day t+3 fail. Each is scored on a chronological "
        "split that trains on the first 75% and tests on the last 25% (Table 5.7). Table 5.6 and Table 5.7 "
        "therefore answer different questions and should not be compared row by row: Table 5.6 asks whether a "
        "failure happens anywhere in the next k days, while Table 5.7 asks about one specific day."))
a(("table", "Table 5.7: 3-day outlook, exact-day targets (outputs/horizon_scores.csv)",
   ["Day predicted", "Test PR-AUC", "Test ROC-AUC", "Base rate", "Lift", "Test failures"],
   [["t+1 (next run)", "0.3282", "0.7318", "0.1103", "2.98", "43"],
    ["t+2", "0.1969", "0.6185", "0.1105", "1.78", "43"],
    ["t+3", "0.2069", "0.6397", "0.1105", "1.87", "43"]],
   [1.3, 1.0, 1.0, 0.9, 0.7, 1.0]))
a(("fig", FIG + "fig5_8_outlook_exact_day.png", "Figure 5.8: Exact-day outlook scores used by the dashboard (outputs/horizon_scores.csv)", 4.9))
a(("p", "For exact days, skill drops from a lift of 2.98 for the next run to 1.78 and 1.87 for two and three days "
        "ahead. The dashboard shows the later days as weak signals, and only the next-run forecast can raise an "
        "alert. One day ahead is a modest horizon. It is also the horizon that can be checked most cleanly against "
        "what happened."))
a(("h2", "5.7 Per-failure-type predictability map"))
a(("p", "This is the headline result. Instead of one blended score, the same method was applied to every pair of "
        "city and failure type with at least 5 events. Because some pairs have few events, the map uses "
        "expanding-window time-series cross-validation over the whole log (5 folds, always training on the past "
        "and predicting the next block) and pools the out-of-fold predictions. A type is called predictable only "
        "when the lower end of the 95% confidence interval for lift is above 1 (Table 5.8, Figure 5.9)."))
a(("table", "Table 5.8: Per-failure-type predictability map (outputs/09_predictability_map.csv)",
   ["City", "Failure type", "Events", "Evaluated events", "PR-AUC", "95% CI", "Base rate", "Lift", "Lift CI low", "Verdict"],
   [["Delhi", "DATA_QUALITY_FAILURE", "130", "89", "0.156", "[0.111, 0.226]", "0.069", "2.27", "1.62", "Predictable"],
    ["Delhi", "API_SLA_BREACH", "3", "-", "-", "-", "-", "-", "-", "Too few events to test"],
    ["Pune", "DATA_QUALITY_FAILURE", "8", "4", "0.004", "[0.002, 0.011]", "0.003", "1.43", "0.64", "Not reliably predictable"],
    ["Pune", "API_SLA_BREACH", "3", "-", "-", "-", "-", "-", "-", "Too few events to test"]],
   [0.55, 1.45, 0.55, 0.7, 0.6, 0.95, 0.6, 0.45, 0.6, 1.05]))
a(("fig", FIG + "fig5_9_predictability_map.png", "Figure 5.9: Lift by city and failure type with the lower 95% bound; dashed line = chance (outputs/09_predictability_map.csv)", 6.2))
a(("p", "Data-quality failures in Delhi are predictable one day ahead: lift is 2.27 and the lower bound of 1.62 is "
        "clearly above chance. In Pune the point estimate of 1.43 is above 1, but only 4 events fall in the "
        "evaluated folds and the lower bound of 0.64 is below 1, so Pune's data-quality failures are not reliably "
        "predictable. API service-level breaches occurred only 3 times in each city and could not be tested."))
a(("p", "The API breaches are also different in kind. They depend on how fast the API answered at the moment the "
        "historical replay ran, which is driven by conditions outside the pipeline. Reliability engineering "
        "separates random failures, which arrive without warning, from systematic ones, which build up through a "
        "process that can be observed. Data-quality failures in Delhi behave like systematic failures: "
        "jumps, drift and stagnation tend to come in runs. External API slowdowns behave more like random "
        "failures and leave no sign in the pipeline's own data."))
a(("p", "The practical message is that a failure-prediction system should report predictability per type. A single "
        "blended score would mix a predictable type with an unpredictable one and hide both. To our knowledge, "
        "per-failure-type predictability is seldom reported explicitly in the 47 reviewed "
        "papers, and this project reports it as a finding."))
a(("h2", "5.8 Cross-city test"))
a(("p", "As a supporting check, a model was trained on all of one city and tested on all of the other, in both "
        "directions. Both cities share the same pipeline, schema and API, so this is a mild out-of-distribution "
        "check under a shared schema and should not be read as strong domain transfer (Table 5.9)."))
a(("table", "Table 5.9: Cross-city test (outputs/11_cross_source.csv)",
   ["Setting", "PR-AUC", "95% CI", "ROC-AUC", "Base rate", "Lift"],
   [["Within Delhi (time split)", "0.229", "[0.157, 0.347]", "0.695", "0.111", "2.07"],
    ["Train Delhi (130 failures), test Pune (8 failures)", "0.245", "[0.011, 0.628]", "0.579", "0.005", "47.68"],
    ["Train Pune (8 failures), test Delhi (130 failures)", "0.161", "[0.126, 0.218]", "0.688", "0.084", "1.92"]],
   [2.9, 0.7, 1.1, 0.7, 0.8, 0.7]))
a(("fig", FIG + "fig5_10_cross_city.png", "Figure 5.10: Cross-city PR-AUC with confidence intervals and base rates (outputs/11_cross_source.csv)", 6.2))
a(("p", "A model trained on Pune's 8 failures still reached a lift of 1.92 on Delhi, with a confidence interval "
        "that stays above Delhi's base rate of 0.084. The signals therefore carry some meaning across the two "
        "cities. The Delhi-to-Pune result has a lift of 47.68, but with 8 test failures and an interval from 0.011 "
        "to 0.628 it is too uncertain to interpret beyond saying that the model is not useless on Pune."))
a(("h2", "5.9 Explainability"))
a(("p", "Global importance was measured as the mean absolute SHAP value of each signal on the test "
        "window. Figure 5.11 shows the top 15 signals and Figure 5.12 the SHAP summary plot. Grouped together, data "
        "signals account for 0.615 of total importance, history for 0.226, infrastructure for 0.094 and calendar "
        "for 0.065 (notebook Section 12)."))
a(("fig", FIG + "fig5_11_importance.png", "Figure 5.11: Top 15 signals by mean |SHAP| on the test window (outputs/12_feature_importance.csv)", 5.6))
a(("fig", OUT + "fig12_shap_summary.png", "Figure 5.12: SHAP summary of the impact of each signal on next-day failure risk (outputs/fig12_shap_summary.png, from the notebook)", 5.0))
a(("p", "The largest hour-to-hour jump in today's data is the strongest single signal, followed by the days since "
        "the last failure, the 7-run trend of jumps, the count of values above hazard limits and the mean drift "
        "score. The leading signals describe the data itself, which agrees with the ablation in Section 5.4. SHAP "
        "rankings in gradient-boosted and tree models can shift between runs when signals are correlated "
        ", so the claim that data signals add value rests on the ablation, and the SHAP ranking is "
        "used as supporting evidence."))
a(("p", "SHAP is also used for single predictions. The function predict_failure(city, date) returns the risk for a "
        "date, the risk level, the likely failure type, the lead time and the top three reasons. For example, for "
        "Delhi on 14 December 2025 it gave a risk of 0.24 against an alarm threshold of 0.12, with large hourly "
        "jumps, the time since the last failure and today's failed run as the reasons; a data-quality failure did "
        "occur that day. For 15 May 2026 it gave 0.09, below the threshold, and the failure that followed was "
        "missed. Both cases are printed in Section 13 of the notebook."))
a(("h2", "5.10 The deployed system"))
a(("p", "The model runs as a daily system on GitHub Actions (Figure 5.13). The workflow daily.yml runs at 08:00 India "
        "time with a backup run at 11:00; the backup does nothing when the first run has already worked. Only one "
        "run can execute at a time, so two runs never write the same logs."))
a(("fig", FIG + "fig5_13_system_flow.png", "Figure 5.13: Flow of the automated daily system", 6.5))
a(("p", "run_daily.py fetches the previous day for both cities and fills in any missed days, up to 60 days back. "
        "Before fetching, a data-ready check reads Open-Meteo's status file to see whether the CAMS run that starts "
        "at 12:00 UTC on that day has been published. Until it is, the evening hours of the day are still forecast "
        "values that will later be replaced. Because the pipeline never re-fetches a finished day, a day is "
        "fetched only once its values are final. If the status file cannot be read, the job waits until 16 hours "
        "after 12:00 UTC."))
a(("p", "On Sundays, retrain_weekly.py retrains the Random Forest on the full Delhi log and appends one row to "
        "performance_history.csv, and horizon_models.py refits the day t+2 and t+3 models. build_dashboard.py then "
        "scores each pipeline, adds the 3-day outlook, appends the day's forecasts to forecast_log.csv and writes "
        "the dashboard. The new data, model and dashboard are committed back to the repository, and pages.yml "
        "publishes the dashboard as Pipeline Radar. Screenshots are in Annexure B."))
a(("p", "forecast_log.csv is the honest record of the deployed system: each forecast is stored with the time it was "
        "made, before the outcome is known. A sample is in Annexure C. The dashboard marks pipelines with fewer "
        "than 30 past failures as low confidence, which applies to Pune."))
a(("h3", "Why the weekly retrain reports a higher score"))
a(("p", "The weekly retrain and the notebook score the same kind of model but use different protocols. The notebook "
        "trains on the first 50% of days, uses the next 25% for model choice, calibration and the threshold, and "
        "tests on the last 25%. The weekly retrain trains on the first 75% and tests on the last 25%, so its model "
        "sees about 50% more history before the test window. The latest retrain, on 10 November 2026, reached a "
        "test PR-AUC of 0.3282 against a base rate of 0.1103, about 3.0 times better than chance. The notebook's "
        "model reached 0.229 against 0.111, about 2.1 times. This report uses the notebook's numbers throughout, "
        "because the notebook keeps a separate validation window for every choice and so gives the more cautious "
        "estimate. Figure 5.14 shows the weekly-retrain scores logged so far."))
a(("table", "Table 5.10: Weekly-retrain scores logged so far (outputs/performance_history.csv, repeated rows removed)",
   ["Retrain date", "Data through", "Rows", "Failures", "Test PR-AUC", "Test ROC-AUC", "Base rate"],
   [["2026-11-08", "2026-11-07", "1,526", "129", "0.3062", "0.6760", "0.1242"],
    ["2026-11-09", "2026-11-07", "1,556", "130", "0.1312", "0.5844", "0.0897"],
    ["2026-11-10", "2026-11-08", "1,557", "130", "0.3282", "0.7318", "0.1103"]],
   [1.0, 1.0, 0.7, 0.8, 1.0, 1.1, 0.9]))
a(("fig", FIG + "fig5_14_performance_history.png", "Figure 5.14: Test PR-AUC and base rate at each weekly retrain (outputs/performance_history.csv)", 5.2))
a(("p", "The 9 November retrain scored only 0.1312. On that day the base rate of its test window was also lower "
        "(0.0897). With three retrains and test windows of a few dozen failures, one retrain can swing a lot, so "
        "these rows are a log of the running system and should not be read as a trend."))

# ---------------------------------------------------------------- Chapter 6
a(("h1", "Result and Discussion"))
a(("p", "Table 6.1 is the results summary produced by Section 15 of the notebook."))
a(("table", "Table 6.1: Summary of results (outputs/15_summary.csv)",
   ["Result", "Value"],
   [["Next-day data-quality failure, main model (test PR-AUC)", "0.229 vs random 0.111"],
    ["Main model ROC-AUC (test)", "0.695"],
    ["Selected algorithm / imbalance handling", "Random Forest / none"],
    ["Recall at chosen threshold", "0.58 (6.0 false alarms / month)"],
    ["DATA-only vs INFRA-only PR-AUC", "0.217 vs 0.116"],
    ["Best rule baseline PR-AUC", "0.169"],
    ["Failures warned at least 1 / 2 days ahead", "58% / 40%"],
    ["Leaky vs honest PR-AUC", "1.000 vs 0.229"]],
   [4.3, 2.7]))
a(("p", "Next-day forecasting of data-quality failures works, at a modest level. The main model reaches 2.1 times "
        "the random baseline on a test year it never saw, and it beats every simple rule. At an alarm threshold "
        "fixed before testing, it warns of 58% of failures a day ahead at a cost of about six false alarms a month. "
        "Several of the reviewed papers report accuracy figures above 90% {P6}{P21}, but on different tasks, often "
        "without the failure rate and sometimes on simulated data. Those figures are not comparable with this "
        "study, and the leakage demonstration shows how a careless setup on this very dataset produces a perfect "
        "1.000."))
a(("p", "Most of the predictive value comes from the data signals. The infrastructure-only model is no better than chance, while the data-only "
        "model gets most of the way to the full model. In this pipeline, the API's speed and the run's duration "
        "say almost nothing about whether tomorrow's values will be broken, while jumps, drift and stagnation in "
        "today's values do. This supports building failure forecasts on data-quality telemetry, which most "
        "observability tools already collect for detection {P25}."))
a(("p", "The per-type map changes how the results should be reported. Data-quality failures in Delhi are "
        "predictable, Pune's few failures are not reliably predictable, and API breaches cannot be tested. A team "
        "adopting this approach should first count how many failures of each type it has. Below a few dozen "
        "events per type, a forecast cannot be validated, and the dashboard flags such pipelines as low "
        "confidence for that reason."))
a(("p", "Lead time is short. Skill is clearest one day ahead and fades to near chance by seven days. For a daily "
        "pipeline, one day is still enough time to check the source or hold a dependent job, and it is the "
        "horizon that can be verified most directly."))
a(("p", "The system also runs every day. The model is retrained weekly, every forecast is stored as it is made, and the "
        "dashboard shows the risk, the reasons and an alert log. In a few months forecast_log.csv will hold a "
        "genuinely out-of-sample record of how the deployed model performed, which the notebook's historical test "
        "window cannot provide."))

# ---------------------------------------------------------------- Chapter 7
a(("h1", "Limitation and Future Scope"))
a(("h2", "7.1 Limitations"))
a(("num", [
    "The data is CAMS model output served by Open-Meteo, and it does not come from ground sensors. Checks such as "
    "stagnation detect stagnant values in the served data, so this report avoids calling them stuck sensors. "
    "Failure patterns in a sensor network may look different.",
    "Pune has only 8 data-quality failures, so its failures are not reliably predictable and the cross-city result "
    "from Delhi to Pune has a very wide confidence interval.",
    "All data comes from one source, the Open-Meteo air-quality API. The two cities share the same API, schema and "
    "code, so the cross-city test is a mild check and does not show transfer to other pipelines.",
    "API service-level breaches occurred only 3 times per city and could not be tested. Their timing also depends "
    "on API speed when the historical replay ran, which may differ from live conditions.",
    "The test window holds 43 failures. The confidence intervals are wide and overlap for several models, so small "
    "differences, such as data-only against the full model, are not established.",
    "On the dashboard, past days are scored by the current model, which was trained on data that includes some of "
    "those days. Only forecast_log.csv holds forecasts exactly as they were made.",
    "The evening hours of 8 and 9 November 2026 were stored before Open-Meteo had published their final values, "
    "so those two days may hold forecast values for some hours. 8 November is inside the analysis data.",
    "The weekly retrain and the notebook use different protocols and report different scores (about 3.0 and 2.1 "
    "times the base rate). This report uses the notebook's numbers.",
    "SHAP rankings can shift between runs when signals are correlated, so they support the ablation and do not "
    "replace it.",
]))
a(("h2", "7.2 Future scope"))
a(("num", [
    "Add more pipelines with different sources and schemas, so that the cross-source test becomes a real transfer "
    "test and more failure types reach enough events to be mapped.",
    "Let forecast_log.csv grow for several months and report the live performance of the deployed model, with "
    "precision, recall and false alarms per month measured as they happened.",
    "Add a source of ground-sensor data, such as monitoring-station readings, to see whether the same signals "
    "forecast failures when the data comes from real sensors.",
    "Run the pipeline more than once a day, so that lead time can be measured in hours and the warning horizon "
    "can be tuned.",
    "Compare with newer tabular models and report seed stability for SHAP rankings.",
    "Link the alert to a safe action, such as holding dependent jobs or opening a review ticket, and measure "
    "whether the warnings reduce downstream incidents.",
]))

# ---------------------------------------------------------------- Annexures
ANNEX = []
b = ANNEX.append
b(("h2", "Annexure A: Project repository and live dashboard"))
b(("p", "Source code, data, notebook and outputs: https://github.com/VrushabLanjekar/DPFP-Project"))
b(("p", "Live dashboard (Pipeline Radar): https://vrushablanjekar.github.io/DPFP-Project/"))
b(("p", "Data source: Open-Meteo Air Quality API, https://open-meteo.com/en/docs/air-quality-api"))
b(("p", "Main files: DPFP_Phase2_Modelling.ipynb (analysis), run_daily.py (daily job), retrain_weekly.py (weekly "
        "retrain), horizon_models.py (3-day outlook models), build_dashboard.py (dashboard and forecast log), "
        ".github/workflows/daily.yml and pages.yml (automation)."))
b(("h2", "Annexure B: Dashboard screenshots"))
b(("p", "Screenshots of the dashboard file dashboard/index.html as built on 10 November 2026."))
b(("fig", FIG + "annex_dashboard_overview.png", "Figure B.1: Pipeline Radar overview, with both pipelines ranked by next-run risk", 6.5))
b(("fig", FIG + "annex_dashboard_detail.png", "Figure B.2: Detail view of the Delhi pipeline, with the 3-day outlook, risk history, reasons, alert log and health signals", 6.0))
b(("h2", "Annexure C: Sample of outputs/forecast_log.csv"))
b(("p", "The full file as of 10 November 2026. Each row is one forecast, stored when it was made. The forecast for "
        "Delhi on 12 November appears twice in the file."))
b(("table", "Table C.1: Forecast log (outputs/forecast_log.csv)",
   ["made_from", "days_ahead", "for_date", "pipeline", "risk", "alert", "logged_at"],
   [["2026-11-09", "1", "2026-11-10", "delhi", "0.118", "1", "2026-11-10T19:53:18+05:30"],
    ["2026-11-09", "1", "2026-11-10", "pune", "0.075", "0", "2026-11-10T19:53:18+05:30"],
    ["2026-11-09", "2", "2026-11-11", "delhi", "0.15", "0", "2026-11-10T20:15:23+05:30"],
    ["2026-11-09", "3", "2026-11-12", "delhi", "0.126", "0", "2026-11-10T20:15:23+05:30"],
    ["2026-11-09", "3", "2026-11-12", "delhi", "0.126", "0", "2026-11-10T20:15:23+05:30"],
    ["2026-11-09", "2", "2026-11-11", "pune", "0.149", "0", "2026-11-10T20:15:23+05:30"],
    ["2026-11-09", "3", "2026-11-12", "pune", "0.143", "0", "2026-11-10T20:15:23+05:30"]],
   [0.95, 0.8, 0.95, 0.7, 0.6, 0.5, 2.3]))
b(("h2", "Annexure D: Plagiarism report"))
b(("p", "[Plagiarism report to be inserted here.]"))

# ---------------------------------------------------------------- References
PAPERS_FILE = "Documents/Research_Findings_47_Papers.xlsx"
EXTRA_REFS = {}
