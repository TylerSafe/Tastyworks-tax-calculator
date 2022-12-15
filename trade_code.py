import csv

if __name__ == "__main__":
    
    #trade_date, root_symbol, trade_type, quantity, price, value, fees, total, remaining
    def get_stock_data(row):
        # remove commas from $ values
        value = row["Value"].replace(",", "")
        
        # check if quantity is 0 for non trade entries
        if float(row["Quantity"]) != 0:
            price = float(value) / float(row["Quantity"])
        else:
            price = 0

        # check if commissions is or has non numeric characters
        if row["Commissions"].isnumeric() == False:
            row["Commissions"] = 0

        total_fees = float(row["Commissions"]) + float(row["Fees"])
        net_cost = float(value) - total_fees
        
        # create list of relevant data
        data = [row["Date"], row["Root Symbol"], row["Action"], row["Quantity"], price, value, total_fees,  net_cost, 0]
        
        return data
        
    # read in data from csv file
    with open("History.csv", "r") as f:
        reader = csv.DictReader(f)
    
        stocks = {}

        # store data in dictionary of lists
        for row in reader:
            if row["Root Symbol"] in stocks.keys():
                stocks[row["Root Symbol"]].append(get_stock_data(row))
            else:
                stocks[row["Root Symbol"]] = [get_stock_data(row)]

    print(stocks["AAPL"])
        