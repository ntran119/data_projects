import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from scipy import stats

from bayes import run_simulations

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Bayesian A/B Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Bayesian A/B Testing Dashboard")
st.caption("Sequential Bayesian testing for conversion rates — configure parameters, run simulations, explore outcomes.")

# ──────────────────────────────────────────────
# Sidebar — parameters
# ──────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Parameters")

    st.subheader("Experiment setup")
    true_rate_a = st.slider("True conversion rate — A", 0.05, 0.50, 0.20, 0.01, format="%.2f")
    true_rate_b = st.slider("True conversion rate — B", 0.05, 0.50, 0.22, 0.01, format="%.2f")

    lift_label = f"{(true_rate_b - true_rate_a) / true_rate_a * 100:+.1f}% relative lift"
    st.caption(lift_label)

    daily_apps = st.slider("Daily visitors per arm", 50, 2000, 400, 50)
    max_days   = st.slider("Max experiment days", 7, 90, 30, 1)
    min_days   = st.slider("Burn-in (min days)", 1, 14, 7, 1)
    min_samples= st.slider("Burn-in (min samples per arm)", 100, 5000, 1000, 100)

    st.subheader("Decision thresholds")
    mde            = st.slider("Minimum detectable effect (MDE)", 0.001, 0.05, 0.01, 0.001, format="%.3f")
    prob_threshold = st.slider("P(meaningful) threshold", 0.50, 0.99, 0.80, 0.01, format="%.2f")

    st.subheader("Business value")
    value_per_conv    = st.number_input("Value per conversion ($)", 100, 100_000, 8_000, 500)
    max_loss_dollars  = st.number_input("Max acceptable expected loss ($)", 100, 500_000, 8_000, 500)

    st.subheader("Simulation settings")
    num_simulations = st.slider("Number of simulations", 50, 1000, 400, 50)
    mc_samples      = st.select_slider("Monte Carlo samples", options=[5_000, 10_000, 20_000, 50_000], value=20_000)
    seed            = st.number_input("Random seed (0 = random)", 0, 9999, 42, 1)

    run = st.button("▶ Run simulations", use_container_width=True, type="primary")

# ──────────────────────────────────────────────
# Run simulations
# ──────────────────────────────────────────────
if run:
    np.random.seed(seed if seed > 0 else None)

    with st.spinner(f"Running {num_simulations} simulations…"):
        results = run_simulations(
            num_simulations=num_simulations,
            true_rate_a=true_rate_a,
            true_rate_b=true_rate_b,
            daily_apps=daily_apps,
            max_days=max_days,
            min_days=min_days,
            min_samples=min_samples,
            mde=mde,
            prob_threshold=prob_threshold,
            value_per_conv=value_per_conv,
            max_loss_dollars=max_loss_dollars,
            mc_samples=mc_samples,
        )

    df = pd.DataFrame(results)
    st.session_state["sim_df"] = df
    st.session_state["params"] = dict(
        true_rate_a=true_rate_a,
        true_rate_b=true_rate_b,
        daily_apps=daily_apps,
        max_days=max_days,
        min_days=min_days,
        mde=mde,
        prob_threshold=prob_threshold,
        value_per_conv=value_per_conv,
        max_loss_dollars=max_loss_dollars,
        num_simulations=num_simulations,
        mc_samples=mc_samples,
    )

# ──────────────────────────────────────────────
# Results
# ──────────────────────────────────────────────
if "sim_df" not in st.session_state:
    st.info("Configure parameters in the sidebar and click **▶ Run simulations** to begin.")
    st.stop()

df = st.session_state["sim_df"]
p  = st.session_state["params"]

COLORS = {
    "SHIP_B":      "#3B6D11",
    "KEEP_A":      "#A32D2D",
    "INCONCLUSIVE":"#5F5E5A",
}
LABELS = {
    "SHIP_B":      "Ship B",
    "KEEP_A":      "Keep A",
    "INCONCLUSIVE":"Inconclusive",
}

counts = df["decision"].value_counts()
total  = len(df)

# ── KPI row ──────────────────────────────────
st.subheader("Decision outcomes")
col1, col2, col3, col4, col5 = st.columns(5)

def pct(key):
    return counts.get(key, 0) / total * 100

col1.metric("Ship B rate",       f"{pct('SHIP_B'):.1f}%",  f"{counts.get('SHIP_B', 0)} sims")
col2.metric("Keep A rate",       f"{pct('KEEP_A'):.1f}%",  f"{counts.get('KEEP_A', 0)} sims")
col3.metric("Inconclusive rate", f"{pct('INCONCLUSIVE'):.1f}%", f"{counts.get('INCONCLUSIVE', 0)} sims")
col4.metric("Avg decision day",  f"{df['decision_day'].mean():.1f}", f"of max {p['max_days']}")
col5.metric("Avg P(B > A)",      f"{df['prob_b_better'].mean()*100:.1f}%")

st.divider()

# ── Row 1: Distribution + Decision day histogram ──
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Decision distribution")
    ordered = ["SHIP_B", "KEEP_A", "INCONCLUSIVE"]
    fig_pie = go.Figure(go.Pie(
        labels=[LABELS[k] for k in ordered],
        values=[counts.get(k, 0) for k in ordered],
        marker_colors=[COLORS[k] for k in ordered],
        hole=0.45,
        textinfo="label+percent",
        hovertemplate="%{label}: %{value} sims (%{percent})<extra></extra>",
    ))
    fig_pie.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=300,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_b:
    st.subheader("Decision day histogram")
    fig_day = go.Figure()
    for key in ["SHIP_B", "KEEP_A", "INCONCLUSIVE"]:
        sub = df[df["decision"] == key]["decision_day"]
        if len(sub):
            fig_day.add_trace(go.Histogram(
                x=sub,
                name=LABELS[key],
                marker_color=COLORS[key],
                nbinsx=p["max_days"],
                opacity=0.85,
            ))
    fig_day.update_layout(
        barmode="stack",
        xaxis_title="Day",
        yaxis_title="Simulations",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40, b=40, l=40, r=10),
        height=300,
    )
    st.plotly_chart(fig_day, use_container_width=True)

st.divider()

# ── Row 2: Posterior distributions + Lift CI ──
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Posterior distributions (using mean cumulative data)")
    mean_row = df.mean(numeric_only=True)
    avg_apps = int(mean_row.get("cum_apps_a", p["daily_apps"] * p["max_days"] // 2))
    avg_book_a = int(avg_apps * p["true_rate_a"])
    avg_book_b = int(avg_apps * p["true_rate_b"])

    alpha_a = 1 + avg_book_a; beta_a_ = 1 + (avg_apps - avg_book_a)
    alpha_b = 1 + avg_book_b; beta_b_ = 1 + (avg_apps - avg_book_b)

    x_max = min(max(p["true_rate_a"], p["true_rate_b"]) * 2, 0.6)
    x = np.linspace(0.001, x_max, 500)

    fig_post = go.Figure()
    fig_post.add_trace(go.Scatter(
        x=x, y=stats.beta.pdf(x, alpha_a, beta_a_),
        name="Variant A", fill="tozeroy",
        line=dict(color="#185FA5"), fillcolor="rgba(24,95,165,0.2)",
    ))
    fig_post.add_trace(go.Scatter(
        x=x, y=stats.beta.pdf(x, alpha_b, beta_b_),
        name="Variant B", fill="tozeroy",
        line=dict(color="#3B6D11"), fillcolor="rgba(59,109,17,0.2)",
    ))
    fig_post.update_layout(
        xaxis_title="Conversion rate",
        yaxis_title="Density",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40, b=40, l=40, r=10),
        height=300,
    )
    st.plotly_chart(fig_post, use_container_width=True)

with col_d:
    st.subheader("Mean lift distribution across simulations")
    fig_lift = go.Figure()
    for key in ["SHIP_B", "KEEP_A", "INCONCLUSIVE"]:
        sub = df[df["decision"] == key]["mean_lift"] * 100
        if len(sub):
            fig_lift.add_trace(go.Histogram(
                x=sub,
                name=LABELS[key],
                marker_color=COLORS[key],
                opacity=0.80,
                nbinsx=40,
            ))
    fig_lift.add_vline(x=p["mde"] * 100, line_dash="dash", line_color="gray",
                       annotation_text=f"MDE ({p['mde']*100:.1f}%)")
    fig_lift.add_vline(x=0, line_color="black", line_width=1)
    fig_lift.update_layout(
        barmode="overlay",
        xaxis_title="Mean lift at decision (pp)",
        yaxis_title="Simulations",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40, b=40, l=40, r=10),
        height=300,
    )
    st.plotly_chart(fig_lift, use_container_width=True)

st.divider()

# ── Row 3: P(B>A) scatter + Expected loss scatter ──
col_e, col_f = st.columns(2)

with col_e:
    st.subheader("P(B > A) — final value per simulation")
    fig_prob = px.scatter(
        df.reset_index(), x="index", y=df["prob_b_better"] * 100,
        color="decision",
        color_discrete_map={k: COLORS[k] for k in COLORS},
        labels={"index": "Simulation #", "y": "P(B > A) %", "decision": "Decision"},
        height=280,
    )
    fig_prob.add_hline(y=p["prob_threshold"] * 100, line_dash="dash", line_color="gray",
                       annotation_text=f"threshold ({p['prob_threshold']*100:.0f}%)")
    fig_prob.update_layout(margin=dict(t=10, b=40, l=40, r=10), showlegend=False)
    st.plotly_chart(fig_prob, use_container_width=True)

with col_f:
    st.subheader("Expected loss $ — final value per simulation")
    fig_loss = px.scatter(
        df.reset_index(), x="index", y="expected_loss_$",
        color="decision",
        color_discrete_map={k: COLORS[k] for k in COLORS},
        labels={"index": "Simulation #", "expected_loss_$": "Expected loss ($)", "decision": "Decision"},
        height=280,
    )
    fig_loss.add_hline(y=p["max_loss_dollars"], line_dash="dash", line_color="gray",
                       annotation_text=f"max loss (${p['max_loss_dollars']:,})")
    fig_loss.update_layout(margin=dict(t=10, b=40, l=40, r=10), showlegend=False)
    st.plotly_chart(fig_loss, use_container_width=True)

st.divider()

# ── Row 4: Decision timing — box + strip ──
st.subheader("Decision timing by outcome")
col_g, col_h = st.columns(2)

df_plot = df.copy()
df_plot["decision_label"] = df_plot["decision"].map(LABELS)
label_order = ["Ship B", "Keep A", "Inconclusive"]
color_seq   = [COLORS["SHIP_B"], COLORS["KEEP_A"], COLORS["INCONCLUSIVE"]]

with col_g:
    fig_box = go.Figure()
    for label, color in zip(label_order, color_seq):
        sub = df_plot[df_plot["decision_label"] == label]["decision_day"]
        if len(sub):
            fig_box.add_trace(go.Box(
                y=sub, name=label,
                marker_color=color,
                boxmean="sd",
                line_width=1.5,
            ))
    fig_box.update_layout(
        xaxis_title="Experiment outcome",
        yaxis_title="Day decision was made",
        showlegend=False,
        margin=dict(t=10, b=40, l=40, r=10),
        height=320,
    )
    st.plotly_chart(fig_box, use_container_width=True)

with col_h:
    fig_strip = go.Figure()
    for i, (label, color) in enumerate(zip(label_order, color_seq)):
        sub = df_plot[df_plot["decision_label"] == label]
        if len(sub):
            jitter = (np.random.rand(len(sub)) - 0.5) * 0.4
            fig_strip.add_trace(go.Scatter(
                x=np.full(len(sub), i) + jitter,
                y=sub["decision_day"].values,
                mode="markers",
                name=label,
                marker=dict(color=color, opacity=0.45, size=6),
            ))
    fig_strip.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(len(label_order))),
            ticktext=label_order,
            title="Experiment outcome",
        ),
        yaxis_title="Day decision was made",
        showlegend=False,
        margin=dict(t=10, b=40, l=40, r=10),
        height=320,
    )
    st.plotly_chart(fig_strip, use_container_width=True)

st.divider()

# ── Row 5: Decision boundary ──
st.subheader("Decision boundary")
col_i, col_j = st.columns(2)

with col_i:
    fig_boundary = px.scatter(
        df_plot,
        x="prob_meaningful",
        y="expected_loss_$",
        color="decision_label",
        color_discrete_map={LABELS[k]: COLORS[k] for k in COLORS},
        opacity=0.55,
        labels={
            "prob_meaningful": "P(lift > MDE)",
            "expected_loss_$": "Expected loss ($)",
            "decision_label": "Decision",
        },
        height=340,
    )
    fig_boundary.add_vline(
        x=p["prob_threshold"], line_dash="dash", line_color="#3B6D11",
        annotation_text=f"P threshold ({p['prob_threshold']:.0%})",
        annotation_position="top right",
    )
    fig_boundary.add_hline(
        y=p["max_loss_dollars"], line_dash="dash", line_color="#A32D2D",
        annotation_text=f"Max loss (${p['max_loss_dollars']:,})",
        annotation_position="bottom right",
    )
    fig_boundary.update_layout(margin=dict(t=10, b=40, l=40, r=10))
    st.plotly_chart(fig_boundary, use_container_width=True)

with col_j:
    try:
        import plotly.figure_factory as ff
        fig_kde = go.Figure()
        for label, color in zip(label_order, color_seq):
            sub = df_plot[df_plot["decision_label"] == label]
            if len(sub) >= 5:
                fig_kde.add_trace(go.Histogram2dContour(
                    x=sub["prob_meaningful"],
                    y=sub["expected_loss_$"],
                    name=label,
                    colorscale=[[0, "rgba(0,0,0,0)"], [1, color]],
                    showscale=False,
                    contours=dict(showlabels=False),
                    line_width=1.5,
                ))
        fig_kde.update_layout(
            xaxis_title="P(lift > MDE)",
            yaxis_title="Expected loss ($)",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=40, l=40, r=10),
            height=340,
        )
        st.plotly_chart(fig_kde, use_container_width=True)
    except Exception:
        st.info("Density contour requires more simulations per decision type.")

st.divider()

# ── Row 6: CI width by decision ──
st.subheader("Uncertainty (CI width) by decision")
col_k, col_l = st.columns(2)

with col_k:
    fig_ci_box = go.Figure()
    for label, color in zip(label_order, color_seq):
        sub = df_plot[df_plot["decision_label"] == label]
        if len(sub):
            fig_ci_box.add_trace(go.Box(
                x=[label] * len(sub),
                y=sub["ci_width"].values,
                name=label,
                marker_color=color,
                boxmean="sd",
                line_width=1.5,
                opacity=0.85,
                boxpoints=False,
            ))
    for i, (label, color) in enumerate(zip(label_order, color_seq)):
        sub = df_plot[df_plot["decision_label"] == label]
        if len(sub):
            jitter = (np.random.rand(len(sub)) - 0.5) * 0.3
            fig_ci_box.add_trace(go.Scatter(
                x=np.full(len(sub), i, dtype=float) + jitter,
                y=sub["ci_width"].values,
                mode="markers",
                showlegend=False,
                xaxis="x2",
                marker=dict(color="rgba(0,0,0,0.22)", size=4),
            ))
    fig_ci_box.update_layout(
        xaxis=dict(title="Decision", type="category"),
        xaxis2=dict(
            overlaying="x",
            range=[-0.5, len(label_order) - 0.5],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        yaxis_title="95% CI width (lift)",
        showlegend=False,
        margin=dict(t=10, b=40, l=40, r=10),
        height=320,
    )
    st.plotly_chart(fig_ci_box, use_container_width=True)

with col_l:
    fig_ci_hist = go.Figure()
    for label, color in zip(label_order, color_seq):
        sub = df_plot[df_plot["decision_label"] == label]["ci_width"]
        if len(sub):
            fig_ci_hist.add_trace(go.Histogram(
                x=sub, name=label,
                marker_color=color,
                opacity=0.80,
                nbinsx=30,
            ))
    fig_ci_hist.update_layout(
        barmode="stack",
        xaxis_title="CI width",
        yaxis_title="Count",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40, b=40, l=40, r=10),
        height=320,
    )
    st.plotly_chart(fig_ci_hist, use_container_width=True)

st.divider()

# ── Summary stats table ──
st.subheader("Summary statistics by decision")

summary = (
    df.groupby("decision")
    .agg(
        count=("decision", "count"),
        avg_day=("decision_day", "mean"),
        avg_prob_b_better=("prob_b_better", "mean"),
        avg_prob_meaningful=("prob_meaningful", "mean"),
        avg_mean_lift=("mean_lift", "mean"),
        avg_expected_loss=("expected_loss_$", "mean"),
        avg_ci_width=("ci_width", "mean"),
    )
    .rename(columns={
        "count": "# sims",
        "avg_day": "Avg day",
        "avg_prob_b_better": "Avg P(B>A)",
        "avg_prob_meaningful": "Avg P(meaningful)",
        "avg_mean_lift": "Avg lift",
        "avg_expected_loss": "Avg exp loss ($)",
        "avg_ci_width": "Avg CI width",
    })
    .reset_index()
)
summary["decision"] = summary["decision"].map(LABELS)
summary["Avg P(B>A)"]       = summary["Avg P(B>A)"].map("{:.1%}".format)
summary["Avg P(meaningful)"]= summary["Avg P(meaningful)"].map("{:.1%}".format)
summary["Avg lift"]         = summary["Avg lift"].map("{:+.3f}".format)
summary["Avg exp loss ($)"] = summary["Avg exp loss ($)"].map("${:,.0f}".format)
summary["Avg CI width"]     = summary["Avg CI width"].map("{:.4f}".format)
summary["Avg day"]          = summary["Avg day"].map("{:.1f}".format)

st.dataframe(summary, use_container_width=True, hide_index=True)

# ── Raw data expander ──
with st.expander("📄 Raw simulation data"):
    display_df = df.copy()
    display_df["decision"] = display_df["decision"].map(LABELS)
    for col in ["prob_b_better", "prob_meaningful"]:
        display_df[col] = display_df[col].map("{:.1%}".format)
    for col in ["mean_lift", "ci_lower", "ci_upper", "ci_width"]:
        display_df[col] = display_df[col].map("{:+.4f}".format)
    display_df["expected_loss_$"] = display_df["expected_loss_$"].map("${:,.0f}".format)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    csv = df.to_csv(index=False)
    st.download_button("⬇ Download CSV", csv, "ab_simulation_results.csv", "text/csv")