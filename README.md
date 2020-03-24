# WirVsVirus Challenge

## Inspiration
Imagine you are a 
...mayor
...news agency
...researcher
...analyst
...anyone making decisions based on the data around Covid-19

and you need & want REALTIME access to all Covid-19 related facts <i>and<i> news for your area, focus group, age group.
But it is spread around, locked-up in dashboards, tables, charts or images.

## What it does
Built on the data from RKI Germany we provide an API that can be tailored to your needs. 
Built your query once - receive the latest data everyday.

##Try it out
A few examples:

* https://covid19-germany-api.eu-de.mybluemix.net/get_data?state=Bayern
* https://covid19-germany-api.eu-de.mybluemix.net/get_totals?state=Bayern&date_range=2020-03-12 2020-03-21
* https://covid19-germany-api.eu-de.mybluemix.net/get_totals?state=Bayern&date_range=2020-03-12 2020-03-21&province=SK München
* https://covid19-germany-api.eu-de.mybluemix.net/get_events?location=Thüringen

Folgende weitere Parameter für /get_data & /get_totals sind verfügbar:

* Bundesland(state), Landkreis(province mit SK oder LK vorne), Geschlecht(sex), Alter von(age_group_start), Alter bis(age_group_end), Abrufdatum(extraction_date YYYY-MM-DD), Datumsbereich (date_range YYYY-MM-DD YYYY-MM-DD) 

Folgende weitere Parameter für /get_events sind verfügbar:
* Ort (location), Bezugsdaten (publish_date), Abrufdaten (extraction_date)

## How I built it
Postgresql, Python Flask, Cloud Functions, Watson NLU, BeautifulSoup
![Basic Architecture]("/public/LEIMDENCAPI.png")


## Challenges I ran into
Data, Data, Data ... the data is so hard to gather in a good quality.

## Accomplishments that I'm proud of
We think that maaaany digital applications (whether its a news agency providing you daily charts or a political staff member providing the daily executive report for its official) can benefit from this. And while our solution can underpin many of those, we are proud that it is not only pure numbers we are providing but we also try to correlate this with events around the crisis on a local level.

## What I learned
My Hypothesis was: there is no easy access to large scale Covid-19 data
...turned out its true.
And some fun new technology and how to built an API and dynamic SQL :)

## Steps to deploy yourself

You can [deploy this application to IBM Cloud](https://cloud.ibm.com/developer/appservice/) or [build it locally](#building-locally) by cloning this repo first. Once the app is live, you can access the `/health` endpoint to check if its up. You'll have to bring your own DB and deploy the filldbscripts in the scripts folder to a functions / serverless.

## What's next for CoVid-19-API
In the future we want to be able to aggregate news information on the COVID-19 virus from reliable sources while avoiding duplicates. Furthermore, we ourselves want to be able to publish some metrics/correlations from the data we gathered. At a later time, if the API is a success, we plan to have it reside inside a kubernetes cluster to ensure availability and scalability.

**Forks and merge requests are highly welcome!**

**Challenge ID** 0193	

**Schlüssel** 0038

Verfügbare Landkreise:
* 'SK Flensburg', 'SK Kiel', 'SK Lübeck', 'SK Neumünster',
       'LK Dithmarschen', 'LK Herzogtum Lauenburg', 'LK Nordfriesland',
       'LK Ostholstein', 'LK Pinneberg', 'LK Plön',
       'LK Rendsburg-Eckernförde', 'LK Schleswig-Flensburg',
       'LK Segeberg', 'LK Steinburg', 'LK Stormarn', 'SK Hamburg',
       'SK Braunschweig', 'SK Salzgitter', 'SK Wolfsburg', 'LK Gifhorn',
       'LK Goslar', 'LK Helmstedt', 'LK Northeim', 'LK Peine',
       'LK Wolfenbüttel', 'LK Göttingen', 'Region Hannover',
       'LK Diepholz', 'LK Hameln-Pyrmont', 'LK Hildesheim',
       'LK Holzminden', 'LK Nienburg (Weser)', 'LK Schaumburg',
       'LK Celle', 'LK Cuxhaven', 'LK Harburg', 'LK Lüchow-Dannenberg',
       'LK Lüneburg', 'LK Osterholz', 'LK Rotenburg (Wümme)',
       'LK Heidekreis', 'LK Stade', 'LK Uelzen', 'LK Verden',
       'SK Delmenhorst', 'SK Emden', 'SK Oldenburg', 'SK Osnabrück',
       'SK Wilhelmshaven', 'LK Ammerland', 'LK Aurich', 'LK Cloppenburg',
       'LK Emsland', 'LK Friesland', 'LK Grafschaft Bentheim', 'LK Leer',
       'LK Oldenburg', 'LK Osnabrück', 'LK Vechta', 'LK Wesermarsch',
       'LK Wittmund', 'SK Bremen', 'SK Bremerhaven', 'SK Düsseldorf',
       'SK Duisburg', 'SK Essen', 'SK Krefeld', 'SK Mönchengladbach',
       'SK Mülheim a.d.Ruhr', 'SK Oberhausen', 'SK Remscheid',
       'SK Solingen', 'SK Wuppertal', 'LK Kleve', 'LK Mettmann',
       'LK Rhein-Kreis Neuss', 'LK Viersen', 'LK Wesel', 'SK Bonn',
       'SK Köln', 'SK Leverkusen', 'StadtRegion Aachen', 'LK Düren',
       'LK Rhein-Erft-Kreis', 'LK Euskirchen', 'LK Heinsberg',
       'LK Oberbergischer Kreis', 'LK Rheinisch-Bergischer Kreis',
       'LK Rhein-Sieg-Kreis', 'SK Bottrop', 'SK Gelsenkirchen',
       'SK Münster', 'LK Borken', 'LK Coesfeld', 'LK Recklinghausen',
       'LK Steinfurt', 'LK Warendorf', 'SK Bielefeld', 'LK Gütersloh',
       'LK Herford', 'LK Höxter', 'LK Lippe', 'LK Minden-Lübbecke',
       'LK Paderborn', 'SK Bochum', 'SK Dortmund', 'SK Hagen', 'SK Hamm',
       'SK Herne', 'LK Ennepe-Ruhr-Kreis', 'LK Hochsauerlandkreis',
       'LK Märkischer Kreis', 'LK Olpe', 'LK Siegen-Wittgenstein',
       'LK Soest', 'LK Unna', 'SK Darmstadt', 'SK Frankfurt am Main',
       'SK Offenbach', 'SK Wiesbaden', 'LK Bergstraße',
       'LK Darmstadt-Dieburg', 'LK Groß-Gerau', 'LK Hochtaunuskreis',
       'LK Main-Kinzig-Kreis', 'LK Main-Taunus-Kreis', 'LK Odenwaldkreis',
       'LK Offenbach', 'LK Rheingau-Taunus-Kreis', 'LK Wetteraukreis',
       'LK Gießen', 'LK Lahn-Dill-Kreis', 'LK Limburg-Weilburg',
       'LK Marburg-Biedenkopf', 'LK Vogelsbergkreis', 'SK Kassel',
       'LK Fulda', 'LK Hersfeld-Rotenburg', 'LK Kassel',
       'LK Schwalm-Eder-Kreis', 'LK Waldeck-Frankenberg',
       'LK Werra-Meißner-Kreis', 'SK Koblenz', 'LK Ahrweiler',
       'LK Altenkirchen', 'LK Bad Kreuznach', 'LK Birkenfeld',
       'LK Cochem-Zell', 'LK Mayen-Koblenz', 'LK Neuwied',
       'LK Rhein-Hunsrück-Kreis', 'LK Rhein-Lahn-Kreis',
       'LK Westerwaldkreis', 'SK Trier', 'LK Bernkastel-Wittlich',
       'LK Bitburg-Prüm', 'LK Vulkaneifel', 'LK Trier-Saarburg',
       'SK Frankenthal', 'SK Kaiserslautern', 'SK Landau i.d.Pfalz',
       'SK Ludwigshafen', 'SK Mainz', 'SK Neustadt a.d.Weinstraße',
       'SK Pirmasens', 'SK Speyer', 'SK Worms', 'SK Zweibrücken',
       'LK Alzey-Worms', 'LK Bad Dürkheim', 'LK Donnersbergkreis',
       'LK Germersheim', 'LK Kaiserslautern', 'LK Kusel',
       'LK Südliche Weinstraße', 'LK Rhein-Pfalz-Kreis',
       'LK Mainz-Bingen', 'LK Südwestpfalz', 'SK Stuttgart',
       'LK Böblingen', 'LK Esslingen', 'LK Göppingen', 'LK Ludwigsburg',
       'LK Rems-Murr-Kreis', 'SK Heilbronn', 'LK Heilbronn',
       'LK Hohenlohekreis', 'LK Schwäbisch Hall', 'LK Main-Tauber-Kreis',
       'LK Heidenheim', 'LK Ostalbkreis', 'SK Baden-Baden',
       'SK Karlsruhe', 'LK Karlsruhe', 'LK Rastatt', 'SK Heidelberg',
       'SK Mannheim', 'LK Neckar-Odenwald-Kreis', 'LK Rhein-Neckar-Kreis',
       'SK Pforzheim', 'LK Calw', 'LK Enzkreis', 'LK Freudenstadt',
       'SK Freiburg i.Breisgau', 'LK Breisgau-Hochschwarzwald',
       'LK Emmendingen', 'LK Ortenaukreis', 'LK Rottweil',
       'LK Schwarzwald-Baar-Kreis', 'LK Tuttlingen', 'LK Konstanz',
       'LK Lörrach', 'LK Waldshut', 'LK Reutlingen', 'LK Tübingen',
       'LK Zollernalbkreis', 'SK Ulm', 'LK Alb-Donau-Kreis',
       'LK Biberach', 'LK Bodenseekreis', 'LK Ravensburg',
       'LK Sigmaringen', 'SK Ingolstadt', 'SK München', 'SK Rosenheim',
       'LK Altötting', 'LK Berchtesgadener Land',
       'LK Bad Tölz-Wolfratshausen', 'LK Dachau', 'LK Ebersberg',
       'LK Eichstätt', 'LK Erding', 'LK Freising', 'LK Fürstenfeldbruck',
       'LK Garmisch-Partenkirchen', 'LK Landsberg a.Lech', 'LK Miesbach',
       'LK Mühldorf a.Inn', 'LK München', 'LK Neuburg-Schrobenhausen',
       'LK Pfaffenhofen a.d.Ilm', 'LK Rosenheim', 'LK Starnberg',
       'LK Traunstein', 'LK Weilheim-Schongau', 'SK Landshut',
       'SK Passau', 'SK Straubing', 'LK Deggendorf',
       'LK Freyung-Grafenau', 'LK Kelheim', 'LK Landshut', 'LK Passau',
       'LK Regen', 'LK Rottal-Inn', 'LK Straubing-Bogen',
       'LK Dingolfing-Landau', 'SK Amberg', 'SK Regensburg',
       'SK Weiden i.d.OPf.', 'LK Amberg-Sulzbach', 'LK Cham',
       'LK Neumarkt i.d.OPf.', 'LK Neustadt a.d.Waldnaab',
       'LK Regensburg', 'LK Tirschenreuth', 'SK Bamberg', 'SK Bayreuth',
       'SK Hof', 'LK Bamberg', 'LK Bayreuth', 'LK Coburg', 'LK Forchheim',
       'LK Hof', 'LK Kronach', 'LK Kulmbach', 'LK Lichtenfels',
       'LK Wunsiedel i.Fichtelgebirge', 'SK Ansbach', 'SK Erlangen',
       'SK Fürth', 'SK Nürnberg', 'SK Schwabach', 'LK Ansbach',
       'LK Erlangen-Höchstadt', 'LK Fürth', 'LK Nürnberger Land',
       'LK Neustadt a.d.Aisch-Bad Windsheim', 'LK Roth',
       'LK Weißenburg-Gunzenhausen', 'SK Aschaffenburg', 'SK Schweinfurt',
       'SK Würzburg', 'LK Aschaffenburg', 'LK Bad Kissingen',
       'LK Rhön-Grabfeld', 'LK Haßberge', 'LK Kitzingen', 'LK Miltenberg',
       'LK Main-Spessart', 'LK Schweinfurt', 'LK Würzburg', 'SK Augsburg',
       'SK Memmingen', 'LK Aichach-Friedberg', 'LK Augsburg',
       'LK Dillingen a.d.Donau', 'LK Günzburg', 'LK Neu-Ulm', 'LK Lindau',
       'LK Ostallgäu', 'LK Unterallgäu', 'LK Donau-Ries', 'LK Oberallgäu',
       'LK Stadtverband Saarbrücken', 'LK Merzig-Wadern',
       'LK Neunkirchen', 'LK Saarlouis', 'LK Saar-Pfalz-Kreis',
       'LK Sankt Wendel', 'SK Berlin Mitte',
       'SK Berlin Friedrichshain-Kreuzberg', 'SK Berlin Pankow',
       'SK Berlin Charlottenburg-Wilmersdorf', 'SK Berlin Spandau',
       'SK Berlin Steglitz-Zehlendorf', 'SK Berlin Tempelhof-Schöneberg',
       'SK Berlin Neukölln', 'SK Berlin Treptow-Köpenick',
       'SK Berlin Marzahn-Hellersdorf', 'SK Berlin Lichtenberg',
       'SK Berlin Reinickendorf', 'SK Brandenburg a.d.Havel',
       'SK Cottbus', 'SK Frankfurt (Oder)', 'SK Potsdam', 'LK Barnim',
       'LK Dahme-Spreewald', 'LK Elbe-Elster', 'LK Havelland',
       'LK Märkisch-Oderland', 'LK Oberhavel', 'LK Oberspreewald-Lausitz',
       'LK Oder-Spree', 'LK Ostprignitz-Ruppin', 'LK Potsdam-Mittelmark',
       'LK Spree-Neiße', 'LK Teltow-Fläming', 'LK Uckermark',
       'SK Rostock', 'SK Schwerin', 'LK Mecklenburgische Seenplatte',
       'LK Rostock', 'LK Vorpommern-Rügen', 'LK Nordwestmecklenburg',
       'LK Vorpommern-Greifswald', 'LK Ludwigslust-Parchim',
       'SK Chemnitz', 'LK Erzgebirgskreis', 'LK Mittelsachsen',
       'LK Vogtlandkreis', 'LK Zwickau', 'SK Dresden', 'LK Bautzen',
       'LK Görlitz', 'LK Meißen', 'LK Sächsische Schweiz-Osterzgebirge',
       'SK Leipzig', 'LK Leipzig', 'LK Nordsachsen', 'SK Dessau-Roßlau',
       'SK Halle', 'SK Magdeburg', 'LK Altmarkkreis Salzwedel',
       'LK Anhalt-Bitterfeld', 'LK Börde', 'LK Burgenlandkreis',
       'LK Harz', 'LK Jerichower Land', 'LK Mansfeld-Südharz',
       'LK Saalekreis', 'LK Salzlandkreis', 'LK Stendal', 'LK Wittenberg',
       'SK Erfurt', 'SK Gera', 'SK Jena', 'SK Suhl', 'SK Weimar',
       'SK Eisenach', 'LK Eichsfeld', 'LK Nordhausen', 'LK Wartburgkreis',
       'LK Unstrut-Hainich-Kreis', 'LK Kyffhäuserkreis',
       'LK Schmalkalden-Meiningen', 'LK Gotha', 'LK Sömmerda',
       'LK Hildburghausen', 'LK Ilm-Kreis', 'LK Weimarer Land',
       'LK Sonneberg', 'LK Saalfeld-Rudolstadt',
       'LK Saale-Holzland-Kreis', 'LK Saale-Orla-Kreis', 'LK Greiz',
       'LK Altenburger Land'
       
## License

This application is licensed under the Apache License, Version 2. Separate third-party code objects invoked within this code pattern are licensed by their respective providers pursuant to their own separate licenses. Contributions are subject to the [Developer Certificate of Origin, Version 1.1](https://developercertificate.org/) and the [Apache License, Version 2](https://www.apache.org/licenses/LICENSE-2.0.txt).

[Apache License FAQ](https://www.apache.org/foundation/license-faq.html#WhatDoesItMEAN)

