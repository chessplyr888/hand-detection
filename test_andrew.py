import sys
from PyQt4 import QtGui, QtCore



class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
    


    def initUI(self):
        
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')
        

        #perform some action!
        #btn.clicked.connect(QtGui.instance().move(100, 100)) 
   
        
        btn1 = QtGui.QPushButton('Button1', self)
        btn1.resize(btn1.sizeHint())
        btn1.move(100, 50)   
    
        btn2 = QtGui.QPushButton('Button2', self)
        btn2.resize(btn2.sizeHint())
        #btn2.clicked.connect(hello(self.handleButton))
        btn2.move(100, 100)     

        btn3 = QtGui.QPushButton('Button3', self)
        btn3.resize(btn3.sizeHint())
        btn3.move(100, 150)       

        btn4 = QtGui.QPushButton('Button4', self)
        btn4.resize(btn4.sizeHint())
        btn4.move(100, 200)     


        self.setGeometry(300, 300, 350, 350)
        self.setWindowTitle('Tooltips')    
        self.show()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    
    ex2 = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

def on_click():
	print("clicked")
