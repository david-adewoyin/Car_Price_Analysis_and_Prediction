# Car Price Estimator: Project Overview

  - Created a tool that estimates car prices (MAE ~ ₦ 1.8M) to help sellers and buyers know what to pay for and sell.
  - Scraped over 2,000 car descriptions from [cars45](https://www.cars45.com/) and [autochek.africa](https://autochek.africa/ng/cars-for-sale) using Python and Playwright.
  - Performed exploratory data analysis to gather insights on car prices, trends, and popularity in the region.
  - Optimized Ridge, Decision Tree, and Random Forest Regressors using GridsearchCV to reach the best model.
  - Created external [Tableau dashboard](https://public.tableau.com/views/CarPriceDeterminantDashboard/Dashboard1?:language=en-US&:display_count=n&:origin=viz_share_link) for visualization.
  - Built a client facing web application using Flask.


 ## Data Cleaning
Because the data was scraped from multiple sources, extensive data cleaning and preparation was required, which includes the following:

 - Removed brackets and commas from all features that used them.
 - Price numeric data was parsed.
 - Colors were standardized, and multiple colors were renamed to be one.
 - Brand and Model were parsed, formatted, and standardized to be the same across all sources.
 - Several outliers were removed, and engine capacity was standardized at milliliters. e.t.c
  
## EDA 

For the Exploratory Analysis, various factors and trends affecting car prices in the region were investigated, as well as questions such as the popularity of brands and models. 


<div style='display:flex;'>
<img src="https://user-images.githubusercontent.com/57121852/213569749-1485cf09-d250-4dcc-8eff-6ede1418aa4b.png">
<img src="https://user-images.githubusercontent.com/57121852/213570571-0afc261a-d7d1-4184-92fe-4366a37aa98c.png" >
</div>

### Tableau Dashboard
<img src="https://user-images.githubusercontent.com/57121852/213936600-c760ea7f-321c-4254-a88d-1ecc208e90e5.png" >

##  Model Building
  Firstly, due to the sheer numbers of car models and brands present, **target mean encoding** was used to encode them, while for the remaining categorical features, ordinal and one hot encoding was used as required.  
  Three different models were created and evaluated using Mean Absolute Error.

## Model Performance

The Random Forest model far outperformed the other approaches on the test and validation sets.

Random Forest : MAE = 1.8M  
Decision Tree: MAE =  2.0M  
Ridge Regression: MAE = 2.2M  
  
 ## Productionalization
This step involved creating a Flask web application and API that was hosted on a local webserver. Users can enter and submit information about the vehicle they want to estimate, and the application will return the estimated price.


![image](https://user-images.githubusercontent.com/57121852/213565832-915b6d87-0084-4135-864d-546e8035691c.png)
