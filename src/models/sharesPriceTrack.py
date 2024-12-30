import requests
import pandas as pd
import numpy as np
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date, timedelta, datetime
import holidays
from dateutil.relativedelta import relativedelta
import json

current_year = date.today().year
year_5yr_ago = current_year - 5
us_holidays = holidays.UnitedStates(years=[year_5yr_ago, current_year])


def adjust_to_prev_business_day(target_date, holiday_list):
    while (
        target_date.weekday() in (5, 6) or target_date in holiday_list
    ):  # 5 = Saturday, 6 = Sunday
        target_date -= timedelta(days=1)  # Move backword by one day
    return target_date


def adjust_to_next_business_day(target_date, holiday_list):
    while (
        target_date.weekday() in (5, 6) or target_date in holiday_list
    ):  # 5 = Saturday, 6 = Sunday
        target_date += timedelta(days=1)  # Move forward by one day
    return target_date


with open("../data/tickers.json", "r") as file:
    tickers_object = json.load(file)

tickers = tickers_object["S&P500"][:41]
# S&P500
# Watch
# Robinhood
# Best2016
# ChatGPT_122224_20_30_toBeDiversified

# companyFacts.headers.get("Content-Type") not "application/json":
# first 20 in S&P500 were good except AMD, AES
# tickers = [
#     "MMM",
#     "ADBE",
#     "AMD",
#     "AES",
# ]

# 1. Plot the stocks with downward share count
headers = {"User-Agent": "alpenchev@yahoo.com"}
companyTickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json", headers=headers
)
companyData = pd.DataFrame.from_dict(companyTickers.json(), orient="index")
companyData["cik_str"] = companyData["cik_str"].astype(str).str.zfill(10)

# shareType = "CommonStockSharesOutstanding"
shareType = "WeightedAverageNumberOfSharesOutstandingBasic"

numQters = 16  # last 4 years
sh_decreased_tickers = {}
sharesByQtrs = pd.DataFrame()
dfs = []
no_data_tickers = []
# ticker = "ICE"

for ticker in tickers:
    # print(f"{ticker}")

    filtered_data = companyData[companyData["ticker"] == f"{ticker}"]

    if not filtered_data.empty and "cik_str" in filtered_data.columns:
        cik = companyData[companyData["ticker"] == f"{ticker}"]["cik_str"].iloc[0]

        companyConcept = requests.get(
            (
                f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}"
                f"/us-gaap/{shareType}.json"
            ),
            headers=headers,
        )

        if companyConcept.headers.get("Content-Type") == "application/json":
            sharesData = pd.DataFrame.from_dict(
                (companyConcept.json()["units"]["shares"])
            )

            sharesFilings = sharesData[
                (
                    ((sharesData["form"] == "10-Q") & (sharesData["frame"].notna()))
                    | (sharesData["form"] == "10-K")
                )
            ]

            sharesFilings = (
                sharesFilings.groupby(["start", "end", "val"], sort=False)
                .first()
                .reset_index()[["start", "end", "val", "fy", "form", "frame"]]
            )

            sharesFilings["fy"] = sharesFilings.apply(
                lambda row: (
                    str(row["fy"])[2:]
                    + "Q4"  # If 'frame' is None, update 'fy' using part of 'fy'
                    if pd.isna(row["frame"])
                    else (
                        row["frame"][4:]
                        + "Q4"  # If 'frame' length is 6, take substring and add "Q4"
                        if len(row["frame"]) == 6
                        else (
                            row["frame"][
                                4:-1
                            ]  # If 'shareType' matches the variable, remove last character
                            if shareType == "CommonStockSharesOutstanding"
                            else row["frame"][
                                4:
                            ]  # Otherwise, take substring from index 4 onwards
                        )
                    )
                ),
                axis=1,
            )

            commShOut = sharesFilings.loc[:, ["fy", "val"]]

            commShOutQtrs = commShOut.tail(numQters)
            is_empty = commShOutQtrs.empty
            if not is_empty:
                temp = commShOutQtrs.rename(columns={"val": f"{ticker}"})
                dfs.append(temp)
            else:
                no_data_tickers.append(ticker)

        else:
            print(
                f'{ticker} companyFacts.headers.get("Content-Type") not "application/json"'
            )
    else:
        print(f'{ticker} companyData[companyData["ticker"] does not exist')

dfs_standardized = []
for df in dfs:
    numeric_cols = df.select_dtypes(include=["number"])
    df_standardized = (numeric_cols - numeric_cols.mean()) / numeric_cols.std()
    df_standardized = pd.concat([df_standardized, df["fy"]], axis=1)
    df_standardized.set_index("fy", inplace=True)
    dfs_standardized.append(df_standardized)


def calculate_trend_line(dataframes):
    slopes_all = {}
    trend_results = []

    for idx, df in enumerate(dataframes):
        time = np.arange(len(df)).reshape(-1, 1)  # Sequential time index

        slopes = {}

        for column in df.columns:
            if column == "fy":
                continue

            y = df[column].values.reshape(-1, 1)

            model = LinearRegression()
            model.fit(time, y)

            slopes[column] = model.coef_[0][0]
            df[f"{column} Trend"] = model.predict(time).flatten()

        slopes_all[f"{column}"] = {"slope": slopes[column].round(4)}
        trend_results.append(df)

    return slopes_all, trend_results


shares_slopes, df_with_trends = calculate_trend_line(dfs_standardized)
steepest_decline = min(shares_slopes.items(), key=lambda x: x[1]["slope"])

shares_slopes_sorted = dict(sorted(shares_slopes.items(), key=lambda x: x[1]["slope"]))
shares_reduction_slope = pd.DataFrame.from_dict(
    shares_slopes_sorted, orient="index"
).sort_values(by="slope")
shares_reduction_slope.rename(
    columns={"slope": f"{numQters/4:.0f} yrs slope"}, inplace=True
)

# ===========================================================
# 2. Get historical prices and find performance against index
indexETF = "SPY"
# beg_period_date = adjust_to_next_business_day(
#     date(date.today().year, 1, 2), us_holidays
# )
endDate = adjust_to_prev_business_day(date.today(), us_holidays)
endDateOffset = adjust_to_next_business_day(
    (endDate + relativedelta(days=1)), us_holidays
)
# In case of a specific date: Year, Month, Day
# current_date = date(2016, 12, 30)  # must be business date
# return_periods = ["YTD"]
return_periods = ["YTD", "OneYear", "TwoYears"]
perf_rank = {}


def getPeriodReturn(
    begDate, endDate, begDateOffset, endDateOffset, period, ticker, indexETF
):
    try:
        stockPrice = yf.download(
            ticker,
            start=f"{begDate}",
            end=f"{begDateOffset}",
            progress=False,
        )["Adj Close"][f"{ticker}"]

        if stockPrice.empty:
            print(f"{ticker} - No data found for the specified date.")

            if f"{ticker}" not in perf_rank:
                perf_rank[f"{ticker}"] = {
                    f"{period}": {
                        "Return": 0,
                        "Return - SPY": 0,
                    }
                }
            else:
                if f"{period}" not in perf_rank[f"{ticker}"]:
                    perf_rank[f"{ticker}"][f"{period}"] = {
                        "Return": 0,
                        "Return - SPY": 0,
                    }
        else:
            stockPrice = yf.download(
                ticker,
                start=f"{begDate}",
                end=f"{begDateOffset}",
                progress=False,
            )["Adj Close"][f"{ticker}"]
            stockPriceBeg = stockPrice.iloc[0]

            stockPrice = yf.download(
                ticker,
                start=f"{endDate}",
                end=f"{endDateOffset}",
                progress=False,
            )["Adj Close"][f"{ticker}"]
            stockPriceEnd = stockPrice.iloc[0]

            stockReturnOneYear = (
                ((stockPriceEnd - stockPriceBeg) / stockPriceBeg) * 100
            ).round(2)

            indexPrice = yf.download(
                indexETF,
                start=f"{begDate}",
                end=f"{begDateOffset}",
                progress=False,
            )["Adj Close"][f"{indexETF}"]
            indexPriceBeg = indexPrice.iloc[0]

            indexPrice = yf.download(
                indexETF,
                start=f"{endDate}",
                end=f"{endDateOffset}",
                progress=False,
            )["Adj Close"][f"{indexETF}"]
            indexPriceEnd = indexPrice.iloc[0]

            indexReturnOneYear = (
                ((indexPriceEnd - indexPriceBeg) / indexPriceBeg) * 100
            ).round(2)

            if f"{ticker}" not in perf_rank:
                perf_rank[f"{ticker}"] = {
                    f"{period}": {
                        "Return": stockReturnOneYear.round(2),
                        "Return - SPY": (stockReturnOneYear - indexReturnOneYear).round(
                            2
                        ),
                    }
                }
            else:
                if f"{period}" not in perf_rank[f"{ticker}"]:
                    perf_rank[f"{ticker}"][f"{period}"] = {
                        "Return": stockReturnOneYear.round(2),
                        "Return - SPY": (stockReturnOneYear - indexReturnOneYear).round(
                            2
                        ),
                    }

            if f"{indexETF}" not in perf_rank:
                perf_rank[f"{indexETF}"] = {
                    f"{period}": {
                        "Return": indexReturnOneYear.round(2),
                        "Return - SPY": indexReturnOneYear.round(2),
                    }
                }
            else:
                if f"{period}" not in perf_rank[f"{indexETF}"]:
                    perf_rank[f"{indexETF}"][f"{period}"] = {
                        "Return": indexReturnOneYear.round(2),
                        "Return - SPY": indexReturnOneYear.round(2),
                    }

    except requests.exceptions.RequestException as req_err:
        print(f"{ticker} RequestException: {req_err}")
    except ValueError as ve:
        print(f"{ticker} ValueError: {ve}")
    except KeyError as ke:
        print(f"{ticker} KeyError: {ke}")
    except Exception as e:
        print(f"{ticker} An error occurred: {e}")


tickers = [x for x in tickers if x not in no_data_tickers]
# ticker = "AMD"
for ticker in tickers:
    # print(f"{ticker}")
    for period in return_periods:
        if period == "YTD":
            begDate = adjust_to_next_business_day(
                date(date.today().year, 1, 2), us_holidays
            )
        elif period == "OneYear":
            begDate = adjust_to_next_business_day(
                endDate - timedelta(days=365), us_holidays
            )

        elif period == "TwoYears":
            begDate = adjust_to_next_business_day(
                endDate - timedelta(days=730), us_holidays
            )

        begDateOffset = adjust_to_next_business_day(
            (begDate + relativedelta(days=1)), us_holidays
        )
        getPeriodReturn(
            begDate, endDate, begDateOffset, endDateOffset, period, ticker, indexETF
        )

sorted_perf_rank = dict(
    sorted(perf_rank.items(), key=lambda x: x[1]["OneYear"]["Return"], reverse=True)
)

perf_rank = {
    company: {period: values["Return"] for period, values in company_data.items()}
    for company, company_data in sorted_perf_rank.items()
}

perf_rank_df = pd.DataFrame.from_dict(perf_rank, orient="index")

sharesPriceTrack = pd.concat(
    [perf_rank_df[["YTD", "OneYear", "TwoYears"]], shares_reduction_slope], axis=1
)

print(sharesPriceTrack)
# sharesPriceTrack.to_csv("shares4yrPrice2yrTrack.csv")
