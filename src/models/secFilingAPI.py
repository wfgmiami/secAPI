import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def millions_formater(x, pos):
    return f"{x/1e6:,.0f}M"


formatter = FuncFormatter(millions_formater)

headers = {"User-Agent": "alpenchev@yahoo.com"}

companyTickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json", headers=headers
)

# print(companyTickers.json().keys())
# firstEntry = companyTickers.json()["0"]
# directCik = companyTickers.json()["0"]["cik_str"]

companyData = pd.DataFrame.from_dict(companyTickers.json(), orient="index")
companyData["cik_str"] = companyData["cik_str"].astype(str).str.zfill(10)

ticker = "BKR"

cik = companyData[companyData["ticker"] == f"{ticker}"]["cik_str"][0]

filingMetadata = requests.get(
    f"https://data.sec.gov/submissions/CIK{cik}.json", headers=headers
)

print(filingMetadata.json().keys())
filingMetadata.json()["filings"]
filingMetadata.json()["filings"].keys()
filingMetadata.json()["filings"]["files"]
filingMetadata.json()["filings"]["recent"]
filingMetadata.json()["filings"]["recent"].keys()

allForms = pd.DataFrame.from_dict(filingMetadata.json()["filings"]["recent"])
# allForms2 = pd.DataFrame.from_dict(filingMetadata.json()["filings"]["files"])
quarterly_filings = allForms[allForms["form"] == "10-Q"]

allForms.columns
allForms[["accessionNumber", "reportDate", "form"]].head(50)

companyFacts = requests.get(
    f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers
)

companyFacts.json().keys()
companyFacts.json()["facts"]
companyFacts.json()["facts"].keys()
companyFacts.json()["facts"]["dei"].keys()
companyFacts.json()["facts"]["dei"]["EntityCommonStockSharesOutstanding"]
companyFacts.json()["facts"]["dei"]["EntityCommonStockSharesOutstanding"].keys()
companyFacts.json()["facts"]["dei"]["EntityCommonStockSharesOutstanding"]["units"]
companyFacts.json()["facts"]["dei"]["EntityCommonStockSharesOutstanding"]["units"][
    "shares"
]
companyFacts.json()["facts"]["dei"]["EntityCommonStockSharesOutstanding"]["units"][
    "shares"
][0]

sh_out = pd.DataFrame.from_dict(
    companyFacts.json()["facts"]["dei"]["EntityCommonStockSharesOutstanding"]["units"][
        "shares"
    ]
)


# availableKey = list(companyFacts.json()["facts"]["dei"].keys())[0]

# sh_out = pd.DataFrame.from_dict(
#     companyFacts.json()["facts"]["dei"][f"{availableKey}"]["units"][
#         "shares"
#     ]
# )

# sh_out = pd.DataFrame.from_dict(companyFacts.json()["facts"]["dei"][f"{availableKey}"]["units"][
#     "USD"
# ])

# sh_out_qly = sh_out[sh_out["form"].str.contains("10-Q", na=False)]
# recent_filings = sh_out_qly[sh_out_qly["fy"] >= 2010]
# print("Recent 10-Q filings:")
# print(recent_filings)

sh_out_qly = sh_out[sh_out["form"] == "10-Q"]

sh_out_qly_date = pd.to_datetime(sh_out_qly["end"])
sh_out_qly_date = sh_out_qly_date.dt.strftime("%m/%y")
sh_out_qly_count = [float(x) for x in sh_out_qly["val"]]

sh_out_qly_df = pd.DataFrame(index=sh_out_qly_date, data=sh_out_qly_count)

fix, ax = plt.subplots()
plt.plot(sh_out_qly_df)

ax.yaxis.set_major_formatter(formatter)
plt.xticks(rotation=45)
ax.set_xlabel("dates", fontsize="small")
ax.tick_params(axis="x", labelsize=8)

ax.set_ylabel("shares", fontsize="small")
ax.tick_params(axis="y", labelsize=8)
plt.title(f"{ticker}")
plt.show()

# concept data // financial statement line items
companyFacts.json()["facts"]["us-gaap"]
usGAAP = companyFacts.json()["facts"]["us-gaap"].keys()

usGAAP_df = pd.DataFrame(usGAAP, columns=["Values"])

usGAAP_sharerepurchase = usGAAP_df[
    usGAAP_df["Values"].str.contains("sharerepurchase", case=False, na=False)
]
usGAAP_shares = usGAAP_df[
    usGAAP_df["Values"].str.contains("shares", case=False, na=False)
]

# CommonStockSharesOutstanding
# WeightedAverageNumberOfDilutedSharesOutstanding
# WeightedAverageNumberOfSharesOutstandingBasic

companyFacts.json()["facts"]["us-gaap"]["CommonStockSharesOutstanding"]
companyFacts.json()["facts"]["us-gaap"][
    "WeightedAverageNumberOfDilutedSharesOutstanding"
]

companyFacts.json()["facts"]["us-gaap"]["WeightedAverageNumberOfSharesOutstandingBasic"]
common_stock = companyFacts.json()["facts"]["us-gaap"]["CommonStockSharesOutstanding"]


companyConcept = requests.get(
    (
        f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}"
        f"/us-gaap/WeightedAverageNumberOfSharesOutstandingBasic.json"
    ),
    headers=headers,
)

# review data
companyConcept.json().keys()
companyConcept.json()["units"]
companyConcept.json()["units"].keys()
companyConcept.json()["units"]["shares"]
companyConcept.json()["units"]["shares"][0]

sharesData = pd.DataFrame.from_dict((companyConcept.json()["units"]["shares"]))

sharesData.columns
sharesData.form
len(sharesData)
shares10Q = sharesData[sharesData.form == "10-Q"]
sharesOnly1 = sharesData[sharesData["val"] == 1]

shares10Q = shares10Q[2:]
sharesOnly1 = shares10Q[shares10Q["val"] == 1]
commShOut = shares10Q.iloc[:, :2]
commShOut = commShOut.drop_duplicates(subset=["end"])
commShOut20Qtrs = commShOut.tail(20)


fix, ax = plt.subplots()
plt.plot(commShOut20Qtrs["end"], commShOut20Qtrs["val"])

ax.yaxis.set_major_formatter(formatter)
plt.xticks(rotation=45)
ax.set_xlabel("dates", fontsize="small")
ax.tick_params(axis="x", labelsize=8)

ax.set_ylabel("shares", fontsize="small")
ax.tick_params(axis="y", labelsize=8)
plt.title(f"{ticker}")
plt.show()

# Loop for all S&P500 tickers
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

sh_out_key = "EntityCommonStockSharesOutstanding"
sh_decreased_tickers = {}

sp_tickers = ["ANSS", "CRWD", "JPM"]
ticker = "CRWD"
for ticker in sp_tickers:
    print(f"{ticker}")

    filtered_data = companyData[companyData["ticker"] == f"{ticker}"]

    if not filtered_data.empty and "cik_str" in filtered_data.columns:
        cik = companyData[companyData["ticker"] == f"{ticker}"]["cik_str"].iloc[0]

        companyConcept = requests.get(
            (
                f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}"
                f"/us-gaap/CommonStockSharesOutstanding.json"
            ),
            headers=headers,
        )

        common_stock = companyFacts.json()["facts"]["us-gaap"][
            "CommonStockSharesOutstanding"
        ]

        if companyConcept.headers.get("Content-Type") == "application/json":
            sharesData = pd.DataFrame.from_dict(
                (companyConcept.json()["units"]["shares"])
            )

            shares10Q = sharesData[sharesData.form == "10-Q"]
            commShOut = shares10Q.iloc[:, :2]
            commShOut = commShOut.drop_duplicates(subset=["end"])
            commShOut20Qtrs = commShOut.tail(20)

            qly_date = pd.to_datetime(commShOut20Qtrs["end"])
            qly_date = qly_date.dt.strftime("%m/%y")
            qly_out_shares = [float(x) for x in commShOut20Qtrs["val"]]

            if len(qly_out_shares) > 0:
                beg_shares = qly_out_shares[0]
                end_shares = qly_out_shares[len(qly_out_shares) - 1]

                if beg_shares > 0:
                    perc_change = (end_shares / beg_shares - 1) * 100

                    if perc_change < 0:
                        key = f"{ticker}"
                        sh_decreased_tickers.update({key: perc_change})
                else:
                    print(f"{ticker} beg_shares = 0")
            else:
                print(f"{ticker} annual_out_shares is empty")
        else:
            print(
                f'{ticker} companyFacts.headers.get("Content-Type") not "application/json"'
            )
    else:
        print(f'{ticker} companyData[companyData["ticker"] does not exist')

sh_decreased_tickers_df = pd.DataFrame(
    sh_decreased_tickers.items(), columns=["Ticker", "Share Reduction"]
)

sorted_sh_decreased_tickers_df = sh_decreased_tickers_df.sort_values(
    by="Share Reduction", ascending=True
)

print(sorted_sh_decreased_tickers_df)

# sorted_sh_decreased_tickers_df.to_csv("sorted_sh_decreased_tickers_df.csv")


# from Adam Getbags
# companyFacts.json()["facts"]["us-gaap"]["AccountsPayable"]
# companyFacts.json()["facts"]["us-gaap"]["Revenues"]
# companyFacts.json()["facts"]["us-gaap"]["Assets"]

# companyConcept = requests.get(
#     (f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}" f"/us-gaap/Assets.json"),
#     headers=headers,
# )

# review data
# companyConcept.json().keys()
# companyConcept.json()["units"]
# companyConcept.json()["units"].keys()
# companyConcept.json()["units"]["USD"]
# companyConcept.json()["units"]["USD"][0]

# parse assets from single filing
# companyConcept.json()["units"]["USD"][0]["val"]

# get all filings data
# assetsData = pd.DataFrame.from_dict((companyConcept.json()["units"]["USD"]))

# review data
# assetsData.columns
# assetsData.form

# get assets from 10Q forms and reset index
# assets10Q = assetsData[assetsData.form == "10-Q"]
# assets10Q = assets10Q.reset_index(drop=True)

# plot
# assets10Q.plot(x="end", y="val")
