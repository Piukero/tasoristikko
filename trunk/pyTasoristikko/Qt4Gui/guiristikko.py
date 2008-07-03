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

"""Tässä modulissa on ristikon graafista kuvaamista varten tarvittavat luokat
."""

from PyQt4 import QtCore, QtGui

from pyTasoristikko.ristikko import *
from ristikkowidgetit import *


class QRistikkoItem(QtGui.QGraphicsItem):
    """Tämä on perusluokka kaikille piirettäville ristikon osille. Tarkoituksen
    on toteuttaa kaikki yhteiset ominaisuudet tässä luokassa. Tämän luokan
    instanssia ei voida piirtää."""
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)
        self.asetukset = None
        """@ivar: Asetuksiin käytettävä widget. Alaluokan tulee luoda tämä.
        @type: L{QAsetusWidget}"""

    def mouseDoubleClickEvent(self, event):
        self.asetukset.asetaKlikkausPos(event.pos())
        self.asetukset.show()

    def keyPressEvent(self, event):
       if event.key == QtCore.Qt.Key_Delete:
           self.poista()

class QNivel(QRistikkoItem, Nivel):
    """Tämä luokka kuvaa piirettävää niveltä."""
    NivelPen = QtGui.QPen(QtCore.Qt.black) #: Nivelen reunaviiva
    NivelPen.setWidth(3)
    
    NivelBrush = QtGui.QBrush(QtCore.Qt.white) #: Nivelen täyttö

    def __init__(self, ristikko, scene, x=0.0, y=0.0):
        QRistikkoItem.__init__(self)
        Nivel.__init__(self,ristikko,x,y)
        self.alustettu = False
        """@ivar: Onko nivel jo alustettu
        @type: C{bool}"""
        self.rect = QtCore.QRectF(-6,-6,12,12)
        """@ivar: Piirettävän alueen C{QRectF}
        @type: C{QtGui.QRectF}"""
        self.pen = QNivel.NivelPen
        """@ivar: Piirossa käytettävä C{QPen}
        @type: C{QtGui.QPen}"""
        self.brush = QNivel.NivelBrush
        """@ivar: Piirossa käytettävä C{QBrush}
        @type: C{QtGui.QBrush}"""
        #self.scene = scene
        #"""@ivar: Scene johon tämä nivel kuuluu.
        #@type: L{QRistikkoScene<ristikkonakyma.QRistikkoScene>}"""
        self.setZValue(100)

        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable |
                      QtGui.QGraphicsItem.ItemIsSelectable |
                      QtGui.QGraphicsItem.ItemIsFocusable)

        scene.addItem(self)
        self.asetukset = QNivelWidget(self.scene(), self)
        self.asetaKoordinaatit(x, y)
        self.alustettu = True

    def asetaKoordinaatit(self, x, y):
        Nivel.asetaKoordinaatit(self, x, y)
        
        pos = QtCore.QPointF(x*self.scene().koordinaattiKerroin,
                             y*self.scene().koordinaattiKerroin)
        pos = self.scene().siirtoMatriisi.map(pos)
        self.setPos(pos)
    
    def paint(self, painter, option, widget=None):
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawEllipse(self.rect)
    
    def boundingRect(self):
        return self.rect


    def itemChange(self, change, value):
        """@todo: tähän varmaan pitäisi pistää myös koordinaattien muunnos."""
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            self.scene().update()
            self._muutaXY()
            if self.alustettu:
                self.asetukset.siirra()

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def _muutaXY(self):
        """Muuttaa tämän nivelen x- ja y-koordinaatit vastaamaan
        C{QGraphicsItem}n positiota."""
        if not self.alustettu:
            return
        matriisi, toimiko = self.scene().siirtoMatriisi.inverted()
        kaanPos = matriisi.map(self.pos())
        self.x = kaanPos.x() / self.scene().koordinaattiKerroin
        self.y = kaanPos.y() / self.scene().koordinaattiKerroin

    def poista(self):
        Nivel.poista(self)
        self.scene().removeItem(self)
        self.scene().removeItem(self.asetukset)
        for sauva in self.sauvat:
            self.scene().removeItem(sauva)

    def lisaaSauva(self, sauva):
        """@type sauva: L{QSauva}"""
        Nivel.lisaaSauva(self, sauva)
        if not sauva in self.scene().items():
            self.scene().addItem(sauva)

    def lisaaPistekuorma(self, pistekuorma):
        """@type pistekuorma: L{QPistekuorma}"""
        Nivel.lisaaPistekuorma(self, pistekuorma)
        if not pistekuorma in self.scene().items():
            self.scene().addItem(pistekuorma)
        pistekuorma.setParent(self)


class QSauva(QRistikkoItem, Sauva):
    """Tämä luokka kuvaa piirettävää sauvaa."""
    def __init__(self, ristikko, nivel1=None, nivel2=None):
        QRistikkoItem.__init__(self)
        Sauva.__init__(self, ristikko, nivel1, nivel2)
        self.pen = QtGui.QPen()
        """@ivar: Piirossa käytettävä C{QPen}
        @type: C{QtGui.QPen}"""
        self.pen.setWidth(6)
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable |
                      QtGui.QGraphicsItem.ItemIsFocusable)

        self.asetukset = QSauvaWidget(self.n1.scene(), self)


    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.drawLine(QtCore.QLineF(self.n1.pos(), self.n2.pos()))

    def boundingRect(self):
        penWidth = self.pen.width()
        extra = penWidth / 2

        return QtCore.QRectF(self.n1.pos(),
                QtCore.QSizeF(self.n2.pos().x() - self.n1.pos().x(),
                              self.n2.pos().y() -
                              self.n1.pos().y())).normalized().adjusted(-extra,
                                      -extra, extra, extra)

class QPistekuorma(QRistikkoItem, Pistekuorma):
    """Tämä luokka kuvaa piirettävää pistekuormaa."""
    def __init__(self, nivel, kuormaX, kuormaY):
        QRistikkoItem.__init__(self)
        Pistekuorma.__init__(self, nivel, kuormaX, kuormaY)
        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable |
                      QtGui.QGraphicsItem.ItemIsSelectable |
                      QtGui.QGraphicsItem.ItemIsFocusable)
       
class QNiveltuki(QRistikkoItem, Tuki):
    """Tämä luokka kuvaa piirettävää niveltukea. Niveltuki on tukevaan
    pintaan jäykästi kiinitetty tuki."""
    def __init__(self, nivel, suuntakulma=0.0):
        """Konstruktori."""
        QRistikkoItem.__init__(self)
        Tuki.__init__(self, nivel, suuntakulma)
        
        self.tukivoimaKulmat = [0.0, 90.0]
        self.luoTukivoimat()

        self.tyyppi = Tuki.NIVELTUKI
        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable |
                      QtGui.QGraphicsItem.ItemIsSelectable |
                      QtGui.QGraphicsItem.ItemIsFocusable)
        
class QRullatuki(QRistikkoItem, Tuki):
    """Tämä luokka kuvaa piirettävää rullatukea. Rullatuki on tukevaan
    pintaan rullilla kiinitetty tuki."""
    def __init__(self, nivel, suuntakulma=0.0):
        """Konstruktori."""
        QRistikkoItem.__init__(self)
        Tuki.__init__(self, nivel, suuntakulma)
        
        self.tukivoimaKulmat = [90.0]
        self.luoTukivoimat()

        self.tyyppi = Tuki.RULLATUKI
        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable |
                      QtGui.QGraphicsItem.ItemIsSelectable |
                      QtGui.QGraphicsItem.ItemIsFocusable)
