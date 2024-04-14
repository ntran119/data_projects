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

