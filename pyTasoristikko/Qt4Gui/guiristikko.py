# -*- coding: utf-8 -*-
# Tasoristikko: Tasristikkoja ratkaiseva ohjelma
# Copyright (C) 2008 Ville Leskinen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tässä modulissa on ristikon graafista kuvaamista varten tarvittavat luokat
."""

from PyQt4 import QtCore, QtGui

from pyTasoristikko.ristikko import *

NivelPen = QtGui.QPen(QtCore.Qt.black) #: Nivelen reunaviiva
NivelPen.setWidth(3)

NivelBrush = QtGui.QBrush(QtCore.Qt.white) #: Nivelen täyttö

class QNivel(QtGui.QGraphicsItem, Nivel):
    """Tämä luokka kuvaa piirettävää niveltä."""
    def __init__(self, ristikko, scene, x=0.0, y=0.0):
        QtGui.QGraphicsItem.__init__(self)
        Nivel.__init__(self,ristikko,x,y)
        self.rect = QtCore.QRectF(-6,-6,12,12) #: Piirettävän alueen QRectF
        self.pen = NivelPen #: Piirrossa käytettävä QPen
        self.brush = NivelBrush #: Piirrossa käytettävä brush

    def asetaKoordinaatit(self, x, y):
        Nivel.asetaKoordinaatit(self, x, y)
        self.setPos(x,y)
    
    def paint(self, painter, option, widget=None):
        painter.setPen(self.pen)
        painter.serBrush(self.brush)
        painter.drawEllipse(self.rect)
    
    def boundingRect(self):
        return self.rect
    
class QSauva(QtGui.QGraphicsItem, Sauva):
    """Tämä luokka kuvaa piirettävää sauvaa."""
    def __init__(self, ristikko, nivel1=None, nivel2=None):
        QtGui.QGraphicsItem.__init__(self)
        Sauva.__init__(self, ristikko, nivel1, nivel2)
        self.pen = QtGui.QPen() #: Piirtämiseen käytettävä QPen
        self.pen.setWidth(6)

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.drawLine(QtCore.QLineF(self.n1.pos(), self.n2.pos()))

class QPistekuorma(QtGui.QGraphicsItem, Pistekuorma):
    """Tämä luokka kuvaa piirettävää pistekuormaa."""
    def __init__(self, nivel, kuormaX, kuormaY):
        QtGui.QGraphicsItem.__init__(self)
        Pistekuorma.__init__(self, nivel, kuormaX, kuormaY)
        
class QNiveltuki(QtGui.QGraphicsItem, Tuki):
    """Tämä luokka kuvaa piirettävää niveltukea. Niveltuki on tukevaan
    pintaan jäykästi kiinitetty tuki."""
    def __init__(self, nivel, suuntakulma=0.0):
        """Konstruktori."""
        QtGui.QGraphicsItem.__init__(self)
        Tuki.__init__(self, nivel, suuntakulma)
        
        self.tukivoimaKulmat = [0.0, 90.0]
        self.luoTukivoimat()
        
class QRullatuki(QtGui.QGraphicsItem, Tuki):
    """Tämä luokka kuvaa piirettävää rullatukea. Rullatuki on tukevaan
    pintaan rullilla kiinitetty tuki."""
    def __init__(self, nivel, suuntakulma=0.0):
        """Konstruktori."""
        QtGui.QGraphicsItem.__init__(self)
        Tuki.__init__(self, nivel, suuntakulma)
        
        self.tukivoimaKulmat = [90.0]
        self.luoTukivoimat()
