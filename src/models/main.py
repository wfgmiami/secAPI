import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("../data/big_mart_Train.csv")
data.sample(5)

# check for null and duplicate values
data.isnull().sum() / len(data) * 100
# Item_Weight and Outlet_Size have null values
data.duplicated().any()

# Univariate Imputation
mean_weight = data["Item_Weight"].mean()
median_weight = data["Item_Weight"].median()

data["Item_Weight_mean"] = data["Item_Weight"].fillna(mean_weight)
data["Item_Weight_median"] = data["Item_Weight"].fillna(median_weight)

print("Original item weight variance: ", data["Item_Weight"].var())
print("Mean imputation item weight variance: ", data["Item_Weight_mean"].var())
print("Median imputation item weight variance: ", data["Item_Weight_median"].var())

data["Item_Weight_interpolate"] = data["Item_Weight"].interpolate(method="linear")

data["Item_Weight"].plot(kind="kde", label="original")
data["Item_Weight_mean"].plot(kind="kde", label="mean")
data["Item_Weight_median"].plot(kind="kde", label="median")
data["Item_Weight_interpolate"].plot(kind="kde", label="interpolate")
plt.legend()
plt.show()

data[
    ["Item_Weight", "Item_Weight_mean", "Item_Weight_median", "Item_Weight_interpolate"]
].boxplot()

# Multivariate imputation
from sklearn.impute import KNNImputer

knn = KNNImputer(n_neighbors=10, weights="distance")
data["knn_imputer"] = knn.fit_transform(data[["Item_Weight"]]).ravel()

data["Item_Weight"].plot(kind="kde", label="Original")
data["knn_imputer"].plot(kind="kde", label="KNN imputer")

data = data.drop(
    ["Item_Weight", "Item_Weight_mean", "Item_Weight_median", "knn_imputer"], axis=1
)

data.isnull().sum()

# impute missing values for Outlet_Size
data["Outlet_Size"].unique()
data["Outlet_Size"].value_counts()

data["Outlet_Type"].value_counts()

mode_outlet = data.pivot_table(
    values="Outlet_Size", columns="Outlet_Type", aggfunc=(lambda x: x.mode()[0])
)
missing_values = data["Outlet_Size"].isnull()
data.loc[missing_values, "Outlet_Size"] = data.loc[missing_values, "Outlet_Type"].apply(
    lambda x: mode_outlet[x]
)
data.isnull().sum()

# Item_Fat_Content
data["Item_Fat_Content"].value_counts()
data.replace(
    {"Item_Fat_Content": {"Low Fat": "LF", "low fat": "LF", "reg": "Regular"}},
    inplace=True,
)

# Item_Visibility
data["Item_Visibility"].value_counts()
data["Item_Visibility_interpolate"] = (
    data["Item_Visibility"].replace(0, np.nan).interpolate(method="linear")
)

data = data.drop("Item_Visibility", axis=1)

# Item_Identifier
data["Item_Identifier"].value_counts()
data["Item_Identifier"] = data["Item_Identifier"].apply(lambda x: x[:2])

# Outlet_Establishment_Year
import datetime as dt

data["Outlet_Establishment_Year"]

current_year = dt.datetime.today().year
data["Outlet_age"] = current_year - data["Outlet_Establishment_Year"]

data = data.drop("Outlet_Establishment_Year", axis=1)

# Handling Categorical Columns
from sklearn.preprocessing import OrdinalEncoder

data_encoded = data.copy()
cat_cols = data.select_dtypes(include=["object"]).columns

for col in cat_cols:
    oe = OrdinalEncoder()
    data_encoded[col] = oe.fit_transform(data_encoded[[col]])
    print(oe.categories_)

X = data_encoded.drop("Item_Outlet_Sales", axis=1)
y = data_encoded["Item_Outlet_Sales"]

# Random Forest Regressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

rf = RandomForestRegressor(n_estimators=100, random_state=42)
# n_estimators=number of trees used to build the model
scores = cross_val_score(rf, X, y, cv=5, scoring="r2")
# cv=cross-validation fold, split the data into 5 sets, train the model on 4 sets,
# and evaluate it on 1 set
# r2=coefficient of determination, measure the proportion of variance in the target variable (ie sales)
# that is explained by the model's predictions R^2=SSR/SST=Sum of Sq Err/Sum of Sq Total
print(scores.mean())

# XGBRFRegressor
from xgboost import XGBRFRegressor

xg = XGBRFRegressor(n_estimators=100, random_state=42)
# scores0 = cross_val_score(xg,X.drop(['Item_Visibility_interpolate','Item_Weight_interpolate',
# 'Item_Type','Outlet_Location_Type','Item_Identifier','Item_Fat_Content'],axis=1),y,cv=5,scoring='r2')
# print(scores.mean())

xg1 = xg.fit(X, y)
pd.DataFrame(
    {"features": X.columns, "XGBRF_importance": xg1.feature_importances_}
).sort_values(by="XGBRF_importance", ascending=False)

scores = cross_val_score(
    xg1,
    X.drop(
        [
            "Item_Visibility_interpolate",
            "Item_Weight_interpolate",
            "Item_Type",
            "Outlet_Location_Type",
            "Item_Identifier",
            "Item_Fat_Content",
        ],
        axis=1,
    ),
    y,
    cv=5,
    scoring="r2",
)
print(scores.mean())

final_data = X.drop(
    [
        "Item_Visibility_interpolate",
        "Item_Weight_interpolate",
        "Item_Type",
        "Outlet_Location_Type",
        "Item_Identifier",
        "Item_Fat_Content",
    ],
    axis=1,
)

xg_final = XGBRFRegressor()
xg_final.fit(final_data, y)  # training with all the data

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

X_train, X_test, y_train, y_test = train_test_split(
    final_data, y, test_size=0.2, random_state=42
)

xg_final.fit(X_train, y_train)  # training with split train/test data
y_predict = xg_final.predict(X_test)
m_abs_err = mean_absolute_error(y_test, y_predict)  # 713.5792

xg_final2 = XGBRFRegressor()
# xg_final2.fit(final_data, y) # skip training on all the data
X_train, X_test, y_train, y_test = train_test_split(
    final_data, y, train_size=0.20, random_state=42
)

xg_final2.fit(X_train, y_train)
y_predict = xg_final2.predict(X_test)
mean_absolute_error(
    y_test, y_predict
)  # 759.0442 - higher compared to when fit on all the data

# Prediction on unseen data
# Item_MRP, Outlet_Identifier, Outlet_Size, Outlet_type, Outlet_age
pred = xg_final.predict(np.array([[141.6180, 9.0, 1.0, 1.0, 24]]))[0]
print(f"Sales volume is between {pred-m_abs_err} and {pred+m_abs_err}")

# Save Model Using Joblib

import joblib

joblib.dump(xg_final, "bigmart_model")

model = joblib.load("bigmart_model")
pred = model.predict(np.array([[141.6180, 9.0, 1.0, 1.0, 24]]))[0]
print(pred)
print(f"Sales volume is between {pred-m_abs_err} and {pred+m_abs_err}")
