## Any questions, contact me at christian.orr@diamond.ac.uk

I got fed up of copying code from Designer every time I made updates so found a simple way of separating the UI code from custom changes eg. button clicks, video feeds, threads etc. 

Full repo where this example is taken from: https://github.com/DiamondLightSource/aithre

# Import your python ui file:

see: https://github.com/DiamondLightSource/aithre/blob/3a1c800f2dc52a681bbb18f28b9021a83cf81698/bin/guiv4_2_6beta.py


    from guiv4_2_6beta import Ui_MainWindow


# Set up up in init

    class MainWindow(QtWidgets.QMainWindow):
        zoomChanged = QtCore.pyqtSignal(int)
    
        def __init__(self):
            super(MainWindow, self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)


Can then make all other changes below this, eg:


        self.ui.actionExit.triggered.connect(self.quit)
