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
Tässä modulista on kaikki tarvittavat ristikon tiedostosta lukemista ja
tiedostoon tallettamista varten tehdyt funktiot. Talennettu tiedosto on yksinkertaisesti sqlite3:lla muodostettu tietokanta.

Tietokannan taulut on esitetty tarkemmin projektin wiki-sivulla 
U{Tiedosto<http://code.google.com/p/tasoristikko/wiki/Tiedosto>}.
"""


import sqlite3
import os

import ristikko
from ristikkopoikkeukset import RistikkoIOVirhe

def TallennaRistikko(ristikko, tiedostoNimi):
    """
    Tallentaa ristikon tiedostoon. Tämä funktio poistaa aikaisemman tiedoston,
    jos sellainen on olemassa. Jos haluaa tehdä tarkistuksia pitää ne tehdä

    muualla.
    @param ristikko: Tallennettava ristikko
    @type ristikko: L{Ristikko<pyTasoristikko.ristikko.Ristikko>}
    @param tiedostoNimi: Tallennettavan tiedoston nimi
    @type tiedostoNimi: C{string}
    @raise RistikkoIOVirhe: Jos tiedostoa ei voida kirjoittaa
    """

    if os.path.exists(tiedostoNimi):
        os.remove(tiedostoNimi)

    if not os.access(os.path.dirname(tiedostoNimi), os.W_OK):
        raise RistikkoIOVirhe(u'Sinulla ei ole oikeuksia kirjoittaa tiedostoa'
                             + u' tähän hakemistoon.');

    conn = sqlite3.connect(tiedostoNimi)
    cur = conn.cursor()

    tableSkripti = """
    create table Nivel(
        NivelNro    INTEGER PRIMARY KEY,
        Nimi        TEXT,
        x           REAL,
        y           REAL
    );

    create table Sauva(
        SauvaNro    INTEGER PRIMARY KEY,
        Nimi        TEXT,
        Suuruus     REAL,
        Yksikko     TEXT,
        Nivel1      INTEGER,
        Nivel2      INTEGER
    );

    create table Tuki(
        TukiNro         INTEGER PRIMARY KEY,
        Tyyppi          INTEGER,
        Suuntakulma     REAL,
        SuuruusX        REAL,
        SuuruusY        REAL,
        Yksikko         TEXT,
        Nivel           INTEGER
    );

    create table Pistekuorma(
        PistekuormaNro  INTEGER PRIMARY KEY,
        XKomp           REAL,
        YKomp           REAL,
        Yksikko         TEXT,
        Nivel           INTEGER
    );
    """

    cur.executescript(tableSkripti)

    nivelDict = {}
    nivelNro = 0
    for nivel in ristikko.nivelet:
        tiedot = (nivelNro, nivel.nimi, nivel.x, nivel.y)
        cur.execute('insert into Nivel(NivelNro, Nimi, x, y) values (?,?,?,?)',
                tiedot)
        nivelDict[nivel] = nivelNro
        nivelNro += 1

    sauvaNro = 0
    for sauva in ristikko.sauvat:
        n1Nro = nivelDict[sauva.n1]
        n2Nro = nivelDict[sauva.n2]
        tiedot = (sauvaNro, sauva.nimi, sauva.suuruus, sauva.yksikko, n1Nro,
                  n2Nro)
        cur.execute('insert into Sauva(SauvaNro, Nimi, Suuruus, Yksikko,'
               +'Nivel1, Nivel2) values (?,?,?,?,?,?)', tiedot)
        sauvaNro += 1

    tukiNro = 0
    for tuki in ristikko.tuet:
        nNro = nivelDict[tuki.nivel]
        suuruusX, suuruusY = tuki.annaResultantti()
        tiedot = (tukiNro, tuki.tyyppi, tuki.suuntakulma, suuruusX, suuruusY,
                  tuki.yksikko, nNro)
        cur.execute('insert into Tuki(TukiNro, Tyyppi, Suuntakulma,'
                   +'SuuruusX,SuuruusY,Yksikko, Nivel)'
                   +' values (?,?,?,?,?,?,?)', tiedot)
        tukiNro += 1

    pistekuormaNro = 0
    for pk in ristikko.pistekuormat:
        nNro = nivelDict[pk.nivel]
        tiedot = (pistekuormaNro, pk.kX, pk.kY, pk.yksikko, nNro)
        cur.execute('insert into Pistekuorma(PistekuormaNro, XKomp, YKomp,'
                + 'Yksikko, Nivel) values (?,?,?,?,?)', tiedot)
        pistekuormaNro += 1

    conn.commit()
    cur.close()

    ristikko.asetaTallennetuksi(tiedostoNimi)

def AvaaRistikko(tiedostoNimi, ristikkoTehdas):
    """
    Avaa ristikon tiedostosta.
    @param tiedostoNimi: Avattavan tiedoston nimi
    @type tiedostoNimi: C{string}
    @param ristikkoTehdas: C{Ristikkotehdas}, jolla ristikko luodaan
    @type ristikkoTehdas: L{Ristikkotehdas<ristikkotehdas.Ristikkotehdas>}
    @raise RistikkoIOExceptio: jos avaus ei onnistunut
    """

    rt = ristikkoTehdas
    if not os.access(tiedostoNimi, os.R_OK):
        raise RistikkoIOVirhe('Sinulla ei ole lukuoikeuksia tiedostoon.')

    try:
        con = sqlite3.connect(tiedostoNimi)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        nivelDict = {}
        rivit = cur.execute('select * from Nivel')
        for rivi in rivit:
            nivelNro = rivi['NivelNro']
            nimi = rivi['Nimi']
            x = rivi['x']
            y = rivi['y']
            nivel = rt.luoNivel(x, y)
            nivelDict[nivelNro] = nivel
        
        rivit = cur.execute('select * from Sauva')
        for rivi in rivit:
            nimi = rivi['Nimi']
            n1Nro = rivi['Nivel1']
            n2Nro = rivi['Nivel2']
            rt.luoSauva(nivelDict[n1Nro], nivelDict[n2Nro])

        rivit = cur.execute('select * from Tuki')
        for rivi in rivit:
            nivelNro = rivi['Nivel']
            tyyppi = rivi['Tyyppi']
            suuntakulma = rivi['Suuntakulma']
            rt.luoTuki(nivelDict[nivelNro], tyyppi, suuntakulma)

        rivit = cur.execute('select * from Pistekuorma')
        for rivi in rivit:
            nivelNro = rivi['Nivel']
            xKomp = rivi['XKomp']
            yKomp = rivi['YKomp']
            rt.luoPistekuorma(nivelDict[nivelNro], xKomp, yKomp)

    except sqlite3.DatabaseError:
        raise RistikkoIOVirhe('Tiedosto ei ole oikeaa muotoa tai se on'
                              +' korruptoitunut.')
    except sqlite3.OperationalError:
        raise RistikkoIOVirhe('')
    
    rt.ristikko.asetaTallennetuksi(tiedostoNimi)

def AvaaAsetukset(tiedostoNimi):
    """
    Avaa tiedostosta mahdollisen gui:n asetukset.
    """
    pass


def LuoTestiRistikko(ristikkoTehdas):
    """Luo yksinkertaisen testiristikon ristikkotehtaan avulla.
    @param ristikkoTehdas: käytettävä ristikkotehdas
    @type ristikkoTehdas: L{Ristikkotehdas<ristikkotehdas.Ristikkotehdas>}"""

    rt = ristikkoTehdas
    n1 = rt.luoNivel(1.0, 1.0)
    n2 = rt.luoNivel(4.0, 1.0)
    n3 = rt.luoNivel(1.0, 4.0)
    n4 = rt.luoNivel(4.0, 4.0)

    rt.luoSauva(n1, n2)
    rt.luoSauva(n2, n3)
    rt.luoSauva(n3, n1)
    rt.luoSauva(n2, n4)
    rt.luoSauva(n3, n4)

    rt.luoPistekuorma(n4, 0.0, -1.0)
