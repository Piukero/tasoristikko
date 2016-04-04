# Nimeäminen #

Muuttujien ja funktioiden nimeämiseen käytetään nk. [CamelCase](http://fi.wikipedia.org/wiki/CamelCase) tyyliä, jossa useista sanoista koostuvat muuttujat kirjoitetaan yhteen isoin alkukirjaimin.
Luokat, modulien funktiot ja modulien muuttujat aloitetaan aina isolla alkukirjaimella, jos ne ovat julkisia. Sen sijaan luokkien sisäiset muuttujat ja funktiot aloitetaan aina pienellä alkukirjaimella. Luokat jotka perivät jonkun Qt:n luokan nimetään niin, että
niiden ensimmäinen kirjain on Q ja toinen kijain on iso. Esimerkiksi:
```
class QNivel(QtGui.QGraphicsItem):
    ...
```

Graafisessa käyttöliittymässä muuttujan nimen eteen aina lisätään muuttujan tyyppi. Esimerkiksi QLabel nimetään seuraavasti:
```
self.labelEsim = QtGui.QLabel('Esim')
```
Jos muuttujan tyyppi on pitkä ja koostuu useasta sanasta, voidaan se lyhentää:
```
self.gwEsim = QtGui.QGraphicsView()
```

Paketit nimetään myös [CamelCase](http://fi.wikipedia.org/wiki/CamelCase) tyylillä, tosin niissä voidaan käyttää tarpeen mukaan isoja tai pieniä alkukirjaimia. Modulit sen sijaan nimetään aina käyttäen pieniä kirjaimia. Myös silloin, kun nimi koostuu useasta kirjaimesta. Qt:n .ui-tiedostoista luodut Python modulit nimetään käyttäen 'ui_' etuliitettä._

# Luokkien muuttujat #

Luokkien muuttujat jätetään yleisesti Python-ohjelmoinnissa käytetyn tavan mukaisesti julkisiksi. Muuttujia ei kuitenkaan ole tarkoitus muuttaa suoraan, vaan sitä varten on luotava luokkaan oma funktio. Pelkää lukemista varten niitä voi sen sijaan käyttää.

# Kommentointi ja dokumentointi #

Koodissa ei tule käyttää turhaa kommentointia. Se, mitä on tehty, tulee usein selville helmpommin vain lukemalla koodia. Jos kuitenkin kokee kommentoinnin tarpeelliseksi voi sitä lisätä koodiin.

Jokaisesta paketista, modulista ja funktiosta tulee olla dokumentti jossain. Myös muuttujat on hyvä dokumentoida selkeyden vuoksi, mutta se ei ole tarpeellista. Perittyjen luokkien osalta ei funktioiden dokumentointi ole tarpeen, jos kyseisen funktion dokumentointi löytyy jo jostain.

Dokumentointiin käytetään [Epydoc](http://epydoc.sourceforge.net)-ohjelmaa. Ohjelman syntaksi mahdollistaa funktioissa tyyppimäärittelyjen esittämisen ja sitä onkin hyvä käyttää selkeyttämään parametrien ja palautettavien arvojen tyyppejä, jotka eivät oletuksena ole Pythonissa niin selkeitä.

## Sisennys ##

Sisennykseen käytetään Pythonissa suositun tavan mukaan välilyöntejä eikä tabeja. Tämä helpottaa tiedostojen käsittelyä eri koodausympäristöissä. Yksi sisennys on neljä välilyöntiä. Esimerkiksi vim:ssä tämän saa automaattiseksi asettamalla:
```
set expandtab
set shitfwidth=4
```