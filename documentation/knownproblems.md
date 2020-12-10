# Sovellukseen jääneet ongelmat
* Kun käyttäjä palauttaa ohjelman, jonka syntaksissa on virhe, virheviesti ei anna alkuperäistä riviä, vaan vastaavan rivin ilman välilyöntejä. Tämän voisi korjata, niin viesti olisi siistempi ja ehkä myös käyttäjäystävällisempi.
Päivitetään lisää, kun sovellus valmistuu.
* Moduuleja on paljon ja ne kannattaisi jakaa paketteihin, niin repositorio olisi siistimpi ja eri moduulien välillä navigointi olisi helpompaa.
* En saanut monesta yrityksestä huolimatta Bootstrapin css-ylikirjoituksia toimimaan oikein. HTML-templatet ovat nyt täynnä inline style- elementtiä, mikä tekee HTML-koodista sotkuisen näköistä. Kunhan osaisin tehdä ylikirjoitukset oikein, siirtäisin style-elementit yhteen static-kansion .css tiedostoon.
* Sovelluksen logiikan voisi suunnitella niin, että tietokantahakujen määrä minimoidaan ja haut ovat tehokkaita. Tällä hetkellä hauissa ei ole olennaisesti keskitytty tehokkuuteen ja turhaa työtä tehdään jonkin verran.

