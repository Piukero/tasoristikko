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

from pyTasoristikko.ristikkotehdas import Ristikkotehdas
from guiristikko import *

class GuiRistikkotehdas(Ristikkotehdas):
    """Luo Qt4 käyttöliittymässä käytettävän ristikon."""
    def __init__(self, scene, ristikko = None):
        """Konstruktori.
        @param scene: QRistikkoScene, johon tämä ristikko lisätään
        @type scene:
        L{QRistikkoScene<ristikkonakyma.QRistikkoScene>}
        @param ristikko: Käytettävä ristikko
        @type ristikko: L{Ristikko<pyTasoristikko.ristikko.Ristikko>}"""
        Ristikkotehdas.__init__(self, ristikko)
        self.scene = scene
        """@ivar: Scene johon ristikko lisätään
        @type: L{QRistikkoScene<ristikkonakyma.QRistikkoScene>}"""

    def luoNivel(self, x, y, nimi):
        nivel = QNivel(self.ristikko, self.scene, x, y)
        return nivel

    def luoSauva(self, nivel1, nivel2, nimi):
        sauva = QSauva(self.ristikko, nivel1, nivel2)

    def luoPistekuorma(self, nivel, kompX, kompY):
        pistekuorma = QPistekuorma(nivel, kompX, kompY)

    def luoTuki(self, nivel, suuntakulmat):
        if len(suuntakulmat) == 1:
            kulma = suuntakulmat[0] - 90.0
            tuki = QRullatuki(nivel, kulma)
        else:
            # TODO: tarkistukset ja kulman laskenta
            tuki = QNiveltuki(nivel)
