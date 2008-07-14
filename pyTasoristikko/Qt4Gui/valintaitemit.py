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

"""Tässä modulissa on C{QRistikkoItemeiden} valintaa kuvaavat luokat. Näiden
luokkien tarkoituksena on näyttää käyttäjälle, että kyseinen item on valittu."""

from PyQt4 import QtCore, QtGui

from guiristikko import *

class QValintaItem(QtGui.QGraphicsItem):
    """Valintaa kuvaavien C{QGraphicsItemien} perusluokka."""
    def __init__(self, ristikkoItem):
        """Konstruktori.
        @param ristikkoItem: C{QRistikkoItem}, jonka valintaa kuvataan.
        @type ristikkoItem:  L{QRistikkoItem}"""
        QtGui.QGraphicsItem.__init__(self)
        
        self.ristikkoItem = ristikkoItem
        """@ivar: C{QRistikkoItem}, jonka valintaa kuvataan.
        @type: L{QRistikkoItem}"""

        self.setParentItem(self.ristikkoItem)
        self.setVisible(False)

class QNivelValinta(QValintaItem):
    """Nivelen valintaa kuvaava luokka."""
    def __init__(self, ristikkoItem):
        QValintaItem.__init__(self, ristikkoItem)
        
        self.rect = QtCore.QRectF(-9, -9, 18, 18)
        """@ivar: Piirettävä C{QRectF}
        @type: C{QtCore.QRectF}"""
        self.pen = QtGui.QPen(QtCore.Qt.gray)
        """@ivar: Piirtämiseen käytettävä C{QPen}
        @type: C{QtGui.QPen}"""
        self.pen.setStyle(QtCore.Qt.DashLine)

        self.setZValue(500.0)

    def paint(self, painter, options, widget):
        painter.setPen(self.pen)
        painter.drawRect(self.rect)

    def boundingRect(self):
        return QtCore.QRectF(-9, -9, 18, 18)


class QSauvaValinta(QValintaItem):
    """Sauvan valintaa kuvaava luokka."""
    def __init__(self, ristikkoItem):
        QValintaItem.__init__(self, ristikkoItem)

    def boundingRect(self):
        return self.ristikkoItem.boundingRect()

    def paint(self, painter, options, widget):
        painter.drawRect(self.ristikkoItem.boundingRect())

class QPistekuormaValinta(QValintaItem):
    """Pistekuorman valintaa kuvaava luokka."""
    def __init__(self, ristikkoItem):
        QValintaItem.__init__(self, ristikkoItem)

        self.pen = QtGui.QPen(QtCore.Qt.gray)
        """@ivar: Piirtämiseen käytettävä C{QPen}
        @type: C{QtGui.QPen}"""
        self.pen.setStyle(QtCore.Qt.DashLine)

        self.rect = QtCore.QRectF(-8, -8, 16, -46)
        """@ivar: Piirettävä C{QRectF}
        @type: C{QtCore.QRectF}"""

    def paint(self, painter, options, widget):
        painter.setPen(self.pen)
        painter.drawRect(self.rect)

    def boundingRect(self):
        return QtCore.QRectF(-8, -8, 16, -46)
