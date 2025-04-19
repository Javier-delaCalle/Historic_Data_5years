# 📈 Financial Asset Analyzer – 5-Year Historical Performance

This Python program allows you to analyze the historical performance of financial assets over the past five years using data from Yahoo Finance. It provides key metrics, generates visual plots, and automatically exports results to CSV files, which are then seamlessly integrated with an Excel dashboard for further analysis.

---

## 🚀 How It Works

### 1. **Launch the Program**
When you run the program, you are presented with a menu of predefined assets to analyze (e.g., Tesla, Apple, Microsoft), including an option to manually enter any ticker symbol.

> ⚠️ The assets included in the menu, the exported CSV data, and the Excel workbook have been **specifically selected and configured** to reflect a custom portfolio inspired by **Harry Browne’s Permanent Portfolio**.  
> This includes a diversified set of assets for long-term stability and performance tracking.

### 2. **Data Retrieval**
The program:
- Downloads 5 years of historical price data from Yahoo Finance.
- Calculates the **daily return** percentage.
- Computes the **total return** and **annualized return**.
- Calculates the **geometric mean** of the closing price over the 5-year period.

### 3. **Data Visualization**
Two separate plots are displayed for each asset:
- **Closing Price over Time**
- **Daily Return (%) over Time**

This allows you to visually assess performance and volatility.

### 4. **CSV Export**
All analyzed data is exported to a CSV file named `[TICKER]_5_years.csv`.

These files are **automatically stored in a dedicated folder called `CSV_Files`**. If the folder does not exist, the program will create it.

---

## 📊 Excel Dashboard Integration

The exported CSV files are connected to an Excel workbook that serves as a dynamic dashboard for further analysis.

### Excel Features:
- **Auto-refresh on open**: Each time the Excel file is opened, it **automatically refreshes** and loads the latest data from the CSV files.
- **Dynamic tables**: The imported tables are updated to reflect any newly analyzed tickers or updated values.
- **Conditional formatting** on **Closing Price**:
  - A color gradient highlights how close each closing price is to the 5-year **geometric mean**.
  - This visual aid helps identify potential **buying opportunities** when the price is significantly below the long-term average.

---

## 🔁 Repeat Analysis

After each analysis, the program will ask if you want to analyze another asset. If you choose "yes", the menu will appear again, allowing you to analyze additional tickers in the same session.

---

## ✅ Requirements

- Python 3.x
- `yfinance`
- `matplotlib`
- `pandas`
- `statistics`

You can install the necessary packages with:

```bash
pip install yfinance matplotlib pandas
```

---

## 📂 Folder Structure

```
/your_project_directory/
│
├── CSV_Files/
│   ├── GLD_5_years.csv
│   ├── TLT_5_years.csv
│   ├── VTI_5_years.csv
│   └── ...
│
├── financial_analyzer.py
└── Excel_Dashboard.xlsx
```

---

## 📌 About the Portfolio

This tool was built to support the design and monitoring of a **personal investment portfolio inspired by the Permanent Portfolio strategy** developed by **Harry Browne**. The chosen assets aim to represent different market conditions (growth, recession, inflation, and deflation) through a balance of stocks, bonds, gold, and cash equivalents.
