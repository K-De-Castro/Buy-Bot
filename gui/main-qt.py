from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLineEdit
import sys
import json
import multiprocessing
import process
from gui.qtdialog import Form

class Swift(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle("Swift")

        label = QtWidgets.QLabel(self)
        label.setText("my first label!")
        label.move(50, 50)

        with open("../profile.json", "r") as jsonFile:
            profile = json.load(jsonFile)

        self.process = process.Process(profile, multiprocessing.Lock())

        self.table_widget = Layout(self, self.process)
        self.setCentralWidget(self.table_widget)

        self.show()
        sys.exit(app.exec_())


class Layout(QWidget):
    def __init__(self, parent, process):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.process = process
        # self.setFixedHeight(600)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Tasks")
        self.tabs.addTab(self.tab2, "Profile")

        # tab 1
        self.tab1.layout = QVBoxLayout(self.tab1)
        self.creatingTables(self.tab1.layout)
        self.newtaskbtn(self.tab1.layout)
        self.starttasks(self.tab1.layout)
        self.tab1.setLayout(self.tab1.layout)

        # tab 2
        self.tab2.layout = QtWidgets.QGridLayout(self.tab2)
        self.cardinfo(self.tab2.layout)
        self.profile(self.tab2.layout)
        self.tab2.setLayout(self.tab2.layout)

        # add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def creatingTables(self, layout):
        tableWidget = QtWidgets.QTableWidget()
        tableWidget.setColumnCount(5)
        tableWidget.setRowCount(0)

        header = tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        tableWidget.resizeColumnsToContents()
        self.tableWidget = tableWidget
        layout.addWidget(tableWidget)

    def newtaskbtn(self, layout):
        button = QtWidgets.QPushButton("Add new task")
        button.clicked.connect(lambda a: Form(self.tableWidget, self.process).exec_())
        button.resize(20,30)
        layout.addWidget(button)

    def starttasks(self, layout):
        button = QtWidgets.QPushButton("Start tasks")
        button.clicked.connect(self.process.run)
        button.resize(20,30)
        layout.addWidget(button)

    def cardinfo(self, layout):
        main = layout
        vbox = QVBoxLayout()
        group = QWidget(self)

        with open("../profile.json", "r") as jsonFile:
            data = json.load(jsonFile)

        # H layout for credit card
        chbox = QtWidgets.QHBoxLayout()
        cvbox = QVBoxLayout()
        label = QtWidgets.QLabel("credit card number:")
        label.setFixedHeight(20)
        credit_card = QtWidgets.QLabel(data["card_number"])
        credit_card.setFixedHeight(30)
        label.setBuddy(credit_card)
        # credit_card.setFixedHeight(20)
        cvbox.addWidget(label)
        cvbox.addWidget(credit_card)
        chbox.addLayout(cvbox)

        ehbox = QtWidgets.QHBoxLayout()
        for i in ["exp_m", "exp_y", "cvv"]:
            v = QVBoxLayout()
            # v.setContentsMargins(0, 0,0,0)
            eline = QtWidgets.QLabel(data[i])
            eline.setFixedHeight(30)
            label = QtWidgets.QLabel(i+":")
            label.setFixedHeight(20)
            v.addWidget(label)
            v.addWidget(eline)
            v.addStretch(1)
            ehbox.addLayout(v)
        ehbox.addStretch(0)
        vbox.addLayout(chbox)
        vbox.addLayout(ehbox)

        group.setLayout(vbox)
        group.setFixedHeight(150)
        main.addWidget(group, 0, 0)


    def profile(self, layout):
        vbox = QVBoxLayout()
        group = QWidget(self)
        # H layout for credit card
        chbox = QtWidgets.QHBoxLayout()
        cvbox = QVBoxLayout()

        with open("../profile.json", "r") as jsonFile:
            data = json.load(jsonFile)

        # credit_card.setFixedHeight(20)
        for i in ["Card Holder", "Email", "Phone number", "Addy1", "City", "State", "Postal Code"]:
            label = QtWidgets.QLabel(i+":")
            label.setFixedHeight(20)
            credit_card = QtWidgets.QLabel(data[i.lower().replace(" ", "_")])
            credit_card.setFixedHeight(30)
            cvbox.addWidget(label)
            cvbox.addWidget(credit_card)
        chbox.addLayout(cvbox)
        group.setLayout(chbox)
        layout.addWidget(group, 0, 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Swift()
    sys.exit(app.exec())
