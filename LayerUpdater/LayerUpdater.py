# -*- coding: utf-8 -*-
# -*- coding: cp1251 -*-

"""
/***************************************************************************
 LayerUpdater
                                 A QGIS plugin
 Layer updater
                              -------------------
        begin                : 2017-09-08
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Vitaliy Prozur/Oleksiy Bondar
        email                : .
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources
from qgis.gui import *
from qgis.core import *
import psycopg2
import sched, time
from threading import Timer
# Import the code for the dialog
from LayerUpdater_dialog import LayerUpdaterDialog
import os.path
import time


class LayerUpdater:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        # nammme = "комутатори".decode('utf-8')
        # l = QgsMapLayerRegistry.instance().mapLayersByName(nammme)

        # self.layer = l
        # for r in l:
        #     self.switches_all = filter(lambda i: True, r.getFeatures())
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'LayerUpdater_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Layer Updater')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'LayerUpdater')
        self.toolbar.setObjectName(u'LayerUpdater')


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('LayerUpdater', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = LayerUpdaterDialog()
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)


        # if self.layer == []:
        #     self.msg = QMessageBox()
        #     self.msg.setIcon(QMessageBox.Critical)
        #     self.msg.setText(u"Layer \"комутатори\" is not found")
        #     #self.setInformativeText("This is additional information")
        #     self.msg.setWindowTitle("Error")
        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/LayerUpdater/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

    def waiter(self):
        while self.tt > 0:
            self.dlg.stateLabel.setText("working..." + str(self.tt) + " sec")
            time.sleep(1.00)
            self.tt = self.tt -1
        self.tt = 0
        return True
        ###############

    def dbData(self):
        city = None
        for item in QgsMapLayerRegistry.instance().mapLayers():
            if 'buildings' in item:
                city = item[0:item.find('_')]
        project = QgsProject.instance()
        with open(project.fileName()) as f:
            content = f.readlines()
        for line in content:
            if ("datasource" in line) & ("host" in line) &("port" in line) & ("user" in line):
                #print line
                list_properties = line.split(" ")
                break
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
        print newstr
        def db(database_name=newstr):
            return psycopg2.connect(database_name)
        def query_db(query, one=False):
            cur = db().cursor()
            cur.execute(query)
            r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
            cur.connection.close()
            return (r[0] if r else None) if one else r
        my_query = query_db("SELECT doorway, cubic_house_num, street, ip_address, switch_model, mon_ping_state, mon_traffic_state FROM "+city+"."+city+"_switches_working where mon_ping_state is not null or mon_traffic_state is not null")
        self.dlg.objectBrowser.clear()
        for i in my_query:
            #[i.values()[5],i.values()[6],i.values()[4],i.values()[2],i.values()[0],i.values()[1],i.values()[3]]
            switches_list = i.values()
            print switches_list
            if switches_list[3] == '0':
                switches_list[3] = 'allDOWN'
            elif switches_list[3] == '1':
                switches_list[3] = 'bothUP'
            elif switches_list[3] == '2':
                switches_list[3] = 'parentUP'
            elif switches_list[3] == '3':
                switches_list[3] = 'childUP'
            if switches_list[1] == '0':
                switches_list[1] = 'NOping'
            elif switches_list[1] == '1':
                switches_list[1] = 'pingOK'

            newItem = QTreeWidgetItem([switches_list[4],switches_list[6],switches_list[2],switches_list[5],switches_list[1],switches_list[0],switches_list[3]])
            self.dlg.objectBrowser.addTopLevelItem (newItem)
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() == "комутатори".decode('utf-8'):
                layer = lyr
                layer.triggerRepaint()

        if self.stop:
            self.dlg.stateLabel.setText("reloading...")
            self.tt = 295
            # while self.tt > 0:
            #     self.dlg.stateLabel.setText("working..." + str(self.tt) + " sec")
            #     time.sleep(1.0)
            #     self.tt = self.tt -1.0

            if self.waiter() == True:
                self.t = Timer(0.01, self.dbData)
            self.t.start()

    '''def changeLayer(arg):
        pass'''
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Layer Updater'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def stopSlot(self):
        self.stop = False
        self.tt = 0
        self.dlg.stateLabel.setText("stoped.")
        self.dlg.objectBrowser.clear()
        try:
            self.t.cancel()
        except:
            pass
    def startSlot(self):
        self.dlg.stateLabel.setText("working...")
        self.stop = True

        self.t = Timer(5.0, self.dbData)
        self.dlg.stateLabel.setText("working...")
        self.t.start()

    def onMapSlot(self,action):
        for i in self.switches_all:
            if unicode(i["cubic_ip_address"])==unicode(action.text(3)):
                ids=[]
                ids.append(i.id())
                self.layer[0].setSelectedFeatures(ids)
                self.iface.mapCanvas().zoomToSelected(self.layer[0])


    def run(self):
        nammme = "Комутатори".decode('utf-8')
        l = QgsMapLayerRegistry.instance().mapLayersByName(nammme)

        self.layer = l
        for r in l:
            self.switches_all = filter(lambda i: True, r.getFeatures())
        """Run method that performs all the real work"""
        # show the dialog
        #self.s = sched.scheduler(time.time(), time.sleep)
        #s.enter(0, 300)

        self.stop = True


        #self.s.run()
        self.dlg.stopButton.clicked.connect(self.stopSlot)
        self.dlg.startButton.clicked.connect(self.startSlot)
        self.dlg.comboBox.clear()
        #plugin is only for switches alerts:) this selection is fake
        for i in self.iface.legendInterface().layers():
            self.dlg.comboBox.addItem(unicode(i.name()))
        self.dlg.comboBox.setVisible(False)
        self.dlg.objectBrowser.itemClicked.connect(self.onMapSlot)
        ##---------------------------------------------------------
        # Run the dialog event loop
        # if self.layer == []:
        #     result = self.msg.exec_()
        # else:
        self.dlg.setWindowModality(True)
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
