# SeabornGroup_JC_DS_12_FinalProject
Team Members :
1. Albert Aldo - 12albertaldo@gmail.com | [LinkedIn](https://www.linkedin.com/in/albertaldo/) | [GitHub](https://github.com/AlbertAldo)
2. Elvin Fatkhunnuha - fatkhuelvin@gmail.com | [LinkedIn](https://www.linkedin.com/in/elvin-fatkhunnuha/) | [GitHub](https://github.com/elvinfatkhu)
3. Mingnarto Lie - mingnarto.lie@gmail.com | [LinkedIn](https://www.linkedin.com/in/mingnarto-lie-a8b77877/) | [GitHub](https://github.com/Mingnarto)

# House Developer Optimizer With Machine Learning

Philadelphia, is a city in the state of Pennsylvania in the United States. It is the sixth-most populous city in the United States and the most populous city in the state of Pennsylvania, with a 2019 estimated population of 1,584,064 With largest population in Pennysylvania real-estate  business is a promising business to provide decent housing to its residents. [Source](https://en.wikipedia.org/wiki/Philadelphia)

As a housing company that wants to spread its wings in Philadelphia, data is a crucial factor in helping us to decide which secondhand property to purchase. To create benchmark in purchasing properties with the best price. What if there was a simple way to predict the house price complete with the house specifications with the best price?

After the property company gets the desired houses, in the selling stage, customers segmentation will be needed to ease the company doing marketing (Marketing Automation) in order to match the target customers. Isn't it easier if we can do marketing that match with the target customers?

In this report, We'll discuss the decisions, we made and show revelant code blocks that describe our modeling process.

# Workflow Project
![Workflow](https://i.imgur.com/mT6ivur.png)

# 1. Data Cleaning

We collected data from [Kaggle](https://www.kaggle.com/adebayo/philadelphia-buildings-database) and shift our focus to residential type. We study the data columns based on [Metadata Philly Government](https://metadata.phila.gov/#home/datasetdetails/5543865f20583086178c4ee5/representationdetails/55d624fdad35c7e854cb21a4/?view_287_per_page=100&view_287_page=1).

For data that has no description found in  [Metadata Philly Government](https://metadata.phila.gov/#home/datasetdetails/5543865f20583086178c4ee5/representationdetails/55d624fdad35c7e854cb21a4/?view_287_per_page=100&view_287_page=1), we decided to drop those columns based on our analytics. We decided to handle the missing values we found. Using not applicable as substitute in several missing values we found in basements, central air, exterior condition, garage type, interior condition, type heater, and view type. The same goes with missing values in parcel shape and topography. The only differentiation is we decided to use mode as the substitute for them. We decided to do this because we want to keep our data integrity intact. The same goes for outliers. [Cleaning Data - GitHub](https://github.com/PurwadhikaDev/SeabornGroup_JC_DS_12_FinalProject/blob/main/1%20-%20Cleaning%20Data.ipynb) 

# 2. Pre-Processing

We did Pre-Processing with cleaned and ready to analyze data. Then we created the House Segment Clustering based on the Market Value, Total Area, Total Livable Area and Zone of those properties by making 5 clusters using KMeans Model. [Data Processing - GitHub](https://github.com/PurwadhikaDev/SeabornGroup_JC_DS_12_FinalProject/blob/main/2%20-%20Data%20Processing.ipynb) 

Those Clusters are:
- Segment Low
- Segment Lower Middle
- Segment Middle
- Segment Upper Middle
- Segment Top

We also do Exploratory Data Analysis Regression (Market Value) & Classification (Segmentation), for full further details please refers to :
- [Exploratory Data Analysis Regression (Market Value) - GitHub](https://github.com/PurwadhikaDev/SeabornGroup_JC_DS_12_FinalProject/blob/main/3%20-%20EDA%20-%20Regression.ipynb)
- [Exploratory Data Analysis Classification (Segmentation) - GitHub](https://github.com/PurwadhikaDev/SeabornGroup_JC_DS_12_FinalProject/blob/main/4%20-%20EDA%20-%20Classification.ipynb)

# 3. Modelling & Feature Engineering

Before we enter the modeling stage, we used Pipeline in order to process Categorical Data by using OneHotEncoder and RobustScaler for Numerical Data.

```
- Regression Machine Learning :
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', RobustScaler())
])

categoric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

_________________________________________________

- Classification Machine Learning :
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean'))
])

categoric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder())
])
```

<hr>

## - Regression

The regression problem was to predict the price of the house based on its specification. [ML Regression - GitHub](https://github.com/PurwadhikaDev/SeabornGroup_JC_DS_12_FinalProject/blob/main/5%20-%20ML%20Regression.ipynb) 

We did several Algorithms such as :
- LinearRegression, Ridge, Lasso, ElasticNet, KNN, SVM, DecisionTreeRegressor, RandomForestRegressor as a Base Model.
- KNN, DecisionTreeRegressor with Hyper Parameter Tuning.
- DecisionTreeRegressor with Fine Tuning.

**DecisionTreeRegressor with Fine Tuning** is the best algorithm that we found, as follows :

```
max_depth = None, max_features = 0.9, min_samples_leaf = 25, min_samples_split = 24, random_state = 42
```

Which resulted in the following scores :

Data  | R2 | MAE | MSE | RMSE
-----|------|------|------|-----|
Training DecisionTreeClassifier Tuned | 0.818   |20350.7 | 2.477e+09 | 49776.09
Test DecisionTreeClassifier Tuned | 0.774   | 22407.63 | 3.019e+09 | 54951.45

<hr>

## - Classification

Classification problem is the target of Customer Marketing Segment to fit with our target customer. [ML Classification - GitHub](https://github.com/PurwadhikaDev/SeabornGroup_JC_DS_12_FinalProject/blob/main/6%20-%20ML%20Classification.ipynb) 

We did several Algorithms such as :
- LogisticRegression, KNN, SVM, DecisionTreeClassifier, RandomForestClassifier as a Base Model.
- LogisticRegression, KNN, DecisionTreeClassifier with Hyper Parameter Tuning.
- DecisionTreeClassifier, RandomForestClassifier with Fine Tuning.

Because the data of each segment is unbalanced, we decided to use random oversampling to equalize the number of data in each segment.

And we tried several Algorithms with Random Over Sampling Data for Minority Class such as :
- LogisticRegression, KNN, SVM, DecisionTreeClassifier, RandomForestClassifier as a Base Model.
- DecisionTreeClassifier, RandomForestClassifier with Fine Tuning.

Based on Random Over Sampling Data for Minority Class, we choose **RandomForestClassifier with Fine Tuning** for the best algorithm that we found, as follows :

```
max_depth = 6, max_features = 0.15, min_samples_leaf = 10, min_samples_split = 5, random_state=42
```

Which resulted in the following scores :

Data  | Accuracy | F1-Score (Macro Avg) | F1-Score (Weighted) |
-----|------|------|------|
Training RandomForestClassifier Tuned | 0.957   |0.92 | 0.961 |
Test RandomForestClassifier Tuned | 0.96   | 0.92 | 0.963 |

# 4. Application

## - Regression Model

When a company buys houses in Philadelphia, this model might become one of the alternatives or choice in determine the house price. Having a benchmark when negotiate with the owners, isn't that fun?

The following picture demonstrates how our Regression Model application flows :

![RegressionModel](https://i.imgur.com/6KoKGWB.png)

Other than predicting, our Model also able to recommend based on similar specifications for example :

![RecommendationSystem](https://i.imgur.com/iporPZP.png)

Please refer to : [Recommendation System - GitHub](https://github.com/PurwadhikaDev/SeabornGroup_JC_DS_12_FinalProject/blob/main/7%20-%20Recommendation%20System.ipynb)

<hr>

## - Classification Model

After the property company gets the desired houses, in the selling stage, customers segmentation will be needed to ease the company doing marketing **(Marketing Automation)** in order to match the target customers. Seems interesting right?

The following picture demonstrates how our Classification Model application flows :

![ClassificationModel](https://i.imgur.com/MXFf8B6.png)

# 5. Conclusion

## - Regression
With this Model, we will be able to help the company to have benchmarks when purchasing houses, which is why this Model may become one of the alternatives for company that wants to spread its wings

But on the other hand, there are some weaknesses that can be found in this Model. Error differences based on Mean Absolute Error is ± $22407.63 with R2 score 0.774, which means several errors may occured within our Regression Model. Our Model also weak in predicting old houses (Building Description: STONE, Year Built < 1950) and houses from MASONRY that located in Central City where our Model predicted low price while the actuality is quite high. Therefore people with expertise in this area will be better in recommending.

<hr>

## - Classification
This Model can help the company in deciding customers segmentation for Marketing Automation. It will be more effective if we know exactly which type of house is more suitable for which customers segment so the company able to maximize their marketing strategies. For example, customers from lower Middle Cluster is not a suitable target if we try to sell them properties from Top Cluster and vice-versa as it will be most inefficient.

This Model also have a high Accuracy Score of 0.96 and through additional Data from Random Over Sampling of the Minority Class. It leads to a better performance in predicting the Minority Class.

# 6. Project Recommendation

## - Regression
- Based on the price of each section, the cheapest can be found in the North & North East. We can buy and redeveloped them on behalf of the North Philadelphia developer, to be sold on the latter-day with higher price.
- If the company prefer to build their properties from scratch, it would be better for them to purchase houses that already in poor condition and therefore below market price.
- When the company decided to buy old houses / houses that are in poor condition, it is of utmost importance to consider the budget in which will be needed to renovate them to prevent the final spending exceeding the main capital.

<hr>

## - Classification
- Even with the same performance from the sales across the segment, the fifth segment managed to get higher profit-margin up to 22.73% and so it is recommended to prioritize this segment as they can give us higher profit and at the same time creates efficiency in sales department.
- It will be more effective if we know exactly which type of house is more suitable for which customers segment so the company able to maximize their marketing strategies. For example, customers from lower Middle Cluster is not a suitable target if we try to sell them properties from Top Cluster and vice-versa as it will be most inefficient.
- We can try to give some promotions such as 0% dp. This will help our marketing side in selling houses to middle-low segment customers so that they become more interested in buying from us and at the same time emptied our stock of houses.

# 7. Dashboard

We create a Dashboard for Deployment our Model. Please refer to [Dashboard - GitHub](https://github.com/PurwadhikaDev/SeabornGroup_JC_DS_12_FinalProject/tree/main/Dashboard)

- ### **Home**
    ![Home](https://i.imgur.com/BPjh4wW.png)

- ### **Project**
    ![Project](https://i.imgur.com/UaNp1kS.png)

- ### **Dataset**
    ![Dataset](https://i.imgur.com/IM4py3v.png)

- ### **Visualization**
    ![Visualization](https://i.imgur.com/thOf8iV.png)

- ### **Market Value Prediction**
    ![MarketValuePrediction](https://i.imgur.com/qzBa72j.png)

    ![MarketValueResult](https://i.imgur.com/j8yQ8fb.png)

    ### **Recommendation System**
    ![RecommendationSystem](https://i.imgur.com/Sr7sxas.png)

- ### **Segmentation Prediction**
    ![SegmentationPrediction](https://i.imgur.com/yZSuICd.png)

    ![SegmentationResult](https://i.imgur.com/sTodI5A.png)

<hr>

**Thanks for reading our project! We hope our project useful and inspiring.**
