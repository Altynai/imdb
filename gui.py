#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from sql import sqlexecuter
from PyQt4 import QtGui, QtCore

class MainFrame(QtGui.QWidget):
    """主窗体类，包括一个TextEdit和TableWidget"""
    def __init__(self):
        super(MainFrame, self).__init__()
        self.initTextEdit()
        self.buildFrame()
    
    def buildFrame(self):
        hbox = QtGui.QHBoxLayout(self)

        columns = 6
        self.tableWidget = QtGui.QTableWidget(1, columns)
        headerLabels = [x.decode('utf-8') for x in ('',) * columns]
        self.tableWidget.setHorizontalHeaderLabels(headerLabels)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.textEdit)
        splitter.addWidget(self.tableWidget)

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
        
        self.currentFile = None
        self.setWindowTitle(u'内存数据库')
        self.initFrame()
        self.initMenuBar()

        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width() / 2, screen.height() / 2)

    def initFrame(self):
        self.mainFrame = MainFrame()
        self.setCentralWidget(self.mainFrame)

    def initMenuBar(self):
        menubar = self.menuBar()
        
        # open
        openAciont = QtGui.QAction(u'打开', self)
        openAciont.setShortcut('Ctrl+O')
        openAciont.setStatusTip(u'打开文件')
        self.connect(openAciont, QtCore.SIGNAL('triggered()'), self.openFile)

        # save
        saveAciont = QtGui.QAction(u'保存', self)
        saveAciont.setShortcut('Ctrl+S')
        saveAciont.setStatusTip(u'保存文件')
        self.connect(saveAciont, QtCore.SIGNAL('triggered()'), self.saveFile)

        # saveAs
        saveAsAciont = QtGui.QAction(u'另存为', self)
        saveAsAciont.setShortcut('Ctrl+Shift+S')
        saveAsAciont.setStatusTip(u'文件另存为')
        self.connect(saveAsAciont, QtCore.SIGNAL('triggered()'), self.saveAsFile)

        # exit
        exitAction = QtGui.QAction(u'退出', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip(u'退出程序')
        self.connect(exitAction, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))


        file = menubar.addMenu(u'&文件')
        file.addAction(openAciont)
        file.addAction(saveAciont)
        file.addAction(saveAsAciont)
        file.addAction(exitAction)

        # run
        runAciont = QtGui.QAction(u'命令', self)
        runAciont.setShortcut('Ctrl+R')
        runAciont.setStatusTip(u'运行命令')
        self.connect(runAciont, QtCore.SIGNAL('triggered()'), self.runCommand)

        run = menubar.addMenu(u'&运行')
        run.addAction(runAciont)


        # Help
        helpAciont = QtGui.QAction(u'帮助', self)
        helpAciont.setShortcut('Ctrl+H')
        helpAciont.setStatusTip('获得帮助')
        self.connect(helpAciont, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        help = menubar.addMenu(u'&帮助')
        help.addAction(helpAciont)

    def openFile(self):
        self.currentFile = QtGui.QFileDialog.getOpenFileName(self, u'打开文件')
        self.mainFrame.textEdit.clear()
        with open(self.currentFile, "r") as fin:
            while True:
                line = fin.readline()
                if not line:
                    break
                self.mainFrame.textEdit.append(line.strip("\n"))

    def saveAsFile(self):
        self.currentFile = QtGui.QFileDialog.getOpenFileName(self, u'另存为')
        self.mainFrame.textEdit.clear()
        with open(self.currentFile, "r") as fin:
            while True:
                line = fin.readline()
                if not line:
                    break
                self.mainFrame.textEdit.append(line)

    def saveFile(self):
        if self.currentFile:
            with open(self.currentFile, "w") as fout:
                fout.write(self.mainFrame.textEdit.toPlainText())

    def runCommand(self):
        sql = self.mainFrame.textEdit.toPlainText()
        runner = sqlexecuter()
        success = False
        resultlist = None
        for sqlcontent in runner.split_sql_text(str(sql)):
            success, resultlist = runner.execute_sql(sqlcontent)
            break
        # select * from book
        if success:
            header = [QtCore.QString.fromUtf8(x[0]) for x in resultlist[0]]
            resultlist = resultlist[1:]
            columnCount = len(header)
            rowCount = len(resultlist)
            self.mainFrame.tableWidget.setColumnCount(columnCount)
            self.mainFrame.tableWidget.setRowCount(rowCount)
            self.mainFrame.tableWidget.setHorizontalHeaderLabels(header)
            for i in xrange(rowCount):
                for j in xrange(columnCount):
                    content = QtCore.QString.fromUtf8(str(resultlist[i][j]))
                    self.mainFrame.tableWidget.setItem(i, j, QtGui.QTableWidgetItem(content))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
