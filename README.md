# Johdatus WHILE-ohjelmointiin

Harjoitustyön aiheena on tehdä web-sovellus, jonka avulla opetellaan tekemään yksinkertaisia WHILE-ohjelmia. Sivustolla kerrotaan WHILE-ohjelmointikielestä ja sen syntaksista, ja perusasiat opeteltuaan käyttäjä voi luoda käyttäjätilin ja ratkaista yksinkertaisia ohjelmointitehtäviä WHILE-kielellä. Käyttäjän lähetettyä ratkaisunsa tehtävään sovellus kertoo, oliko käyttäjän antama ratkaisu oikein ja tarkistaa, että annettu ohjelma todella on WHILE-ohjelma. Käyttäjä pystyy tilinsä avulla seuraamaan etenemistään ja katselemaan tilastoja ratkaisemistaan tehtävistä. Sovelluksessa on hakutoiminto, jonka avulla toisia käyttäjiä voi hakea ja lisätä omalle kaverilistalle ja kaverit pystyvät seuraamaan toistensa etenemistä. Sivustolla on tavallisten käyttäjien lisäksi ylläpitäjä, joka pystyy muokkaamaan ja lisäämään tehtäviä. Jonkinlainen keskustelumahdollisuus voisi myös olla hauska lisätä, vaikka jokaisen tehtävän omalle sivulle tai keskitetysti yhteen paikkaan.

Wikipedia artikkeli, joka kertoo WHILE-ohjelmointikielestä: [WHILE-Programm](https://de.wikipedia.org/wiki/WHILE-Programm) (valitettavasti artikkeli on saksankielinen)  
PDF, jossa kerrotaan WHILE-kielestä: [Theory of Computer Science - LOOP- and WHILE-Computability](https://ai.dmi.unibas.ch/_files/teaching/fs16/theo/slides/theory-d02.pdf)

Linkki sovellukseen [Johdatus WHILE-ohjelmointiin](https://whileohjelmointi.herokuapp.com).

Projektin nimi tulee mahdollisesti muuttumaan vielä harjoitustyön edetessä.
Web-sovellus on harjoitustyö Helsingin yliopiston kurssille Tietokantasovellus.

!! Ratkaisua ei voi vielä lähettää tiedostona !!

## Tilannekatsaus: välipalautus 3
Iso osa oleellisista toiminnallisuuksista pitäisi olla nyt käytettävissä ja toimia Herokussa. Repon documentation-kansiossa on TODO-lista, johon olen kirjoittanut tällä hetkellä tiedossa olevia virheitä ja puutteita, sekä mitä ainakin on vielä suunnitteilla tehdä. Lyhyesti, käyttäjätunnuksen tekemisen ja sisään kirjautumisen pitäisi toimia, tehtävään pitäisi voida lähettää vastaus ja sivuilla pitäisi olla ohjeet siihen, miten ratkaisu lähetetään johonkin tehtävään. Etusivu, perusteet- ja ohjeet sivut ovat ainoat, jotka on siistitty ja muissa on vielä tekemistä. Sovelluksen pitäisi antaa käyttäjälle palautetta, jos ratkaisu ei toimi ja kertoa jotain siitä, miksi ratkaisu on väärin. Kun tehtävän saa onnistuneesti tehtyä, pääsee kommentti-sivulle, jossa näkee tehtävän ratkaisseiden käyttäjien määrän sekä voi lähettää kommenttia tehtävään. Sivuilla on myös leaderboard-sivu, joka on tarkoitus piilottaa kirjautumattomilta, mutta on nyt toistaiseksi vielä koko maailman katseltavana.

Sovelluksessa ei ole vielä erikseen admin-käyttäjää, mutta sivuilla on "piilotettuna" ylläpitäjälle tarkoitettuja sivuja, joissa voi muokata tehtävää, tehdä uuden tehtävän ja lisätä, muokata ja poistaa tehtävän testejä. Nämä on tarkoitus suojata ennen loppupalautusta, kunhan olen saanut tehtyä käyttäjille roolit. Koodista näkee mitkä sivujen osoitteet ovat. Kaikkien näiden toiminnallisuuksien pitäisi olla kunnossa ja toimia odotetulla tavalla. Tehtävien tekemiseen ja suunnitteluun meni sen verran aikaa, että olisi mukavaa, jos niitä tai testejä ei muokata tai lisätä. Pliiss!

4 ensimmäistä tehtävää on testattu OK, mutta uudemmissa tehtävissä on vielä epävarmuutta testien sopivuudesta, joten jos näissä on jotain virhettä, niin niitä tullaan korjaamaan ja viilaamaan tässä piakkoin.

Seuraavaksi sovellukseen on tarkoitus toteuttaa lisää tehtäviä, TODO-listassa mainitut virheet pitää korjata, ulkoasu pitää siistiä ja tämän jälkeen toteutan eri käyttäjäroolit ja alan tekemään profiilisivua ja käyttäjien hakutoiminnallisuutta.

Jos sovelluksessa tulee vastaan virheitä, joita ei ole mainittu TODO-listassa, niin ilmoittakaa ihmeessä minulle! Automaattisia testejä ei ole, joten aina välillä jotain saattaa hajota huomaamatta.
