# -*- coding: utf-8 -*-
import csv
import resources_rc
import sys
'''from docx import Document
from docx.shared import Inches'''
from PyQt4.QtGui import *
from qgis.gui import *
from qgis.core import *
from PyQt4.QtGui import QCursor, QPixmap
from PyQt4.QtCore import *
from qgis.gui import *
from PyQt4.QtGui import QAction, QMainWindow
from PyQt4.QtCore import SIGNAL, Qt, QPointF, QUrl, QVariant
import os
import psycopg2
import json
import urllib2
import requests
from PIL import Image
from PIL import ImageQt
from StringIO import StringIO
import qgis.analysis
import os

LIST_LAYERS = [u"вузли Топології КТБ"]
TEST_URL = 'https://10.112.129.171'
#Class of window that appear when we click on CTV
class ScrollArea( QScrollArea):
    def __init__(self, parent=None):
        super(ScrollArea, self).__init__(parent=parent)

    def resizeEvent(self, event):
        #print(event.size().width())
        pass
class Widget( QWidget):
    def __init__(self):
        super( QWidget,self).__init__()
        self.currentRectLeft = None
        self.currentRectRight = None
        self.setFixedSize(3000, 3000)
        self.lay =  QVBoxLayout()
        self.btn =  QPushButton()
        self.lay.addWidget(self.btn)
        self._im =  QImage(self.width(), self.height(),  QImage.Format_ARGB32)
        self._im.fill( QColor("white"))
        self.imageLabel =  QLabel()
        self.imageLabel.setPixmap( QPixmap.fromImage(self._im))
        self.lay.addWidget(self.imageLabel)
        self.currentNumberLeft = None
        self.currentNumberRight = None
    def paintScene(self,arrayLeft,arrayRight):
        painter =  QPainter(self._im)
        self.arrayLeft = arrayLeft
        self.arrayRight = arrayRight
        #self.orient = orient
        for i in range(len(self.arrayLeft)):
            if int(i)==int(self.arrayLeft[i][0]):
                painter.setPen( QPen( QColor("#fc6c2d"), 1,  Qt.SolidLine,  Qt.RoundCap))
                painter.setBrush( QBrush( QColor("#fc6c2d"),  Qt.SolidPattern))
                painter.drawRect(0,93+i*180, 20, 15)
                painter.setPen( QPen( QColor("#000000"), 1,  Qt.SolidLine,  Qt.RoundCap))
                painter.setBrush( QBrush( QColor("#fc6c2d"),  Qt.SolidPattern))
                painter.drawRect(20,20+i*180, 50, 155)
                r=  QRectF (20,20+i*180, 50, 155)
                painter.drawText(r, Qt.AlignCenter,str(i))
                painter.setPen( QPen( QColor("#000000"), 1,  Qt.SolidLine,  Qt.RoundCap))
                painter.setBrush( QBrush( QColor("yellow"),  Qt.SolidPattern))
                for j in range(len(self.arrayLeft[i][2])):
                    painter.drawRect(70,20+self.arrayLeft[i][2][j]*20+i*180, 15, 15)
                    r1 =  QRectF (70,20+self.arrayLeft[i][2][j]*20+i*180, 15, 15)
                    painter.drawText(r1, Qt.AlignCenter,str(self.arrayLeft[i][2][j]))
        for i in self.conn_array:
            painter.drawLine(85,20+i[0][0]*20+i[0][1]*180,605,35+i[1][0]*20+180*i[1][1])

        for i in range(len(self.arrayRight)):
            if int(i)==int(self.arrayRight[i][0]):
                print "hello"
                painter.setPen( QPen( QColor("#fc6c2d"), 1,  Qt.SolidLine,  Qt.RoundCap))
                painter.setBrush( QBrush( QColor("#fc6c2d"),  Qt.SolidPattern))
                painter.drawRect(670,93+i*180, 20, 15)
                painter.setPen( QPen( QColor("#000000"), 1,  Qt.SolidLine,  Qt.RoundCap))
                painter.setBrush( QBrush( QColor("#fc6c2d"),  Qt.SolidPattern))
                painter.drawRect(620,20+i*180, 50, 155)
                r=  QRectF (620,20+i*180, 50, 155)
                painter.drawText(r, Qt.AlignCenter,str(i))
                painter.setPen( QPen( QColor("#000000"), 1,  Qt.SolidLine,  Qt.RoundCap))
                painter.setBrush( QBrush( QColor("yellow"),  Qt.SolidPattern))
                for j in range(len(self.arrayRight[i][2])):
                    painter.drawRect(605,20+self.arrayRight[i][2][j]*20+i*180, 15, 15)
                    r1 =  QRectF (605,20+self.arrayRight[i][2][j]*20+i*180, 15, 15)
                    painter.drawText(r1, Qt.AlignCenter,str(self.arrayRight[i][2][j]))
        painter.end()
        self.update()
    def mouseReleaseEvent(self, event):
        x=event.pos().x()
        y=event.pos().y()
        self.painter =  QPainter(self._im)
        self.painter.setPen( QPen( QColor("white"), 1,  Qt.SolidLine,  Qt.RoundCap))
        self.painter.setBrush( QBrush( QColor("red"),  Qt.SolidPattern))
        for i in range(len(self.arrayLeft)):
            if i==self.arrayLeft[i][0]:
                for j in range(len(self.arrayLeft[i][2])):
                    if (x>=70) and (x<=85) and (y>=20+self.arrayLeft[i][2][j]*20+i*180) and (y<=35+self.arrayLeft[i][2][j]*20+i*180):
                        if self.currentRectLeft!=None:
                            self.painter.drawRect(70,20+self.arrayLeft[i][2][j]*20+i*180, 15, 15)
                            r1 =  QRectF (70,20+self.arrayLeft[i][2][j]*20+i*180, 15, 15)
                            self.painter.drawText(r1, Qt.AlignCenter,str(self.arrayLeft[i][2][j]))
                            self.painter.setPen( QPen( QColor("#000000"), 1,  Qt.SolidLine,  Qt.RoundCap))
                            self.painter.setBrush( QBrush( QColor("yellow"),  Qt.SolidPattern))
                            self.painter.drawRect(70,20+20*self.currentRectLeft+self.currentNumberLeft*180, 15, 15)
                            r1 =  QRectF (70,20+self.currentRectLeft*20+self.currentNumberLeft*180, 15, 15)
                            self.painter.drawText(r1, Qt.AlignCenter,str(self.currentRectLeft))
                            self.currentRectLeft=self.arrayLeft[i][2][j]
                            self.currentNumberLeft=i
                        else:
                            self.currentRectLeft=self.arrayLeft[i][2][j]
                            self.currentNumberLeft=i
                            self.painter.drawRect(70,20+self.arrayLeft[i][2][j]*20+i*180, 15, 15)
                            r1 =  QRectF (70,20+self.arrayLeft[i][2][j]*20+i*180, 15, 15)
                            self.painter.drawText(r1, Qt.AlignCenter,str(self.arrayLeft[i][2][j]))
        for i in range(len(self.arrayRight)):
            if i==self.arrayRight[i][0]:
                for j in range(len(self.arrayRight[i][2])):
                    if (x>=605) and (x<=620) and (y>=20+self.arrayRight[i][2][j]*20+i*180) and (y<=35+self.arrayRight[i][2][j]*20+i*180):
                        if self.currentRectRight!=None:
                            self.painter.drawRect(605,20+self.arrayRight[i][2][j]*20+i*180, 15, 15)
                            r1 =  QRectF (605,20+self.arrayRight[i][2][j]*20+i*180, 15, 15)
                            self.painter.drawText(r1, Qt.AlignCenter,str(self.arrayRight[i][2][j]))
                            self.painter.setPen( QPen( QColor("#000000"), 1,  Qt.SolidLine,  Qt.RoundCap))
                            self.painter.setBrush( QBrush( QColor("yellow"),  Qt.SolidPattern))
                            self.painter.drawRect(605,20+20*self.currentRectRight+self.currentNumberRight*180, 15, 15)
                            r1 =  QRectF (605,20+20*self.currentRectRight+self.currentNumberRight*180, 15, 15)
                            self.painter.drawText(r1, Qt.AlignCenter,str(self.currentRectRight))
                            self.currentRectRight=self.arrayRight[i][2][j]
                            self.currentNumberRight=i
                        else:
                            self.currentRectRight=self.arrayRight[i][2][j]
                            self.currentNumberRight=i
                            self.painter.drawRect(605,20+self.arrayRight[i][2][j]*20+i*180, 15, 15)
                            r1 =  QRectF (605,20+20*self.currentRectRight+self.currentNumberRight*180, 15, 15)
                            self.painter.drawText(r1, Qt.AlignCenter,str(self.currentRectRight))
        self.painter.end()
        self.update()
    def paintEvent(self, event):
        painter =  QPainter(self)
        painter.drawImage(0, 0, self._im)
        painter.end()

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.widget = Widget()
        self.widget.conn_array=[]
        muft1=[0,7,[0,1,2,3,5,6,7]]
        muft2=[1,8,[0,1,2,3,4,5,6,7]]
        muft3=[0,6,[0,1,3,4,6,7]]
        self.widget.leftArray=[muft1,muft2]
        self.widget.rightArray=[muft3]
        self.widget.widget = Widget()
        self.widget.paintScene([muft1,muft2],self.widget.rightArray)
        #widget.paintScene(2,False)
        #widget.show()
        self.paintDialog = QMainWindow()
        self.paintDock = QDockWidget()
        self.paintScroll = ScrollArea()
        self.paintDock.setAllowedAreas(Qt.TopDockWidgetArea | Qt.RightDockWidgetArea)
        self.btn_conn = QPushButton("Connect")
        self.btn_conn.clicked.connect(self.CreateConn)
        self.btn_del = QPushButton("Delete connect")
        self.btn_del.clicked.connect(self.DeleteConn)
        self.btn_add_mft = QPushButton("Add Mft")
        self.btn_add_mft.clicked.connect(self.addMuftEvent)
        self.btn_del_mft = QPushButton("Delete Mft")
        self.btn_del_mft.clicked.connect(self.deleteMftLeft)
        self.tmpwdg = QWidget()
        self.tmplay = QVBoxLayout()
        self.tmplay.addWidget(self.btn_conn)
        self.tmplay.addWidget(self.btn_del)
        self.tmplay.addWidget(self.btn_add_mft)
        self.tmplay.addWidget(self.btn_del_mft)
        self.tmpwdg.setLayout(self.tmplay)
        self.paintDock.setWidget(self.tmpwdg)
        self.paintDialog.addDockWidget(Qt.RightDockWidgetArea, self.paintDock)
        self.paintScroll.setWidget(self.widget)
        self.paintDialog.setCentralWidget(self.paintScroll)
        self.widget.update()
        #self.paintDialog.show()
        self.names= []
        self.values = []
        self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle("Схема зварок".decode("utf-8"))

        self.dock = QDockWidget("information")
        self.dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.infoList = QTreeWidget()
        self.infoList.setColumnCount(1)
        header=QTreeWidgetItem(["Feature","Value"])
        self.infoList.setHeaderItem(header)

        self.leftDock = QDockWidget("Files")
        self.fileList = QListWidget()
        self.leftDock.setWidget(self.fileList)
        self.leftDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.leftDock)

        self.left = QAction(QIcon(':/plugins/MuftInfo/left.png'), 'Move left', self)
        self.left.setShortcut('Ctrl+Left')
        self.toolbar = self.addToolBar('Move left')
        self.toolbar.addAction(self.left)

        self.right = QAction(QIcon(':/plugins/MuftInfo/right.png'), 'Move right', self)
        self.right.setShortcut('Ctrl+Right')
        self.toolbar = self.addToolBar('Move right')
        self.toolbar.addAction(self.right)

        self.conn = QAction(QIcon(':/plugins/MuftInfo/conn.png'), 'New connection', self)
        self.conn.setShortcut('Ctrl+N')
        self.toolbar = self.addToolBar('New connection')
        self.toolbar.addAction(self.conn)
        self.conn.triggered.connect(self.CreateConnEvent)

        self.plus = QAction(QIcon(':/plugins/MuftInfo/plus.png'), 'Zoom +', self)
        self.plus.setShortcut(Qt.CTRL + Qt.Key_Plus)
        self.toolbar = self.addToolBar('Zoom +')
        self.toolbar.addAction(self.plus)

        self.minus = QAction(QIcon(':/plugins/MuftInfo/minus.png'), 'Zoom -', self)
        self.minus.setShortcut(Qt.CTRL + Qt.Key_Minus)
        self.toolbar = self.addToolBar('Zoom -')
        self.toolbar.addAction(self.minus)

        self.printer = QAction(QIcon(':/plugins/MuftInfo/printer.png'), 'Print', self)
        self.printer.setShortcut('Ctrl+P')
        self.toolbar = self.addToolBar('Print')
        self.toolbar.addAction(self.printer)


        self.help = QAction(QIcon(':/plugins/MuftInfo/info.png'), 'Help', self)
        self.help.setShortcut('Ctrl+H')
        self.toolbar = self.addToolBar('Help')
        self.toolbar.addAction(self.help)
        self.Picture = QLabel()
        self.Picture.setAlignment(Qt.AlignCenter)
        self.scroll = QScrollArea()
        self.childrenMenu = QMenu(self)
        self.childrenMenu.setStyleSheet("QMenu::item:selected {border-color: darkblue;background: rgba(100, 100, 100, 150);}")

        self.parentsMenu = QMenu(self)
        self.parentsMenu.setStyleSheet("QMenu::item:selected {border-color: darkblue;background: rgba(100, 100, 100, 150);}")

        self.printerMenu = QMenu(self)
        self.printerMenu.setStyleSheet("QMenu::item:selected {border-color: darkblue;background: rgba(100, 100, 100, 150);}")

        self.scroll.setWidgetResizable(True)
        self.setCentralWidget(self.scroll)
        self.help.triggered.connect(self.helpWindow)
        self.right.triggered.connect(self.menuChildrenSlot)
        self.left.triggered.connect(self.menuParentsSlot)
        self.printer.triggered.connect(self.menuPrinterSlot)
        self.label = QLabel()
        self.dock.setWidget(self.infoList)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)

        self.saveImage = QAction (u"Зберегти схему...",self)
        self.saveImageName = ''
        self.saveImage.triggered.connect(self.saveImageSlot)

        self.saveInfo = QAction (u"Зберегти інформацію...",self)
        self.saveInfo.triggered.connect(self.saveInfoSlot)


        self.menubar = self.menuBar()
        File = self.menubar.addMenu('&File')
        File.addAction(self.saveImage)
        File.addAction(self.saveInfo)
        Tools = self.menubar.addMenu('&Tools')
        Tools.addAction(self.left)
        Tools.addAction(self.right)
        Tools.addAction(self.plus)
        Tools.addAction(self.minus)
        Tools.addAction(self.conn)
    def addMuftEvent(self):
        dial = QDialog()
        lay = QGridLayout()
        lbl = QLabel("Smth")
        com = QComboBox()
        #var1 = QRadioButton
        lay.addWidget(lbl,1,0)
        lay.addWidget(com,1,1)
        dial.setLayout(lay)
        btn_ok = QPushButton("Create")
        btn_cancel = QPushButton("Cancel")
        lay.addWidget(btn_ok,2,0)
        lay.addWidget(btn_cancel,2,1)
        dial.exec_()
        pass
    def CreateConnEvent(self):
        self.paintDialog.show()
    def CreateConn(self):
        flag = True
        currentConn = [[self.widget.currentNumberLeft,self.widget.currentRectLeft],[self.widget.currentNumberRight,self.widget.currentRectRight]]
        for i in self.widget.conn_array:
            #print j,"    ",currentConn[0],"     ",currentConn[1]
            if currentConn[0]==i[0] or currentConn[1]==i[1]:
                flag=False
                break
        self.widget.painter = QPainter(self.widget._im)
        if flag:
            self.widget.conn_array.append(currentConn)
            self.widget.painter.drawLine(85,20+self.widget.currentRectLeft*20+self.widget.currentNumberLeft*180,605,35+self.widget.currentRectRight*20+180*self.widget.currentNumberRight)
        self.widget.update()
        self.widget.painter.end()
    def DeleteConn(self):
        self.widget.painter = QPainter(self.widget._im)
        currentConn = [[self.widget.currentNumberLeft,self.widget.currentRectLeft],[self.widget.currentNumberRight,self.widget.currentRectRight]]
        self.widget.conn_array.remove(currentConn)
        self.widget.painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine, Qt.RoundCap))
        self.widget.painter.drawLine(85,20+self.widget.currentRectLeft*20+self.widget.currentNumberLeft*180,605,35+self.widget.currentRectRight*20+165*self.widget.currentNumberRight)
        self.widget.update()
        self.widget.painter.end()
    def addMftLeft(self):
        maxIndex = 0
        for i in self.widget.leftArray:
            if maxIndex<i[0]:
                maxIndex=i[0]
        if len(self.widget.leftArray)>0:
            newMuft = [maxIndex+1,8,[0,1,2,3,4,5,6,7]]
        else:
            newMuft = [maxIndex,8,[0,1,2,3,4,5,6,7]]
        self.widget.leftArray.append(newMuft)
        self.widget.update()
        self.widget.paintScene(self.widget.leftArray,self.widget.rightArray)

    def deleteMftLeft(self):
        j=0
        for i in self.widget.leftArray:
            if self.widget.currentNumberLeft==i[0]:
                break
            j+=1
        tmp_arr=[]
        tmp_arr.extend(self.widget.conn_array)
        #print conn_array
        for i in tmp_arr:
            #print "lalalala     "+str(i)
            if i[0][0]==j:
                tmp=self.widget.currentNumberLeft
                tmptmp = self.widget.currentRectLeft
                tmp1 = self.widget.currentNumberRight
                tmptmp1 = self.widget.currentRectRight
                self.widget.currentNumberLeft=i[0][0]
                self.widget.currentRectLeft=i[0][1]
                self.widget.currentNumberRight=i[1][0]
                self.widget.currentRectRight=i[1][1]
                self.DeleteConn()
                self.widget.currentNumberLeft=tmp
                self.widget.currentRectLeft=tmptmp
                self.widget.currentNumberRight=tmp1
                self.widget.currentRectRight=tmptmp1

        if len(self.widget.leftArray)-1!=j:
            self.widget.leftArray[j+1][0]=self.widget.currentNumberLeft

        self.widget.leftArray.pop(j)
        painter = QPainter(self.widget._im)
        painter.setPen(QPen(QColor("white"), 1, Qt.SolidLine, Qt.RoundCap))
        painter.setBrush(QBrush(QColor("white"), Qt.SolidPattern))
        painter.drawRect(0,0, 85, 3000)
        self.widget.currentNumberLeft = None
        self.widget.currentRectLeft = None
        painter.end()
        self.widget.paintScene(self.widget.leftArray,self.widget.rightArray)

    def saveImageSlot(self):
        tmp = QFileDialog.getSaveFileName(self,"Save File","/home/"+self.saveImageName,"Images (*.png *.xpm *.jpg)")

        self.Picture.pixmap().save(tmp)

    def saveInfoSlot(self):
        rowdata = []
        for i in range(len(self.names)):
            self.names[i] = self.names[i].encode("utf-8")
        for i in range(len(self.values)):
            self.values[i] = self.values[i].encode("utf-8")
        rows = zip(self.names,self.values)
        tmp = QFileDialog.getSaveFileName(self,"Save File","/home/untitled.csv","CSV Files(*.csv)")
        with open(unicode(tmp), 'wb') as stream:
            writer = csv.writer(stream)
            for i in rows:
                writer.writerow(i)

    #menu with children when we ckick on move right
    def menuChildrenSlot(self):
        self.childrenMenu.exec_(QCursor.pos())
        pass
    def menuParentsSlot(self):
    #menu with parents when we click on move left
        self.parentsMenu.exec_(QCursor.pos())
        pass
    #menu with printers
    def menuPrinterSlot(self):
        self.printerMenu.exec_(QCursor.pos())
        pass
    #here we create help window for users
    def helpWindow(self):
        self.helpwnd = QDialog()
        self.helpwnd.lay = QHBoxLayout(self.helpwnd)
        self.helpwnd.setWindowTitle("Help")
        varList =  QListWidget()
        varList.setStyleSheet("QListWidget {show-decoration-selected: 1;} QListWidget::item{height:50;} QListWidget::item:alternate {background: #EEEEEE;} QListWidget::item:selected {} QListWidget::item:selected:!active {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #cce6ff, stop: 1 #99ccff);} QListWidget::item:selected:active {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #cce6ff, stop: 1 #99ccff);} QListView::item:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #FAFBFE, stop: 1 #DCDEF1); padding-left:10px;}")
        QListWidgetItem("Printer",varList)
        QListWidgetItem("Left",varList)
        QListWidgetItem("Right",varList)
        QListWidgetItem("About",varList)
        self.textOfHelp = QTextEdit()
        self.textOfHelp.setReadOnly(True)
	self.printerText = "<b>Printer</b> <br> <br> Choose a printer through the given list of connected printers and print photo using him."
        self.leftText = "<b>Left button</b> <br> <br> Choose parent object through the given list - click on it to move there."
        self.rightText = "<b>Right button</b> <br> <br> Choose child object through the given list - click on it to move there."
        self.aboutText = "<b>About</b> <br> <br> This plugin is used to check/change Layout scheme of CTV objects OR to check detailed pits info.<br> TODO: create connections between CTV objects and make physical lines in qgis using them."
        varList.itemClicked.connect(self.helpVar)
        self.helpwnd.lay.addWidget(varList)
        self.helpwnd.lay.addWidget(self.textOfHelp)
        self.helpwnd.resize(600,400)
        self.helpwnd.exec_()
        pass
    #slot for help window, its will change text of help
    def helpVar(self,item):
        self.textOfHelp.clear()
        if item.text()=="Printer":
            self.textOfHelp.append(self.printerText)
        elif item.text()=="Left":
            self.textOfHelp.append(self.leftText)
        elif item.text()=="Right":
            self.textOfHelp.append(self.rightText)
        elif item.text()=="About":
            self.textOfHelp.append(self.aboutText)
class NearestFeatureMapTool(QgsMapToolIdentify,):
    chosen_item=None
    parents = None
    children = None
    text = None
    printers = None
    windows_emount = 0
    print_image = None
    ourLayer = None
    workLayer  = 0
    def __init__(self, canvas):
        self.canvas = canvas
        self.wnd = mainWindow()

        QgsMapToolIdentify.__init__(self, canvas)
        self.cursor = QCursor(Qt.WhatsThisCursor)
        self.ctv_all=[]
        self.kol_all=[]
        self.zoomArray={}
        self.counterOfZoom=None
        self.already_connected = True
        self.empty_info_image = QPixmap(":/plugins/MuftInfo/patrik.png")
        #nammme = u"Топологія КТБ"
        nammme = LIST_LAYERS[0]
        l = QgsMapLayerRegistry.instance().mapLayersByName(nammme)
        def bla0(i):
            try:
                if (i.attribute("cubic_name")==u"Кросс-муфта" or i.attribute("cubic_name")==u"Магистральный распределительный узел" or i.attribute("cubic_name")==u"Оптический узел" or i.attribute("cubic_name") == u"Оптичний приймач" or i.attribute("cubic_name") == u"Передатчик оптический"):
                    return True
            except KeyError:
                pass
            return False
        for r in l:
            self.ctv_all = filter(lambda i: bla0(i), r.getFeatures())

        nammme = u"Колодязі КК"
        l = QgsMapLayerRegistry.instance().mapLayersByName(nammme)
        def bla(i):
            for j in i.fields():
                try:
                    if j.name() == "pit_short_description":
                        return True
                except:
                    pass
            return False
        for r in l:
            self.kol_all = filter(lambda i:bla(i), r.getFeatures())

    def activate(self):
        self.canvas.setCursor(self.cursor)


    def screenToLayerCoords(self, screenPos, layer):
        transform = self.canvas.getCoordinateTransform()
        canvasPoint = QgsMapToPixel.toMapCoordinates(   transform,
                                                        screenPos.x(),
                                                        screenPos.y() )

        layerEPSG = layer.crs().authid()
        projectEPSG = self.canvas.mapRenderer().destinationCrs().authid()
        if layerEPSG != projectEPSG:
            renderer = self.canvas.mapRenderer()
            layerPoint = renderer.mapToLayerCoordinates(    layer,
                                                            canvasPoint )
        else:
            layerPoint = canvasPoint
        # Convert this point (QgsPoint) to a QgsGeometry
        return QgsGeometry.fromPoint(layerPoint)


    def itemSearch(self,c_p):
        self.counterOfZoom = 8
        if self.workLayer == 1:
            for i in self.ctv_all:
                if i.attribute("cubic_code")==c_p and i.attribute("cubic_ou_name")!="":
                    self.feat = i
                    ids=[]
                    ids.append(i.id())
                    self.results[0].mLayer.setSelectedFeatures(ids)
                    self.canvas.zoomToSelected(self.results[0].mLayer)
                    self.pic()
        elif self.workLayer == 2:
            for i in self.kol_all:
                if str(i.attribute("pit_id"))==c_p:
                    self.feat = i
                    ids=[]
                    ids.append(i.id())
                    self.results[0].mLayer.setSelectedFeatures(ids)
                    self.canvas.zoomToSelected(self.results[0].mLayer)
                    self.pic()

    def parentsEvent(self, Action):
        self.chosen_item=Action.text()[0:Action.text().find(" ")]
        self.itemSearch(Action.text()[0:Action.text().find(" ")])

    def childrenEvent(self, Action):
        self.chosen_item=Action.text()[0:Action.text().find(" ")]
        self.itemSearch(Action.text()[0:Action.text().find(" ")])

    def Print(self, Action):
        self.chosen_printer = Action.text().encode("utf-8")
        self.chosen_printer = str(self.chosen_printer)
        self.chosen_printer = self.chosen_printer.decode("utf-8")
        #self.wnd.setWindowTitle(self.chosen_printer)
        for i in self.printers:
            name = i.printerName()
            name = name.encode("utf-8")
            name = str(name)
            name = name.decode("utf-8")
            if name == self.chosen_printer:
                printer = QPrinter(i)
                break
        doc=QTextDocument()
        cursor = QTextCursor(doc)
        self.print_image = self.print_image.scaledToWidth(600, Qt.SmoothTransformation)
        cursor.insertImage(self.print_image)
        doc.print_(printer)

    def ZoomInEvent(self):
        if self.counterOfZoom == 1:
            self.wnd.plus.setDisabled(False)
        if self.counterOfZoom<8:
            self.counterOfZoom+=1
            self.wnd.Picture.setPixmap(self.zoomArray[self.currentImage][self.counterOfZoom])
        else:
            self.wnd.minus.setDisabled(True)




    def ZoomOutEvent(self):
        if self.counterOfZoom == 8:
            self.wnd.minus.setDisabled(False)
        if self.counterOfZoom>1:
            self.counterOfZoom-=1
            self.wnd.Picture.setPixmap(self.zoomArray[self.currentImage][self.counterOfZoom])
        else:
            self.wnd.plus.setDisabled(True)

    def fileListVar(self,item):
        if item!= None and (item.text()[-4:]==".jpg" or item.text()[-4:]==".png" or item.text()[-4:]==".JPG" or item.text()[-4:]==".PNG"):
            self.currentImage = item.text()
            self.wnd.Picture.setPixmap(self.zoomArray[item.text()][self.counterOfZoom])
            self.wnd.scroll.setWidget(self.wnd.Picture)
            self.wnd.scroll.horizontalScrollBar().setValue(75)
            self.wnd.scroll.verticalScrollBar().setValue(75)

    def fileListVarChanged(self,item_curr,item_pr):
        if item_curr.text()[-4:]==".jpg" or item_curr.text()[-4:]==".png" or item_curr.text()[-4:]==".JPG" or item_curr.text()[-4:]==".PNG":
            self.currentImage = item_curr.text()
            self.wnd.Picture.setPixmap(self.zoomArray[item_curr.text()][self.counterOfZoom])
            self.wnd.scroll.setWidget(self.wnd.Picture)
            self.wnd.scroll.horizontalScrollBar().setValue(75)
            self.wnd.scroll.verticalScrollBar().setValue(75)


    def pic(self):
        self.wnd.Picture.setPixmap(self.empty_info_image)
        city = None
        for item in QgsMapLayerRegistry.instance().mapLayers():
            if 'ctv_topology' in item:
                city = item[0:item.find('_')]

        project = QgsProject.instance()
        with open(project.fileName()) as f:
            content = f.readlines()
        for line in content:
            if ("datasource" in line) & ("host" in line) &("port" in line) & ("user" in line):
                list_properties = line.split(" ")
                break

        count = 0
        for prop in list_properties:
            if count != 2:
                if 'user' in prop:
                    username = prop.split('=')[1]
                    count += 1
                elif 'password' in prop:
                    password = prop.split('=')[1]
                    count += 1

        def searching(i):
            if "'" in i:
                find = i[i.find("=")+2:len(i)-1:]
            else:
                find = i[i.find("=")+1::]
            return find

        final_list=[]
        for i in list_properties:
            if "host" in i:
                final_list.append(searching(i))
            if "port" in i:
                final_list.append(searching(i))
            if "user" in i:
                final_list.append(searching(i))
            if "password" in i:
                final_list.append(searching(i))

        newstr = "dbname='postgres' host="+final_list[0]+" port="+final_list[1]+" user="+final_list[2]+" password="+final_list[3]

        def db(database_name=newstr):
            return psycopg2.connect(database_name)

        def query_db(query, one=False):
            cur = db().cursor()
            cur.execute(query)
            r = [dict((cur.description[i][0], value) \
                       for i, value in enumerate(row)) for row in cur.fetchall()]
            cur.connection.close()
            return (r[0] if r else None) if one else r


        if self.results[0].mLayer.name()==LIST_LAYERS[0]:
            self.workLayer = 1
            my_query = query_db("SELECT json_data FROM "+city+"."+city+"_ctv_topology where cubic_code ="+"'"+str(self.chosen_item)+"'")
        elif self.results[0].mLayer.name()==u"Колодязі КК":
            self.workLayer = 2
            my_query = query_db("SELECT json_data FROM "+city+"."+city+"_cable_channel_pits where pit_id ="+"'"+str(self.chosen_item)+"'")

        self.wnd.fileList.clear()
        self.zoomArray.clear()
        self.wnd.printerMenu.clear()
        self.wnd.parentsMenu.clear()
        self.wnd.childrenMenu.clear()
        self.wnd.infoList.clear()
        del self.wnd.names[:]
        del self.wnd.values[:]
        self.wnd.left.setDisabled(False)
        self.wnd.right.setDisabled(False)
        if not(my_query == None or my_query == 'NULL' or my_query == False or my_query[0]['json_data']==None):
            self.wnd.plus.setDisabled(True)
            self.wnd.minus.setDisabled(True)
            self.wnd.printer.setDisabled(False)
            json_acceptable_string = my_query[0]['json_data'].replace("'", "\"")
            dict_info = json.loads(json_acceptable_string)
            dict_info['archive_link'] = 'https://'+ final_list[0] + dict_info["archive_link"][22:]
            pic = dict_info["archive_link"]
            cubic_code = dict_info["id"]
            self.parents=[]
            self.children=[]
            self.vvv = str(dict_info)
            if dict_info["parents"] == "null" or dict_info["parents"] == None:
                dict_info["parents"] = []
            elif type(dict_info["parents"]) == list:
                self.parents.extend(dict_info["parents"])
            else:
                self.parents.append(dict_info["parents"])
            if dict_info["children"] == "null" or dict_info["children"] == None:
                dict_info["children"] = []
            elif type(dict_info["children"]) == list:
                self.children.extend(dict_info["children"])
            else:
                self.children.append(dict_info["children"])

            pic_arr = []
            pic_name_arr = []
            url = dict_info["archive_link"]
            self.wnd.Picture.setPixmap(self.empty_info_image)

            try:
                fl = dict_info["file_names"]
                for i in fl:
                    self.wnd.fileList.addItem(i)
                    if ( i[-4:] == ".png" or i[-4:] == ".jpg" or i[-4:] == ".JPG"):
                        pic_name = i
                        pic_name = unicode(pic_name)
                        pic_name_arr.append(pic_name)
                        pic = url + pic_name
                        pic_arr.append(pic)
                        self.wnd.saveImageName = pic_name
                for j in range(len(pic_arr)):
                    response = requests.get(pic_arr[j], auth=(username, password), verify=False)
                    re = str(response)
                    if response.status_code == 200:
                        python_image = Image.open(StringIO(response.content))
                        pyqt_image = ImageQt.ImageQt(python_image)
                        self.print_image = pyqt_image
                        pixmap = QPixmap.fromImage(pyqt_image)
                        self.wnd.Picture.setPixmap(pixmap)
                        self.zoomArray[pic_name_arr[j]] = []
                        h = self.wnd.Picture.pixmap().height()
                        w = self.wnd.Picture.pixmap().width()
                        x = self.wnd.pos().x()
                        y = self.wnd.pos().y()

                        for i in range(9):
                            self.zoomArray[pic_name_arr[j]].append(i)
                            self.zoomArray[pic_name_arr[j]][i] = self.wnd.Picture.pixmap().scaled(w-w*i*0.1, h-h*i*0.1,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
                        if x == 0 and y == 0 :
                            self.wnd.setGeometry(200,200,550 + self.zoomArray[pic_name_arr[0]][8].width(), 500)
                        else:
                            self.wnd.setGeometry(x+10,y+38,550 + self.zoomArray[pic_name_arr[0]][8].width(), 500)

                        self.wnd.scroll.setWidget(self.wnd.Picture)


                        self.wnd.scroll.horizontalScrollBar().setValue(75)
                        self.wnd.scroll.verticalScrollBar().setValue(75)


            except KeyError:
                self.wnd.Picture.setPixmap(self.empty_info_image)
                self.wnd.saveImageName = 'emptyInfo.png'
                self.wnd.scroll.setWidget(self.wnd.Picture)
                self.wnd.printer.setDisabled(True)
                self.wnd.plus.setDisabled(True)
                self.wnd.minus.setDisabled(True)
            self.printers = QPrinterInfo.availablePrinters()
            for i in self.printers:
                name = i.printerName()
                name = name.encode("utf-8")
                name = str(name)
                name = name.decode("utf-8")
                self.wnd.printerMenu.addAction(name)
            Parents_empty = True
            for i in self.parents:
                if self.workLayer == 1:
                    for j in self.ctv_all:
                        if j.attribute("cubic_code") == i:
                            Parents_empty = False
                            info = str(i)+" ( " + str(j.attribute("cubic_street").encode("utf-8"))+str(j.attribute("cubic_house").encode("utf-8"))+" "+str(j.attribute("cubic_coment").encode("utf-8"))+" )"
                            info = str(info)
                            info = info.decode("utf-8")
                            self.wnd.parentsMenu.addAction(info)
                            break
                elif self.workLayer == 2:
                    for j in self.kol_all:
                        if j.attribute("pit_id") == i:
                            Parents_empty = False
                            info = str(i) + " (pit_number : " + str(j.attribute("pit_number").encode("utf-8")) + ")"
                            info = str(info)
                            info = info.decode("utf-8")
                            self.wnd.parentsMenu.addAction(info)
                            break
            Children_empty = True
            for i in self.children:
                if self.workLayer == 1:
                    for j in self.ctv_all:
                        if j.attribute("cubic_code") == i:
                            Children_empty = False
                            info = str(i)+" ( " + str(j.attribute("cubic_street").encode("utf-8"))+str(j.attribute("cubic_house").encode("utf-8"))+" "+str(j.attribute("cubic_coment").encode("utf-8"))+" )"
                            info = str(info)
                            info = info.decode("utf-8")
                            self.wnd.childrenMenu.addAction(info)
                            break
                elif self.workLayer == 2:
                    for j in self.kol_all:
                        if j.attribute("pit_id") == i:
                            Children_empty = False
                            info = str(i) + " (pit_number : " + str(j.attribute("pit_number").encode("utf-8")) + ")"
                            info = str(info)
                            info = info.decode("utf-8")
                            self.wnd.childrenMenu.addAction(info)
                            break
            if Parents_empty:
                self.wnd.left.setDisabled(True)
            if Children_empty:
                self.wnd.right.setDisabled(True)
            try:
                self.wnd.plus.setDisabled(False)
                self.wnd.minus.setDisabled(True)
                self.wnd.printer.setDisabled(False)
                self.currentImage = pic_name_arr[0]
                self.wnd.Picture.setPixmap(self.zoomArray[pic_name_arr[0]][8])
                #self.wnd.setGeometry(200,200,550 + self.zoomArray[pic_name_arr[0]][8].width(), 500)
            except IndexError:
                self.wnd.printer.setDisabled(True)
                self.wnd.plus.setDisabled(True)
                self.wnd.minus.setDisabled(True)
                self.wnd.Picture.setPixmap(self.empty_info_image)
                x = self.wnd.pos().x()
                y = self.wnd.pos().y()
                self.wnd.setGeometry(x+10,y+38,530 + self.empty_info_image.width(), 500)
                self.wnd.saveImageName = 'emptyInfo.png'

            for i in range(30):
                try:
                    ss = self.feat[i]
                    self.wnd.names.append(unicode(self.feat.fields()[i].name()))
                    self.wnd.values.append(unicode(ss))
                    newItem = QTreeWidgetItem([self.feat.fields()[i].name(),unicode(ss)])
                    self.wnd.infoList.addTopLevelItem (newItem)
                except KeyError:
                    pass
        else:
            self.wnd.plus.setDisabled(True)
            self.wnd.minus.setDisabled(True)
            self.wnd.printer.setDisabled(True)
            self.wnd.Picture.setPixmap(self.empty_info_image)
            self.wnd.setGeometry(200,200,530 + self.empty_info_image.width(), 500)
            self.wnd.saveImageName = 'emptyInfo.png'
    def canvasReleaseEvent(self, mouseEvent):
        """
        Each time the mouse is clicked on the map canvas, perform
        the following tasks:
            Loop through all visible vector layers and for each:
                Ensure no features are selected
                Determine the distance of the closes feature in the layer to the mouse click
                Keep track of the layer id and id of the closest feature
            Select the id of the closes feature
        """


        namme = LIST_LAYERS[0]
        namme1 = u"Колодязі КК"
        q=QgsMapLayerRegistry.instance().mapLayersByName(namme)
        #q1=QgsMapLayerRegistry.instance().mapLayersByName(namme1)
        #q.extend(q1)
        if self.wnd.close():
            self.wnd.setGeometry(200,200,530 + self.empty_info_image.width(), 500)
        self.canvas.setSelectionColor(QColor("orange") )
        check = True
        try:
            self.results = self.identify(mouseEvent.x(),mouseEvent.y(), self.DefaultQgsSetting , q, self.VectorLayer)
            r = self.results[0].mLayer.getFeatures()
            self.feat = self.results[0].mFeature
        except IndexError:
            check = False
        if self.already_connected:
            self.wnd.childrenMenu.triggered.connect(self.childrenEvent)
            self.wnd.parentsMenu.triggered.connect(self.parentsEvent)
            self.wnd.printerMenu.triggered.connect(self.Print)
            self.wnd.plus.triggered.connect(self.ZoomOutEvent)
            self.wnd.minus.triggered.connect(self.ZoomInEvent)
            self.wnd.fileList.itemClicked.connect(self.fileListVar)
            self.wnd.fileList.currentItemChanged.connect(self.fileListVar)

            self.counterOfZoom = 8
            self.already_connected = False
        if check and self.results[0].mLayer.name()==LIST_LAYERS[0]:
            self.workLayer = 1
            if len(self.results)>0 and (self.results[0].mFeature.attribute("cubic_name")==u"Кросс-муфта" or self.results[0].mFeature.attribute("cubic_name")==u"Магистральный распределительный узел" or self.results[0].mFeature.attribute("cubic_name")==u"Оптический узел" or self.results[0].mFeature.attribute("cubic_name") == u"Оптичний приймач" or self.results[0].mFeature.attribute("cubic_name") == u"Передатчик оптический"):
                i=self.results[0].mFeature
                ids=[]
                ids.append(i.id())
                info = str(i.attribute("cubic_code")) + " "+str(i.attribute("cubic_name").encode("utf-8"))+" ( " + str(i.attribute("cubic_street").encode("utf-8"))+""+str(i.attribute("cubic_house").encode("utf-8"))+" "+str(i.attribute("cubic_coment").encode("utf-8"))+" )"
                info = str(info)
                info = info.decode("utf-8")
                self.results[0].mLayer.setSelectedFeatures(ids)
                self.canvas.zoomToSelected(self.results[0].mLayer)
                self.chosen_item = self.results[0].mFeature.attribute("cubic_code")
                self.pic()
                self.already_connected = False
                self.wnd.show()

        elif check and self.results[0].mLayer.name()==u"Колодязі КК":
            self.workLayer = 1
            if len(self.results)>0:
                i=self.results[0].mFeature
                ids=[]
                ids.append(i.id())
                self.results[0].mLayer.setSelectedFeatures(ids)
                self.canvas.zoomToSelected(self.results[0].mLayer)
                self.chosen_item = self.results[0].mFeature.attribute("pit_id")
                self.pic()
                self.already_connected = False
                self.wnd.show()
