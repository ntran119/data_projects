import numpy as np


def beta_posterior(conversions: int, visitors: int) -> tuple[int, int]:
    """Return (alpha, beta) for a Beta posterior with flat prior."""
    alpha = 1 + conversions
    beta  = 1 + (visitors - conversions)
    return alpha, beta


def run_experiment(
    true_rate_a: float,
    true_rate_b: float,
    daily_apps: int,
    max_days: int,
    min_days: int,
    min_samples: int,
    mde: float,
    prob_threshold: float,
    mc_samples: int,
) -> dict:
    """
    Simulate a single sequential Bayesian A/B experiment.

    Decision logic (mutually exclusive, applied after burn-in):
      SHIP_B       - P(lift > MDE) > prob_threshold  AND  mean_lift > 0
      KEEP_A       - P(lift > MDE) < 0.10  OR  P(B > A) < 0.05
      CONTINUE     - everything else, until max_days
      INCONCLUSIVE - max_days reached without a decision
    """
    cum_apps_a = cum_apps_b = 0
    cum_book_a = cum_book_b = 0

    prob_b_better = prob_meaningful = 0.0
    ci_lower = ci_upper = mean_lift = 0.0

    for day in range(1, max_days + 1):

        cum_book_a += np.random.binomial(daily_apps, true_rate_a)
        cum_book_b += np.random.binomial(daily_apps, true_rate_b)
        cum_apps_a += daily_apps
        cum_apps_b += daily_apps

        alpha_a, beta_a = beta_posterior(cum_book_a, cum_apps_a)
        alpha_b, beta_b = beta_posterior(cum_book_b, cum_apps_b)

        p_a  = np.random.beta(alpha_a, beta_a, mc_samples)
        p_b  = np.random.beta(alpha_b, beta_b, mc_samples)
        lift = p_b - p_a

        prob_b_better   = float(np.mean(p_b > p_a))
        prob_meaningful = float(np.mean(lift > mde))
        mean_lift       = float(np.mean(lift))
        ci_lower        = float(np.percentile(lift, 2.5))
        ci_upper        = float(np.percentile(lift, 97.5))

        burn_in_done = day >= min_days and cum_apps_a >= min_samples

        if not burn_in_done:
            decision = "WAIT"
        elif prob_meaningful > prob_threshold and mean_lift > 0:
            decision = "SHIP_B"
        elif prob_meaningful < 0.10 or prob_b_better < 0.05:
            decision = "KEEP_A"
        else:
            decision = "CONTINUE"

        if decision in ("SHIP_B", "KEEP_A"):
            return _build_result(
                day, decision,
                cum_apps_a, cum_apps_b,
                prob_b_better, prob_meaningful,
                ci_lower, ci_upper, mean_lift,
            )

    return _build_result(
        max_days, "INCONCLUSIVE",
        cum_apps_a, cum_apps_b,
        prob_b_better, prob_meaningful,
        ci_lower, ci_upper, mean_lift,
    )


def _build_result(
    day, decision,
    cum_apps_a, cum_apps_b,
    prob_b_better, prob_meaningful,
    ci_lower, ci_upper, mean_lift,
) -> dict:
    return {
        "decision_day":    day,
        "decision":        decision,
        "cum_apps_a":      cum_apps_a,
        "cum_apps_b":      cum_apps_b,
        "prob_b_better":   prob_b_better,
        "prob_meaningful": prob_meaningful,
        "ci_lower":        ci_lower,
        "ci_upper":        ci_upper,
        "ci_width":        ci_upper - ci_lower,
        "mean_lift":       mean_lift,
    }


def run_simulations(num_simulations: int, **experiment_kwargs) -> list[dict]:
    return [run_experiment(**experiment_kwargs) for _ in range(num_simulations)]