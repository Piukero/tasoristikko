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

"""Tässä modulissa ovat käyttöliittymässä ristikon näyttävät luokat."""

from PyQt4 import QtCore, QtGui

from ristikkowidgetit import QAsetusWidget
from pyTasoristikko.ristikko import Ristikko

class QRistikkoView(QtGui.QGraphicsView):
    """Ristikon näyttävä QGraphicsView"""
    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)

        self.setRenderHints(QtGui.QPainter.Antialiasing |
                QtGui.QPainter.SmoothPixmapTransform)

        self.skaalaus = 1.0
        """@ivar: Näkymän zoomaus
        @type: C{float}"""

        self.mwPaaikkuna = parent
        """@ivar: Pääikkuna
        @type: L{QRistikkoMainWindow<mainwindow.QRistikkoMainWindow>}"""

    def ruudukkoValinta(self, paalla):
        """Valitsee onko ruudukko näkyvissä.
        @param paalla: onko ruudukko päällä
        @type paalla: boolean"""
        self.scene.ruudukkoValinta(paalla)

    def setScene(self, scene):
        QtGui.QGraphicsView.setScene(self, scene)
        vsb = self.verticalScrollBar()
        vsb.setSliderPosition(vsb.maximum())

class QRistikkoScene(QtGui.QGraphicsScene):
    """QGraphicsScene, jolla ristikko piirretään."""
    def __init__(self, parent=None):
        QtGui.QGraphicsScene.__init__(self, parent)
        self.setSceneRect(QtCore.QRectF(-40,0,3000,3000))
        
        self.siirtoMatriisi = QtGui.QMatrix(1, 0, 0, -1, 0,self.height() - 100)
        """@ivar: Siirtomatriisi. Tällä käännetään ristikon koordinaatisto.
        Tällä kerrotaan nivelen koordinaatteja, että saadaan ne oikein päin.
        @type: C{QtGui.QMatrix}"""

        self.ruudukkoPaalla = True 
        """@ivar: Onko taustaruudukko päällä
        @type: C{bool}"""

        self.koordinaattiKerroin = 100
        """@ivar: Koordinaattien kerroin
        @type: C{int}"""

        self.widgetit = []
        """@ivar: skenen widgetit
        @type: C{list} of L{QAsetusWidget}"""

        self.ristikko = None
        """@ivar: Skeneen kuuluva ristikko
        @type: L{Ristikko}"""

    def drawBackground(self, painter, rect):
        # Ristikko
        if self.ruudukkoPaalla:
            topLeft = self.sceneRect().topLeft()
            bottomRight = self.sceneRect().bottomRight()
            x = topLeft.x()
            y = topLeft.y()
            x += -x % 100
            y += -y % 100
            painter.setPen(QtCore.Qt.lightGray)
            while x < bottomRight.x():
                painter.drawLine(x, topLeft.y(), x, bottomRight.y())
                x += 100
            while y < bottomRight.y():
                painter.drawLine(topLeft.x(), y, bottomRight.x(), y)
                y += 100

        # Nuoli
        painter.setPen(QtCore.Qt.black)
        origo = self.siirtoMatriisi.map(QtCore.QPointF(0, 0))
        karkiX = QtCore.QPointF(100,0)
        nuoliX1 = karkiX + QtCore.QPointF(-10,10)
        nuoliX2 = karkiX + QtCore.QPointF(-10,-10)
        karkiY = QtCore.QPointF(0,100)
        nuoliY1 = karkiY + QtCore.QPointF(10,-10)
        nuoliY2 = karkiY + QtCore.QPointF(-10,-10)
        painter.drawLine(origo, self.siirtoMatriisi.map(karkiX))
        painter.drawLine(origo, self.siirtoMatriisi.map(karkiY))
        painter.drawLine(self.siirtoMatriisi.map(karkiX),
                self.siirtoMatriisi.map(nuoliX1))
        painter.drawLine(self.siirtoMatriisi.map(karkiX),
                self.siirtoMatriisi.map(nuoliX2))
        painter.drawLine(self.siirtoMatriisi.map(karkiY),
                self.siirtoMatriisi.map(nuoliY1))
        painter.drawLine(self.siirtoMatriisi.map(karkiY),
                self.siirtoMatriisi.map(nuoliY2))

        # Teksti
        tekstiX = karkiX + QtCore.QPointF(-20,-20)
        painter.drawText(self.siirtoMatriisi.map(tekstiX),'x')
        tekstiY = karkiY + QtCore.QPointF(-20,-20)
        painter.drawText(self.siirtoMatriisi.map(tekstiY), 'y')

    def ruudukkoValinta(self, paalla):
        """Valitsee onko ruudukko näkyvissä.
        @param paalla: onko ruudukko päällä
        @type paalla: boolean"""
        self.ruudukkoPaalla = paalla
        self.update()
        
    def asetaRistikko(self, ristikko):
        """Asettaa scenen ristikon.
        @param ristikko: lisättävä ristikko
        @type ristikko: L{Ristikko<pyTasoristikko.ristikko.Ristikko>}"""
        for w in self.widgetit:
            if w in self.items():
                self.removeItem(w)
        if self.ristikko:
            self.ristikko.poista()
        self.ristikko = ristikko

    def lisaaWidget(self, widget):
        """Lisää sekeneen widgetin.
        @param widget: lisättävä widget
        @type widget: L{QAsetusWidget}"""
        if not widget in self.widgetit:
            self.widgetit.append(widget)
            self.addItem(widget)

    def piilotaMuutWidgetit(self, widget):
        """Piilottaa scenen muut widgetit paitsi annetun.
        @param widget: Widgetti, jota ei piiloteta.
        @type widget: L{QAsetusWidget}"""
        for item in self.widgetit:
            if isinstance(item, QAsetusWidget) and not item == widget:
                item.hide()

    def valitseItem(self, item):
        """Asettaa annetun C{QGraphicsItemin} valituksi. Poistaa samalla muiden
        itemien valinnat.
        @param item: Valittava C{QGraphicsItem}
        @type item: C{QGraphicsItem}"""
        for i in self.items():
            i.setSelected(i == item)

    def uusiRistikko(self):
        """Luo skeneen uuden tyhjän ristikon.
        @todo: tarksitukset, että onko vanha ristikko tallenettu."""
        self.asetaRistikko(Ristikko())
