#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import logging
from tool import isRedisCommand
from executer import Executer
from PyQt4 import QtGui, QtCore

loggerformat ='line:[%(lineno)d] %(asctime)s %(filename)s %(levelname)s %(message)s'

logging.basicConfig(format = loggerformat,
                filename = 'log/gui.log',
                filemode = 'w',
                level = logging.DEBUG)

tabCount = 1

class MainFrame(QtGui.QWidget): 
    """主窗体类，包括一个TextEdit和TableWidget"""
    def __init__(self):
        super(MainFrame, self).__init__()
        global tabCount
        self.fileName = u'newfile%d' % tabCount
        tabCount += 1
        self.filePath = ""
        self.initTextEdit()
        self.buildFrame()
    
    def buildFrame(self):
        vbox = QtGui.QVBoxLayout(self)
        columns = 6
        self.tableWidget = QtGui.QTableWidget(1, columns)
        headerLabels = [x.decode('utf-8') for x in ('',) * columns]
        self.tableWidget.setHorizontalHeaderLabels(headerLabels)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.textEdit)
        splitter.addWidget(self.tableWidget)

        vbox.addWidget(splitter)
        self.setLayout(vbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        self.tableWidget.setVisible(False)

    def initTextEdit(self):
        self.textEdit = QtGui.QTextEdit()
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidget(self.textEdit)



class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.logger = logging.getLogger()
        self.runner = Executer()

        self.setWindowTitle(u'内存数据库')
        self.centralWidget = QtGui.QTabWidget()
        self.tabWidge = QtGui.QTabWidget()
        vbox = QtGui.QVBoxLayout(self)
        
        self.initActionTableWidget()
        self.newFile()
        self.initMenuBar()

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.tabWidge)
        splitter.addWidget(self.actionTableWidget)

        vbox.addWidget(splitter)
        self.centralWidget.setLayout(vbox)
        self.setCentralWidget(self.centralWidget)

        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(screen.width() * 0.3, screen.height() * 0.3, screen.width() * 0.5, screen.height() * 0.6)


    def initActionTableWidget(self):
        self.actionTableWidget = QtGui.QTableWidget(0, 5)
        self.actionCount = 0
        headerLabels = [u'zhuangtai', u'时间', u'语句', u'结果', u'执行时间']
        self.actionTableWidget.setHorizontalHeaderLabels(headerLabels)
        self.actionTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.actionTableWidget.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.actionTableWidget.setVisible(False)


    def initMenuBar(self):
        menubar = self.menuBar()

        # new
        newAction = QtGui.QAction(u'新建', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip(u'新建文件')
        self.connect(newAction, QtCore.SIGNAL('triggered()'), self.newFile)
        
        # open
        openAction = QtGui.QAction(u'打开', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip(u'打开文件')
        self.connect(openAction, QtCore.SIGNAL('triggered()'), self.openFile)

        # save
        saveAction = QtGui.QAction(u'保存', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip(u'保存文件')
        self.connect(saveAction, QtCore.SIGNAL('triggered()'), self.saveFile)

        # saveAs
        saveAsAction = QtGui.QAction(u'另存为', self)
        saveAsAction.setShortcut('Ctrl+Shift+S')
        saveAsAction.setStatusTip(u'另存为')
        self.connect(saveAsAction, QtCore.SIGNAL('triggered()'), self.saveAsFile)

        # closeFile
        closeFileAction = QtGui.QAction(u'关闭', self)
        closeFileAction.setShortcut('Ctrl+W')
        closeFileAction.setStatusTip(u'关闭文件')
        self.connect(closeFileAction, QtCore.SIGNAL('triggered()'), self.closeFile)

        # exit
        exitAction = QtGui.QAction(u'退出', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip(u'退出程序')
        self.connect(exitAction, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))


        file = menubar.addMenu(u'&文件')
        file.addAction(newAction)
        file.addAction(openAction)
        file.addAction(saveAction)
        file.addAction(saveAsAction)
        file.addAction(closeFileAction)
        file.addAction(exitAction)

        # run
        runAction = QtGui.QAction(u'命令', self)
        runAction.setShortcut('Ctrl+R')
        runAction.setStatusTip(u'运行命令')
        self.connect(runAction, QtCore.SIGNAL('triggered()'), self.runCommand)

        # clear
        clearAction = QtGui.QAction(u'清除', self)
        clearAction.setShortcut('Ctrl+D')
        clearAction.setStatusTip(u'清除执行记录')
        self.connect(clearAction, QtCore.SIGNAL('triggered()'), self.clearCommand)

        run = menubar.addMenu(u'&工具')
        run.addAction(runAction)
        run.addAction(clearAction)

        # Help
        helpAction = QtGui.QAction(u'帮助', self)
        helpAction.setShortcut('Ctrl+H')
        helpAction.setStatusTip('获得帮助')
        self.connect(helpAction, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        help = menubar.addMenu(u'&帮助')
        help.addAction(helpAction)

    def newFile(self):
        mainFrame = MainFrame()
        self.tabWidge.addTab(mainFrame, mainFrame.fileName)
        self.tabWidge.setCurrentWidget(mainFrame)

    def openFile(self):
        self.saveFile()
        currentFrame = self.tabWidge.currentWidget()
        currentIndex = self.tabWidge.currentIndex()
        filePath = QtGui.QFileDialog.getOpenFileName(self, u'打开文件')
        if filePath == '':
            return
        fileName = filePath.split('/')[-1]
        self.tabWidge.setTabText(currentIndex, fileName)
        currentFrame.fileName = fileName
        currentFrame.filePath = filePath
        currentFrame.textEdit.clear()

        with open(filePath, "r") as fin:
            while True:
                line = fin.readline()
                if not line:
                    break
                currentFrame.textEdit.append(line.strip("\n"))

    def saveAsFile(self):
        self.saveFile()
        filePath = QtGui.QFileDialog.getOpenFileName(self, u'另存为')
        if not filePath:
            return
        with open(filePath, "w") as fout:
            fout.write(currentFrame.textEdit.toPlainText())

    def saveFile(self):
        currentFrame = self.tabWidge.currentWidget()
        currentIndex = self.tabWidge.currentIndex()
        modified = currentFrame.textEdit.document().isModified()
        fileName = currentFrame.fileName
        filePath = currentFrame.filePath
        
        if not modified:
            return
        if not filePath:
            filePath = QtGui.QFileDialog.getSaveFileName(self, u'保存')
            if not filePath:
                return
            fileName = filePath.split('/')[-1]

        self.tabWidge.setTabText(currentIndex, fileName)
        currentFrame.fileName = fileName
        currentFrame.filePath = filePath
        with open(filePath, "w") as fout:
            fout.write(currentFrame.textEdit.toPlainText())

    def closeFile(self):
        self.saveFile()
        tabCount = self.tabWidge.count()
        currentIndex = self.tabWidge.currentIndex()
        self.tabWidge.removeTab(currentIndex)
        if tabCount == 1:
            self.newFile()

    def addAction(self, action = "", message = "", duration = "", correct = False):
        self.actionTableWidget.setVisible(True)
        self.actionTableWidget.insertRow(self.actionCount)
        currentTime = time.strftime(r"%H:%M:%S", time.localtime())

        png = "icon/yes.png" if correct else "icon/no.png"
        icon = QtGui.QIcon(QtGui.QPixmap(png))

        arglist = ['', currentTime, action, message, duration]
        for i in xrange(len(arglist)):
            content = QtCore.QString.fromUtf8(arglist[i])
            if i:
                self.actionTableWidget.setItem(self.actionCount, i, QtGui.QTableWidgetItem(content))
            else:
                self.actionTableWidget.setItem(self.actionCount, i, QtGui.QTableWidgetItem(icon, ""))
        self.actionCount +=1

    def runCommand(self):
        currentFrame = self.tabWidge.currentWidget()
        text = str(currentFrame.textEdit.toPlainText())

        for action in self.runner.splitCommand(text):
            if isRedisCommand(action):
                durantion = self.runRedisCommand(action)
            else:
                durantion = self.runSQLCommand(action)


    def runRedisCommand(self, command):
        currentFrame = self.tabWidge.currentWidget()
        startTime = time.time()
        success, resultlist = self.runner.executeRedis(command)
        durantion = "%.4lfsec" % (time.time() - startTime)

        if success:
            
        else:
            message = str(resultlist)

        self.addAction(command, message, durantion, success)

    def runSQLCommand(self, command):
        startTime = time.time()
        currentFrame = self.tabWidge.currentWidget()
        success, resultlist = self.runner.executeSQL(command)
        durantion = "%.4lfsec" % (time.time() - startTime)

        self.logger.debug(command)
        self.logger.debug(str(success) + " " + str(resultlist))

        # select * from book
        if success:
            if isinstance(resultlist, list):
                header = [QtCore.QString.fromUtf8(x[0]) for x in resultlist[0]]
                resultlist = resultlist[1:]
                columnCount = len(header)
                rowCount = len(resultlist)
                currentFrame.tableWidget.setVisible(True)
                currentFrame.tableWidget.setColumnCount(columnCount)
                currentFrame.tableWidget.setRowCount(rowCount)
                currentFrame.tableWidget.setHorizontalHeaderLabels(header)
                for i in xrange(rowCount):
                    for j in xrange(columnCount):
                        content = QtCore.QString.fromUtf8(str(resultlist[i][j]))
                        currentFrame.tableWidget.setItem(i, j, QtGui.QTableWidgetItem(content))
                message = "%d rows returned" % rowCount
            else:
                message = "%d rows affected" % resultlist

        else:
            message = str(resultlist)

        self.addAction(command, message, durantion, success)

    def clearCommand(self):
        for i in xrange(self.actionTableWidget.rowCount()):
            self.actionTableWidget.removeRow(0)
        self.actionCount = 0
        self.actionTableWidget.setVisible(False)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
