# -*- coding: utf-8 -*-
# Tasoristikko: Tasristikkoja ratkaiseva ohjelma
# Copyright (C) 2008 Ville Leskinen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tässä modulissa on ohjelman pääikkuna."""

from PyQt4 import QtCore, QtGui
from ui_ristikkomainwindow import Ui_RistikkoMainWindow
from ristikkonakyma import QRistikkoView

class QRistikkoMainWindow(QtGui.QMainWindow, Ui_RistikkoMainWindow):
    """Tasoristikko-ohjelman pääikkuna."""
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        self.gwRistikko = QRistikkoView(self)
        """@ivar: Ristikon näyttävä widget
        @type: L{QRisitkkoView<ristikkonakyma.QRistikkoView>}"""
        gl = QtGui.QGridLayout()
        gl.addWidget(self.gwRistikko)
        cw = QtGui.QWidget(self)
        cw.setLayout(gl)
        self.setCentralWidget(cw)
        
        self.generateConnections()

    def generateConnections(self):
        """Luo actioneille connectionit"""
        self.connect(self.actionRuudukko, QtCore.SIGNAL('triggered(bool)'),
                self.gwRistikko.ruudukkoValinta)
        self.connect(self.actionAvaa, QtCore.SIGNAL('triggered()'),
                self.avaaRistikko)
        self.connect(self.actionTallenna, QtCore.SIGNAL('triggered()'),
                self.tallennaRistikko)


    def avaaRistikko(self):
        """Kysyy dialogilla ristikko-tiedoston ja avaa sen.
        @todo: Ristikko pitäis saada vielä auki"""
        tiedostoNimi = QtGui.QFileDialog.getOpenFileName(self, 'Avaa ristikko',
                '', 'Ristikko (*.ris)')

        if tiedostoNimi:
            pass

    def tallennaRistikko(self):
        """Kysyy tallennettavan tiedoson nimen ja tallentaa ristikon.
        @todo: Ristikko pitäisi vielä tallentaa
        @todo: Tarkastetaan onko ristikko jo tallenettu jollain nimellä.
        @todo: Lisätään viimeisempien tiedostojen listaan?"""
        tiedostoNimi = QtGui.QFileDialog.getSaveFileName(self, 'Tallenna ristikko',
                'ristikko.ris', 'Ristikko (*.ris)')

        if tiedostoNimi:
            pass
