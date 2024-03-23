# Predicting Medical Insurance Costs
 

## Dataset

The dataset for this project can be found on [Kaggle](https://www.kaggle.com/datasets/teertha/ushealthinsurancedataset)

## Objectives

The main objective of this project is:

> ** To clean and analyze the dataset and generate a linear model to predict insurance costs based on patient demographics.

To achieve this, the objectives are futher broken down into 3 sub-objectives
1. Perform exploratory data analysis of the dataset 
2. Train a Linear Model
3. Evaluate/improve the Model

## Main Insights

From the exploratory data analysis, we found some interesting insights.

* While exploring for multi-colinear variables, our correlation matrix reveals that being a smoker is highly correlated with increased insurance charges:

![CR_mat](figures/cor_mat.png)


* There are other interesting associations in the matrix such as BMI being positively associated with a southeast region and insurance charges being positively correlated with BMI and age. To further explore the effect of smoking on insurance charges we visualized the difference between smoking and non-smoker on a histogram

![smoking_hist](figures/smoker_histogram.png)

* 