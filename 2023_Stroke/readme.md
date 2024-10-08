# Predicting Stroke Propensity
 

## Dataset

The dataset for this project can be found on [Kaggle](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset)

## Objectives

The main objective of this project is:

> ** To clean and analyze the dataset and generate a logistic model to predict stroke propensity based on patient demographics.

To achieve this, the objectives are futher broken down into 3 sub-objectives
1. Main Insights: Perform exploratory data analysis of the dataset and report key findings
2. Model Training: Train a Logistic Model and analyze the significance and impact of its coefficients
3. Evaluation: Analyze the accuracy and suggest model improvements

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

The results of the t-test led to the rejection of the null hypothesis, providing strong evidence that age is a significant determinant of stroke.

## Model Training 

A logistic model was trained to predict medical insurance charges using the statsmodels library


```shell
                                Coefficient  Z-Statistic       P-Value   P-value < 0.05  odds_ratio        VIF
age                                0.070759    13.111353  2.834943e-39      Significant       1.073   6.694922
hypertension                       0.404587     2.460286  1.388262e-02      Significant       1.499   1.205089
heart_disease                      0.292121     1.533414  1.251740e-01  Not Significant       1.339   1.161208
avg_glucose_level                  0.004061     3.399995  6.738713e-04      Significant       1.004   6.188126
bmi                               -0.001324    -0.117977  9.060857e-01  Not Significant       0.999  10.439046
gender_Male                        0.008921     0.063058  9.497203e-01  Not Significant       1.009   1.672654
gender_Other                      -3.353043    -0.050460  9.597559e-01  Not Significant       0.035   1.002318
work_type_Never_worked           -16.405281    -0.000924  9.992627e-01  Not Significant       0.000   1.017193
work_type_Private                  0.267173     1.884524  5.949407e-02  Not Significant       1.306   2.526406
Residence_type_Urban               0.091492     0.663227  5.071854e-01  Not Significant       1.096   1.935815
smoking_status_formerly smoked     0.045085     0.218489  8.270478e-01  Not Significant       1.046   1.858002
smoking_status_never smoked       -0.154715    -0.788922  4.301574e-01  Not Significant       0.857   2.574499
smoking_status_smokes              0.146531     0.634982  5.254398e-01  Not Significant       1.158   1.675731
```


![model_coeff](figures/odds_ratio_and_vif.png)

Analysis of the logistic regression model coefficients reveals that age, hypertension, and average glucose level are significant factors in determining the likelihood of stroke.

The odds ratio of hypertension is highest at 1.5, indicating that if a patient has hypertension, their odds of experiencing a stroke increase by approximately 1.5 times. Furthermore, the odds ratio of 1.5 suggests a moderate positive association between hypertension and stroke. Additionally, it possesses a VIF factor of 1.2, indicating no multicollinearity with other predictor variables.

Conversely, age and average glucose level exhibit VIF values greater than 6, suggesting a high association with other predictors. Therefore, it is advisable to consider dropping these variables to optimize the model, along with other insignificant features.

## Evaluation

```shell
 Overall Model Accuracy: 95.15
 ```
![model_acc](figures/accuracy_and_confusion_matrix_subplots.png)

The overall model accuracy is calculated to be 95.15%, indicating a remarkably high level of accuracy and suggesting strong performance of the model. However, when investigating the model accuracy across different thresholds, it becomes evident that the model achieves exceptionally high accuracy, surpassing 80%, even with a low threshold set at 0.1. This observation underscores the impact of class imbalance within the dataset, as there are relatively few observations of patients with stroke compared to those without. This notion is further supported by the confusion matrix, which reveals that the model predominantly predicts observations as non-stroke, yet still attains a 95% accuracy rate.

It might be best to explore the utilization of resampling techniques, such as oversampling the stroke class, to mitigate the impact of class imbalance on model evaluation. This approach aims to address the disparity in class frequencies by artificially increasing the representation of the minority class, thereby potentially improving the model's ability to accurately predict stroke occurrences.