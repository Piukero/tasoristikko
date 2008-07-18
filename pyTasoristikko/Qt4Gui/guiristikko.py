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

from math import *

from pyTasoristikko.ristikko import *
from ristikkowidgetit import *
from valintaitemit import *


class QRistikkoItem(QtGui.QGraphicsItem):
    """Tämä on perusluokka kaikille piirettäville ristikon osille. Tarkoituksen
    on toteuttaa kaikki yhteiset ominaisuudet tässä luokassa. Tämän luokan
    instanssia ei voida piirtää."""
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)
        self.asetukset = None
        """@ivar: Asetuksiin käytettävä widget. Alaluokan tulee luoda tämä.
        @type: L{QAsetusWidget}"""
        self.valinta = None
        """@ivar: Itemin valintaa kuvaava C{QValintaItem}. Alaluokan tulee luoda
        tämä.
        @type: L{QValintaItem}"""
        self.menu = QtGui.QMenu()
        """@ivar: Itemin kontekstimenu
        @type: C{QtGui.QMenu}"""

        self.luoMenuActionit()

    def mouseDoubleClickEvent(self, event):
        self.asetukset.asetaKlikkausPos(event.pos())
        self.asetukset.show()

    def keyPressEvent(self, event):
        if event.key == QtCore.Qt.Key_Delete:
           self.poista()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.scene().valitseItem(self)

    def setSelected(self, selected):
        if self.valinta:
            self.valinta.setVisible(selected)
        QtGui.QGraphicsItem.setSelected(self, selected)

    def luoMenuActionit(self):
        """Luo kontekstimenulle actionit. Alaluokka voi overideta, jos tarvitaan
        omia actioneja."""
        self.poistaAction = QtGui.QAction('Poista', self.menu)
        """@ivar: Menun 'poista'-action
        @type: C{QtGui.QAction}"""
        self.menu.addAction(self.poistaAction)
        QtCore.QObject.connect(self.poistaAction, QtCore.SIGNAL('triggered()'),
                    self.poista)

        self.asetuksetAction = QtGui.QAction('Asetukset', self.menu)
        """@ivar: Menun action, joka näytää asetuswidgetin.
        @type: C{QtGui.QAction}"""
        self.menu.addAction(self.asetuksetAction)
        QtCore.QObject.connect(self.asetuksetAction, QtCore.SIGNAL('triggered()'),
                self._naytaAsetukset)

    def contextMenuEvent(self, event):
        self.asetukset.asetaKlikkausPos(event.pos())
        self.menu.exec_(event.screenPos())

    def _naytaAsetukset(self):
        """Kutsuu asetuswidgetin show():ta."""
        self.asetukset.show()

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

        self.setZValue(100)

        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable |
                      QtGui.QGraphicsItem.ItemIsSelectable |
                      QtGui.QGraphicsItem.ItemIsFocusable)

        self.setCursor(QtCore.Qt.ClosedHandCursor)

        scene.addItem(self)
        self.asetukset = QNivelWidget(self.scene(), self)

        self.valinta = QNivelValinta(self)

        self.asetaKoordinaatit(x, y)
        self.alustettu = True

    def luoMenuActionit(self):
        self.lisaaNiveltukiAction = QtGui.QAction(u'Lisää niveltuki', self.menu)
        """@ivar: C{QAction}, jolla voi lisätä niveltuen niveleen
        @type: C{QtGui.QAction}"""
        self.menu.addAction(self.lisaaNiveltukiAction)
        QtCore.QObject.connect(self.lisaaNiveltukiAction,
                               QtCore.SIGNAL('triggered()'),
                               self._menuLisaaNiveltuki)

        self.lisaaRullatukiAction = QtGui.QAction(u'Lisää rullatuki', self.menu)
        """@ivar: C{QAction}, jolla voi lisätä rullauten niveleen
        @type: C{QtGui.QAction}"""
        self.menu.addAction(self.lisaaRullatukiAction)
        QtCore.QObject.connect(self.lisaaRullatukiAction,
                               QtCore.SIGNAL('triggered()'),
                               self._menuLisaaRullatuki)

        self.menu.addSeparator()
        QRistikkoItem.luoMenuActionit(self)

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
        self.scene().removeItem(self.asetukset)
        for sauva in self.sauvat:
            self.scene().removeItem(sauva)
        self.scene().removeItem(self)

    def lisaaSauva(self, sauva):
        """@type sauva: L{QSauva}"""
        Nivel.lisaaSauva(self, sauva)
        if not sauva in self.scene().items():
            self.scene().addItem(sauva)

    def lisaaPistekuorma(self, pistekuorma):
        """@type pistekuorma: L{QPistekuorma}"""
        Nivel.lisaaPistekuorma(self, pistekuorma)
        pistekuorma.setParentItem(self)
        if not pistekuorma in self.scene().items():
            self.scene().addItem(pistekuorma)

    def lisaaTuki(self, tuki):
        Nivel.lisaaTuki(self, tuki)
        tuki.setParentItem(self)

    def _menuLisaaNiveltuki(self):
        """Lisää niveltuen tähän niveleen."""
        tuki = QNiveltuki(self)

    def _menuLisaaRullatuki(self):
        """Lisää rullatuen tähän niveleen."""
        tuki = QRullatuki(self)


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
        self.valinta = QSauvaValinta(self)


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
    """Tämä luokka kuvaa piirettävää pistekuormaa.
    @todo: Voiman suuruus ja yksikkö pitäisi piirtää jotenkin
    @todo: Pistekurman siirto (toiseen niveleen ja pyöritys"""
    def __init__(self, nivel, kuormaX, kuormaY):
        QRistikkoItem.__init__(self)
        Pistekuorma.__init__(self, nivel, kuormaX, kuormaY)
        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable |
                      QtGui.QGraphicsItem.ItemIsSelectable |
                      QtGui.QGraphicsItem.ItemIsFocusable)

        self.pen = QtGui.QPen(QtCore.Qt.black)
        """@ivar: Nuolen piirtämiseen käytettävä C{QPen}
        @type: C{QtGui.QPen}"""
        self.pen.setWidth(3)

        self.suuntakulma = self.laskeSuuntakulma()
        """@ivar: Tuen komponenteista laskettu suuntakulma
        @type: C{float}"""
        self.asetaSuuntakulma(self.suuntakulma)

        self.resultantti = self.laskeResultantti()
        """@ivar: Pistekuorman komponenttien resultantti
        @type: C{float}"""

        self.valinta = QPistekuormaValinta(self)
        self.asetukset = QPistekuormaWidget(self.nivel.scene(), self)

        self.setCursor(QtCore.Qt.ClosedHandCursor)

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.drawLine(-50, 0, -10, 0)
        painter.drawLine(-10, 0, -20, 5)
        painter.drawLine(-10, 0, -20, -5)

    def boundingRect(self):
        return QtCore.QRectF(-10, -5, -40, 10)

    def asetaSuuntakulma(self, suuntakulma):
        """Asettaa pistekuorman suuntakulman.
        @param suuntakulma: Asetettava suuntakulma
        @type suuntakulma: C{float}
        @todo: komponentit pitäis laskea"""
        rotMatriisi = QtGui.QMatrix()
        rotMatriisi.rotate(360.0-suuntakulma)
        self.setMatrix(rotMatriisi)

        self.suuntakulma = suuntakulma

    def laskeSuuntakulma(self):
        """Laskee akseleiden suuntaisista komponenteista pistekuorman
        suuntakulma x-akselin suhteen. Suuntakulma on aina positiivinen ja
        väliltä 0-359.
        @returns: pistekuorman suuntakulma
        @rtype: C{float}"""
        kulma = degrees(atan2(self.kY, self.kX))
        if kulma < 0:
            kulma = 360.0 + kulma

        return kulma

    def laskeResultantti(self):
        """Laskee voiman komponenteista resultantin.
        @returns: Voiman komponenttien resultantti
        @rtype: C{float}"""
        return sqrt(pow(self.kX,2) + pow(self.kY,2))

class QTuki(QRistikkoItem):
    """Tämä luokka kuvaa piirettävää tukea. Tämän luokan instanssit eivät ole
    varsinaisesti piirettäviä, mutta toteuttavat tuille yhteisiä
    ominaisuuksia."""
    def __init__(self):
        QRistikkoItem.__init__(self)

        self.naytetaanTukivoimat = False
        """@ivar: Piiretäänkö tuen sijasta tukivoimat
        @type: C{bool}"""

    def luoMenuActionit(self):
        self.naytaTukivoimatAction = QtGui.QAction(u'Näytä tukivoimat',
                self.menu)
        """@ivar: Actioni, jolla voi valita näytetäänkö tukivoimat vai tuki
        @type: C{QtGui.QAction}"""
        self.naytaTukivoimatAction.setCheckable(True)
        self.naytaTukivoimatAction.setChecked(False)
        self.menu.addAction(self.naytaTukivoimatAction)

        QtCore.QObject.connect(self.naytaTukivoimatAction,
        QtCore.SIGNAL('triggered(bool)'), self._asetaNaytaTukivoimat)

        self.menu.addSeparator()
        QRistikkoItem.luoMenuActionit(self)

    def _asetaNaytaTukivoimat(self, naytetaanko):
        """Asettaa näytetäänkö tukivoimat.
        @param naytetaanko: Näytetäänkö tukivoimat
        @type naytetaanko: C{bool}"""
        self.naytetaanTukivoimat = naytetaanko

    def paint(self, painter, options, widget):
        """Alaluokan ei tarvitse enää toteuttaa tätä. C{boundingRect()} pitää
        kuitekin toteuttaa."""
        if self.naytetaanTukivoimat:
            self.piirraTukivoimat(painter)
        else:
            self.piirraTuki(painter)

    def piirraTukivoimat(self, painter):
        """Piirtää tuen tukivoimat. Alaluokan tulee toteuttaa.
        @param painter: Piirtämiseen käytettävä C{QPainter}
        @type painter: C{QtGui.QPainter}"""
        pass

    def piirraTuki(self, painter):
        """Piirtää itse tuen. Alaluokan tulee toteuttaa.
        @param painter: Piirtämiseen käytettävä C{QPainter}
        @type painter: C{QtGui.QPainter}"""
        pass

    def _piirraKolmio(self, painter):
        """Piirtää tuen 'kolmion'.
        @param painter: Piirtämiseen käytettävä C{QPainter}
        @type painter: C{QtGui.QPainter}"""
        pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
        
        painter.drawConvexPolygon(
                 QtCore.QPointF(0, 7),
                 QtCore.QPointF(-15, 30),
                 QtCore.QPointF(15, 30))

    def _piirraTaso(self, painter, etaisyys):
        """Piirtää tason, johon tuki liitetään.
        @param painter: Piirtämiseen käytettävä C{QPainter}
        @type painter: C{QtGui.QPainter}
        @param etaisyys: Etäisyys nivelen keskipisteestä
        @type etaisyys: C{int}"""
        painter.drawLine(-20, etaisyys, 20, etaisyys)
        for x in range(-15, 20, 5):
            painter.drawLine(x, etaisyys, x-5, etaisyys + 5)


class QNiveltuki(QTuki, Tuki):
    """Tämä luokka kuvaa piirettävää niveltukea. Niveltuki on tukevaan
    pintaan jäykästi kiinitetty tuki."""
    def __init__(self, nivel, suuntakulma=0.0):
        """Konstruktori."""
        QTuki.__init__(self)
        Tuki.__init__(self, nivel, suuntakulma)
        
        self.tukivoimaKulmat = [0.0, 90.0]
        self.luoTukivoimat()

        self.tyyppi = Tuki.NIVELTUKI
        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable |
                      QtGui.QGraphicsItem.ItemIsSelectable |
                      QtGui.QGraphicsItem.ItemIsFocusable)

        self.valinta = QTukiValinta(self)
        self.asetukset = QTukiWidget(nivel.scene(), self)
        
    def piirraTuki(self, painter):
        self._piirraKolmio(painter)
        self._piirraTaso(painter, 30)
            
    def boundingRect(self):
        return QtCore.QRectF(-20, 7, 40, 35)
 
    def asetaSuuntakulma(self, suuntakulma):
        Tuki.asetaSuuntakulma(self, suuntakulma)

        rotMatriisi = QtGui.QMatrix()
        rotMatriisi.rotate(360.0-suuntakulma)
        self.setMatrix(rotMatriisi)

class QRullatuki(QTuki, Tuki):
    """Tämä luokka kuvaa piirettävää rullatukea. Rullatuki on tukevaan
    pintaan rullilla kiinitetty tuki."""
    def __init__(self, nivel, suuntakulma=0.0):
        """Konstruktori."""
        QTuki.__init__(self)
        Tuki.__init__(self, nivel, suuntakulma)
        
        self.tukivoimaKulmat = [90.0]
        self.luoTukivoimat()

        self.tyyppi = Tuki.RULLATUKI
        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable |
                      QtGui.QGraphicsItem.ItemIsSelectable |
                      QtGui.QGraphicsItem.ItemIsFocusable)

        self.valinta = QTukiValinta(self)
        self.asetukset = QTukiWidget(nivel.scene(), self)

    def piirraTuki(self, painter):
        self._piirraKolmio(painter)
        painter.drawEllipse(-15, 30, 15, 15)
        painter.drawEllipse(0, 30, 15, 15)
        self._piirraTaso(painter, 45)

    def boundingRect(self):
        return QtCore.QRectF(-20, 7, 40, 50)

    def asetaSuuntakulma(self, suuntakulma):
        Tuki.asetaSuuntakulma(self, suuntakulma)

        rotMatriisi = QtGui.QMatrix()
        rotMatriisi.rotate(360.0-suuntakulma)
        self.setMatrix(rotMatriisi)

