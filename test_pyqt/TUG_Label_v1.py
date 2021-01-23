# coding: utf-8
#---------- conda(tug) env

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


testWindow = uic.loadUiType("mainWin.ui")[0]

class TestWindow (QMainWindow, testWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # 화면에 ui 보여줌
        # self.center()
   
        # event handler 
        self.saveBtn.clicked.connect(self.saveData)
        self.clearBtn.clicked.connect(self.close) #--- close qt 자체적으로 제공
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())






    # event function == slots???
    def saveData(self): # saveBtn 클릭 시
        with open("data.csv", "a", encoding="utf-8") as f:
            s = "%s\n" % (self.nameEdit.text()) # nameEdit 객체에서 text 가져
            f.write(s)
        QMessageBox.information(self, "저장", "성공적으로 저장")

    def closeEvent(self, event):
        self.nameEdit.clear()  # display clear 
        quitCheck = QMessageBox.question(self, 'Quit Message', "정말로 종료할거임?",QMessageBox.Yes | QMessageBox.No , QMessageBox.No)
        if quitCheck == QMessageBox.No:
            event.ignore()

        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_window = TestWindow()
    test_window.show()
    app.exec_()  # event loop 생성 (slots) 