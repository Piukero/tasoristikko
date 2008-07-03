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

"""Tässä modulissa on ristikon asetusten muuttamiseen tarkoitetyt luokat."""

from PyQt4 import QtCore, QtGui


class QAsetusWidget(QtGui.QGraphicsWidget):
    """Tämä luokka kuvaa perus asetus widgetiä. Ei tee vielä juuri mitään."""
    def __init__(self, scene, parent=None, wFlags=0):
        """Konstruktori.
        @param scene: Scene, johon tämä widget lisätään
        @type scene: L{QRistikkoScene<ristikkonakyma.QRistikkoScene>}"""
        QtGui.QGraphicsWidget.__init__(self, parent)
        self.frame = QtGui.QFrame()
        """@ivar: frame johon asetuskentät piirretään
        @type: C{QtGui.QFrame}"""
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.klikkausPos = None
        """@ivar: Tuplaklikkauksen positio
        @type: C{QtCore.QPointF}"""

        self.setZValue(1000)

        layout = QtGui.QGraphicsLinearLayout()
        layout.addItem(scene.addWidget(self.frame))
        self.setLayout(layout)

        scene.lisaaWidget(self)

        self.hide()

    def asetaKlikkausPos(self, pos):
        """Asettaa tuplaklikkauksen position.
        @param pos: tuplaklikkauksen positio
        @type pos: C{QtCore.QPointF}"""
        self.klikkausPos = pos

    def vaihdaAsetukset(self):
        """Vaihtaa ristikkoinstanssinsa asetukset. Kutsutaan, kun käyttäjä on
        painanut C{enter} widgetin sisällä."""
        pass

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.setVisible(False)
        elif event.key() == QtCore.Qt.Key_Return:
            self.vaihdaAsetukset()
        else:
            QtGui.QGraphicsWidget.keyPressEvent(self, event)

    def showEvent(self, event):
        """Pyytää sceneä piilottamaan muut asetuswidgetit.
        @todo: asetetaan ikkunnalle focus"""
        self.scene().piilotaMuutWidgetit(self)
        self.scene().setActiveWindow(self)


class QNivelWidget(QAsetusWidget):
    """Tämä luokka kuvaa nivelen viereen luotavaa asetus ikkunaa."""
    def __init__(self, scene, nivel, parent=None, wFlags=0):
        QAsetusWidget.__init__(self, scene, parent, wFlags)

        lX = QtGui.QLabel('x:')
        lY = QtGui.QLabel('y:')
        lNimi = QtGui.QLabel('Nimi:')
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
        self.lineEditNimi = QtGui.QLineEdit(self.nivel.nimi)
        """@ivar: Nimen C{QLineEdit}
        @type: C{QtGui.QLineEdit}"""

        gl = QtGui.QGridLayout()
        iY = 0
        gl.addWidget(lNimi, iY, 0)
        gl.addWidget(self.lineEditNimi, iY, 1)
        iY += 1
        gl.addWidget(lX, iY, 0)
        gl.addWidget(self.lineEditX, iY, 1)
        gl.addWidget(lM1, iY, 2)
        iY += 1
        gl.addWidget(lY, iY, 0)
        gl.addWidget(self.lineEditY, iY, 1)
        gl.addWidget(lM2, iY, 2)

        self.frame.setLayout(gl)

        self.siirra()

    def vaihdaAsetukset(self):
        """Vaihtaa nivelen koordinaatit ja piilottaa itsensä."""
        x = float(self.lineEditX.text())
        y = float(self.lineEditY.text())
        self.setVisible(False)
        self.nivel.asetaKoordinaatit(x, y)

    def showEvent(self, event):
        QAsetusWidget.showEvent(self, event)
        self.siirra()

    def siirra(self):
        """Siirrä widget C{nivelen} viereen. Asettaa samalla C{lineEditien}
        tekstit."""
        self.setPos(self.nivel.pos() + QtCore.QPointF(6, -6))
        self.lineEditX.setText('%.2f' % self.nivel.x)
        self.lineEditY.setText('%.2f' % self.nivel.y)

class QSauvaWidget(QAsetusWidget):
    """Tämä luokka kuvaa sauvan asetuswidgettiä."""
    def __init__(self, scene, sauva, parent=None, wFlags=0):
        """@param sauva: Widgetin sauva
        @type sauva: L{QSauva}"""
        QAsetusWidget.__init__(self, scene, parent, wFlags)

        self.sauva = sauva
        """@ivar: Sauva, johon tämä widget kuuluu
        @type: L{QSauva}"""

        lNimi = QtGui.QLabel('Nimi:')
        self.lineEditNimi = QtGui.QLineEdit()
        """@ivar: Nimen C{lineEdit}
        @type: C{QtGui.QLineEdit}"""
        self.lineEditNimi.setFixedWidth(50)

        gl = QtGui.QGridLayout()
        iY = 0
        gl.addWidget(lNimi, iY, 0)
        gl.addWidget(self.lineEditNimi, iY, 1)

        self.frame.setLayout(gl)

    def showEvent(self, event):
        self.setPos(self.klikkausPos)
        self.lineEditNimi.setText(self.sauva.nimi)
        QAsetusWidget.showEvent(self, event)
        
