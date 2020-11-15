# Johdatus WHILE-ohjelmointiin

Harjoitustyön aiheena on tehdä web-sovellus, jonka avulla opetellaan tekemään yksinkertaisia WHILE-ohjelmia. Sivustolla kerrotaan WHILE-ohjelmointikielestä ja sen syntaksista, ja perusasiat opeteltuaan käyttäjä voi luoda käyttäjätilin ja ratkaista yksinkertaisia ohjelmointitehtäviä WHILE-kielellä. Käyttäjän lähetettyä ratkaisunsa tehtävään sovellus kertoo, oliko käyttäjän antama ratkaisu oikein ja tarkistaa, että annettu ohjelma todella on WHILE-ohjelma. Käyttäjä pystyy tilinsä avulla seuraamaan etenemistään ja katselemaan tilastoja ratkaisemistaan tehtävistä. Sovelluksessa on hakutoiminto, jonka avulla toisia käyttäjiä voi hakea ja lisätä omalle kaverilistalle ja kaverit pystyvät seuraamaan toistensa etenemistä. Sivustolla on tavallisten käyttäjien lisäksi ylläpitäjä, joka pystyy muokkaamaan ja lisäämään tehtäviä. Jonkinlainen keskustelumahdollisuus voisi myös olla hauska lisätä, vaikka jokaisen tehtävän omalle sivulle tai keskitetysti yhteen paikkaan.

Wikipedia artikkeli, joka kertoo WHILE-ohjelmointikielestä: [WHILE-Programm](https://de.wikipedia.org/wiki/WHILE-Programm) (valitettavasti artikkeli on saksankielinen)  
PDF, jossa kerrotaan WHILE-kielestä: [Theory of Computer Science - LOOP- and WHILE-Computability](https://ai.dmi.unibas.ch/_files/teaching/fs16/theo/slides/theory-d02.pdf)

Linkki sovellukseen [Johdatus WHILE-ohjelmointiin](https://whileohjelmointi.herokuapp.com).

Projektin nimi tulee mahdollisesti muuttumaan vielä harjoitustyön edetessä.
Web-sovellus on harjoitustyö Helsingin yliopiston kurssille Tietokantasovellus.

## Tilannekatsaus: välipalautus 2
Sovelluksella pitäisi olla nyt toimiva sivupohja oleellisten toimintojen osalta. Kaikki tällä hetkellä olemassa olevat sivut ja linkit pitäisi toimia myös Herokussa, mutta jos siellä tulee ongelmia, niin korjaan ne pikimmiten! Sivut ovat vielä todella sekaisin ja asettelut eivät ole kohdallaan ja kaikki tekstit ovat toistaiseksi placeholdereita,että sain suunniteltua sivupohjan. Erityisesti WHILE-ohjelmoinnista kertova sivu on vielä monimutkainen ja huono. Viilailen ulkoasua sitten hieman myöhemmin!

Tällä hetkellä työstän sitä, että tehtävien tarkistaminen (onko WHILE-ohjelma) ja simuloiminen saadaan toimimaan alusta loppuun. Parserin pitäisi toimia, mutta sitä ei ole vielä kovin paljon testattu. Seuraavaksi toteutan simuloinnin ja teen muutaman tehtävän valmiiksi, niin että niille voi tehdä testit ja pääsen kunnolla kokeilemaan, eihän parseriin ja simulaattoriin ole jäänyt bugeja. Kun tehtävien käsittely ja simulointi onnistuu oikein, kirjoitan sivustolle paremmat tekstit ja ohjeet siihen, miten tehtäviä lähetetään. Tämän jälkeen alan tekemään varmaan profiili-sivuja ja piilotan tehtävien lähettämisen muilta kuin kirjautuneilta käyttäjiltä.

### Update:
Ehdin tässä vielä illalla tehdä simuloinnista luonnosversion valmiiksi. Vein muutokset myös Herokuun ja kokeilin, miten ohjelma siellä toimii. Tällä hetkellä, jos ensimmäiseen tehtävään lähettää jotain pitäisi voida saada seuraavat vastaukset:
* Jos sovelluksen ensimmäinen rivi ei ole   input: x1, x2;   tulee Internal Server Error.
* Ohjelma odottaa, että se saa kaksi input-muuttujaa, ja niiden arvoiksi asetetaan 8 ja 13. Jos ohjelman syntaksi on oikea, sovellus kertoo mitä ohjelman suorituksen loputtua ans-nimisessä muuttujassa on arvona.
Syntaksia ei kerrota vielä missään, mutta se seuraa läheisesti Javan-syntaksia. Tässä nopea esimerkki:  
input: x1, x2;  
a = x1 + 0;  
while (a != 0) {  
    x2 = x2 + 1;  
    a = a - 1;  
}  
ans = x2 + 0;  
* Jos syntaksi ei ole oikein, sovelluksen pitäisi kertoa tämä. Poikkeuksena tosiaan ensimmäinen input-rivi.
Luonnoksessa on vielä paljon tekemättömiä asioita, joten se toimii vielä hyvin epävakaasti. Halusin kuitenkin kokeilla hieman, että ensimmäinen versio toimii!

Sovelluksen linkki on tuossa yläpuolella ja siellä pitäisi olla mahdollista luoda käyttäjätunnus, sekä kirjautua sisään. Tällä hetkellä tehtävien lähettäminen on mahdollista kenelle vain, joten käyttäjätunnuksesta ei vielä ole mitään iloa. Jos sovellus antaa jossain kohtaa virheviestin, niin minulle voi ilmoittaa!
