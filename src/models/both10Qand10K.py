import requests
import pandas as pd
import numpy as np
from scipy.stats import linregress
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

# sp_tickers = ["FICO", "APO", "VIRT", "LEN", "MCD", "MRK", "AZO", "LLY", "MUSA", "RL"]
sp_tickers = ["AAP", "CMCSA", "DLTR", "GT", "MKC", "SWBI", "MSFT", "TROW"]
# sp_tickers = ["AAP", "CMCSA", "ICE"]
# shareType = "CommonStockSharesOutstanding"
shareType = "WeightedAverageNumberOfSharesOutstandingBasic"

numQters = 16  # last 4 years
sh_decreased_tickers = {}
sharesByQtrs = pd.DataFrame()
dfs = []
ticker = "AAP"
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
            print(sharesFilings.tail(16))
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


df_combined = dfs[0]
df_combined = df_combined.reset_index(drop=True)

for df in dfs[1:]:
    ticker = df.columns[1]

    df_combined = pd.concat(
        [df_combined, df[[f"{ticker}"]].reset_index(drop=True)], axis=1
    )


numeric_cols = df_combined.select_dtypes(include=["number"])

df_standardized = (numeric_cols - numeric_cols.mean()) / numeric_cols.std()
df_standardized = pd.concat([df_standardized, df_combined["fy"]], axis=1)
df_standardized.set_index("fy", inplace=True)

print(df_standardized)


def calculate_slope(df_standardized):
    x = np.arange(len(df_standardized))  # Time indices
    # slope, intercept, r_value, p_value, std_err = linregress(x, data)
    slope, _, _, _, _ = linregress(x, df_standardized)
    return slope


downtrend_series = {
    col: df_standardized[col]
    for col in df_standardized.columns
    if calculate_slope(df_standardized[col]) < 0
}

plt.figure(figsize=(10, 6))
for name, series in downtrend_series.items():
    plt.plot(series, label=name)

plt.title("Downtrending Shares Outstanding")
plt.xlabel("Report Period")
plt.ylabel("Standardized Shares")
plt.legend()
plt.show()

# 2. Get historical prices and find performance against index
# indexETF = "SPY"
# ticker = "ICE"
# data = yf.download(ticker, start="2024-01-01", end="2024-12-13")

# print(data.head())
