# Predicting Stroke Propensity
 

## Dataset

The dataset for this project can be found on [Kaggle](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset)

## Objectives

The main objective of this project is:

> ** To clean and analyze the dataset and generate a logistic model to predict stroke propensity based on patient demographics.

To achieve this, the objectives are futher broken down into 3 sub-objectives
1. Main Insights: Perform exploratory data analysis of the dataset and report key findings
2. Model Training: Train a Logistic Model and analyze the significance and impact of its coefficients
3. Evaluation: Analyze the residuals and suggest model improvements

## Main Insights

During the exploratory data analysis (EDA), a slight positive correlation between age and stroke was revealed while exploring for multicollinearity. Age was also found to be slightly correlated with other ailments in the dataset, such as hypertension, heart disease, and BMI.

![CR_mat](figures/cor_mat.png)

To further explore the relationship between stroke and age, histograms were utilized to visualize the distributions of the two groups. Additionally, a bar graph was employed to illustrate the counts of each group.

![stroke_hist](figures/stroke_histogram.png)

The histogram analysis indicates a visually distinct difference in the mean age between the two groups, with stroke victims generally exhibiting older ages compared to non-stroke victims. However, the bar graph highlights a limitation in the dataset, particularly the scarcity of observations pertaining to stroke cases. This dataset's imbalance may introduce a significant bias towards predicting the absence of stroke, potentially resulting in elevated false-negative predictions when the model is applied to new and unseen data.

A two-sample t-test was conducted to quantitatively assess the difference in means of age between stroke and non-stroke classes.

$H_0$: There is no difference between these two populations. $\mu_a = \mu_b$

$H_1$: There is a difference between these two populations. $\mu_a \neq \mu_b$

Significance Level $\alpha$ = 0.05

```shell
Stroke Mean Age: 67.73
Non-stroke Mean Age: 41.97
t_statistic: 18.08083426887953
p_value: 7.0307775129939774e-71
Reject the Null Hypothesis, the test is significant (p-value < 0.05)
```

The results of the t-test led to the rejection of the null hypothesis, providing strong evidence that age is a significant determinant of stroke. This implies that age will likely possess a high coefficient when training our logistic regression model.

## Model Training 

A logistic model was trained to predict medical insurance charges using the statsmodels library


|                                |   Coefficient |   Z-Statistic |   P-Value |   P-value < 0.05 |   odds_ratio |    VIF |
|-------------------------------:|--------------:|--------------:|----------:|-----------------:|-------------:|-------:|
|                            age |         0.071 |        13.111 |     0.000 |      Significant |        1.073 |  6.695 |
|                   hypertension |         0.405 |         2.460 |     0.014 |      Significant |        1.499 |  1.205 |
|                  heart_disease |         0.292 |         1.533 |     0.125 |  Not Significant |        1.339 |  1.161 |
|              avg_glucose_level |         0.004 |         3.400 |     0.001 |      Significant |        1.004 |  6.188 |
|                            bmi |        -0.001 |        -0.118 |     0.906 |  Not Significant |        0.999 | 10.439 |
|                    gender_Male |         0.009 |         0.063 |     0.950 |  Not Significant |        1.009 |  1.673 |
|                   gender_Other |        -3.353 |        -0.050 |     0.960 |  Not Significant |        0.035 |  1.002 |
|         work_type_Never_worked |       -16.405 |        -0.001 |     0.999 |  Not Significant |        0.000 |  1.017 |
|              work_type_Private |         0.267 |         1.885 |     0.059 |  Not Significant |        1.306 |  2.526 |
|           Residence_type_Urban |         0.091 |         0.663 |     0.507 |  Not Significant |        1.096 |  1.936 |
| smoking_status_formerly smoked |         0.045 |         0.218 |     0.827 |  Not Significant |        1.046 |  1.858 |
|    smoking_status_never smoked |        -0.155 |        -0.789 |     0.430 |  Not Significant |        0.857 |  2.574 |
|          smoking_status_smokes |         0.147 |         0.635 |     0.525 |  Not Significant |        1.158 |  1.676 |


![model_coeff](figures/log_coeff.png)

