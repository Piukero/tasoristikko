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

"""
Tässä modulista on kaikki ristkon ratkaisuun tarvittavat funktiot.
"""

from numpy import array
from numpy.linalg import solve

def MuodostaKerroinmatriisi(nivelet, sauvat, tukivoimat):
    """Muodostaa lineaarisen yhtälöryhmän kerroinmatriisin.
    @param nivelet: ristikon nivelet
    @type nivelet: C{list} of L{Nivel<ristikko.Nivel>}
    @param sauvat: ristikon sauvat
    @type sauvat: C{list} of L{Sauva<ristikko.Sauva>}
    @param tukivoimat: ristikon tukivoimat
    @type tukivoimat: C{list} of L{Tukivoima<ristikko.Tukivoima>}
    @returns: yhtälöryhman kerroinmatriisi
    @rtype: C{numpy.array}"""
    A = []
    for nivel in nivelet:
        x = []
        y = []
        for sauva in sauvat:
            if sauva in nivel.sauvat:
                yVektori = sauva.annaYksikkovektori()
                if nivel == sauva.n2: # TODO: teeppä tää
                    yVektori *= -1
            else:
                x.append(0.0)
                y.append(0.0)
        for tukivoima in tukivoimat:
            if tukivoima in nivel.tukivoimat:
                pass # TODO: tee tämä
            else:
                x.append(0.0)
                y.append(0.0)
                
        A.append(x)
        A.append(y)
    return array(A)

def MuodostaPistekuormaPystyvektori(nivelet):
    """Muodostaa pistekuormista pystyvektorin.
    @param nivelet: ristikon nivelet
    @type nivelet: C{list} of L{Nivel<ristikko.Nivel>}
    @returns: pistekuormista muodostettu kerroinmatriisi
    @rtype: C{numpy.array}"""
    P = []
    for nivel in nivelet:
        Px = 0.0
        Py = 0.0
        for pistekuorma in nivel.pistekuormat:
            Px += pistekuorma.kX
            Py += pistekuorma.kY
        P.append(Px)
        P.append(Py)
    return array(P)

def RatkaiseRistikko(ristikko):
    """Ratkaisee annetun ristikon ja asettaa ratkistut arvot
    voimasuureisiin.
    @param ristikko: Ratkaistava ristikko
    @type ristikko: L{Ristikko<pyTasoristikko.ristikko.Ristikko>}"""
    A = muodostaKerroinmatriisi(ristikko.nivelet, ristikko.savat,
                                ristikko.tukivoimat)
    p = muodostaPistekuormaPystyvektori(ristikko.pistekuormat)
    ratkaisu = solve(A,p)
    
    ratkaisuNro = 0
    for sauva in ristikko.sauvat:
        sauva.suuruus = 0.0
        ratkaisuNro += 1
        
    for tukivoima in ristikko.tukivoimat:
        tukivoima.suuruus = 0.0
        ratkaisuNro += 1
        
    ristikko.asetaRatkaistuksi()
