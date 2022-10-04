import sys

from qgis.PyQt import QtWidgets

class NgisInputTypeDialog(QtWidgets.QWidget):
    
    item = None
    ok = False
    
    def __init__(self, options):
        super().__init__()
        self.initUI(options)

    # def initUI(self, options):
    #     self.btn = QtWidgets.QPushButton('Show Dialog', self)
    #     self.btn.move(20, 20)
    #     self.btn.clicked.connect(self.showDialog)

    #     self.le = QtWidgets.QLineEdit(self)
    #     self.le.move(130, 22)

    #     self.setGeometry(300, 300, 300, 150)
    #     self.setWindowTitle('Input Dialog')        
    #     self.show()

    # def showDialog(self):
    #     text, ok = QtWidgets.QInputDialog.getText(self, 'input dialog', 'Is this ok?')
    #     if ok:
    #         self.le.setText(str(text))
    
    def initUI(self, options):
        self.item, self.ok = QtWidgets.QInputDialog.getItem(self, "Avgrensingslinje", "Spesifisér type avgrensingslinje", options, 0, False)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = NgisInputTypeDialog()
    sys.exit(app.exec_())