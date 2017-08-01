# -*- coding: utf-8 -*-
#
# Valitsee csv-tiedostosta ajoneuvot käyttöönottovuosiluvun mukaan
#
# 1. --laske optiolla printataan ruutuun ajoneuvomäärät vuosittain
#
# 2. --suodata optiolla tallennetaan _filtered -tiedostoon uudemmat autot
import argparse
import sys
import csv
import json

parser = argparse.ArgumentParser(description="lasketaan/suodatetaan trafin open dataa")
group = parser.add_mutually_exclusive_group(required=True)
parser.add_argument("tiedosto", help="CSV tiedosto, jossa open data on")
group.add_argument("--suodata", nargs=1, type=int, metavar=('VUOSI'), help="valitse rivit, joiden vuosi on tämä tai uudempi")
group.add_argument("--laske", nargs=1, type=int, metavar=('VUOSI'), help="laske rivit, joiden vuosi on tämä tai uudempi")

args = parser.parse_args()


if args.tiedosto and args.laske:
    with open(args.tiedosto, encoding="latin1") as csv_in:
        reader = csv.DictReader(csv_in, delimiter=";")
        counter = 0
        counters = {}
        for row in reader:
            vuosi = row['kayttoonottopvm'][:4]
            if str(args.laske[0]) <= vuosi:
                if vuosi in counters:
                    counters[vuosi] = counters[vuosi] + 1
                else:
                    counters[vuosi] = 1

            counter = counter + 1
            if counter % 100000 == 0 and counter != 0:
                print( counter )
        print( "ajoneuvoja yhteensä:", counter )
        print( "ajoneuvomäärät vuosittain" )
        print(json.dumps(counters,indent=2, sort_keys=True))


elif args.tiedosto and args.suodata:
    with open(args.tiedosto, encoding="latin1") as csv_in:
        with open(str(args.tiedosto)+"_filtered", "w") as csv_out:
            reader = csv.DictReader(csv_in, delimiter=";")
            writer = csv.DictWriter(csv_out, delimiter=";", fieldnames=reader.fieldnames)
            filtered = []
            counter = 0
            counters = {}
            for row in reader:
                vuosi = row['kayttoonottopvm'][:4]
                if vuosi in counters:
                    counters[vuosi] = counters[vuosi] + 1
                else:
                    counters[vuosi] = 1

                if str(args.suodata[0]) <= vuosi and row['ajoneuvoluokka'] in ['M1', 'M1G']:
                    counter = counter + 1
                    filtered.append(row)
                if counter % 10000 == 0 and counter != 0:
                    print( "löydetty ", counter )
            #filtered = filter(lambda p: str(args.vuosi[0]) <= p['kayttoonottopvm'], reader)
            print( "ajoneuvoja yhteensä:", counter )
            print(json.dumps(counters,indent=2, sort_keys=True))
            print( "saving filtered file..." )
            writer.writeheader()
            writer.writerows(filtered)
            print( "done")
