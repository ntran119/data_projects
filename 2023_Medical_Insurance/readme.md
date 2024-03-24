# Predicting Medical Insurance Costs
 

## Dataset

The dataset for this project can be found on [Kaggle](https://www.kaggle.com/datasets/teertha/ushealthinsurancedataset)

## Objectives

The main objective of this project is:

> ** To clean and analyze the dataset and generate a linear model to predict insurance costs based on patient demographics.

To achieve this, the objectives are futher broken down into 3 sub-objectives
1. Main Insights: Perform exploratory data analysis of the dataset and report key findings
2. Model Training: Train a Linear Model and analyze the significance and impact of its coefficients
3. Evaluate/Improve the Model

## Main Insights

From the exploratory data analysis, we found some interesting insights.

While exploring for multi-colinear variables, our correlation matrix reveals that being a smoker is highly correlated with increased insurance charges:

![CR_mat](figures/cor_mat.png)


There are other interesting associations in the matrix such as BMI being positively associated with a southeast region and insurance charges being positively correlated with BMI and age. To further explore the effect of smoking on insurance charges we visualized the difference between smoking and non-smoker on a histogram

![smoking_hist](figures/smoker_histogram.png)

The associated insurance charges for Smokers has a higher variability overall (the insurance changes are more spread). The distributions of the two categories is visually distinct. There is only a small overlap of values and the means of both distributions are quite far apart. This is good indication that being a smoker has a significant likely-hood of increasing medical insurance costs. 

We ran a two-sample t-test (2 tail) to compare the medical insurance costs of these two populations.

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

From the results of the test, we reject the Null Hypothesis. Smoking is a significant factor in determining insurance charges. This indicates that it will have a high linear coefficient in our model.


## Model Training 

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