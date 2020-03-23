# WirVsVirus Challenge

Eine globale und zentrale Datenbank/Datalake mit Schnittstellen APIs

## Das Problem
Wenn Applikationen entwickelt werden um das Virus zu bekämpfen / Informationen zu sammeln, müssen diese Daten der
Allgemeinheit und weiteren Applikationen zur Verfügung gestellt werden. Wie gelange ich als Entwickler, z.B. einer App.
zur Prädikation zur Virusausbreitung, an Daten für die Applikation? Wo kann ich die Daten die meine App. sammelt
hochladen und anderen Entwicklern oder Statistikern zur Verfügung stellen?	

## Der Lösungsansatz
Ein zentraler Datalake / eine zentrale Datenbank auf den/die Informationen oder Daten des Virus von Applikationen
geladen werden. Dieser Datalake hat wiederum Application Programm Interfaces (APIs) um die Daten an weitere
Applikationen zu verteilen.

**Probier es aus**
Ein paar Beispiele:

* http://35.180.178.217:5000/get_data?state=Bayern
* http://35.180.178.217:5000/get_totals?state=Bayern&date_range=2020-03-12 2020-03-21
* http://35.180.178.217:5000/get_totals?state=Bayern&date_range=2020-03-12 2020-03-21&province=SK München
* http://35.180.178.217:5000/get_events?location=Thüringen

Folgende weitere Parameter für /get_data & /get_totals sind verfügbar:

* Bundesland(state), Landkreis(province), Geschlecht(sex), Alter von(age_group_start), Alter bis(age_group_end), Abrufdatum(extraction_date YYYY-MM-DD), Datumsbereich (date_range YYYY-MM-DD YYYY-MM-DD) 

Folgende weitere Parameter für /get_events sind verfügbar:
* Ort (location), Bezugsdaten (publish_date), Abrufdaten (extraction_date)

# WirVsVirus Challenge
A global and central database/datalake accessible through an API

## The Problem
If applications are developed to fight the virus / collect information, this data must be made available to the general
public and other applications. How do I as a developer, e.g. of an app for predicting the spread of a virus, obtain data
for the application? Where can I upload the data that my app collects and make it available to other developers or
statisticians?

## The Solution
A Central Datalake / Central Database where this information or virus data can be uploaded from applications. This datalake in turn has application program interfaces to distribute the data to other applications.

##### Tags
*0038_Daten: Wie können wir Daten besser aufbereiten und nutzen?*

**Challenge ID** 0193	

**Schlüssel** 0038

**Probier es aus**
Ein paar Beispiele:

* http://35.180.178.217:5000/get_data?state=Bayern
* http://35.180.178.217:5000/get_totals?state=Bayern&date_range=2020-03-12 2020-03-21
* http://35.180.178.217:5000/get_totals?state=Bayern&date_range=2020-03-12 2020-03-21&province=SK München
* http://35.180.178.217:5000/get_events?location=Thüringen

Folgende weitere Parameter für /get_data & /get_totals sind verfügbar:

* Bundesland(state), Landkreis(province), Geschlecht(sex), Alter von(age_group_start), Alter bis(age_group_end), Abrufdatum(extraction_date YYYY-MM-DD), Datumsbereich (date_range YYYY-MM-DD YYYY-MM-DD) 

Folgende weitere Parameter für /get_events sind verfügbar:
* Ort (location), Bezugsdaten (publish_date), Abrufdaten (extraction_date)


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