from PyQt4.QtCore import *
from PyKDE4.kdecore import *
from PyKDE4 import plasmascript

from fah_utils import current_simulation


class FAHDataEngine(plasmascript.DataEngine):
    def __init__(self, parent, args=None):
        plasmascript.DataEngine.__init__(self, parent)

    def init(self):
        self.setMinimumPollingInterval(1000)

    def sources(self):
        return ['FAHStatus']

    def sourceRequestEvent(self, name):
        return self.updateSourceEvent(name)

    def updateSourceEvent(self, name):
        self.setData("FAHStatus", "status", current_simulation())
        return True


def CreateDataEngine(parent):
    return FAHDataEngine(parent)
