# coding: utf-8
#---------- conda(tug) env

import sys, os
from PyQt5.QtWidgets import *  
from PyQt5.QtCore import *  # Qt ; to use keyboard hanlder 
from PyQt5.QtGui import * # QKeySequence, QShortcut
from PyQt5 import uic  # to convert ".ui" to ".py"



mainGui = uic.loadUiType('TUG_Labeling_v1.ui')[0]


class MainWindow (QMainWindow, mainGui):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # 화면에 ui 보여줌
        self.center()

        self.trialFolder = None
        self.actionImagelist = [0,0,0,0,0,0]  

        
        self.actionDisplay.setText(str(self.actionImagelist[0])) 
        self.directory_path = QFileDialog.getExistingDirectory(None, '              !!!  Find arragnedData folder !!!', os.getcwd(), QFileDialog.ShowDirsOnly)

        self.objectInit()
               
    def center(self):   # 모니터 해상도 읽고, 중앙에 UI display
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())    



    def keyPressEvent(self, event):  # 
        self.keyState = event.key()
        if event.key() == Qt.Key_Escape:
            self.close()

        elif event.key() == Qt.Key_S:
            print(" [Fix this part] Save Data --- key event")
            self.saveData()
            self.actionFunction(mode ='reset')

        elif event.key() in [Qt.Key_Return, Qt.Key_Enter]: 
            self.listItemClick()  
            self.directory.setEnabled(True)


        elif event.key() == Qt.Key_1:   # Action Selection
            self.startMove_Btn.setChecked(True)
            self.actionFunction()
            print( " [0] Start Move: ", self.imageIndexDisplay.text())

        elif event.key() == Qt.Key_2:
            self.startWalk_Btn.setChecked(True)
            self.actionFunction()
            print( " [1] Start Walking: " , self.imageIndexDisplay.text())

        elif event.key() == Qt.Key_3:
            self.startTurn_Btn.setChecked(True)
            self.actionFunction()
            print( " [2] Start Turning: " , self.imageIndexDisplay.text())
        elif event.key() == Qt.Key_4:
            self.endTurn_Btn.setChecked(True)
            self.actionFunction()
            print( " [3] End Turning: " , self.imageIndexDisplay.text())

        elif event.key() == Qt.Key_5:
            self.startSit_Btn.setChecked(True)
            self.actionFunction()
            print( " [4] Start Sitting: " , self.imageIndexDisplay.text())

        elif event.key() == Qt.Key_6:
            self.endSit_Btn.setChecked(True)
            self.actionFunction()
            print( " [5] End Sitting: " , self.imageIndexDisplay.text())
            


    def objectInit(self): 
        # Init. Folder Open Button
        self.saveBtn.clicked.connect(self.saveData)
   
        # Init. Action Selection Group Button
        self.startMove_Btn.clicked.connect(self.actionFunction)
        self.startWalk_Btn.clicked.connect(self.actionFunction)
        self.startTurn_Btn.clicked.connect(self.actionFunction)
        self.endTurn_Btn.clicked.connect(self.actionFunction)
        self.startSit_Btn.clicked.connect(self.actionFunction)
        self.endSit_Btn.clicked.connect(self.actionFunction)

        # Init. QlistWidget 
        self.directory.itemDoubleClicked.connect (self.listItemClick)
        self.directory.currentItemChanged.connect(self.imageDisplay)
        self.list_reset()
        self.show()


    def imageDisplay(self):
        itemRow = self.directory.currentItem()
        if itemRow is not None:
            currentItem = self.directory.currentItem().text()
            print("Current Item : " + currentItem)
            if ".jpg" in currentItem:
               # imageFile = self.directory.currentItem().text()
                self.imageIndexDisplay.setText(currentItem)

                imageDir = self.pathDisplay.text() 
                selectedImage = os.path.join(imageDir,currentItem )
                print("Selected Image", selectedImage)

                imageView = QLabel(self)
                imageView.setGeometry( 100, 150, 1400, 800)
                pixmap = QPixmap(selectedImage)
                pixmapResize = pixmap.scaled(1400,800, Qt.KeepAspectRatio)
                imageView.setPixmap(pixmapResize)
                imageView.show()
            

    def listItemClick(self):
        clicked_item = self.directory.currentItem().text()       
        print("Current Folders (double Clicked) : " + str(clicked_item ) )

        if clicked_item == '..':
            self.directory_path = self.directory_outer(self.directory_path )
            self.list_reset()
        else:
            moved = self.directory_inner(self.directory_path , clicked_item)
            if moved != self.directory_path :
                self.directory_path = moved
            self.list_reset()

        
        self.pathDisplay.setText(self.directory_path)

    def dir(self, path):
        return os.path.isdir(path) and [".."] + os.listdir(path) or ''

    def list_reset(self):
        self.listViewClear()
        dirs = self.dir(self.directory_path)
        for dir in dirs:
            self.directory.addItem(str(dir))

    def listViewClear(self):
        self.directory.clear()

    def directory_outer(self, path):
        dir_path_splits = path.split("\\")[:-1]
        return "\\".join(dir_path_splits)

    def directory_inner(self, cur_path, dir):
        moved = "%s\%s" % (cur_path, dir)
        if os.path.isdir(moved):
            return moved
        else:
            return cur_path 

    def actionFunction(self, mode = 'action'):
        if mode =='reset':
            self.actionImagelist = [0,0,0,0,0,0]  
            self.startMove_Btn.setChecked(True)

            self.startMove_Btn.setText("Start Move (1): ")
            self.startWalk_Btn.setText("Start Walking (2): ")
            self.startTurn_Btn.setText("Start Turning (3): ")
            self.endTurn_Btn.setText("End Turn (4): ")
            self.startSit_Btn.setText("Start Sit (5): ")
            self.endSit_Btn.setText("End Sit (6): ")


        if  self.startMove_Btn.isChecked() and mode == 'action':
            self.actionImagelist[0] = self.imageIndexDisplay.text()
            self.startMove_Btn.setText("Start Move (1): " +  self.imageIndexDisplay.text() )

        elif  self.startWalk_Btn.isChecked() and mode == 'action':
            self.actionImagelist[1] = self.imageIndexDisplay.text()
            self.startWalk_Btn.setText("Start Walking (2): " +  self.imageIndexDisplay.text() )

        elif  self.startTurn_Btn.isChecked() and mode == 'action':
            self.actionImagelist[2] = self.imageIndexDisplay.text()
            self.startTurn_Btn.setText("Start Turning (3): " +  self.imageIndexDisplay.text() )

        elif  self.endTurn_Btn.isChecked():
            self.actionImagelist[3] = self.imageIndexDisplay.text()
            self.endTurn_Btn.setText("End Turn (4): " +  self.imageIndexDisplay.text() )

        elif  self.startSit_Btn.isChecked() and mode == 'action':
            self.actionImagelist[4] = self.imageIndexDisplay.text()
            self.startSit_Btn.setText("Start Sit (5): " +  self.imageIndexDisplay.text() )

        elif  self.endSit_Btn.isChecked() and mode == 'action':
            self.actionImagelist[5] = self.imageIndexDisplay.text()
            self.endSit_Btn.setText("End Sit (6): " +  self.imageIndexDisplay.text() )
        self.actionDisplay.setText(self.imageIndexDisplay.text() )
   
    def saveData(self): # saveBtn 클릭 시
        dirList = self.directory_path.split("\\")   # [ D:/~~/arrangeData , sideView, 2020_11_03, 'bys' , 001]
        print(dirList)

        self.save_path = os.path.join( dirList[0] ,'saveResults' ) #, dirList[1], dirList[2], dirList[3] )
        os.chdir(dirList[0])

        if os.path.isdir(self.save_path):
            print("Save Root: ",self.save_path )
        else:
            os.mkdir('saveResults')
       
        for i in range(1,5,1):
            os.chdir(self.save_path)
            self.save_path = os.path.join(self.save_path, dirList[i])
            if os.path.isdir(self.save_path):
                print("Save Root: ",self.save_path )
            else:
                os.mkdir(dirList[i])


        os.chdir(self.save_path)
        fileName = dirList[3] + "_" + dirList[4] +".csv"
        print("Saved File Name: ", fileName)
        fileList = os.listdir(self.save_path) 

        if fileName in fileList:
            os.remove(fileName)

        with open(self.save_path +"/" + fileName, "a", encoding="utf-8") as f:
            header = "startMove,startWalk,startTurn,endTurn,startSit,endSit\n"
            f.write(header)
            data ="%s,%s,%s,%s,%s,%s\n" %  (self.actionImagelist[0], self.actionImagelist[1],self.actionImagelist[2],self.actionImagelist[3],self.actionImagelist[4],self.actionImagelist[5])
            f.write(data)
        
        os.chdir(self.directory_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_window = MainWindow()
    test_window.show()
    app.exec_()  # event loop 생성 (slots) 