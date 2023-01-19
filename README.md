# Car Price Estimator: Project Overview

  - Create a tool that estimates car prices (MAE ~ ₦ 1.8M) to help sellers and buyers knows what to pay for and sell.
  - Scraped over 2000 cars decriptions from [cars45](https://www.cars45.com/) and [autochek.africa](https://autochek.africa/ng/cars-for-sale) using python and playwright.
  - Performed exploratory data analysis to gather insights on car prices, trends and popularity in the region.
  - Optimized Ridge, Decision Tree and Random Forest Regressors using GridsearchCV to reach the best model.
  - Built a client facing API and webpage using flask.
  
 ## Data Cleaning
 Due to the nature of scraping data from multiple sources, extensive data cleaning and preparation were done with a few such as:
 
 - Removed brackets,commas from all features containing them.
 - Parsed numeric data from prices.
 - Standardized the color feature and rename mulitple colors to be one.
 - Parsed, formatted and standardized Brand and Model to be the same across the sources.
 - Removed various outliers and standardized engine capacity to be milliliters. e.t.c
  
## EDA 
For the Exploratory Analysis, various factors and trends affecting car prices in the region were investigated, as well as questions such as the popularity of brands and models. ?  

![image](https://user-images.githubusercontent.com/57121852/213570571-0afc261a-d7d1-4184-92fe-4366a37aa98c.png)


![image](https://user-images.githubusercontent.com/57121852/213569749-1485cf09-d250-4dcc-8eff-6ede1418aa4b.png)

##  Model Building
  First due to the sheer numbers of models and brands present, **target mean encoding** was used to encode them, while for the remaining categorical features, ordinal and one hot encoding was used as suilted.  
  Three different models were created and evaluated using Mean Absolute Error.

## Model Performance

The Random Forest model far outperformed the other approaches on the test and validation sets.

Random Forest : MAE = 1.8M  
Decision Tree: MAE =  2.0M  
Ridge Regression: MAE = 2.2M  
  
 ## Productionalization
This step involved creating a Flask website and API that was hosted on a local webserver. Users can enter and submit information about the vehicle they want to estimate, and the website will return the estimated price.


![image](https://user-images.githubusercontent.com/57121852/213565832-915b6d87-0084-4135-864d-546e8035691c.png)
