# Yleistä #

Tiedosto on sqlite3:lla muodostettu tietokanta. Tiedostossa voi ristikon lisäksi olla kuvattuna joitain graafisen käyttöliittymän ominausuuksia, kuten näkymään zoomaus ja paikka.
Näitä asetuksia ei ole vielä tarkemmin määritelty, eikä niille ole taulua.

# Ristikon taulut #

Ohessa on kuvattuna ristikon taulut.

## Nivel ##

| _Kentta_ | _Tyyppi_ | _Selite_ |
|:---------|:---------|:---------|
| NivelNro | INTEGER PRIMARY KEY | Nivelen numero. Käytetään muissa tauluissa viittauksena.|
| Nimi     | TEXT     | Nivelen mahdollinen nimi |
| x        | REAL     | Nivelen x-koordinaatti |
| y        | REAL     | Nivelen y-koordinaatti |

## Sauva ##

Sauvan taulu ei ole vielä lopullinen. Vielä täytyy miettiä, tarvitaanko pinta-alalle ja kimmokertoimelle yksiköt.

| _Kentta_ | _Tyyppi_ | _Selite_ |
|:---------|:---------|:---------|
| SauvaNro | INTEGER PRIMARY KEY | Sauvan numero |
| Nimi     | TEXT     | Sauvan nimi |
| PintaAla | REAL     | Sauvan pinta-ala (ei vielä käytössä) |
| Kimmokerroin | REAL     | Sauvan kimmokerroin (ei vielä käytössä) |
| Suuruus  | REAL     | Sauvavoiman suuruus |
| Yksikko  | TEXT     | Sauvavoiman yksikko |
| Nivel1   | INTEGER  | Sauvan pään _1_ nivel |
| Nivel2   | INTEGER  | Sauvan pään _2_ nivel |

## Tuki ##

Tallennettavassa tiedostossa ei ole Tukivoima-taulua vaan tukivoimat luodaan tämän taulun tiedoista.

| _Kentta_ | _Tyyppi_ | _Selite_ |
|:---------|:---------|:---------|
| TukiNro  | INTEGER PRIMARY KEY | Tuen numero |
| Tyyppi   | INTEGER  | Tuen tyyppi (0 = niveltuki, 1 = rullatuki) |
| Suuntakulma | REAL     | Tuen suuntakulma aseteissa |
| SuuruusX | REAL     | Tukivoimien resultanttien x-akselin suuntainen komponentti. |
| SuuruusY | REAL     | Tukivoimien resultanttien y-akselin suuntainen komponentti. |
| Yksikko  | TEXT     | Tukivoimien yksikkö |
| Nivel    | INTEGER  | Nivel, johon tukivoimat liittyvät |
| Nimi     | TEXT     | Tuen nimi |

## Pistekuorma ##

| _Kentta_ | _Tyyppi_ | _Selite_ |
|:---------|:---------|:---------|
| PistekuormaNro |  INTEGER PRIMARY KEY | Pistekuorman numero |
| XKomp    | REAL     | Pistekuorman x-akselin suuntainen komponentti |
| YKomp    | REAL     | Pistekuorman y-akselin suuntainen komponentti |
| Yksikko  | TEXT     | Pistekuorman yksikko |
| Nivel    | INTEGER  | Nivel, johon pistekuorma liittyy |