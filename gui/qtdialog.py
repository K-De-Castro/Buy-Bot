import sys
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog)
from  PyQt5 import QtWidgets
from PyQt5 import QtCore

class Form(QDialog):

    def __init__(self, tableWidget, process, parent=None ):
        super(Form, self).__init__(parent)
        self.process = process
        # Create widgets
        self.website = QLineEdit("https://geeksnfreeks.myshopify.com")
        self.keywords = QLineEdit("legend,ink,backpack")
        # self. = QLineEdit("Write my name here")
        self.size = QLineEdit("")

        self.button = QPushButton("Creat Task")
        # Create layout and add widgets
        layout = QVBoxLayout()
        website = QtWidgets.QLabel("Store:")
        layout.addWidget(website)
        layout.addWidget(self.website)
        keywords = QtWidgets.QLabel("Keywords: (seperate wih commas)")
        layout.addWidget(keywords)
        layout.addWidget(self.keywords)
        size = QtWidgets.QLabel("Size:")
        layout.addWidget(size)
        layout.addWidget(self.size)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # rezie window
        self.resize(500, 200)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.tableWidget = tableWidget

        # Add button signal to greetings slot
        self.button.clicked.connect(self.create)

    # Greets the user
    def create(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row+1)
        self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(self.website.text()))
        self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(self.keywords.text()))
        self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(self.size.text()))
        self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem("Idle"))
        self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem("Name"))

        self.process.add_search(self.website.text(), self.keywords.text().split(","), self.size.text())

        self.close()
