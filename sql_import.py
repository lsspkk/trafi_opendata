# -*- coding: utf-8 -*-
#
# Koostaa migrations tiedoston eli nipun SQL-lausekkeita,
# jolla saa Postgresql kantaan lisättyä CSV-datan
#
# käyttö
# python3 sql_import.py tiedostonnimi
# - voit tarkistaa miltä näyttää
# python3 sql_import.py tiedostonnimi > import_data.sql
# - voit printata tiedot tiedostoon, ja siitä sitten SQL-tietokantaan
#
import argparse
import sys
import csv
import json


parser = argparse.ArgumentParser(description="suodatetaan trafin open dataa")
parser.add_argument("tiedosto", help="CSV tiedosto, jossa open data on")

args = parser.parse_args()

keys = ["ajoneuvoluokka",
    "ensirekisterointipvm",
    "ajoneuvoryhma",
    "ajoneuvonkaytto",
    "kayttoonottopvm",
    "vari",
    "ovienLukumaara",
    "korityyppi",
    "ohjaamotyyppi",
    "istumapaikkojenLkm",
    "omamassa",
    "teknSuurSallKokmassa",
    "tieliikSuurSallKokmassa",
    "ajonKokPituus",
    "ajonLeveys",
    "ajonKorkeus",
    "kayttovoima",
    "iskutilavuus",
    "suurinNettoteho",
    "sylintereidenLkm",
    "ahdin",
    "sahkohybridi",
    "merkkiSelvakielinen",
    "mallimerkinta",
    "vaihteisto",
    "vaihteidenLkm",
    "kaupallinenNimi",
    "voimanvalJaTehostamistapa",
    "tyyppihyvaksyntanro",
    "variantti",
    "versio",
    "yksittaisKayttovoima",
    "kunta",
    "Co2",
    "jarnro",
    "alue",
    "matkamittarilukema",
    "valmistenumero2" ]

no_quotes = [
    "suurinNettoteho",
    "Co2",
    "iskutilavuus"
]

if args.tiedosto:
    with open(args.tiedosto, encoding="utf-8") as csv_in:
        reader = csv.DictReader(csv_in, delimiter=";")
        count = 0
        rows = []
        for row in reader:

            values = []
            for k in keys:
                if k in no_quotes:
                    if len(row[k]) == 0:
                        #print('ei numeroarvoa autolla\n',row)
                        break
                    v = row[k]
                    values.append(v)
                else:
                    v = row[k].replace("'", r"''")
                    if len(v) == 0: v = "None"
                    values.append("'"+ v +"'")

            # this wont run if valueloop did a break
            else:
                rows.append("("+','.join(values)+")")
                count = count + 1
                if count % 10000 == 0 and count:
                    print( "\nINSERT INTO cars (", ','.join(keys), ") VALUES ")
                    print(',\n'.join(rows)+";")
                    rows = []

        if( len(rows) != 0 ):
            print( "\nINSERT INTO cars (", ','.join(keys), ") VALUES ")
            print(',\n'.join(rows)+";")
            rows = []
