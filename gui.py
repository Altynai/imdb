#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class MainFrame(QtGui.QWidget):
	"""docstring for MainFrame"""
	def __init__(self):
		super(MainFrame, self).__init__()
		self.initTextEdit()
		self.buildFrame()
	
	def buildFrame(self):
		hbox = QtGui.QHBoxLayout(self)

		self.bottomFrame = QtGui.QFrame(self)
		self.bottomFrame.setFrameShape(QtGui.QFrame.StyledPanel)

		splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
		splitter.addWidget(self.textEdit)
		splitter.addWidget(self.bottomFrame)

		hbox.addWidget(splitter)
		self.setLayout(hbox)
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))


	def initTextEdit(self):
		self.textEdit = QtGui.QTextEdit()
		self.scrollArea = QtGui.QScrollArea()
		self.scrollArea.setWidget(self.textEdit)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.setWindowTitle('GUI')
        self.initMenuBar()
        self.initFrame()

       	screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width() / 2, screen.height() / 2)

    def initFrame(self):
		self.mainFrame = MainFrame()
		self.setCentralWidget(self.mainFrame)

    def initMenuBar(self):
        menubar = self.menuBar()
    	
    	# open
    	openAciont = QtGui.QAction('Open', self)
    	openAciont.setShortcut('Ctrl+O')
        openAciont.setStatusTip('Open File')
        self.connect(openAciont, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

		# save
    	saveAciont = QtGui.QAction('Save', self)
    	saveAciont.setShortcut('Ctrl+S')
        saveAciont.setStatusTip('Save File')
        self.connect(saveAciont, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        # exit
    	exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        self.connect(exitAction, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))


        file = menubar.addMenu('&File')
        file.addAction(openAciont)
        file.addAction(exitAction)

        # run
        runAciont = QtGui.QAction('Run', self)
    	runAciont.setShortcut('Ctrl+R')
        runAciont.setStatusTip('Run Commands')
        self.connect(runAciont, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        run = menubar.addMenu('&Run')
        run.addAction(runAciont)


        # Help
        helpAciont = QtGui.QAction('Help', self)
    	helpAciont.setShortcut('Ctrl+H')
        helpAciont.setStatusTip('Helps')
        self.connect(helpAciont, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        help = menubar.addMenu('&Help')
        help.addAction(helpAciont)

    def openFile(self, file):
    	self.mainFrame.textEdit.clear()
    	with open(file, "r") as fin:
    		while True:
    			line = fin.readline()
    			if not line:
    				break
    			self.mainFrame.textEdit.append(line)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())