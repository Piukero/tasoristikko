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

"""
Tässä modulista on kaikki tarvittavat ristikon tiedostosta lukemista ja
tiedostoon tallettamista varten tehdyt funktiot. Talennettu tiedosto on yksinkertaisesti sqlite3:lla muodostettu tietokanta.
Tietokannasta löytyvät seuraavat taulut.

    - Nivel
        - NivelNro
        - Nimi
        - x
        - y
    - Sauva
        - SauvaNro
        - Nimi
        - Suuruus
        - Yksikko
        - Nivel1
        - Nivel2
    - Tukivoima
        - TukvoimaNro
        - Suuruus
        - Yksikko
        - Suuntakulma
        - Nivel
    - Pistekuorma
        - PistekuormaNro
        - XKomp
        - YKomp
        - Yksikko
        - Nivel
"""

import sqlite3
import os

import ristikko

def TallennaRistikko(ristikko, tiedostoNimi):
    """
    Tallentaa ristikon tiedostoon.
    @param ristikko: Tallennettava ristikko
    @type ristikko: L{Ristikko<pyTasoristikko.ristikko.Ristikko>}
    @param tiedostoNimi: Tallennettavan tiedoston nimi
    @type tiedostoNimi: string
    """

    onkoTiedostoa = os.path.exists(tiedostoNimi)

    conn = sqlite3.connection(tiedostoNimi)
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

    create table Tukivoima(
        TukivoimaNro    INTEGER PRIMARY KEY,
        Suuruus         REAL,
        Yksikko         TEXT,
        Suuntakulma     REAL,
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

    if onkoTiedostoa:
        cur.execute("delete from table Nivel, Sauva, Tukivoima, Pistekuorma")
    else:
        cur.executescript(tableSkripti)

    nivelDict = {}
    nivelNro = 0
    for nivel in ristikko.nivelet:
        tiedot = (nivelNro, nivel.nimi, nivel.x, nivel.y)
        cur.execute("insert into Nivel(NivelNro, Nimi, x, y) values (?,?,?,?)",
                tiedot)
        nivelDict[nivel] = nivelNro
        nivelNro += 1

    sauvaNro = 0
    for sauva in ristikko.sauvat:
        n1Nro = nivelDict[sauva.n1]
        n2Nro = nivelDict[sauva.n2]
        tiedot = (sauvaNro, sauva.nimi, sauva.suuruus, sauva.yksikko, n1Nro,
                n2Nro)
        cur.execute("insert into Sauva(SauvaNro, Nimi, Suuruus, Yksikko,"
               +"Nivel1, Nivel2) values (?,?,?,?,?,?)", tiedot)
        sauvaNro += 1

    tukivoimaNro = 0
    for tv in ristikko.tukivoimat:
        nNro = nivelDict[tv.nivel]
        tiedot = (tukivoimaNro, tv.suuruus, tv.yksikko, tv.suuntakulma, nNro)
        cur.execute("insert into Tukivoima(TukivoimaNro, Suuruus, Yksikko,"
                +"Suuntakulma, Nivel) values (?,?,?,?,?)", tiedot)
        tukivoimaNro += 1

    pistekuormaNro = 0
    for pk in ristikko.pistekuormat:
        nNro = nivelDict(pk.nivel)
        tiedot = (pistekuormaNro, pk.kX, pk.kY, pk.yksikko, nNro)
        cur.execute("insert into Pistekuorma(PistekuormaNro, XKomp, YKomp,"
                + "Yksikko, Nivel) values (?,?,?,?,?)", tiedot)
        pistekuormaNro += 1

    conn.commit()
    cur.close()

def AvaaRistikko(tiedostoNimi):
    """
    Avaa ristikon tiedostosta.
    """
    
    ris = ristikko.Ristikko()
    return ris

def AvaaAsetukset(tiedostoNimi):
    """
    Avaa tiedostosta mahdollisen gui:n asetukset.
    """
    pass
