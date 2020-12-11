# Sovellukseen jääneet ongelmat
* Kun käyttäjä palauttaa ohjelman, jonka syntaksissa on virhe, virheviesti ei anna alkuperäistä riviä, vaan vastaavan rivin ilman välilyöntejä. Tämän voisi korjata, niin viesti olisi siistempi ja ehkä myös käyttäjäystävällisempi.
Päivitetään lisää, kun sovellus valmistuu.
* Moduuleja on paljon ja ne kannattaisi jakaa paketteihin, niin repositorio olisi siistimpi ja eri moduulien välillä navigointi olisi helpompaa.
* En saanut monesta yrityksestä huolimatta Bootstrapin css-ylikirjoituksia toimimaan oikein. HTML-templatet ovat nyt täynnä inline style- elementtiä, mikä tekee HTML-koodista sotkuisen näköistä. Kunhan osaisin tehdä ylikirjoitukset oikein, siirtäisin style-elementit yhteen static-kansion .css tiedostoon.
* Sovelluksen logiikan voisi suunnitella niin, että tietokantahakujen määrä minimoidaan ja haut ovat tehokkaita. Tällä hetkellä hauissa ei ole olennaisesti keskitytty tehokkuuteen ja turhaa työtä tehdään jonkin verran.
* Halusin tehdä oman sivun, missä ylläpitäjä voi järjestää tehtävät drag-and-drop -tyylisessä listassa, mutta kun aikaa oli enää vähän, en jaksanut alkaa opettelemaan JavaScriptiä, kun en ole sitä paljon aikaisemmin käyttänyt. Tämän hetken logiikka olettaa, että uusia tehtäviä lisättäessä järjestys on mietitty etukäteen ja mitään kovin isoja muutoksia ei tarvitse tehdä. Tehtäviä on kuitenkin onneksi melko pieni määrä yhdessä aihealueessa. Tämä hienoinen epämukavuus ei onneksi kuitenkaan näy käyttäjälle mitenkään.
* Automaattiset testit helpottaisivat koodin refaktorointia huomattavasti. Kurssin loppuakohden kului melko paljon muutosten jälkeen käsin tarkistaessa, että mitään odottamattonta ei ollut mennyt rikki, eikä ikinä saanut luottoa siihen, että kaikki varmasti toimii. En kuitenkaan alkanut tämän kurssin aikana nyt opettelemaan, miten tehdä pythonilla testejä web-sovellukselle.
* Tällä hetkellä käyttäjän ratkaisua testataan vähän ja käytössä on vain rajattu määrä käsin tehtyjä testejä. En keskittynyt tähän kovin paljon tällä kurssilla, mutta jos sovellusta haluaisi jatkokehittää, olisi hyvä tehdä ratkaisuille myös kattavat koneelliset testit käsin tehtyjen testien lisäksi.