import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def millions_formater(x, pos):
    return f"{x/1e6:,.0f}M"


def is_strictly_decreasing(arr):
    for i in range(1, len(arr)):
        if arr[i] >= arr[i - 1]:
            return False
    return True


formatter = FuncFormatter(millions_formater)

headers = {"User-Agent": "alpenchev@yahoo.com"}

companyTickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json", headers=headers
)

companyData = pd.DataFrame.from_dict(companyTickers.json(), orient="index")
companyData["cik_str"] = companyData["cik_str"].astype(str).str.zfill(10)

ticker = "HBAN"
cik = companyData[companyData["ticker"] == f"{ticker}"]["cik_str"][0]

companyFacts = requests.get(
    f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers
)

sh_out = pd.DataFrame.from_dict(
    companyFacts.json()["facts"]["dei"]["EntityCommonStockSharesOutstanding"]["units"][
        "shares"
    ]
)

sh_out_qly = sh_out[sh_out["form"] == "10-K"]

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


# go over all stocks in S&P500
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

sh_out_key = "EntityCommonStockSharesOutstanding"
sh_decreased_tickers = {}

# tickers = ["AZO", "MUSA", "ICE", "WMT", "JPM"]
for ticker in sp_tickers:
    print(f"{ticker}")

    filtered_data = companyData[companyData["ticker"] == f"{ticker}"]

    if not filtered_data.empty and "cik_str" in filtered_data.columns:
        cik = companyData[companyData["ticker"] == f"{ticker}"]["cik_str"].iloc[0]
        companyFacts = requests.get(
            f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers
        )

        if companyFacts.headers.get("Content-Type") == "application/json":
            dei_dict = companyFacts.json()["facts"]["dei"]

            if sh_out_key in dei_dict:
                eqCommStockShOut = pd.DataFrame.from_dict(
                    companyFacts.json()["facts"]["dei"][
                        "EntityCommonStockSharesOutstanding"
                    ]
                )

                sharesData = pd.DataFrame.from_dict(
                    (eqCommStockShOut["units"]["shares"])
                )
                annual_sharesData = sharesData[sharesData["form"] == "10-K"]

                annual_date = pd.to_datetime(annual_sharesData["end"])
                annual_date = annual_date.dt.strftime("%m/%y")
                annual_out_shares = [float(x) for x in annual_sharesData["val"]]

                if len(annual_out_shares) > 0:
                    beg_shares = annual_out_shares[0]
                    end_shares = annual_out_shares[len(annual_out_shares) - 1]

                    if beg_shares > 0:
                        # print(f"{ticker} share count beg: {beg_shares}")
                        # print(f"{ticker} share count end: {end_shares}")
                        perc_change = (end_shares / beg_shares - 1) * 100
                        # print(f"{ticker} % shares change: {perc_change:.1f}%")
                        if perc_change < 0:
                            key = f"{ticker}"
                            sh_decreased_tickers.update({key: perc_change})
                        # print(is_strictly_decreasing(sh_out_qly_count))
                    else:
                        print(f"{ticker} beg_shares = 0")
                else:
                    print(f"{ticker} annual_out_shares is empty")

            else:
                print(f"{ticker} EntityCommonStockSharesOutstanding does not exist")
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
sorted_sh_decreased_tickers_df.to_csv("sorted_sh_decreased_tickers_df.csv")
