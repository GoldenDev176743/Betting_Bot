from PyQt6 import uic
from PyQt6.uic import loadUi
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QRadioButton, QStyledItemDelegate, QApplication, QMainWindow, QPushButton, QTableView, QLabel, QComboBox, QMessageBox
from PyQt6.QtCore import Qt
import sys
from time import sleep
import json

Ui_MainWindow, QtBaseClass = uic.loadUiType('app_window.ui')

class CenterDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter
        super().paint(painter, option, index)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.prevPageButton = self.findChild(QPushButton, 'prevPage')        
        self.nextPageButton = self.findChild(QPushButton, 'nextPage')
        self.refreshButton = self.findChild(QPushButton, 'refresh')
        self.statusButton = self.findChild(QPushButton, 'status')
        self.currPage = self.findChild(QLabel, 'currentPage')
        self.rowsCount = self.findChild(QComboBox, 'rowsCount')
        self.tabelView = self.findChild(QTableView, 'tableView')

        self.tabelView.verticalHeader().setDefaultSectionSize(40)

        self.totalCount = self.findChild(QLabel, 'totalCount')
        self.totalAmount = self.findChild(QLabel, 'totalAmount')
        self.totalBenefit = self.findChild(QLabel, 'totalBenefit')
        self.totalLoss = self.findChild(QLabel, 'totalLoss')
        self.totalWin = self.findChild(QLabel, 'totalWin')

        self.radioMarathon = self.findChild(QRadioButton, 'marathon')
        self.radioMarathon.toggled.connect(self.on_radio_selected)
        self.radioMegapari= self.findChild(QRadioButton, 'megapari')
        self.radioMegapari.toggled.connect(self.on_radio_selected)
        self.radioPinnacle = self.findChild(QRadioButton, 'pinnacle')
        self.radioPinnacle.toggled.connect(self.on_radio_selected)
        self.radioVbet = self.findChild(QRadioButton, 'vbet')
        self.radioVbet.toggled.connect(self.on_radio_selected)
        self.radioAll = self.findChild(QRadioButton, 'all')
        self.radioAll.toggled.connect(self.on_radio_selected)

        self.prevPageButton.clicked.connect(self.prevPageButtonClicked)
        self.nextPageButton.clicked.connect(self.nextPageButtonClicked)
        self.refreshButton.clicked.connect(self.resetID)
        self.rowsCount.currentIndexChanged.connect(self.rowsCountChanged)
        self.tabelView.doubleClicked.connect(self.handleDoubleClick)
        self.statusButton.clicked.connect(self.statusButtonClicked)
        
        self.isClickedStatusButton = False
        # Set the delegate to center-align the cells
        delegate = CenterDelegate()
        self.tableView.setItemDelegate(delegate)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        # self.db.setDatabaseName('/Users/macos/Documents/bot/info.db')
        self.db.setDatabaseName("info.db")

        if not self.db.open():
            print("Error: Failed to connect to database")

        # Create a model and set the table
        self.model = QSqlTableModel()
       
        self.currPageNumber = 1
        self.currRowsCount = int(self.rowsCount.currentText())

        self.resetID()

    def statusButtonClicked(self):
        self.isClickedStatusButton = True
        while True:
            with open('_store.json', 'r') as fp:
                store = json.load(fp)
            if str(store) == '0':
                break
            sleep(1)
        self.resetID()
        with open('_status.json', 'r') as fp:
            status = json.load(fp)
        if len(status) != 0:
            with open('_store.json', 'w') as fp:
                json.dump('history', fp)
            while True:
                with open('_store.json', 'r') as fp:
                    store = json.load(fp)
                if str(store) == 'historydonedonedonedone':
                    break
                sleep(1)
            with open('_status.json', 'r') as fp:
                status = json.load(fp)
            for index in status:
                row = int(index['row_id'])
                record = self.model.record(row)
                record.setValue('status', index['status'])  # Set the ID value to the current row index
                self.model.setRecord(row, record)  # Update the record in the model
            self.model.submitAll()
            self.resetID()
            with open('_store.json', 'w') as fp:
                json.dump('0', fp)
        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Notification")
            msg_box.setText("Unsettled Status Does Not Exist.")
            msg_box.setIcon(QMessageBox.Icon.Question)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()


    def on_radio_selected(self):
        if self.radioMarathon.isChecked():
            self.model.setFilter(f"{'bookie'} = '{'MARATHON'}'")
        elif self.radioMegapari.isChecked():
            self.model.setFilter(f"{'bookie'} = '{'MEGAPARI'}'")
        elif self.radioPinnacle.isChecked():
            self.model.setFilter(f"{'bookie'} = '{'PINNACLE'}'")
        elif self.radioVbet.isChecked():
            self.model.setFilter(f"{'bookie'} = '{'VBET'}'")
        else:
            self.resetID()
            return
        self.count = self.model.rowCount()
        self.totalCount.setText(str(self.count))
        
        totalAmount = 0
        totalBenefit = 0
        totalWin = 0
        totalLoss = 0

        for row in range(self.count):
            totalAmount += float(self.model.data(self.model.index(row, 7)))
            if str(self.model.data(self.model.index(row, 10))) == 'Won':
                totalWin += float(self.model.data(self.model.index(row, 8)))
            if str(self.model.data(self.model.index(row, 10))) == 'Loss':
                totalLoss += float(self.model.data(self.model.index(row, 7)))
        self.totalAmount.setText(str(round(totalAmount, 3)))
        self.totalWin.setText(str(round(totalWin, 3)))
        self.totalLoss.setText('-' + str(round(totalLoss, 3)))
        totalBenefit = totalWin - totalLoss
        self.totalBenefit.setText(str(round(totalBenefit, 3)))
        self.currPageNumber = 1
        self.currPage.setText(str(self.currPageNumber))

    def prevPageButtonClicked(self):
        if self.currPageNumber > 1:
            self.model.setFilter('')
            self.model.sort(0, Qt.SortOrder.DescendingOrder)
            self.currPageNumber -= 1
            end = self.count - self.currRowsCount * (self.currPageNumber - 1)
            start = self.count - self.currRowsCount * self.currPageNumber - 1
            self.model.setFilter(f"ROWID > {start} AND ROWID < {end}")
            self.nextPageButton.setEnabled(True)
            self.currPage.setText(str(self.currPageNumber))
        if self.currPageNumber == 1:
            self.prevPageButton.setEnabled(False)

    def nextPageButtonClicked(self):
        self.end = self.currRowsCount * self.currPageNumber - 1
        if self.end < self.count:
            self.model.setFilter('')
            self.model.sort(0, Qt.SortOrder.DescendingOrder)
            self.currPageNumber += 1
            end = self.count - self.currRowsCount * (self.currPageNumber - 1)
            start = self.count - self.currRowsCount * self.currPageNumber - 1
            self.model.setFilter(f"ROWID > {start} AND ROWID < {end}")
            self.prevPageButton.setEnabled(True)
            self.currPage.setText(str(self.currPageNumber))
        if self.end > self.count:
            self.nextPageButton.setEnabled(False)


    def rowsCountChanged(self):
        self.currRowsCount = int(self.rowsCount.currentText())
        end = self.count - self.currRowsCount * (self.currPageNumber - 1)
        start = self.count - self.currRowsCount * self.currPageNumber - 1
        self.model.setFilter(f"ROWID > {start} AND ROWID < {end}")
    
    def handleDoubleClick(self, index):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Notification")
        msg_box.setText("Do you really want to delete this data?")
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)

        # Show the message box and check the result
        result = msg_box.exec()

        # Check if the user clicked OK or Cancel
        if result == QMessageBox.StandardButton.Ok:
            self.model.removeRow(index.row())
            self.resetID()

    def resetID(self):
        self.radioAll.click()
        self.model.setTable('data')
        self.model.select()
        self.count = self.model.rowCount()

        totalAmount = 0
        totalBenefit = 0
        totalLoss = 0
        totalWin = 0
        status = []
        for row in range(self.count):
            record = self.model.record(row)
            record.setValue('id', row)  # Set the ID value to the current row index
            self.model.setRecord(row, record)  # Update the record in the model
            totalAmount += float(self.model.data(self.model.index(row, 7)))
            if str(self.model.data(self.model.index(row, 10))) == 'Won':
                totalWin += float(self.model.data(self.model.index(row, 8)))
            if str(self.model.data(self.model.index(row, 10))) == 'Loss':
                totalLoss += float(self.model.data(self.model.index(row, 7)))
            if self.isClickedStatusButton:
                row_data = {}
                row_data['row_id'] = row
                row_data['bookie'] = str(self.model.data(self.model.index(row, 2)))
                row_data['bet_id'] = str(self.model.data(self.model.index(row, 9)))
                row_data['status'] = str(self.model.data(self.model.index(row, 10)))
                if str(row_data['status']) == 'Unsettled':
                    status.append(row_data)
        if self.isClickedStatusButton:
            self.isClickedStatusButton = False
            with open('_status.json', 'w') as fp:
                json.dump(status, fp)
        self.totalAmount.setText(str(round(totalAmount, 3)))
        self.totalWin.setText(str(round(totalWin, 3)))
        self.totalLoss.setText('-' + str(round(totalLoss, 3)))
        totalBenefit = totalWin - totalLoss
        self.totalBenefit.setText(str(round(totalBenefit, 3)))

        self.model.sort(0, Qt.SortOrder.DescendingOrder)
        self.model.submitAll()
        self.end = self.count - self.currRowsCount * (self.currPageNumber - 1)
        self.start = self.count - self.currRowsCount * self.currPageNumber - 1
        self.model.setFilter(f"ROWID > {self.start} AND ROWID < {self.end}")
        self.model.select()
        self.tabelView.setModel(self.model)
        self.tabelView.setColumnHidden(0, True)
        # self.tabelView.resizeColumnsToContents()
        self.tabelView.setColumnWidth(1, 175)
        self.tabelView.setColumnWidth(2, 100)
        self.tabelView.setColumnWidth(3, 100)
        self.tabelView.setColumnWidth(4, 175)
        self.tabelView.setColumnWidth(5, 175)
        self.tabelView.setColumnWidth(6, 100)
        self.tabelView.setColumnWidth(7, 100)
        self.tabelView.setColumnWidth(8, 100)
        self.tabelView.setColumnWidth(9, 175)
        self.tabelView.setColumnWidth(10, 70)

        self.totalCount.setText(str(self.count))

        if self.currPageNumber == 1:
            self.prevPageButton.setEnabled(False)
        else:
            self.prevPageButton.setEnabled(True)
        
        if self.end > self.count:
            self.nextPageButton.setEnabled(False)
        else:
            self.nextPageButton.setEnabled(True)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
