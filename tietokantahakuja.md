sql-komentoja
täs ekaks perus grouppia, lopuks histogrammin laskentaa
http://tapoueh.org/blog/2014/02/postgresql-aggregates-and-histograms/



# yleisimmät autot
select cars.merkkiselvakielinen, count(cars.merkkiselvakielinen) from cars group by cars.merkkiSelvakielinen order by count(cars.merkkiselvakielinen) desc;

# yleisimmät skodan mallit
select q1.mallimerkinta,count(q1.mallimerkinta) from (select * from cars where cars.merkkiselvakielinen = 'Skoda') as q1 group by q1.mallimerkinta order by count(q1.mallimerkinta) desc limit 15;

# yleisimmät Toyotan mallit vuonna 2016
select q1.mallimerkinta,count(q1.mallimerkinta) from (select * from cars where cars.merkkiselvakielinen = 'Toyota' and cars.kayttoonottopvm > '20160000' and
cars.kayttoonottopvm < '20170000'
) as q1 group by q1.mallimerkinta order by count(q1.mallimerkinta) desc limit 15;

# vuonna 2017
select q1.mallimerkinta,count(q1.mallimerkinta) from (select * from cars where cars.merkkiselvakielinen = 'Toyota' and cars.kayttoonottopvm > '20170000' and
cars.kayttoonottopvm < '20180000'
) as q1 group by q1.mallimerkinta order by count(q1.mallimerkinta) desc limit 15;


# tehokkaimmat toyotat 2017
select q1.suurinnettoteho,q1.mallimerkinta,count(q1.mallimerkinta) from (select * from cars where cars.merkkiselvakielinen = 'Toyota' and cars.kayttoonottopvm > '20170000' and
cars.kayttoonottopvm < '20180000'
) as q1 group by q1.mallimerkinta, q1.suurinnettoteho order by q1.suurinnettoteho desc limit 15;

# tehokkaimmat skodat 2017
select q1.suurinnettoteho,q1.mallimerkinta,count(q1.mallimerkinta) from (select * from cars where cars.merkkiselvakielinen = 'Skoda' and cars.kayttoonottopvm > '20170000' and
cars.kayttoonottopvm < '20180000'
) as q1 group by q1.mallimerkinta, q1.suurinnettoteho order by q1.suurinnettoteho desc limit 15;


#tehokkaimmat bmw:t 2017
select q1.suurinnettoteho,q1.mallimerkinta,count(q1.mallimerkinta) from (select * from cars where cars.merkkiselvakielinen = 'BMW' and cars.kayttoonottopvm > '20170000' and
cars.kayttoonottopvm < '20180000'
) as q1 group by q1.mallimerkinta, q1.suurinnettoteho having count(q1.mallimerkinta) > 5 order by q1.suurinnettoteho desc limit 15;


#suurimmat co2-päästöt, BMW 2017
select q1.co2,q1.mallimerkinta,count(q1.mallimerkinta) from (select * from cars where cars.merkkiselvakielinen = 'BMW' and cars.kayttoonottopvm > '20170000' and
cars.kayttoonottopvm < '20180000'
) as q1 group by q1.mallimerkinta, q1.co2 having count(q1.mallimerkinta) > 5 order by q1.co2 desc limit 15;


# tehot ja paastot, BMW 2017
select q1.suurinnettoteho,q1.co2,q1.mallimerkinta,count(q1.mallimerkinta) from (select * from cars where cars.merkkiselvakielinen = 'BMW' and cars.kayttoonottopvm > '20170000' and
cars.kayttoonottopvm < '20180000'
) as q1 group by q1.mallimerkinta, q1.co2, q1.suurinnettoteho having count(q1.mallimerkinta) > 5 order by q1.co2 desc limit 15;


# tehot ja paastot, Skoda 2017
select q1.suurinnettoteho,q1.co2,q1.mallimerkinta,count(q1.mallimerkinta) from (select * from cars where cars.merkkiselvakielinen = 'Skoda' and cars.kayttoonottopvm > '20170000' and
cars.kayttoonottopvm < '20180000'
) as q1 group by q1.mallimerkinta, q1.co2, q1.suurinnettoteho having count(q1.mallimerkinta) > 5 order by q1.co2 asc limit 15;


#histogrammi tehot
with drb_stats as (
    select min(suurinnettoteho) as min,
           max(suurinnettoteho) as max
      from cars

),
     histogram as (
   select width_bucket(suurinnettoteho, min, max, 29) as bucket,
          int4range(min(suurinnettoteho), max(suurinnettoteho), '[]') as range,
          count(*) as freq
     from cars, drb_stats

 group by bucket
 order by bucket
)
 select bucket, range, freq,
        repeat('■',
               (   freq::float
                 / max(freq) over()
                 * 30
               )::int
        ) as bar
   from histogram;
bucket |   range   |  freq  |              bar               
--------+-----------+--------+--------------------------------
      1 | [12,13)   |      1 |
      2 | [33,49)   |   4437 | ■
      3 | [49,67)   | 104344 | ■■■■■■■■■■■■■■
      4 | [67,85)   | 169732 | ■■■■■■■■■■■■■■■■■■■■■■■■
      5 | [85,102)  | 216316 | ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
      6 | [103,121) | 187194 | ■■■■■■■■■■■■■■■■■■■■■■■■■■
      7 | [121,139) |  70519 | ■■■■■■■■■■
      8 | [139,157) |  38377 | ■■■■■
      9 | [157,174) |  11940 | ■■
     10 | [175,194) |  11974 | ■■
     11 | [194,212) |   2513 |
     12 | [212,230) |   2160 |
     13 | [230,248) |   1518 |
     14 | [250,266) |    618 |
     15 | [268,284) |    413 |
     16 | [285,302) |    254 |
     17 | [302,319) |    124 |
     18 | [320,337) |    185 |
     19 | [338,352) |     16 |
     20 | [357,374) |     63 |
     21 | [375,391) |     82 |
     22 | [395,411) |     41 |
     23 | [412,428) |     80 |
     24 | [430,446) |     22 |
     25 | [449,464) |      7 |
     27 | [486,494) |      3 |
     30 | [537,538) |      1 |




#histogrammi paastot
with drb_stats as (
    select min(co2) as min,
           max(co2) as max
      from cars

),
     histogram as (
   select width_bucket(co2, min, max, 19) as bucket,
          int4range(min(co2), max(co2), '[]') as range,
          count(*) as freq
     from cars, drb_stats

 group by bucket
 order by bucket
)
 select bucket, range, freq,
        repeat('■',
               (   freq::float
                 / max(freq) over()
                 * 30
               )::int
        ) as bar
   from histogram;


 bucket |   range   |  freq  |              bar               
--------+-----------+--------+--------------------------------
      1 | [0,15)    |     14 |
      2 | [27,28)   |      1 |
      3 | [49,60)   |     37 |
      4 | [70,88)   |  10482 | ■
      5 | [88,110)  | 116099 | ■■■■■■■■■■■■■
      6 | [110,132) | 273094 | ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
      7 | [132,153) | 239504 | ■■■■■■■■■■■■■■■■■■■■■■■■■■
      8 | [153,175) | 122788 | ■■■■■■■■■■■■■
      9 | [175,197) |  44678 | ■■■■■
     10 | [197,219) |   9481 | ■
     11 | [219,241) |   3990 |
     12 | [241,263) |   1755 |
     13 | [263,284) |    653 |
     14 | [284,306) |    226 |
     15 | [306,328) |     73 |
     16 | [328,350) |     31 |
     17 | [353,370) |     19 |
     18 | [372,393) |      7 |
     19 | [400,401) |      1 |
     20 | [415,416) |      1 |







#histogrammi paastot skoda 2017
with drb_stats as (
    select min(co2) as min,
           max(co2) as max
      from cars

      where cars.merkkiselvakielinen = 'Skoda' and cars.kayttoonottopvm > '20170000' and
      cars.kayttoonottopvm < '20180000'
),
     histogram as (
   select width_bucket(co2, min, max, 19) as bucket,
          int4range(min(co2), max(co2), '[]') as range,
          count(*) as freq
     from cars, drb_stats

     where cars.merkkiselvakielinen = 'Skoda' and cars.kayttoonottopvm > '20170000' and
     cars.kayttoonottopvm < '20180000'

 group by bucket
 order by bucket
)
 select bucket, range, freq,
        repeat('■',
               (   freq::float
                 / max(freq) over()
                 * 30
               )::int
        ) as bar
   from histogram;


# histogrammi tehot skoda 2017
with drb_stats as (
   select min(suurinnettoteho) as min,
          max(suurinnettoteho) as max
     from cars

     where cars.merkkiselvakielinen = 'Skoda' and cars.kayttoonottopvm > '20170000' and
     cars.kayttoonottopvm < '20180000'
),
    histogram as (
  select width_bucket(suurinnettoteho, min, max, 19) as bucket,
         int4range(min(suurinnettoteho), max(suurinnettoteho), '[]') as range,
         count(*) as freq
    from cars, drb_stats

    where cars.merkkiselvakielinen = 'Skoda' and cars.kayttoonottopvm > '20170000' and
    cars.kayttoonottopvm < '20180000'

group by bucket
order by bucket
)
select bucket, range, freq,
       repeat('■',
              (   freq::float
                / max(freq) over()
                * 30
              )::int
       ) as bar
  from histogram;



 bucket |   range   | freq |              bar               
--------+-----------+------+--------------------------------
      1 | [44,45)   |   20 | ■
      2 | [55,56)   |  134 | ■■■■
      3 | [66,67)   |  469 | ■■■■■■■■■■■■■
      4 | [77,78)   |    2 |
      5 | [81,86)   |  899 | ■■■■■■■■■■■■■■■■■■■■■■■■■■
      6 | [88,93)   |   97 | ■■■
      8 | [110,111) | 1046 | ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
     11 | [132,136) |  524 | ■■■■■■■■■■■■■■■
     12 | [140,141) |  170 | ■■■■■
     14 | [162,163) |   45 | ■
     15 | [169,170) |   12 |
     20 | [206,207) |   17 |




#histogrammi paastot bmw 2017
with drb_stats as (
    select min(co2) as min,
           max(co2) as max
      from cars

      where cars.merkkiselvakielinen = 'BMW' and cars.kayttoonottopvm > '20170000' and
      cars.kayttoonottopvm < '20180000'
),
     histogram as (
   select width_bucket(co2, min, max, 19) as bucket,
          int4range(min(co2), max(co2), '[]') as range,
          count(*) as freq
     from cars, drb_stats

     where cars.merkkiselvakielinen = 'BMW' and cars.kayttoonottopvm > '20170000' and
     cars.kayttoonottopvm < '20180000'

 group by bucket
 order by bucket
)
 select bucket, range, freq,
        repeat('■',
               (   freq::float
                 / max(freq) over()
                 * 30
               )::int
        ) as bar
   from histogram;



# histogrammi tehot bmw 2017
with drb_stats as (
   select min(suurinnettoteho) as min,
          max(suurinnettoteho) as max
     from cars

     where cars.merkkiselvakielinen = 'BMW' and cars.kayttoonottopvm > '20170000' and
     cars.kayttoonottopvm < '20180000'
),
    histogram as (
  select width_bucket(suurinnettoteho, min, max, 19) as bucket,
         int4range(min(suurinnettoteho), max(suurinnettoteho), '[]') as range,
         count(*) as freq
    from cars, drb_stats

    where cars.merkkiselvakielinen = 'BMW' and cars.kayttoonottopvm > '20170000' and
    cars.kayttoonottopvm < '20180000'

group by bucket
order by bucket
)
select bucket, range, freq,
       repeat('■',
              (   freq::float
                / max(freq) over()
                * 30
              )::int
       ) as bar
  from histogram;
 bucket |   range   | freq |              bar               
--------+-----------+------+--------------------------------
      1 | [70,76)   |    5 |
      2 | [85,86)   |   69 | ■■■■■
      3 | [100,111) |  400 | ■■■■■■■■■■■■■■■■■■■■■■■■■■■
      4 | [120,121) |    3 |
      5 | [135,136) |  176 | ■■■■■■■■■■■■
      6 | [140,142) |  451 | ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
      7 | [160,166) |    2 |
      8 | [170,171) |    6 |
      9 | [180,191) |   49 | ■■■
     10 | [195,196) |    4 |
     12 | [230,231) |    6 |
     13 | [235,241) |   14 | ■
     14 | [250,251) |   10 | ■
     15 | [272,273) |    2 |
     16 | [280,281) |    1 |
     17 | [294,295) |    1 |
     18 | [317,318) |    1 |
     20 | [331,332) |    1 |




# Suomen tehokkaimmat autot 2017
select suurinnettoteho,merkkiselvakielinen,mallimerkinta from cars order by suurinnettoteho desc limit 10;
 suurinnettoteho | merkkiselvakielinen |                  mallimerkinta                   
-----------------+---------------------+--------------------------------------------------
             537 | Audi                | RS 6 AVANT Farmari (AC) 4ov 3993cm3 A
             493 | Ferrari             | 488 GTB Coupé (AD) 2ov 3902cm3 A
             493 | Ferrari             | 488 Spider Avoauto (AE) 2ov 3902cm3 A
             486 | Ferrari             | FF Coupé (AD) 2ov 6262cm3 A
             463 | Bentley             | Continental Supersports Coupé (AD) 2ov 5998cm3 A
             460 | Bentley             | Flying Spur W12 Sedan (AA) 4ov 5998cm3 A
             456 | Porsche             | 911 GT2 RS Coupé (AD) 2ov 3600cm3
             456 | Ferrari             | 599 GTB Coupé (AD) 2ov 5999cm3
             449 | Lamborghini         | Huracan Avoauto (AE) 2ov 5204cm3
             449 | Audi                | R8 Coupe Coupé (AD) 2ov 5204cm3 A


# suomen tehottomimmat autot 2017
select suurinnettoteho,merkkiselvakielinen,mallimerkinta from cars order by suurinnettoteho asc limit 10;
 suurinnettoteho | merkkiselvakielinen |                mallimerkinta                
-----------------+---------------------+---------------------------------------------
              12 | Mercedes-Benz       | SPRINTER Matkailuauto (SA) 5ov 2143cm3 A
              33 | Smart               | FORTWO COUPE CDI Coupé (AD) 2ov 799cm3 A
              33 | Smart               | FORTWO CABRIO CDI Avoauto (AE) 2ov 799cm3 A
              33 | Smart               | FORTWO COUPE CDI Coupé (AD) 2ov 799cm3 A
              33 | Smart               | FORTWO COUPE CDI Coupé (AD) 2ov 799cm3 A
              33 | Smart               | FORTWO COUPE CDI Coupé (AD) 2ov 799cm3 A
              33 | Smart               | FORTWO COUPE CDI Coupé (AD) 2ov 799cm3 A
              33 | Smart               | FORTWO CABRIO CDI Avoauto (AE) 2ov 799cm3 A
              33 | Smart               | FORTWO COUPE CDI Coupé (AD) 2ov 799cm3 A
              33 | Smart               | FORTWO COUPE CDI Coupé (AD) 2ov 799cm3 A
