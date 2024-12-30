import requests
from lxml import etree

# SEC EDGAR headers (provide your own contact details)
HEADERS = {"User-Agent": "YourName/YourEmail"}

# Step 1: Get the submission metadata
cik = "0000016918"  # CIK for Constellation Brands, Inc.
submissions_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
response = requests.get(submissions_url, headers=HEADERS)
data = response.json()

# Step 2: Find the most recent 10-Q or 10-K
for idx, form in enumerate(data["filings"]["recent"]["form"]):
    if form in ["10-K", "10-Q"]:
        accession_number = data["filings"]["recent"]["accessionNumber"][idx]
        cik = "0000016918"  # Replace with the actual CIK
        xbrl_index_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number.replace('-', '')}/{accession_number}-index.htm"
        break

# Step 3: Fetch and parse the XBRL file
response = requests.get(xbrl_index_url, headers=HEADERS)
xbrl_file_url = xbrl_index_url.replace("-index.htm", "_htm.xml")
xbrl_response = requests.get(xbrl_file_url, headers=HEADERS)

# Parse the XBRL XML
xbrl_tree = etree.fromstring(xbrl_response.content)
shares_outstanding = xbrl_tree.xpath(
    "//dei:EntityCommonStockSharesOutstanding",
    namespaces={"dei": "http://xbrl.sec.gov/dei/2022-01-31"},
)

# Extract the value
if shares_outstanding:
    print("Outstanding Shares:", shares_outstanding[0].text)
else:
    print("Shares outstanding not found.")
