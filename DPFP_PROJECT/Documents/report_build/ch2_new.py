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
