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

class QRistikkoView(QtGui.QGraphicsView):
    """Ristikon näyttävä QGraphicsView"""
    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        
        self.scene = QRistikkoScene()
        """@ivar: Risitkon scene
        @type: L{QRistikkoScene}"""
        self.setScene(self.scene)
        self.setRenderHints(QtGui.QPainter.Antialiasing |
                QtGui.QPainter.SmoothPixmapTransform)

        self.skaalaus = 1
        """@ivar: Näkymän zoomaus
        @type: C{float}"""

        self.mwPaaikkuna = parent
        """@ivar: Pääikkuna
        @type: L{QRistikkoMainWindow<mainwindow.QRistikkoMainWindow>}"""

        vsb = self.verticalScrollBar()
        vsb.setSliderPosition(vsb.maximum())

    def ruudukkoValinta(self, paalla):
        """Valitsee onko ruudukko näkyvissä.
        @param paalla: onko ruudukko päällä
        @type paalla: boolean"""
        self.scene.ruudukkoValinta(paalla)


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
        
    def lisaaRistikko(self, ristikko):
        """Lisää sceneen ristikon.
        @param ristikko: lisättävä ristikko
        @type ristikko: L{Ristikko<pyTasoristikko.ristikko.Ristikko>}"""
        self.ristikko = ristikko #: Sceneen kuuluva ristikko

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
