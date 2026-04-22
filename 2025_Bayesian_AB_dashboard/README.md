# Bayesian A/B Testing Dashboard

A Streamlit dashboard for sequential Bayesian A/B testing on conversion rates.
Configure experiment parameters, run Monte Carlo simulations, and explore decision outcomes interactively.
https://2025bayesianabdashboard-ewov9mndg2zphfrjbtmwd4.streamlit.app/
## Features

- Sequential Bayesian testing with Beta-Binomial conjugate model
- Configurable burn-in periods, MDE, probability thresholds, and business value inputs
- Dollar-denominated expected loss for business-interpretable stopping decisions
- Clean 3-branch decision logic: **Ship B** / **Keep A** / **Inconclusive**
- Charts: posterior distributions, decision day histogram, lift distribution, P(B>A) scatter, expected loss scatter
- Summary stats table and raw CSV export

## Decision logic

After the burn-in period (`min_days` and `min_samples` both satisfied):

| Condition | Decision |
|---|---|
| `P(lift > MDE) > threshold` AND `mean_lift > 0` AND `expected_loss_$ < max_loss` | **SHIP_B** |
| `P(lift > MDE) < 0.10` OR `P(B > A) < 0.05` | **KEEP_A** |
| Max days reached without decision | **INCONCLUSIVE** |

## Project structure

```
bayesian-ab-dashboard/
├── app.py              # Streamlit dashboard
├── bayes.py            # Bayesian engine (posteriors, simulation loop)
├── requirements.txt
└── README.md
```

## Running locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/bayesian-ab-dashboard.git
cd bayesian-ab-dashboard

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

## Deploying to Streamlit Community Cloud (free)

1. Push this repo to GitHub (must be public for the free tier)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select your repo → set `app.py` as the main file
4. Click **Deploy** — live in ~2 minutes, auto-redeploys on every `git push`

## Publishing to GitHub

```bash
git init
git add .
git commit -m "Initial commit — Bayesian A/B dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/bayesian-ab-dashboard.git
git push -u origin main
```

## Parameters reference

| Parameter | Description |
|---|---|
| True rate A / B | Ground truth conversion rates (used only for simulation) |
| Daily visitors per arm | Traffic split 50/50 between A and B |
| Max experiment days | Hard ceiling — experiment ends here regardless |
| Burn-in (min days / min samples) | No decisions made before both thresholds are met |
| MDE | Minimum detectable effect — lift must exceed this to be "meaningful" |
| P(meaningful) threshold | How confident we need to be that lift > MDE before shipping |
| Value per conversion | Used to convert expected loss from rate to dollars |
| Max acceptable expected loss | Decision is only made if remaining opportunity cost is below this |
| Simulations | How many independent experiments to run |
| Monte Carlo samples | Samples drawn from each posterior per day — higher = more accurate, slower |
