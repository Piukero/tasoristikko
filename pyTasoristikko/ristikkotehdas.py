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

"""Tässä modulissa on ristikkoja luova luokka. Tarkoitus on, että mahdolliset
graafiset käyttöliittymät perivät modulin luokan luodakseen käyttöliittymässä
käytettävän ristikon."""

from ristikko import Ristikko

class Ristikkotehdas(object):
    """Ristikkoja luova luokka."""
    def __init__(self, ristikko = None):
        """Konstruktori. Parametriksi voi antaa ristikon, jos se on eri kuin
        perusristikko.
        @param ristikko: luotava ristikko
        @type ristikko: L{Ristikko<pyTasoristikko.ristikko.Ristikko>}"""
        self.ristikko = ristikko
        """@ivar: Luotava ristikko
        @type: L{Ristikko<ristikko.Ristikko>}"""
        if not self.ristikko:
            self.ristikko = Ristikko()

    def luoNivel(self, x, y):
        """Luo ristikon nivelen. Alaluokat toteuttavat.
        @param x: nivelen x-koordinaatti
        @type x: float
        @param y: nivelen y-koordinaatti
        @type y: float
        @returns: luotu nivel
        @rtype: L{Nivel<pyTasoristikko.ristikko.Nivel>}"""
        pass

    def luoSauva(self, nivel1, nivel2):
        """Luo ristikon sauvan. Alaluokat toteuttavat.
        @param nivel1: sauvan päähän 1 liittyvä nivel
        @type nivel1: L{Nivel<pyTasoristikko.ristikko.Nivel>}
        @param nivel2: sauvan päähän 2 liittyvä nivel
        @type nivel2: L{Nivel<pyTasoristikko.ristikko.Nivel>}"""
        pass

    def luoTuki(self, nivel, tyyppi, suuntakulma):
        """Luo ristikkoon tuen. Alaluokat toteuttavat.
        @param nivel: nivel, johon tukivoima kohdistuu
        @type nivel: L{Nivel<pyTasoristikko.ristikko.Nivel>}
        @param tyyppi: Nivelen tyyppi
        @type tyyppi: L{ristikko.Tuki.NIVELTUKI} tai L{ristikko.Tuki.RULLATUKI}
        @param suuntakulma: tuen suuntakulma
        @type suuntakulma: C{float}
        @raise RistikkoIOVirhe: Jos annettu tyyppi on tuntematon."""
        pass

    def luoPistekuorma(self, nivel, kompX, kompY):
        """Luo ristikkoon pistekuorman. Alaluokat toteuttavat.
        @param nivel: nivel, johon tukivoima kohdistuu
        @type nivel: L{Nivel<pyTasoristikko.ristikko.Nivel>}
        @param kompX: pistekuorman x-akselin suuntainen komponentti
        @type kompX: float
        @param kompY: pistekuorman y-akselin suuntainen komponentti
        @type kompY: float"""
        pass
