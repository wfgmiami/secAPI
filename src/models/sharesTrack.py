import requests
import pandas as pd
import numpy as np
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import yfinance as yf

# 1. Plot the stocks with downward share count
headers = {"User-Agent": "alpenchev@yahoo.com"}
companyTickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json", headers=headers
)
companyData = pd.DataFrame.from_dict(companyTickers.json(), orient="index")
companyData["cik_str"] = companyData["cik_str"].astype(str).str.zfill(10)

sp_tickers = [
    "MMM",
    "AOS",
    "ABT",
    "ABBV",
    "ACN",
    "ADBE",
    "AMD",
    "AES",
    "AFL",
    "A",
    "APD",
    "ABNB",
    "AKAM",
    "ALB",
    "ARE",
    "ALGN",
    "ALLE",
    "LNT",
    "ALL",
    "GOOGL",
    "GOOG",
    "MO",
    "AMZN",
    "AMCR",
    "AMTM",
    "AEE",
    "AEP",
    "AXP",
    "AIG",
    "AMT",
    "AWK",
    "AMP",
    "AME",
    "AMGN",
    "APH",
    "ADI",
    "ANSS",
    "AON",
    "APA",
    "AAPL",
    "AMAT",
    "APTV",
    "ACGL",
    "ADM",
    "ANET",
    "AJG",
    "AIZ",
    "T",
    "ATO",
    "ADSK",
    "ADP",
    "AZO",
    "AVB",
    "AVY",
    "AXON",
    "BKR",
    "BALL",
    "BAC",
    "BAX",
    "BDX",
    "BRK.B",
    "BBY",
    "TECH",
    "BIIB",
    "BLK",
    "BX",
    "BK",
    "BA",
    "BKNG",
    "BWA",
    "BSX",
    "BMY",
    "AVGO",
    "BR",
    "BRO",
    "BF.B",
    "BLDR",
    "BG",
    "BXP",
    "CHRW",
    "CDNS",
    "CZR",
    "CPT",
    "CPB",
    "COF",
    "CAH",
    "KMX",
    "CCL",
    "CARR",
    "CTLT",
    "CAT",
    "CBOE",
    "CBRE",
    "CDW",
    "CE",
    "COR",
    "CNC",
    "CNP",
    "CF",
    "CRL",
    "SCHW",
    "CHTR",
    "CVX",
    "CMG",
    "CB",
    "CHD",
    "CI",
    "CINF",
    "CTAS",
    "CSCO",
    "C",
    "CFG",
    "CLX",
    "CME",
    "CMS",
    "KO",
    "CTSH",
    "CL",
    "CMCSA",
    "CAG",
    "COP",
    "ED",
    "STZ",
    "CEG",
    "COO",
    "CPRT",
    "GLW",
    "CPAY",
    "CTVA",
    "CSGP",
    "COST",
    "CTRA",
    "CRWD",
    "CCI",
    "CSX",
    "CMI",
    "CVS",
    "DHR",
    "DRI",
    "DVA",
    "DAY",
    "DECK",
    "DE",
    "DELL",
    "DAL",
    "DVN",
    "DXCM",
    "FANG",
    "DLR",
    "DFS",
    "DG",
    "DLTR",
    "D",
    "DPZ",
    "DOV",
    "DOW",
    "DHI",
    "DTE",
    "DUK",
    "DD",
    "EMN",
    "ETN",
    "EBAY",
    "ECL",
    "EIX",
    "EW",
    "EA",
    "ELV",
    "EMR",
    "ENPH",
    "ETR",
    "EOG",
    "EPAM",
    "EQT",
    "EFX",
    "EQIX",
    "EQR",
    "ERIE",
    "ESS",
    "EL",
    "EG",
    "EVRG",
    "ES",
    "EXC",
    "EXPE",
    "EXPD",
    "EXR",
    "XOM",
    "FFIV",
    "FDS",
    "FICO",
    "FAST",
    "FRT",
    "FDX",
    "FIS",
    "FITB",
    "FSLR",
    "FE",
    "FI",
    "FMC",
    "F",
    "FTNT",
    "FTV",
    "FOXA",
    "FOX",
    "BEN",
    "FCX",
    "GRMN",
    "IT",
    "GE",
    "GEHC",
    "GEV",
    "GEN",
    "GNRC",
    "GD",
    "GIS",
    "GM",
    "GPC",
    "GILD",
    "GPN",
    "GL",
    "GDDY",
    "GS",
    "HAL",
    "HIG",
    "HAS",
    "HCA",
    "DOC",
    "HSIC",
    "HSY",
    "HES",
    "HPE",
    "HLT",
    "HOLX",
    "HD",
    "HON",
    "HRL",
    "HST",
    "HWM",
    "HPQ",
    "HUBB",
    "HUM",
    "HBAN",
    "HII",
    "IBM",
    "IEX",
    "IDXX",
    "ITW",
    "INCY",
    "IR",
    "PODD",
    "INTC",
    "ICE",
    "IFF",
    "IP",
    "IPG",
    "INTU",
    "ISRG",
    "IVZ",
    "INVH",
    "IQV",
    "IRM",
    "JBHT",
    "JBL",
    "JKHY",
    "J",
    "JNJ",
    "JCI",
    "JPM",
    "JNPR",
    "K",
    "KVUE",
    "KDP",
    "KEY",
    "KEYS",
    "KMB",
    "KIM",
    "KMI",
    "KKR",
    "KLAC",
    "KHC",
    "KR",
    "LHX",
    "LH",
    "LRCX",
    "LW",
    "LVS",
    "LDOS",
    "LEN",
    "LLY",
    "LIN",
    "LYV",
    "LKQ",
    "LMT",
    "L",
    "LOW",
    "LULU",
    "LYB",
    "MTB",
    "MPC",
    "MKTX",
    "MAR",
    "MMC",
    "MLM",
    "MAS",
    "MA",
    "MTCH",
    "MKC",
    "MCD",
    "MCK",
    "MDT",
    "MRK",
    "META",
    "MET",
    "MTD",
    "MGM",
    "MCHP",
    "MU",
    "MSFT",
    "MAA",
    "MRNA",
    "MHK",
    "MOH",
    "TAP",
    "MDLZ",
    "MPWR",
    "MNST",
    "MCO",
    "MS",
    "MOS",
    "MSI",
    "MSCI",
    "NDAQ",
    "NTAP",
    "NFLX",
    "NEM",
    "NWSA",
    "NWS",
    "NEE",
    "NKE",
    "NI",
    "NDSN",
    "NSC",
    "NTRS",
    "NOC",
    "NCLH",
    "NRG",
    "NUE",
    "NVDA",
    "NVR",
    "NXPI",
    "ORLY",
    "OXY",
    "ODFL",
    "OMC",
    "ON",
    "OKE",
    "ORCL",
    "OTIS",
    "PCAR",
    "PKG",
    "PLTR",
    "PANW",
    "PARA",
    "PH",
    "PAYX",
    "PAYC",
    "PYPL",
    "PNR",
    "PEP",
    "PFE",
    "PCG",
    "PM",
    "PSX",
    "PNW",
    "PNC",
    "POOL",
    "PPG",
    "PPL",
    "PFG",
    "PG",
    "PGR",
    "PLD",
    "PRU",
    "PEG",
    "PTC",
    "PSA",
    "PHM",
    "QRVO",
    "PWR",
    "QCOM",
    "DGX",
    "RL",
    "RJF",
    "RTX",
    "O",
    "REG",
    "REGN",
    "RF",
    "RSG",
    "RMD",
    "RVTY",
    "ROK",
    "ROL",
    "ROP",
    "ROST",
    "RCL",
    "SPGI",
    "CRM",
    "SBAC",
    "SLB",
    "STX",
    "SRE",
    "NOW",
    "SHW",
    "SPG",
    "SWKS",
    "SJM",
    "SW",
    "SNA",
    "SOLV",
    "SO",
    "LUV",
    "SWK",
    "SBUX",
    "STT",
    "STLD",
    "STE",
    "SYK",
    "SMCI",
    "SYF",
    "SNPS",
    "SYY",
    "TMUS",
    "TROW",
    "TTWO",
    "TPR",
    "TRGP",
    "TGT",
    "TEL",
    "TDY",
    "TFX",
    "TER",
    "TSLA",
    "TXN",
    "TPL",
    "TXT",
    "TMO",
    "TJX",
    "TSCO",
    "TT",
    "TDG",
    "TRV",
    "TRMB",
    "TFC",
    "TYL",
    "TSN",
    "USB",
    "UBER",
    "UDR",
    "ULTA",
    "UNP",
    "UAL",
    "UPS",
    "URI",
    "UNH",
    "UHS",
    "VLO",
    "VTR",
    "VLTO",
    "VRSN",
    "VRSK",
    "VZ",
    "VRTX",
    "VTRS",
    "VICI",
    "V",
    "VST",
    "VMC",
    "WRB",
    "GWW",
    "WAB",
    "WBA",
    "WMT",
    "DIS",
    "WBD",
    "WM",
    "WAT",
    "WEC",
    "WFC",
    "WELL",
    "WST",
    "WDC",
    "WY",
    "WMB",
    "WTW",
    "WYNN",
    "XEL",
    "XYL",
    "YUM",
    "ZBRA",
]

sp_tickers = [
    "FICO",
    "APO",
    "VIRT",
    "LEN",
    "MCD",
    "MRK",
    "AZO",
    "LLY",
    "MUSA",
    "RL",
    "ICE",
    "URI",
    "JPM",
]
# sp_tickers = ["AAP", "CMCSA", "DLTR", "GT", "MKC", "SWBI", "MSFT", "TROW"]
# sp_tickers = ["AAP", "CMCSA", "ICE"]
# shareType = "CommonStockSharesOutstanding"
shareType = "WeightedAverageNumberOfSharesOutstandingBasic"

numQters = 16  # last 4 years
sh_decreased_tickers = {}
sharesByQtrs = pd.DataFrame()
dfs = []
ticker = "NVDA"
for ticker in sp_tickers:
    print(f"{ticker}")

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

            # shares10K = sharesData[
            #     (sharesData["form"] == "10-K") & (sharesData["frame"].notna())
            # ]

            # shares10KForm = sharesData[sharesData["form"] == "10-K"]

            # shares10K = (
            #     shares10KForm.groupby(["start", "end", "val"])
            #     .first()
            #     .reset_index()[["start", "end", "val", "fy"]]
            # )

            # shares10K["fy"] = shares10K["fy"].apply(lambda x: str(x)[2:] + "Q4")

            # shares10K.rename(columns={"fy": "frame"}, inplace=True)
            # shares10K = shares10K.loc[:, ["frame", "val"]]

            # shares10Q = sharesData[
            #     (sharesData["form"] == "10-Q") & (sharesData["frame"].notna())
            # ]
            # shares10Q = shares10Q.loc[:, ["frame", "val"]]

            sharesFilings = sharesData[
                (
                    ((sharesData["form"] == "10-Q") & (sharesData["frame"].notna()))
                    | (sharesData["form"] == "10-K")
                )
            ]
            # print(sharesFilings.tail(16))
            # print(sharesFilings[sharesFilings["form"] == "10-K"].tail(20))

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

            # print(sharesFilings.tail(16))

            commShOut = sharesFilings.loc[:, ["fy", "val"]]

            commShOutQtrs = commShOut.tail(numQters)
            temp = commShOutQtrs.rename(columns={"val": f"{ticker}"})
            dfs.append(temp)

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

# print(df_standardized)


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

        slopes_all[f"{column}"] = slopes[column]
        trend_results.append(df)

    return slopes_all, trend_results


shares_slopes, df_with_trends = calculate_trend_line(dfs_standardized)
steepest_decline = min(shares_slopes.items(), key=lambda x: x[1])

print("Stocks with the steepest share reduction:")
print(f"  Product: {steepest_decline[0]}")
print(f"  Slope: {steepest_decline[1]:.4f}")

print("\nSlopes for all stocks:")
for ticker, slope in shares_slopes.items():
    print(f"{ticker}: Slope = {slope:.4f}")


# # Plot each product's price trend and trend line
# plt.figure(figsize=(12, 8))

# for product, prices in product_prices.items():
#     time = np.arange(len(prices))  # Time steps (X-axis)

#     # Calculate slope and trend line
#     slope, trend_line = calculate_trend_line(prices)

#     # Plot original data
#     plt.plot(time, prices, marker="o", label=f"{product} (Slope: {slope:.2f})")

#     # Plot trend line
#     plt.plot(time, trend_line, linestyle="--", label=f"{product} Trend Line")

# # Customize the plot
# plt.title("Product Price Trends with Regression Lines", fontsize=16)
# plt.xlabel("Time (e.g., Days or Months)", fontsize=12)
# plt.ylabel("Price", fontsize=12)
# plt.legend(fontsize=10, loc="best")  # Add legend
# plt.grid(True)
# plt.show()


# 2. Get historical prices and find performance against index
from datetime import date, timedelta
import holidays
from dateutil.relativedelta import relativedelta


# Function to find the closest previous business day
def adjust_to_business_day(target_date, holiday_list):
    while (
        target_date.weekday() in (5, 6) or target_date in holiday_list
    ):  # 5 = Saturday, 6 = Sunday
        target_date -= timedelta(days=1)
    return target_date


indexETF = "SPY"
ticker = "ICE"

current_date = date.today()
one_year_ago = current_date - timedelta(days=365)

# Get the list of U.S. federal holidays for the relevant year
us_holidays = holidays.UnitedStates(years=[one_year_ago.year])

# Adjust the one-year-ago date to the closest previous business day
adjusted_one_year_ago = adjust_to_business_day(one_year_ago, us_holidays)

stockPrice = yf.download(
    ticker,
    start=f"{adjusted_one_year_ago}",
    end=f"{adjusted_one_year_ago + relativedelta(days=1)}",
)["Adj Close"][f"{ticker}"]
stockPriceBeg = stockPrice.iloc[0]

stockPrice = yf.download(
    ticker, start=f"{current_date}", end=f"{current_date + relativedelta(days=1)}"
)["Adj Close"][f"{ticker}"]
stockPriceEnd = stockPrice.iloc[0]

stockReturnOneYear = (((stockPriceEnd - stockPriceBeg) / stockPriceBeg) * 100).round(2)

indexPrice = yf.download(
    indexETF,
    start=f"{adjusted_one_year_ago}",
    end=f"{adjusted_one_year_ago+ relativedelta(days=1)}",
)["Adj Close"][f"{indexETF}"]
indexPriceBeg = indexPrice.iloc[0]

indexPrice = yf.download(
    indexETF,
    start=f"{current_date}",
    end=f"{current_date+ relativedelta(days=1)}",
)["Adj Close"][f"{indexETF}"]
indexPriceEnd = indexPrice.iloc[0]

indexReturnOneYear = (((indexPriceEnd - indexPriceBeg) / indexPriceBeg) * 100).round(2)

print(
    f"{ticker} one year return vs SPY = {(stockReturnOneYear - indexReturnOneYear).round(2)}"
)

sp_tickers = [
    "FICO",
    "APO",
    "VIRT",
    "LEN",
    "MCD",
    "MRK",
    "AZO",
    "LLY",
    "AMTM",
    "MUSA",
    "RL",
    "ICE",
    "URI",
    "JPM",
]
# sp_tickers = ["AAP", "CMCSA", "DLTR", "GT", "MKC", "SWBI", "MSFT", "TROW"]
indexETF = "SPY"
for ticker in sp_tickers:
    # print(f"{ticker}")

    current_date = date.today()
    one_year_ago = current_date - timedelta(days=365)

    # Get the list of U.S. federal holidays for the relevant year
    us_holidays = holidays.UnitedStates(years=[one_year_ago.year])

    # Adjust the one-year-ago date to the closest previous business day
    adjusted_one_year_ago = adjust_to_business_day(one_year_ago, us_holidays)

    try:
        stockPrice = yf.download(
            ticker,
            start=f"{adjusted_one_year_ago}",
            end=f"{adjusted_one_year_ago + relativedelta(days=1)}",
            progress=False,
        )["Adj Close"][f"{ticker}"]

        if stockPrice.empty:
            print(f"{ticker} - No data found for the specified date.")
        else:
            stockPrice = yf.download(
                ticker,
                start=f"{adjusted_one_year_ago}",
                end=f"{adjusted_one_year_ago + relativedelta(days=1)}",
                progress=False,
            )["Adj Close"][f"{ticker}"]
            stockPriceBeg = stockPrice.iloc[0]

            stockPrice = yf.download(
                ticker,
                start=f"{current_date}",
                end=f"{current_date + relativedelta(days=1)}",
                progress=False,
            )["Adj Close"][f"{ticker}"]
            stockPriceEnd = stockPrice.iloc[0]

            stockReturnOneYear = (
                ((stockPriceEnd - stockPriceBeg) / stockPriceBeg) * 100
            ).round(2)

            indexPrice = yf.download(
                indexETF,
                start=f"{adjusted_one_year_ago}",
                end=f"{adjusted_one_year_ago+ relativedelta(days=1)}",
                progress=False,
            )["Adj Close"][f"{indexETF}"]
            indexPriceBeg = indexPrice.iloc[0]

            indexPrice = yf.download(
                indexETF,
                start=f"{current_date}",
                end=f"{current_date+ relativedelta(days=1)}",
                progress=False,
            )["Adj Close"][f"{indexETF}"]
            indexPriceEnd = indexPrice.iloc[0]

            indexReturnOneYear = (
                ((indexPriceEnd - indexPriceBeg) / indexPriceBeg) * 100
            ).round(2)

            if (stockReturnOneYear - indexReturnOneYear) > 0:
                print(
                    f"{ticker} one year return vs SPY = {(stockReturnOneYear - indexReturnOneYear).round(2)}"
                )

    except yf.shared.YFPricesMissingError:
        print(
            f"{ticker} -Data could not be retrieved. Check the ticker and date range."
        )
