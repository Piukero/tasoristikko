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
        for nivel in ristikko.nivelet:
            self.addItem(nivel)
        for sauva in ristikko.sauvat:
            self.addItem(sauva)
        for tuki in ristikko.tuet:
            self.addItem(tuki)
        for pistekuorma in ristikko.pistekuormat:
            self.addItem(pistekuorma)

class QNivelKoordinaattiWidget(QtGui.QGraphicsWidget):
    """Tämä luokka kuvaa nivelen viereen luotavaa koordinaatti-ikkunaa."""
    def __init__(self, scene, nivel, parent=None, wFlags=0):
        QtGui.QGraphicsWidget.__init__(self, parent)

        frame = QtGui.QFrame()
        frame.setFrameShadow(QtGui.QFrame.Plain)
        frame.setFrameShape(QtGui.QFrame.StyledPanel)

        lX = QtGui.QLabel('x:')
        lY = QtGui.QLabel('y:')
        lM1 = QtGui.QLabel('m')
        lM2 = QtGui.QLabel('m')

        self.nivel = nivel
        """@ivar: Nivel, johon tämä ikkuna liittyy
        @type: L{QNivel<guiristikko.QNivel>}"""

        self.lineEditX = QtGui.QLineEdit('%.2f' % self.nivel.x)
        """@ivar: x-koordinaatin C{QLineEdit}
        @type: C{QtGui.QLineEdit}"""
        self.lineEditX.setFixedWidth(50)
        self.lineEditX.setAlignment(QtCore.Qt.AlignRight)
        self.lineEditY = QtGui.QLineEdit('%.2f' % self.nivel.y)
        """@ivar: y-koordinaatin C{QLineEdit}
        @type: C{QtGui.QLineEdit}"""
        self.lineEditY.setFixedWidth(50)
        self.lineEditY.setAlignment(QtCore.Qt.AlignRight)
        self.connect(self.lineEditX, QtCore.SIGNAL('returnPressed()'),
                self.vaihdaKoordinaatit)
        self.connect(self.lineEditY, QtCore.SIGNAL('returnPressed()'),
                self.vaihdaKoordinaatit)
        
        gl = QtGui.QGridLayout()
        gl.addWidget(lX, 0, 0)
        gl.addWidget(self.lineEditX, 0, 1)
        gl.addWidget(lM1, 0, 2)
        gl.addWidget(lY, 1, 0)
        gl.addWidget(self.lineEditY, 1, 1)
        gl.addWidget(lM2, 1, 2)

        frame.setLayout(gl)

        layout = QtGui.QGraphicsLinearLayout()
        layout.addItem(scene.addWidget(frame))
        self.setLayout(layout)

        self.setPos(self.nivel.pos() + QtCore.QPointF(6,-6))

        self.setZValue(100.0)

    def vaihdaKoordinaatit(self):
        """Vaihtaa nivelen koordinaatit ja piilottaa itsensä."""
        x = float(self.lineEditX.text())
        y = float(self.lineEditY.text())
        self.setVisible(False)
        self.nivel.asetaKoordinaatit(x, y)

    def showEvent(self, event):
        """@todo: asetetaan ikkunnalle focus"""
        self.setPos(self.nivel.pos() + QtCore.QPointF(6, -6))
        self.lineEditX.setText('%.2f' % self.nivel.x)
        self.lineEditY.setText('%.2f' % self.nivel.y)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.setVisible(False)
        elif event.key() == QtCore.Qt.Key_Return:
            self.vaihdaKoordinaatit()
        else:
            QtGui.QGraphicsWidget.keyPressEvent(self, event)

