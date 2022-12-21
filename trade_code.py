import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys

# create the UI and add functionality
class Ui_Form(object):
    def __init__(self) -> None:
        self.comboBox = QtWidgets.QComboBox(Form)

    # create the UI elements
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1080, 720)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(460, 90, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.PL = QtWidgets.QLabel(Form)
        self.PL.setGeometry(QtCore.QRect(320, 60, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.PL.setFont(font)
        self.PL.setObjectName("PL")
        self.PL_2 = QtWidgets.QLabel(Form)
        self.PL_2.setGeometry(QtCore.QRect(210, 60, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.PL_2.setFont(font)
        self.PL_2.setObjectName("PL_2")
        self.PL_3 = QtWidgets.QLabel(Form)
        self.PL_3.setGeometry(QtCore.QRect(80, 60, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.PL_3.setFont(font)
        self.PL_3.setObjectName("PL_3")
        self.comboBox.setGeometry(QtCore.QRect(38, 190, 141, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.activated.connect(self.create_table)
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    # adjust names of UI elements
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Tastyworks Trade Calculator"))
        self.pushButton.setText(_translate("Form", "Calculate"))
        self.PL.setText(_translate("Form", "Total P/L"))
        self.PL_2.setText(_translate("Form", "Sold"))
        self.PL_3.setText(_translate("Form", "Bought"))

    # add options to drop down menu
    def add_menu_option(self, stock):
        self.comboBox.addItem(stock)

    # create a table of trades for the selected stock
    def create_table(self):
        stock = self.comboBox.currentText()
        
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(38, 240, 630, 350))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setRowCount(len(stocks[stock]))
        self.tableWidget.setHorizontalHeaderLabels(["Date", "Symbol", "Type", "Quantity", "Price", "Value", "Fees", "Total", "Remaining"])

        # populate table with data
        for i in range(len(stocks[stock])):
            for j in range(9):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(stocks[stock][i][j])))

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.show()

# class that reads the csv file and creates a dictionary of stocks
class Data:
    def get_stock_data(self, row):
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

    # read in data from csv file and return a dictionary of trades
    def read_csv(self):    
        # read in data from csv file
        with open("History.csv", "r") as f:
            reader = csv.DictReader(f)
        
            stocks = {}

            # store data in dictionary of lists
            for row in reader:
                if row["Root Symbol"] in stocks.keys():
                    stocks[row["Root Symbol"]].append(self.get_stock_data(row))
                else:
                    stocks[row["Root Symbol"]] = [self.get_stock_data(row)]

                    # check if symbol is blank
                    if row["Root Symbol"] == "":
                        ui.add_menu_option("Non-Stock Related")
                    else:
                        ui.add_menu_option(row["Root Symbol"])
            
        return stocks
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    data = Data()    
    stocks = data.read_csv()

    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
        