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
Tästä modulista löytyy kaikki ristikon piirtämistä varten luodut luokat.
Tarkoitus on, että ainoastan C{Nivel} lisätään ristikkoon. Muut luokat
lisätään niveleen, joka puolestaan lisää ne ristikkoon. Myös kaikki
muut operaatiot tehdään C{Nivel}-luokan kautta. Ideana on, että alemman tason
luokkien operaatiot yksinkertaistuvat, jolloin ei tarvitse miettiä, mistä
kaikista luokista pitää operaatioita kutsua.

Instanssien voimat kuvataan niin, että voimien muuttujien kerroin on aina yksi.
Yksikko-muuttujalla kerrotaan ainoastaan miten voima kuvataan esimerkiksi
käyttöliittymässä. Esimerkiksi jos voima on I{1 kN} on voiman muuttuja I{1000}
ja C{yksikko} on 'kN'.
"""

from numpy import sqrt, square, sin, cos, pi, array

YKSIKOT = [ 'N', 'kN', 'MN' ] #: Voimissa käytettävät yksiköt
YKSIKKOKERTOIMET = { 'N' : 1,
                     'kN': 1000,
                     'MN': 1000000 } #: Yksikköjen kertoimet


class Voimasuure(object):
    """Tämä luokka kuvaa yksinkertaista skalaarista voimasuuretta."""
    def __init__(self, suuruus=0.0, yksikko=''):
        self.suuruus = suuruus
        """@ivar: Voiman suuruus
        @type: C{float}"""
        self.yksikko = yksikko
        """@ivar: Voiman yksikkö
        @type: C{string}"""

    def annaYksikkovektori(self):
        """Palauttaa voimasuureen suuntaisen yksikkövektorin. Alaluokkien tulee
        toteuttaa tämä funktio."""
        pass

    def asetaSuuruus(self, suuruus):
        """Asettaa voimasuureen suuruuden.
        @param suuruus: voimasuureen suuruus
        @type suuruus: C{float}"""
        self.suuruus = suuruus

    def asetaYksikko(self, yksikko):
        """Asettaa voimasuureen yksikön.
        @param yksikko: voimasuureen yksikko
        @type yksikko: C{string}"""
        self.yksikko = yksikko

class Nivel(object):
    """Tämä luokka kuvaa ristikon niveltä."""
    def __init__(self, ristikko, x=0.0, y=0.0):
        self.ristikko = ristikko
        """@ivar: C{Ristikko}, johon nivel kuuluu
        @type: L{Ristikko}"""
        self.pistekuormat = []
        """@ivar: Niveleen kohdistuvat pistekuormat
        @type: C{list} of L{Pistekuorma}"""
        self.tukivoimat = []
        """@ivar: Niveleen kohdistuvat tukivoimat
        @type: C{list} of L{Tukivoima}"""
        self.tuet = []
        """@ivar: Niveleen kohdistuvat tuet
        @type: C{list} of L{Tuki}"""
        self.sauvat = []
        """@ivar: Niveleen liittyvät sauvat
        @type: C{list} of L{Sauva}"""
        self.x = x
        """@ivar: Nivelen x-koordinaatti
        @type: C{float}"""
        self.y = y
        """@ivar: Nivelen y-koordinaatti
        @type: C{float}"""
        self.nimi = ''
        """@ivar: Nivelen nimi
        @type: C{string}"""

        if self.ristikko:
            self.ristikko.lisaaNivel(self)

    def asetaNimi(self, nimi):
        """Asettaa nivelen nimen.
        @param nimi: Nivelen nimi
        @type nimi: C{string}"""
        self.nimi = nimi
        self.ristikko.muuttui()

    def lisaaSauva(self, sauva):
        """Lisää niveleen sauvan.
        @param sauva: Lisättävä sauva
        @type sauva: L{Sauva<pyTasoristikko.ristikko.Sauva>}"""
        if not sauva in self.sauvat:
            self.sauvat.append(sauva)
            self.ristikko.lisaaSauva(sauva)
        self.ristikko.muuttui()
            
    def lisaaTukivoima(self, tukivoima):
        """Lisää niveleen tukivoiman. Tätä ei yleensä tarvitse kutsua luokan
        ulkopuolelta.
        @param tukivoima: Lisättävä tukivoima
        @type tukivoima: L{Tukivoima<pyTasoristikko.ristikko.Tukivoima>}"""
        if not tukivoima in self.tukivoimat:
            self.tukivoimat.append(tukivoima)
        self.ristikko.muuttui()
            
    def lisaaPistekuorma(self, pistekuorma):
        """Lisää niveleen pistekuorman.
        @param pistekuorma: lisättävä pistekuorma
        @type pistekuorma: L{Pistekuorma<pyTasoristikko.ristikko.Pistekuorma>}"""
        if not pistekuorma in self.pistekuormat:
            self.pistekuormat.append(pistekuorma)
            self.ristikko.lisaaPistekuorma(pistekuorma)
        self.ristikko.muuttui()
            
    def lisaaTuki(self, tuki):
        """Lisää niveleen tuen."""
        if not tuki in self.tuet:
            self.tuet.append(tuki)
            self.ristikko.lisaaTuki(tuki)
            for tukivoima in tuki.tukivoimat:
                self.lisaaTukivoima(tukivoima)
        self.ristikko.muuttui()

    def asetaKoordinaatit(self, x, y):
        """Asettaa nivelen koordinaatit
        @param x: x-koordinaatti
        @type x: float
        @param y: y-koordinaatti
        @type y: float"""
        self.x = x
        self.y = y
        self.ristikko.muuttui()

    def poista(self):
        """Poistaa nivelen ja kaikki niveleen kuuluvat osat ristikosta."""
        self.ristikko.poistaNivel(self)

    def poistaPistekuorma(self, pistekuorma):
        """Poistaa nivelestä ja ristikosta pistekuorman.
        @param pistekuorma: poistettava pistekuorma
        @type pistekuorma: L{Pistekuorma}"""
        if pistekuorma in self.pistekuormat:
            self.pistekuormat.remove(pistekuorma)
        self.ristikko.poistaPistekuorma(pistekuorma)
        self.ristikko.muuttui()

    def poistaSauva(self, sauva):
        """Poistaa nivelestä ja ristikosta sauvan.
        @param sauva: poistettava sauva
        @type sauva: L{Sauva}"""
        if sauva in self.sauvat:
            self.sauvat.remove(sauva)
        self.ristikko.poistaSauva(sauva)

    def poistaTuki(self, tuki):
        """Poistaa nivelestä ja ristikosta tuen.
        @param tuki: poistettava tuki
        @type tuki: L{Tuki}"""
        if tuki in self.tuet:
            for tv in tuki.tukivoimat:
                if tv in self.tukivoimat:
                    self.tukivoimat.remove(tv)
            self.tuet.remove(tuki)
        self.ristikko.poistaTuki(tuki)

class Sauva(Voimasuure):
    """Tämä luokka kuvaa ristikon sauvaa."""
    def __init__(self, ristikko, nivel1=None, nivel2=None):
        Voimasuure.__init__(self)
        self.ristikko = ristikko
        """@ivar: Ristikko, johon sauva kuuluu
        @type: L{Ristikko}"""
        self.n1 = nivel1
        """@ivar: Sauvan pään I{1} nivel
        @type: L{Nivel}"""
        if self.n1:
            self.n1.lisaaSauva(self)
        self.n2 = nivel2
        """@ivar: Sauvan pään I{2} nivel
        @type: L{Nivel}"""
        if self.n2:
            self.n2.lisaaSauva(self)

        self.nimi = ''
        """@ivar: Sauvan nimi
        @type: C{string}"""

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
            self.n1.poistaSauva(self)
        if self.n2:
            self.n2.poistaSauva(self)
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
        @rtype: C{numpy.array}
        """
        pituus = self.annaPituus()
        ex = (self.n2.x - self.n1.x)/pituus
        ey = (self.n2.y - self.n1.y)/pituus
        return array([ex,ey])

    def asetaNimi(self, nimi):
        """Asettaa sauvalle nimen
        @param nimi: Sauvan nimi
        @type nimi: C{string}"""
        self.nimi = nimi
        self.ristikko.muuttui()

    def poista(self):
        """Poistaa sauvan."""
        self.ristikko.poistaSauva(self)

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
        @rtype: C{numpy.array}"""
        rx = cos(pi*self.suuntakulma/180.0)
        ry = sin(pi*self.suuntakulma/180.0)
        return array([rx,ry])
    
    def asetaSuuntakulma(self, suuntakulma):
        """Asettaa tukivoiman suuntakulman.
        @param suuntakulma: asetettava suuntakulma
        @type suuntakulma: C{float}"""
        self.suuntakulma = suuntakulma
        self.nivel.ristikko.muuttui()

class Pistekuorma(object):
    """Tämä luokka kuvaa niveleen kohdsituvaa pistekuormaa."""
    def __init__(self, nivel, kuormaX, kuormaY):
        """Konstruktori.
        @param nivel: Nivel, johon kuorma liittyy
        @type nivel: L{Nivel}
        @param kuormaX: Kuorman x-akselin suuntainen komponentti
        @type kuormaX: C{float}
        @param kuormaY: Kuorman y-akselin suuntainen komponentti
        @type kuormaY: C{float}"""
        self.nivel = nivel
        """@ivar: Nivel, johon kuorma liittyy
        @type: L{Nivel}"""
        self.kX = kuormaX
        """@ivar: Voiman x-akselin suuntainen komponentti
        @type: C{float}"""
        self.kY = kuormaY
        """@ivar: Voiman y-akselin suuntainen komponentti
        @type: C{float}"""
        self.yksikko = ''
        """@ivar: Pistekuorman yksikko
        @type: C{string}"""
        self.nivel.lisaaPistekuorma(self)

    def poista(self):
        """Poistaa pistekuorman."""
        self.nivel.poistaPistekuorma(self)

class Ristikko(object):
    """Tämä luokka kuvaa yksinkertaista tasoristikkoa."""
    def __init__(self):
        self.sauvat = []
        """@ivar: Ristikon sauvat
        @type: C{list} of L{Sauva}"""
        self.nivelet = []
        """@ivar: Ristikon nivelet
        @type: C{list} of L{Nivel}"""
        self.pistekuormat = []
        """@ivar: Risitkon pistekuormat
        @type: C{list} of L{Pistekuorma}"""
        self.tukivoimat = []
        """@ivar: Risitkon tukivoimat
        @type: C{list} of L{Tukivoima}"""
        self.tuet = []
        """@ivar: Ristikon tuet
        @type: C{list} of L{Tuki}"""
        self.ratkaistu = False
        """@ivar: Onko ristikko ratkaistu
        @type: C{bool}"""
        self.tiedostoNimi = ''
        """@ivar: Tiedosto, johon ristikko on tallenettu
        @type: C{string}"""
        self.tallennettu = False
        """@ivar: Onko tämä versio ristikosta tallenettu
        @type: C{bool}"""

    def lisaaSauva(self, sauva):
        """Lisää ristikkoon sauvan.
        @param sauva: lisättävä sauva
        @type sauva: L{Sauva}"""
        if not sauva in self.sauvat:
            self.sauvat.append(sauva)
        self.muuttui()

    def lisaaNivel(self, nivel):
        """Lisää ristikkoon nivelen.
        @param nivel: lisättävä nivel
        @type nivel: L{Nivel}"""
        if not nivel in self.nivelet:
            self.nivelet.append(nivel)
        self.muuttui()

    def lisaaPistekuorma(self, pistekuorma):
        """Lisää ristikkoon pistekuorman.
        @param pistekuorma: lisättävä pistekuorma
        @type pistekuorma: L{Pistekuorma}"""
        if not pistekuorma in self.pistekuormat:
            self.pistekuormat.append(pistekuorma)
        self.muuttui()

    def lisaaTukivoima(self, tukivoima):
        """Lisää ristikkoon tukivoiman. Tätä ei ole yleensä tarvetta kutsua
        luokan ulkopuolelta.
        @param tukivoima: Lisättävä tukivoima
        @type tukivoima: L{Tukivoima}"""
        if not tukivoima in self.tukivoimat:
            self.tukivoimat.append(tukivoima)
        self.muuttui()
    
    def lisaaTuki(self, tuki):
        """Lisää ristikkoon tuen.
        @param tuki: Lisättävä tuki
        @type tuki: L{Tuki}"""
        if not tuki in self.tuet:
            self.tuet.append(tuki)
            for tukivoima in tuki.tukivoimat:
                self.lisaaTukivoima(tukivoima)
        self.muuttui()

    def asetaTallennetuksi(self, tiedosto):
        """Kertoo ristikolle, että se on tallennettu tiedostoon.
        @param tiedosto: Tiedosto, johon tallennettu
        @type tiedosto: C{string}"""
        self.tiedostoNimi = tiedosto
        self.tallennettu = True
    
    def asetaRatkaistuksi(self):
        """Asettaa ristikon ratkaistuksi."""
        self.ratkaistu = True
    
    def annaStaattinenKertaluku(self):
        """Palauttaa ristikon staattisen määräävyyden kertaluvun. Ristikko on
        staattisesti määrätty jos kertaluku == 0, staattisesti määräämätön
        jos > 0 ja mekanismi jos < 0.
        @return: staattisen määräävyden kertaluku
        @rtype: C{int}"""
        n = len(self.nivelet)
        s = len(self.sauvat)
        t = len(self.tukivoimat)
        return 2*n - s - t

    def poistaNivel(self, nivel):
        """Poistaa annetun nivelen ristikosta.
        @param nivel: poistettava nivel
        @type nivel: L{Nivel}"""
        if nivel in self.nivelet:
            for tuki in nivel.tuet:
                self.poistaTuki(tuki)
            for sauva in nivel.sauvat:
                self.poistaSauva(sauva)
            for pistekuorma in nivel.pistekuormat:
                self.poistaPistekuorma(pistekuorma)
            self.nivelet.remove(nivel)
        self.muuttui()

    def poistaSauva(self, sauva):
        """Poistaa annetun sauvan ristikosta.
        @param sauva: poistettava sauva
        @type sauva: L{Sauva}"""
        if sauva in self.sauvat:
            self.sauvat.remove(sauva)
        self.muuttui()

    def poistaTuki(self, tuki):
        """Poistaa annetun tuen ristikosta.
        @param tuki: poistettava tuki
        @type tuki: L{Tuki}"""
        if tuki in self.tuet:
            for tv in tuki.tukivoimat:
                if tv in self.tukivoimat:
                    self.tukivoimat.remove(tv)
            self.tuet.remove(tuki)
        self.muuttui()

    def poistaPistekuorma(self, pistekuorma):
        """Poistaa annetun pistekuorman ristikosta.
        @param pistekuorma: poistettava pistekuorma
        @type pistekuorma: L{Pistekuorma}"""
        if pistekuorma in self.pistekuormat:
            self.pistekuormat.remove(pistekuorma)
        self.muuttui()

    def poista(self):
        """Poistaa koko ristikon."""
        nivelet = self.nivelet[:]
        for nivel in nivelet:
            nivel.poista()

    def muuttui(self):
        """Tätä kutsumalla kerrotaan ristikolle, että se muuttui."""
        self.ratkaistu = False
        self.tallennettu = False

class Tuki(object):
    """Tämä luokka kuvaa nivleen liitettyä tukea. Yhdessä tuessa voi olla
    useampi tukivoima."""

    TUNTEMATON, NIVELTUKI, RULLATUKI = range(3)

    def __init__(self, nivel, suuntakulma=0.0):
        """
        Konstruktori.
        @param nivel: nivel, johon tämä tuki on liittynyt
        @type nivel: L{Nivel}
        @param suuntakulma: Tuen suuntakulma pystyasemaan nähden
        @type suuntakulma: C{float}
        """
        self.tukivoimat = []
        """@ivar: Tuen tukivoimat
        @type: C{list} of L{Tukivoima}"""
        self.tukivoimaKulmat = []
        """@ivar: Tukivoimien suuntakulmat tuen suhteessa
        @type: C{list} of C{float}"""
        self.suuntakulma = suuntakulma
        """@ivar: Tuen suuntakulma pystyasemaan nähden
        @type: C{float}"""
        self.asetaSuuntakulma(suuntakulma)

        self.nivel = nivel
        """@ivar: Nivel, johon tuki liittyy
        @type: L{Nivel}"""
        self.tyyppi = Tuki.TUNTEMATON
        """@ivar: Nivelen tyyppi
        @type: C{int}"""
        self.yksikko = ''
        """@ivar: Tuen tukivoimien yksikko
        @type: C{String}"""
        self.nimi = ''
        """@ivar: Tuen nimi
        @type: C{string}"""
        
    def asetaSuuntakulma(self, suuntakulma):
        """Asettaa tuen ja sen tukivoimien suuntakulman.
        @param suuntakulma: tuen uusi suuntakulma
        @type suuntakulma: float"""
        self.suuntakulma = suuntakulma
        for tuki, tsuuntakulma in zip(self.tukivoimat, self.tukivoimaKulmat):
            tuki.asetaSuuntakulma(tsuuntakulma+self.suuntakulma)
        self.nivel.ristikko.muuttui()
            
    def luoTukivoimat(self):
        """Luo tukivoimaKulmat listasta tukivoimat listan. Tätä ei yleensä
        ole tarvetta kutsua luokan ulkopuolelta."""
        for tKulmat in self.tukivoimaKulmat:
            self.tukivoimat.append(Tukivoima(self.nivel,
                                         tKulmat + self.suuntakulma))
        self.nivel.lisaaTuki(self)

    def poista(self):
        """Poistaa tuen."""
        self.nivel.poistaTuki(self)

    def annaResultantti(self):
        """Palauttaa tuen tukivoimien muodostaman resultantin. Jos ristikkoa ei
        ole ratkaistu palauttaa C{(0.0,0.0)}
        @returns: tukivoimien resultantti.
        @rtype: C{tuple} of C{float}"""
        x = 0.0
        y = 0.0
        if not self.nivel.ristikko.ratkaistu:
            return (x, y)
        for tukivoima in self.tukivoimat:
            x += cos(tukivoima.suuntakulma*180/pi)*tukivoima.suuruus
            y += sin(tukivoima.suuntakulma*180/pi)*tukivoima.suuruus
        return (x, y)

    def asetaSuuruus(self, suuruus, yksikko):
        """Asettaa tuen tukivoimille suuruudet.
        @param suuruus: tukivoiman resultantin suuruus
        @type suuruus: C{float}
        @param yksikko: tukivoiman yksikko
        @type yksikko: C{string}"""
        pass

    def asetaNimi(self, nimi):
        """Asettaa tuelle nimen.
        @type nimi: Tuen nimi
        @param nimi: C{string}"""
        self.nimi = nimi
        self.nivel.ristikko.muuttui()
