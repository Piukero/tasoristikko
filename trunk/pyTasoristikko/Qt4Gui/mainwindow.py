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
from ristikkonakyma import *
from guiristikkotehdas import GuiRistikkotehdas
from pyTasoristikko.ristikko import Ristikko
from pyTasoristikko.ristikkoIO import *
from pyTasoristikko.ristikkopoikkeukset import *

class QRistikkoMainWindow(QtGui.QMainWindow, Ui_RistikkoMainWindow):
    """Tasoristikko-ohjelman pääikkuna."""
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        self.scRistikko = QRistikkoScene()
        """@ivar: Risitkon scene
        @type: L{QRistikkoScene}"""

        self.gwRistikko = QRistikkoView(self)
        """@ivar: Ristikon näyttävä widget
        @type: L{QRisitkkoView<ristikkonakyma.QRistikkoView>}"""
        self.gwRistikko.setScene(self.scRistikko)
        gl = QtGui.QGridLayout()
        gl.addWidget(self.gwRistikko)
        cw = QtGui.QWidget(self)
        cw.setLayout(gl)
        self.setCentralWidget(cw)
        
        self.generateConnections()

        self._teeTestiRistikko()
    
    def _teeTestiRistikko(self):
        """Luodaan käyttöliittymään testiristikko."""
        ristikko = Ristikko()
        tehdas = GuiRistikkotehdas(self.scRistikko, ristikko)
        LuoTestiRistikko(tehdas)
        self.scRistikko.asetaRistikko(ristikko)

    def generateConnections(self):
        """Luo actioneille connectionit"""
        self.connect(self.actionRuudukko, QtCore.SIGNAL('triggered(bool)'),
                self.gwRistikko.ruudukkoValinta)
        self.connect(self.actionAvaa, QtCore.SIGNAL('triggered()'),
                self.avaaRistikko)
        self.connect(self.actionTallenna, QtCore.SIGNAL('triggered()'),
                self.tallennaRistikko)
        self.connect(self.actionTallennaNimella, QtCore.SIGNAL('triggered()'),
                self.tallennaRistikkoNimella)
        self.connect(self.actionUusi, QtCore.SIGNAL('triggered()'),
                self.uusiRistikko)


    def avaaRistikko(self):
        """Kysyy dialogilla ristikko-tiedoston ja avaa sen.
        @todo: Ristikko pitäis saada vielä auki"""

        if not self.talletusTarkistus():
            return

        tiedostoNimi = QtGui.QFileDialog.getOpenFileName(self, 'Avaa ristikko',
                '', 'Ristikko (*.tris)')

        try:
            if tiedostoNimi:
                ristikko = Ristikko()
                tehdas = GuiRistikkotehdas(self.scRistikko, ristikko)
                AvaaRistikko(unicode(tiedostoNimi), tehdas)
                self.scRistikko.asetaRistikko(ristikko)
                ristikko.asetaTallennetuksi(tiedostoNimi)
        except RistikkoIOVirhe, v:
            QtGui.QMessageBox.information(self, 'Avaus ei onnistunut',
                                          unicode(v))

    def tallennaRistikkoNimella(self):
        """Tallennetaan ristikko nimellä."""
        self.tallennaRistikko(True)

    def tallennaRistikko(self, nimella=False):
        """Kysyy tallennettavan tiedoson nimen ja tallentaa ristikon.
        @param nimella: 'Tallenetaanko nimellä?'
        @type nimella: C{bool}
        @todo: Lisätään viimeisempien tiedostojen listaan?"""

        tiedostoNimi = None
        if self.scRistikko.ristikko.tiedostoNimi and not nimella:
            tiedostoNimi = self.scRistikko.ristikko.tiedostoNimi
        else:
            tiedostoNimi = QtGui.QFileDialog.getSaveFileName(self,
                           'Tallenna ristikko', 'ristikko.tris',
                           'Ristikko (*.tris)')
        try:
            if tiedostoNimi:
                TallennaRistikko(self.scRistikko.ristikko,
                                 unicode(tiedostoNimi))

        except RistikkoIOVirhe, v:
            QtGui.QMessageBox.information(self, 'Tallennus ei onnistunut',
                    unicode(v))

    def uusiRistikko(self):
        """Luo uuden risitkon."""
        if not self.talletusTarkistus():
            return

        self.scRistikko.uusiRistikko()

    def closeEvent(self, event):
        if not self.talletusTarkistus():
            event.ignore()
        else:
            event.accept()

    def talletusTarkistus(self):
        """Jos ristikko ei ole tallennettu, kysyy tallennetaanko.
        @return: C{False}, jos käyttäjä painoi 'Peruuta'. Muuten C{True}
        @rtype: C{bool}"""
        if not self.scRistikko.ristikko.tallennettu and len(self.scRistikko.ristikko.nivelet) > 0:
            vast = QtGui.QMessageBox.question(self, 'Tallenetaanko ristikko',
                    'Muokattua ristikkoa ei ole tallennettu. Tallenetaanko?',
                    u'Kyllä', 'Ei', 'Peruuta')
            if vast == 0:
                self.tallennaRistikko()
            elif vast == 2:
                return False

        return True

