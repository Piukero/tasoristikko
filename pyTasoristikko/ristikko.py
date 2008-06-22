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
Tästä modulista löytyy kaikki ristikon piirtämistä varten luodut luokat.
"""

from numpy import sqrt, square, sin, cos, pi, array

class Voimasuure(object):
    """Tämä luokka kuvaa yksinkertaista skalaarista voimasuuretta."""
    def __init__(self, suuruus=0.0, yksikko=''):
        self.suuruus = suuruus #: Voiman suuruus
        self.yksikko = yksikko #: Voiman yksikkö

    def annaYksikkovektori(self):
        """Palauttaa voimasuureen suuntaisen yksikkövektorin. Alaluokkien tulee
        toteuttaa tämä funktio."""
        pass

class Nivel(object):
    """Tämä luokka kuvaa ristikon niveltä."""
    def __init__(self, ristikko, x=0.0, y=0.0):
        self.ristikko = ristikko #: Ristikko, johon nivel kuuluu
        self.pistekuormat = [] #: Niveleen kohdistuvat pistekuormat
        self.tukivoimat = [] #: Niveleen kohdistuvat tukivoimat
        self.tuet = [] #: Niveleen kohdistuvat tuet
        self.sauvat = [] #: Niveleen liittyvät sauvat
        self.x = x #: Nivelen x-koordinaatti
        self.y = y #: Nivelen y-koordinaatti
        self.nimi = '' #: Nivelen nimi

    def lisaaSauva(self, sauva):
        """Lisää niveleen sauvan.
        @param sauva: Lisättävä sauva
        @type sauva: L{Sauva<pyTasoristikko.ristikko.Sauva>}"""
        if not sauva in self.sauvat:
            self.sauvat.append(sauva)
            self.ristikko.lisaaSauva(sauva)
            
    def lisaaTukivoima(self, tukivoima):
        """Lisää niveleen tukivoiman. Tätä ei yleensä tarvitse kutsua luokan
        ulkopuolelta.
        @param tukivoima: Lisättävä tukivoima
        @type tukivoima: L{Tukivoima<pyTasoristikko.ristikko.Tukivoima>}"""
        if not tukivoima in self.tukivoimat:
            self.tukivoimat.append(tukivoima)
            
    def lisaaPistekuorma(self, pistekuorma):
        """Lisää niveleen pistekuorman.
        @param pistekuorma: lisättävä pistekuorma
        @type pistekuorma: L{Pistekuorma<pyTasoristikko.ristikko.Pistekuorma>}"""
        if not pistekuorma in self.pistekuorma:
            self.pistekuorma.append(pistekuorma)
            self.ristikko.lisaaPistekuorma(pistekuorma)
            
    def lisaaTuki(self, tuki):
        """Lisää niveleen tuen."""
        if not tuki in self.tuet:
            self.tuet.append(tuki)
            self.ristikko.lisaaTuki(tuki)
            for tukivoima in tuki.tukivoimat:
                self.lisaaTukivoima(tukivoima)

    def asetaKoordinaatit(self, x, y):
        """Asettaa nivelen koordinaatit
        @param x: x-koordinaatti
        @type x: float
        @param y: y-koordinaatti
        @type y: float"""
        self.x = x
        self.y = y

class Sauva(Voimasuure):
    """Tämä luokka kuvaa ristikon sauvaa."""
    def __init__(self, ristikko, nivel1=None, nivel2=None):
        Voimasuure.__init__(self)
        self.ristikko = ristikko #: Ristikko, johon sauva kuuluu
        self.n1 = nivel1 #: Sauvan pään I{1} nivel
        if self.n1:
            self.n1.lisaaSauva(self)
        self.n2 = nivel2 #: Sauvan pään I{2} nivel
        if self.n2:
            self.n2.lisaaSauva(self)

        self.nimi = '' #: Sauvan nimi

    def asetaNivelet(self, nivel1, nivel2):
        """
        Asettaa nivelet, joihin tämä sauva liittyy. Jos sauva on liitetty
        aikaisemmin muihin niveliin poistetaan se niistä.
        @param nivel1: Sauvan päähän I{1} liittyvä nivel
        @type nivel1: L{Nivel<pyTasoritikko.ristikko.Nivel>}
        @param nivel2: Sauvan päähän I{2} liittyvä nivel
        @type nivel2: L{Nivel<pyTasoritikko.ristikko.Nivel>}
        """
        if self.n1:
            pass
        if self.n2:
            pass
        self.n1 = nivel1
        self.n1.lisaaSauva(self)
        self.n2 = nivel2
        self.n2.lisaaSauva(self)

    def annaPituus(self):
        """
        Laskee sauvan pituuden.
        @return: Sauvan pituus
        """
        x2 = square(self.n2.x - self.n1.x)
        y2 = square(self.n2.y - self.n1.y)
        return sqrt(x2+y2)

    def annaYksikkovektori(self):
        """
        Antaa sauvan yksikkövektorin. Yksikkövektorin suunta on sauvan päästä 1
        päähän 2.
        @return: Sauvan yksikkövektori
        @rtype: numpy.array
        """
        pituus = self.annaPituus()
        ex = (self.n2.x - self.n1.x)/pituus
        ey = (self.n2.y - self.n1.y)/pituus
        return array([ex,ey])

class Tukivoima(Voimasuure):
    """Tämä luokka kuvaa niveleen kohdistuvaa tukivoimaa."""
    def __init__(self, nivel, suuntakulma=90.0):
        """
        Alustaa olion.
        @param nivel: Nivel, johon tukivoima kohdistuu
        @type nivel: L{Nivel<pyTasoristikko.ristikko.Nivel>}
        @param suuntakulma: Tukivoiman suuntakulma x-akselin suhteen
        @type suuntakulma: float
        """
        Voimasuure.__init__(self)
        self.nivel = nivel
        self.suuntakulma = suuntakulma

    def annaYksikkovektori(self):
        """
        Antaa tukivoiman suuntaisen yksikkövektorin.
        @return: Tukivoiman yksikkövektori.
        @rtype: numpy.array"""
        rx = cos(pi*self.suuntakulma/180.0)
        ry = sin(pi*self.suuntakulma/180.0)
        return array([rx,ry])
    
    def asetaSuuntakulma(self, suuntakulma):
        """Asettaa tukivoiman suuntakulman.
        @param suuntakulma: asetettava suuntakulma
        @type suuntakulma: float"""
        self.suuntakulma = suuntakulma

class Pistekuorma(object):
    """Tämä luokka kuvaa niveleen kohdsituvaa pistekuormaa."""
    def __init__(self, nivel, kuormaX, kuormaY):
        """Konstruktori.
        @param nivel: Nivel, johon kuorma liittyy
        @type nivel: L{Nivel<pyTasoristikko.ristikko.Nivel>}
        @param kuormaX: Kuorman x-akselin suuntainen komponentti
        @type kuormaX: float
        @param kuormaY: Kuorman y-akselin suuntainen komponentti
        @type kuormaY: float"""
        self.nivel = nivel #: Nivel, johon kuorma liittyy
        self.kX = kuormaX #: Voiman x-akselin suuntainen komponentti
        self.kY = kuormaY #: Voiman y-akselin suuntainen komponentti
        self.nivel.lisaaPistekuorma(self)

class Ristikko(object):
    """Tämä luokka kuvaa yksinkertaista tasoristikkoa."""
    def __init__(self):
        self.sauvat = [] #: Ristikon sauvat
        self.nivelet = [] #: Ristikon nivelet 
        self.pistekuormat = [] #: Risitkon pistekuormat
        self.tukivoimat = [] #: Risitkon tukivoimat
        self.tuet = [] #: Ristikon tuet
        self.ratkaistu = False #: Onko ristikko ratkaistu

    def lisaaSauva(self, sauva):
        """Lisää ristikkoon sauvan.
        @param sauva: lisättävä sauva
        @type sauva: L{Sauva<pyTasoristikko.ristikko.Sauva>}"""
        if not sauva in self.sauvat:
            self.sauvat.append(sauva)
        self.ratkaistu = False

    def lisaaNivel(self, nivel):
        """Lisää ristikkoon nivelen.
        @param nivel: lisättävä nivel
        @type nivel: L{Nivel<pyTasoristikko.ristikko.Nivel>}"""
        if not nivel in self.nivelet:
            self.nivelet.append(nivel)
        self.ratkaistu = False

    def lisaaPistekuorma(self, pistekuorma):
        """Lisää ristikkoon pistekuorman.
        @param pistekuorma: lisättävä pistekuorma
        @type pistekuorma: L{Pistekuorma<pyTasoristikko.ristikko.Pistekuorma>}"""
        if not pistekuorma in self.pistekuormat:
            self.pistekuormat.append(pistekuorma)
        self.ratkaistu = False

    def lisaaTukivoima(self, tukivoima):
        """Lisää ristikkoon tukivoiman. Tätä ei ole yleensä tarvetta kutsua
        luokan ulkopuolelta.
        @param tukivoima: Lisättävä tukivoima
        @type tukivoima: L{Tukivoima<pyTasorsitikko.ristikko.Tukivoima>}"""
        if not tukivoima in self.tukivoimat:
            self.tukivoimat.append(tukivoima)
        self.ratkaistu = False
    
    def lisaaTuki(self, tuki):
        """Lisää ristikkoon tuen.
        @param tuki: Lisättävä tuki
        @type tuki: L{Tuki<pyTasoristikko.ristikko.Tuki>}"""
        if not tuki in self.tuet:
            self.tuet.append(tuki)
            for tukivoima in tuki.tukivoimat:
                self.lisaaTukivoima(tukivoima)
        self.ratkaistu = False
    
    def asetaRatkaistuksi(self):
        """Asettaa ristikon ratkaistuksi."""
        self.ratkaistu = True
    
    def annaStaattinenKertaluku(self):
        """Palauttaa ristikon staattisen määräävyyden kertaluvun. Ristikko on
        staattisesti määrätty jos kertaluku == 0, staattisesti määräämätön
        jos > 0 ja mekanismi jos < 0.
        @return: staattisen määräävyden kertaluku
        @rtype: int"""
        return 0

class Tuki(object):
    """Tämä luokka kuvaa nivleen liitettyä tukea. Yhdessä tuessa voi olla
    useampi tukivoima."""
    def __init__(self, nivel, suuntakulma=0.0):
        """
        Konstruktori.
        @param nivel: nivel, johon tämä tuki on liittynyt
        @type nivel: L{Nivel<pyTasoristikko.ristikko.Nivel>}
        @param suuntakulma: Tuen suuntakulma pystyasemaan nähden
        @type suuntakulma: float
        """
        self.tukivoimat = [] #: Tukeen kohdistuvat tukivoimat
        self.tukivoimaKulmat = [] #: Tukivoimien suuntakulmat tuen suhteessa
        self.suuntakulma = suuntakulma #: Tuen suuntakulma pystyasemaan nähden
        self.nivel = nivel #: Nivel, johon tuki liittyy
        
    def asetaSuuntakulma(self, suuntakulma):
        """Asettaa tuen ja sen tukivoimien suuntakulman.
        @param suuntakulma: tuen uusi suuntakulma
        @type suuntakulma: float"""
        self.suuntakulma = suuntakulma
        for tuki, tsuuntakulma in zip(self.tukivoimat, self.tukivoimaKulmat):
            tuki.asetaSuuntakulma(tsuuntakulma+self.suuntakulma)
            
    def luoTukivoimat(self):
        """Luo tukivoimaKulmat listasta tukivoimat listan. Tätä ei yleensä
        ole tarvetta kutsua luokan ulkopuolelta."""
        for tKulmat in self.tukivoimaKulmat:
            self.tukivoimat.append(Tukivoima(self.nivel,
                                         tKulmat + self.suuntakulma))
        self.nivel.lisaaTuki(self)
            
