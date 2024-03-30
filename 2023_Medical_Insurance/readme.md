# Predicting Medical Insurance Costs
 

## Dataset

The dataset for this project can be found on [Kaggle](https://www.kaggle.com/datasets/teertha/ushealthinsurancedataset)

## Objectives

The main objective of this project is:

> ** To clean and analyze the dataset and generate a linear model to predict insurance costs based on patient demographics.

To achieve this, the objectives are futher broken down into 3 sub-objectives
1. Main Insights: Perform exploratory data analysis of the dataset and report key findings
2. Model Training: Train a Linear Model and analyze the significance and impact of its coefficients
3. Evaluation: Analyze the residuals and suggest model improvements

## Main Insights

During the exploratory data analysis, several noteworthy insights were uncovered. While examining for multicollinearity among variables, a strong positive correlation between smoking status and increased insurance charges was revealed in the correlation matrix. This indicates that individuals who smoke tend to have higher medical insurance costs compared to non-smokers.

![CR_mat](figures/cor_mat.png)


Additionally, other interesting associations were observed in the correlation matrix. For instance, a positive correlation was found between BMI and living in the southeast region, as well as between insurance charges, BMI, and age. These associations provide valuable insights into potential relationships between different variables in the dataset.

![smoking_hist](figures/smoker_histogram.png)

To further investigate the impact of smoking on insurance charges, the difference between smokers and non-smokers was visualized using a histogram. The distributions of insurance charges for smokers and non-smokers exhibited distinct patterns, with smokers displaying higher insurance costs with higher variability. Furthermore, the means of both distributions were notably different, indicating a significant disparity in insurance charges between the two groups. This visual evidence strongly suggests that smoking status is a significant factor contributing to increased medical insurance costs.

A two-sample t-test (two-tailed) comparing the means of insurance costs between smokers and non-smokers was conducted to quantitatively assess the difference

$H_0$: There is no difference between these two populations. $\mu_a = \mu_b$

$H_1$: There is a difference between these two populations. $\mu_a \neq \mu_b$

Significance Level $\alpha$ = 0.05

```shell
Smoker Insurance Mean: 32050.23
Non-Smoker Insurance Mean: 8440.66
t_statistic: 46.64479459840305
p_value: 1.4067220949376498e-282
Reject the Null Hypothesis, the test is significant (p-value < 0.05)
```

The results of the test led to the rejection of the null hypothesis, providing strong evidence that smoking status is indeed a significant determinant of insurance charges. Consequently, it is anticipated that smoking will have a high linear coefficient in the regression model, reflecting its substantial impact on insurance costs.


## Model Training 

A linear model was trained to predict medical insurance charges using the statsmodels library. 

```shell
             Coefficient  T-Statistic       P-Value   P-value < 0.05
age           256.764611    21.554732  1.324461e-88      Significant
bmi           339.250364    11.857229  6.721670e-31      Significant
children      474.820486     3.443299  5.925434e-04      Significant
male         -129.481478    -0.388606  6.976303e-01  Not Significant
smoker_yes  23847.328844    57.693117  0.000000e+00      Significant
northeast     960.081385     2.008093  4.483556e-02      Significant
northwest     610.854854     1.278587  2.012658e-01  Not Significant
southeast     -75.184216    -0.159691  8.731486e-01  Not Significant

R-Squared = 0.751

```

![model_coeff](figures/linear_coeff.png)

A linear regression model was trained to predict medical insurance charges using the statsmodels library. Based on the constructed model, an R-squared value of 0.751 was obtained, indicating that approximately 75% of the variability in medical insurance charges in the dataset can be explained by the predictors included in the model. This suggests that the model provides a reasonably good fit to the data.

One of the key predictors that emerged from the analysis is smoking status, which was found to have a high coefficient in the model and a statistically significant associated p-value. This suggests that smoking status is a strong predictor of higher insurance charges, even after accounting for other factors included in the model.

On the other hand, factors such as gender (male) and geographical region (specifically living in the northwest or southeast regions) were found to be non-significant based on their p-values. This implies that these variables do not have a statistically significant impact on insurance charges in the model. Therefore, consideration may be given to dropping these variables from the model to optimize its predictive performance further.

## Evaluation


![model_resids](figures/residual_plots.png)

Upon examining the histogram of model residuals, it was observed that the distribution appears to have a right skew, indicating that the residuals are not perfectly normally distributed and may contain outliers or systematic deviations from the model's predictions. Additionally, deviations from the straight line pattern were noticed in the probability plot, particularly in the tails of the distribution, suggesting that the distribution of residuals may have heavier tails than a normal distribution.

Furthermore, the homoscedasticity plot revealed a pattern where the variance of the residuals spreads out more as the values of the predictor variable (X) increase. This phenomenon suggests that the model's predictions become less reliable for higher insurance costs, indicating a potential limitation in predictive accuracy for higher insurance charges.

