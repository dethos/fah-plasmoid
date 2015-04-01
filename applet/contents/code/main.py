# -*- coding: utf-8 -*-
from datetime import datetime

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript


# Very Simple plasmoid UI
class FAHApplet(plasmascript.Applet):

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)

    def init(self):
        self.setHasConfigurationInterface(False)
        self.layout = QGraphicsGridLayout(self.applet)

        # Static Text Labels
        username_label = Plasma.Label(self.applet)
        username_label.setText("User:")
        self.layout.addItem(username_label, 1, 1)

        team_label = Plasma.Label(self.applet)
        team_label.setText("Team:")
        self.layout.addItem(team_label, 2, 1)

        start_date_label = Plasma.Label(self.applet)
        start_date_label.setText("Started:")
        self.layout.addItem(start_date_label, 3, 1)

        deadline_label = Plasma.Label(self.applet)
        deadline_label.setText("Deadline:")
        self.layout.addItem(deadline_label, 4, 1)

        # Dynamic labels
        self.username = Plasma.Label(self.applet)
        self.layout.addItem(self.username, 1, 2)

        self.team = Plasma.Label(self.applet)
        self.layout.addItem(self.team, 2, 2)

        self.start_date = Plasma.Label(self.applet)
        self.layout.addItem(self.start_date, 3, 2)

        self.deadline = Plasma.Label(self.applet)
        self.layout.addItem(self.deadline, 4, 2)

        self.progress = Plasma.Label(self.applet)
        self.progress.setText("0%")
        self.progress.setStyleSheet("font-size: 80px")
        self.layout.addItem(self.progress, 1, 3, 4, 1)

        self.connectBtn = Plasma.PushButton(self.applet)
        self.connectBtn.setText("Connect")
        self.connect(self.connectBtn,
                     SIGNAL("clicked ()"),
                     self.connectToEngine)
        self.layout.addItem(self.connectBtn, 4, 3, 1, 1)

        # General Actions
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
        self.applet.setLayout(self.layout)
        self.connectToEngine()

    def connectToEngine(self):
        self.FAHEngine = self.dataEngine("fah-plasmoid-data-engine")
        self.FAHEngine.connectSource("FAHStatus", self, 5000)
        self.connectBtn.hide()
        self.progress.show()

    @pyqtSignature("dataUpdated(const QString &, const Plasma::DataEngine::Data &)")
    def dataUpdated(self, sourceName, data):
        fah_data = data[QString('status')]

        if QString("error") not in fah_data:
            self.username.setText(fah_data[QString("user")])
            self.team.setText(fah_data[QString("team")])

            date = str(fah_data[QString("start_time")])
            dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            self.start_date.setText(dt.strftime("%d-%m-%Y %H:%M"))

            deadline = datetime.fromtimestamp(fah_data[QString("deadline")])
            self.deadline.setText(deadline.strftime("%d-%m-%Y %H:%M"))

            progress = "%3.1f" % (fah_data[QString('progress')] * 100)
            self.progress.setText(progress + "%")
        else:
            self.FAHEngine.disconnectSource("FAHStatus", self)
            self.progress.hide()
            self.connectBtn.show()


def CreateApplet(parent):
    return FAHApplet(parent)
