"""Redraws the report charts from outputs/*.csv with data labels.
Originals in outputs/ are not changed. Run from the project folder."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
O = Path("outputs"); F = Path("Documents/report_figures")
plt.rcParams.update({"font.family": "Calibri", "font.size": 11, "figure.dpi": 150,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})
C1, C2, C3, CB = "#2a6f97", "#e07a5f", "#9aa5b1", "#c0392b"


def save(name):
    plt.tight_layout(); plt.savefig(F / name, dpi=200); plt.close()


def lab(ax, bars, fmt="{:.3f}", pad=3, size=9, horiz=False):
    for b in bars:
        v = b.get_width() if horiz else b.get_height()
        if np.isnan(v):
            continue
        if horiz:
            ax.annotate(fmt.format(v), (v, b.get_y() + b.get_height() / 2), xytext=(pad, 0),
                        textcoords="offset points", va="center", fontsize=size)
        else:
            ax.annotate(fmt.format(v), (b.get_x() + b.get_width() / 2, v), xytext=(0, pad),
                        textcoords="offset points", ha="center", fontsize=size)


# 4.1 failures per quarter (run logs, same cut-off as 01_data_audit: up to 2026-11-08)
rows = []
for city, p in [("Delhi", "logs/delhi_runs/pipeline_runs.csv"), ("Pune", "logs/api_runs/pipeline_runs.csv")]:
    d = pd.read_csv(p); d["run_date"] = pd.to_datetime(d["run_date"])
    d = d.sort_values(["run_date", "start_time"]).drop_duplicates("run_date", keep="last")
    d = d[d.run_date <= "2026-11-08"]
    d["fail"] = (d.overall_status.str.upper() == "FAIL").astype(int)
    q = d.groupby(d.run_date.dt.to_period("Q"))["fail"].sum(); q.name = city; rows.append(q)
    print(city, "runs", len(d), "FAIL", d.fail.sum())
Q = pd.concat(rows, axis=1).fillna(0).astype(int)
fig, ax = plt.subplots(figsize=(10, 3.8)); x = np.arange(len(Q)); w = .4
lab(ax, ax.bar(x - w / 2, Q.Delhi, w, color=C1, label="Delhi"), "{:.0f}")
lab(ax, ax.bar(x + w / 2, Q.Pune, w, color=C2, label="Pune"), "{:.0f}")
ax.set_xticks(x); ax.set_xticklabels([str(p) for p in Q.index], rotation=45, fontsize=9)
ax.set_ylabel("failed runs"); ax.legend(frameon=False)
ax.set_title("Pipeline failures per quarter (5 Aug 2022 to 8 Nov 2026)")
save("fig4_1_failures_per_quarter.png"); Q.to_csv(F / "fig4_1_data.csv")

# 4.2 chronological split
s = pd.read_csv(O / "03_split.csv")
fig, ax = plt.subplots(figsize=(6.5, 3.4)); b = ax.bar(s.split, s.failures_next_day, color=[C3, C2, C1])
for bb, n, r, dd in zip(b, s.failures_next_day, s["rate_%"], s.days):
    ax.annotate(f"{n} failures\n{r}% of {dd} days", (bb.get_x() + bb.get_width() / 2, n), xytext=(0, 3),
                textcoords="offset points", ha="center", fontsize=9)
ax.set_ylim(0, s.failures_next_day.max() * 1.35); ax.set_ylabel("next-day DQ failures")
ax.set_title("Chronological split (Delhi)")
save("fig4_2_split.png")

# 5.1 leakage gap
L = pd.read_csv(O / "10_leakage_gap.csv")
fig, ax = plt.subplots(figsize=(7, 2.6))
b = ax.barh(["Honest: today -> tomorrow", "Leaky: same run (invalid)"], L["PR-AUC"][::-1].values, color=[C1, CB])
lab(ax, b, "{:.3f}", horiz=True); ax.set_xlim(0, 1.15); ax.set_xlabel("test PR-AUC")
ax.set_title("Same-run leakage vs the honest next-day model")
save("fig5_1_leakage_gap.png")

# 5.2 imbalance ablation
A = pd.read_csv(O / "04_imbalance_ablation.csv")
piv = A.pivot(index="imbalance", columns="model", values="val PR-AUC").loc[["none", "weights", "smote", "both"]]
base_val = pd.read_csv(O / "03_split.csv").set_index("split").loc["validation", "rate_%"] / 100
fig, ax = plt.subplots(figsize=(8.5, 3.8)); x = np.arange(4); w = .27
for i, (m, c) in enumerate(zip(piv.columns, [C3, C1, C2])):
    lab(ax, ax.bar(x + (i - 1) * w, piv[m], w, color=c, label=m), "{:.3f}", size=8)
ax.axhline(base_val, ls="--", color="k", lw=1, label=f"random (base rate {base_val:.3f})")
ax.set_xticks(x); ax.set_xticklabels(piv.index); ax.set_ylabel("validation PR-AUC"); ax.set_ylim(0, .21)
ax.legend(frameon=False, fontsize=9, ncol=2); ax.set_title("Model x imbalance strategy (validation window)")
save("fig5_2_imbalance_ablation.png")

# 5.4 baselines and ablation
B = pd.read_csv(O / "06_baselines_and_ablation.csv").iloc[::-1]
ci = B["PR-AUC 95% CI"].str.strip("[]").str.split(", ", expand=True).astype(float)
fig, ax = plt.subplots(figsize=(9, 4.2))
cols = [C1 if ("DATA" in n or "ALL" in n) else (C2 if "INFRA" in n else C3) for n in B.model]
b = ax.barh(B.model, B["PR-AUC"], xerr=np.vstack([B["PR-AUC"] - ci[0], ci[1] - B["PR-AUC"]]), color=cols, capsize=3)
for bb, v, lo, hi in zip(b, B["PR-AUC"], ci[0], ci[1]):
    ax.annotate(f"{v:.3f}  [{lo:.3f}, {hi:.3f}]", (hi, bb.get_y() + bb.get_height() / 2), xytext=(4, 0),
                textcoords="offset points", va="center", fontsize=9)
ax.axvline(B["base rate"].iloc[0], ls="--", color="k", lw=1, label=f"random ({B['base rate'].iloc[0]:.3f})")
ax.set_xlim(0, .5); ax.set_xlabel("test PR-AUC with 95% bootstrap CI"); ax.legend(frameon=False, loc="upper right")
ax.set_title("Baselines and feature-group ablation (test window)")
save("fig5_4_baselines_ablation.png")

# 5.6 operating point outcomes
P = pd.read_csv(O / "07_operating_point.csv").iloc[0]
fig, ax = plt.subplots(figsize=(6.5, 3.3))
names = ["caught 1 day ahead (TP)", "missed (FN)", "false alarms (FP)"]
b = ax.bar(["Caught (TP)", "Missed (FN)", "False alarms (FP)"], [P[n] for n in names], color=[C1, C3, C2])
lab(ax, b, "{:.0f}")
ax.set_ylabel("days in test window"); ax.set_ylim(0, P["false alarms (FP)"] * 1.2)
ax.set_title(f"Test outcomes at threshold {P['threshold (from validation)']:.3f}: "
             f"recall {P['recall']:.2f}, precision {P['precision']:.2f}", fontsize=10)
save("fig5_6_operating_point.png")

# 5.7 horizon curve (fails within k days) + run-up shares printed by the notebook (Section 8)
H = pd.read_csv(O / "08_horizon_curve.csv")
fig, axes = plt.subplots(1, 2, figsize=(11, 3.9), gridspec_kw={"width_ratios": [1.6, 1]})
ax = axes[0]
ax.fill_between(H.horizon_days, H.CI_lo, H.CI_hi, color=C1, alpha=.15, label="95% CI")
ax.plot(H.horizon_days, H["test PR-AUC"], "o-", color=C1, label="model PR-AUC")
ax.plot(H.horizon_days, H["base rate"], "s--", color=C3, label="random (base rate)")
for k, v, br, li in zip(H.horizon_days, H["test PR-AUC"], H["base rate"], H.lift):
    ax.annotate(f"{v:.3f}\n(lift {li:.2f})", (k, v), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=8)
    ax.annotate(f"{br:.3f}", (k, br), xytext=(0, -13), textcoords="offset points", ha="center", fontsize=8, color="#555")
ax.set_xlabel("k: a failure within the next k days"); ax.set_ylabel("test PR-AUC"); ax.set_ylim(0, .72)
ax.legend(frameon=False, fontsize=9, loc="upper left"); ax.set_title("Horizon curve (08_horizon_curve.csv)", fontsize=10)
ax = axes[1]
b = ax.bar(["warned >= 1 day", "warned >= 2 days", "warned >= 3 days"], [58, 40, 30], color=C1)
lab(ax, b, "{:.0f}%"); ax.set_ylim(0, 75); ax.set_ylabel("% of the 43 test failures")
ax.set_title("Alarm run-up before test failures", fontsize=10); ax.tick_params(axis="x", labelsize=9)
save("fig5_7_lead_time.png")

# 5.8 exact-day 3-day outlook (horizon_scores.csv)
S = pd.read_csv(O / "horizon_scores.csv")
fig, ax = plt.subplots(figsize=(7, 3.6)); x = np.arange(len(S)); w = .38
b1 = ax.bar(x - w / 2, S.test_PR_AUC, w, color=C1, label="test PR-AUC")
b2 = ax.bar(x + w / 2, S.base_rate, w, color=C3, label="base rate")
lab(ax, b1, "{:.4f}"); lab(ax, b2, "{:.4f}")
for xi, li, v in zip(x, S.lift, S.test_PR_AUC):
    ax.annotate(f"lift {li:.2f}", (xi - w / 2, v), xytext=(0, 15), textcoords="offset points", ha="center", fontsize=9, color=C1)
ax.set_xticks(x); ax.set_xticklabels([f"day t+{d}" for d in S.days_ahead]); ax.set_ylim(0, .45)
ax.set_ylabel("PR-AUC"); ax.legend(frameon=False)
ax.set_title("3-day outlook: exact-day targets (horizon_scores.csv)", fontsize=10)
save("fig5_8_outlook_exact_day.png")

# 5.9 predictability map
M = pd.read_csv(O / "09_predictability_map.csv")
fig, ax = plt.subplots(figsize=(8.5, 3.8))
lbl = [f"{c}\n{t}" for c, t in zip(M.city, M["failure type"])]
colors = [C1 if v.startswith("PREDICTABLE") else (C2 if v.startswith("NOT") else "#dddddd") for v in M.verdict]
b = ax.bar(lbl, M.lift.fillna(0).values, color=colors)
for bb, (_, r) in zip(b, M.iterrows()):
    xm = bb.get_x() + bb.get_width() / 2
    if pd.isna(r["lift"]):
        ax.annotate(f"{r['events']} events:\ntoo few to test", (xm, 0), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=9)
    else:
        ax.plot([xm, xm], [r["lift CI low"], r["lift"]], color="k", lw=1)
        ax.plot(xm, r["lift CI low"], "k_", ms=12)
        ax.annotate(f"lift {r['lift']:.2f}\n(CI low {r['lift CI low']:.2f})\n{r['events']} events",
                    (xm, r["lift"]), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=9)
ax.axhline(1, ls="--", color="k", lw=1, label="lift = 1 (chance)")
ax.set_ylim(0, 3.4); ax.set_ylabel("lift = PR-AUC / base rate"); ax.legend(frameon=False, loc="upper right")
ax.tick_params(axis="x", labelsize=9); ax.set_title("Per-failure-type predictability map (expanding-window CV)", fontsize=10)
save("fig5_9_predictability_map.png")

# 5.10 cross-source
X = pd.read_csv(O / "11_cross_source.csv")
fig, ax = plt.subplots(figsize=(9, 3.2))
names = ["Within Delhi (time split)", "Train Delhi -> test Pune", "Train Pune -> test Delhi"]
b = ax.barh(names[::-1], X["PR-AUC"][::-1].values, color=[C2, C3, C1])
for bb, (_, r) in zip(b, X.iloc[::-1].iterrows()):
    ax.annotate(f"{r['PR-AUC']:.3f} {r['PR-AUC 95% CI']}, base rate {r['base rate']:.3f}",
                (r["PR-AUC"], bb.get_y() + bb.get_height() / 2), xytext=(4, 0), textcoords="offset points", va="center", fontsize=9)
ax.set_xlim(0, .62); ax.set_xlabel("PR-AUC"); ax.set_title("Cross-city test (shared schema)", fontsize=10)
save("fig5_10_cross_city.png")

# 5.11 feature importance
I = pd.read_csv(O / "12_feature_importance.csv", index_col=0).head(15)[::-1]
fig, ax = plt.subplots(figsize=(8, 5))
b = ax.barh(I.index, I.importance, color=[{"DATA": C1, "INFRA": C2}.get(g, C3) for g in I.group])
lab(ax, b, "{:.4f}", horiz=True, size=8); ax.set_xlim(0, I.importance.max() * 1.2)
ax.set_xlabel("mean |SHAP| on the test window")
ax.set_title("Top 15 signals (blue = data, orange = infra, grey = history/calendar)", fontsize=10)
save("fig5_11_importance.png")

# 5.14 performance over time (duplicate rows dropped)
Hh = pd.read_csv(O / "performance_history.csv").drop_duplicates().sort_values("retrain_date")
fig, ax = plt.subplots(figsize=(7.5, 3.6)); x = np.arange(len(Hh))
ax.plot(x, Hh.test_PR_AUC, "o-", color=C1, label="test PR-AUC")
ax.plot(x, Hh.base_rate, "s--", color=C3, label="base rate")
for xi, v, br in zip(x, Hh.test_PR_AUC, Hh.base_rate):
    ax.annotate(f"{v:.4f}", (xi, v), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=9)
    ax.annotate(f"{br:.4f}", (xi, br), xytext=(0, -14), textcoords="offset points", ha="center", fontsize=9, color="#555")
ax.set_xticks(x); ax.set_xticklabels([f"{d}\n({n} rows)" for d, n in zip(Hh.retrain_date, Hh.n_rows)], fontsize=9)
ax.set_xlim(-.4, len(Hh) - .6); ax.set_ylim(0, .42); ax.set_ylabel("PR-AUC (held-out tail)"); ax.legend(frameon=False)
ax.set_title("Weekly-retrain protocol: score at each retrain", fontsize=10)
save("fig5_14_performance_history.png")

# 5.13 system flow diagram
fig, ax = plt.subplots(figsize=(10, 2.5)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0.3, 3.0)
boxes = [(0.1, "GitHub Actions\n08:00 IST run\n11:00 IST backup"), (2.1, "run_daily.py\ndata-ready check,\nfetch Pune + Delhi"),
         (4.1, "Validate + enrich\nfailure or warning,\nsignals logged"), (6.1, "Sunday:\nretrain_weekly.py\n+ horizon_models.py"),
         (8.1, "build_dashboard.py\nforecast_log.csv,\nPipeline Radar")]
for x0, t in boxes:
    ax.add_patch(plt.Rectangle((x0, 1.3), 1.75, 1.5, fc="#eaf2f8", ec=C1, lw=1.5))
    ax.text(x0 + .875, 2.05, t, ha="center", va="center", fontsize=9)
for x0, _ in boxes[:-1]:
    ax.annotate("", (x0 + 2.0, 2.05), (x0 + 1.78, 2.05), arrowprops=dict(arrowstyle="->", lw=1.5))
ax.text(5, .6, "New logs, model and dashboard are committed back to the repository; pages.yml then publishes the dashboard.",
        ha="center", fontsize=9)
save("fig5_13_system_flow.png")
print("done")
