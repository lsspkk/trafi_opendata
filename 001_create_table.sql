drop table cars;
CREATE TABLE cars (
    id integer not null,
    ajoneuvoluokka text,
    ensirekisterointipvm text,
    ajoneuvoryhma text,
    ajoneuvonkaytto text,
    kayttoonottopvm text,
    vari text,
    ovienLukumaara text,
    korityyppi text,
    ohjaamotyyppi text,
    istumapaikkojenLkm text,
    omamassa text,
    teknSuurSallKokmassa text,
    tieliikSuurSallKokmassa text,
    ajonKokPituus text,
    ajonLeveys text,
    ajonKorkeus text,
    kayttovoima text,
    iskutilavuus text,
    suurinNettoteho text,
    sylintereidenLkm text,
    ahdin text,
    sahkohybridi text,
    merkkiSelvakielinen text,
    mallimerkinta text,
    vaihteisto text,
    vaihteidenLkm text,
    kaupallinenNimi text,
    voimanvalJaTehostamistapa text,
    tyyppihyvaksyntanro text,
    variantti text,
    versio text,
    yksittaisKayttovoima text,
    kunta text,
    Co2 text,
    jarnro text,
    alue text,
    matkamittarilukema text,
    valmistenumero2 text
);

ALTER TABLE public.cars OWNER TO postgres;

--
-- Name: cars_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE cars_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cars_id_seq OWNER TO postgres;

ALTER TABLE ONLY cars ALTER COLUMN id SET DEFAULT nextval('cars_id_seq'::regclass);

--
-- Name: cars_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY cars
    ADD CONSTRAINT cars_pkey PRIMARY KEY (id);


--
-- Name: cars; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE cars FROM PUBLIC;
REVOKE ALL ON TABLE cars FROM postgres;
GRANT ALL ON TABLE cars TO postgres;
