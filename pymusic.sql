--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: aaronwishnick; Tablespace: 
--

CREATE TABLE alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO aaronwishnick;

--
-- Name: feeds; Type: TABLE; Schema: public; Owner: aaronwishnick; Tablespace: 
--

CREATE TABLE feeds (
    id integer NOT NULL,
    url character varying(255),
    title character varying(255)
);


ALTER TABLE public.feeds OWNER TO aaronwishnick;

--
-- Name: feeds_id_seq; Type: SEQUENCE; Schema: public; Owner: aaronwishnick
--

CREATE SEQUENCE feeds_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.feeds_id_seq OWNER TO aaronwishnick;

--
-- Name: feeds_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aaronwishnick
--

ALTER SEQUENCE feeds_id_seq OWNED BY feeds.id;


--
-- Name: songs; Type: TABLE; Schema: public; Owner: aaronwishnick; Tablespace: 
--

CREATE TABLE songs (
    id integer NOT NULL,
    title character varying(255),
    player_id integer,
    song_id character varying(50),
    disliked integer,
    feed_id integer,
    pub_date timestamp without time zone
);


ALTER TABLE public.songs OWNER TO aaronwishnick;

--
-- Name: songs_id_seq; Type: SEQUENCE; Schema: public; Owner: aaronwishnick
--

CREATE SEQUENCE songs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.songs_id_seq OWNER TO aaronwishnick;

--
-- Name: songs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aaronwishnick
--

ALTER SEQUENCE songs_id_seq OWNED BY songs.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: aaronwishnick
--

ALTER TABLE ONLY feeds ALTER COLUMN id SET DEFAULT nextval('feeds_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: aaronwishnick
--

ALTER TABLE ONLY songs ALTER COLUMN id SET DEFAULT nextval('songs_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: aaronwishnick
--

COPY alembic_version (version_num) FROM stdin;
224b16ee675
\.


--
-- Data for Name: feeds; Type: TABLE DATA; Schema: public; Owner: aaronwishnick
--

COPY feeds (id, url, title) FROM stdin;
1	http://freshnewtracks.com/feed	Fresh New Tracks
2	http://knackfortracks.com/feed/	Knack For Tracks
\.


--
-- Name: feeds_id_seq; Type: SEQUENCE SET; Schema: public; Owner: aaronwishnick
--

SELECT pg_catalog.setval('feeds_id_seq', 2, true);


--
-- Data for Name: songs; Type: TABLE DATA; Schema: public; Owner: aaronwishnick
--

COPY songs (id, title, player_id, song_id, disliked, feed_id, pub_date) FROM stdin;
40	Misterwives – Reflections (Gryffin Remix)	0	145922509	0	1	2014-04-27 05:27:11
41	Peter Thomas – All Of You (Steerner Bootleg)	0	146547801	0	1	2014-04-26 16:28:59
42	Lincoln Jesser x Elephante – A Trillion Somethings Right	0	145792038	0	1	2014-04-26 03:43:25
43	Sigma – Nobody To Love (Third Party Remix)	1	kQSdY0rHonQ	0	1	2014-04-25 22:19:19
44	Jez Dior – Old No. 7 (featuring G-Eazy) (prod. By Danny Score)	0	144862031	0	1	2014-04-25 19:20:52
45	JMSN – Thing U Miss (The Ninetys Remix)	0	146286300	0	1	2014-04-25 09:26:21
46	D!RTY AUD!O – Flame (AndDrop! Remix)	0	145778800	0	1	2014-04-24 18:13:40
47	Anna Graceman – Words (Glastrophobie Remix)	0	146223356	0	1	2014-04-24 15:01:48
48	Ansolo & Special Features – Unite	0	145814951	0	1	2014-04-24 03:22:59
49	Audien – Hindsight (Original Mix)	0	141929808	0	2	2014-04-27 19:27:32
50	Tritonal & Paris Blohm ft. Sterling Fox – Colors (Alan Morris Remix)	0	144656302	0	2	2014-04-27 19:21:21
51	Lush & Simon vs. Project 46 – City Of Words (Jigsaw Mashup)	0	146744672	0	2	2014-04-27 18:03:57
52	DJ Snake & Lil Jon – Turn Down For What (Remix) [ft. 2Chainz, Juicy J & French Montana]	0	146609291	0	2	2014-04-27 17:54:46
53	NONONO – Pumpin’ Blood (Michele Fasciano Remix)	0	145987963	0	2	2014-04-27 13:24:56
54	Boyce Avenue – I’ll Be The One (feat. Milkman)	0	141023492	0	2	2014-04-27 01:44:49
55	Tove Lo – Habits (Oliver Nelson Remix)	0	145962355	0	2	2014-04-26 23:47:41
56	R3HAB @ Story, Miami	1	c6oUywoicjA	0	2	2014-04-26 21:48:09
57	Beyoncé – Haunted (MoonBeat Remix)	0	146585078	0	2	2014-04-26 21:34:24
\.


--
-- Name: songs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: aaronwishnick
--

SELECT pg_catalog.setval('songs_id_seq', 57, true);


--
-- Name: feeds_pkey; Type: CONSTRAINT; Schema: public; Owner: aaronwishnick; Tablespace: 
--

ALTER TABLE ONLY feeds
    ADD CONSTRAINT feeds_pkey PRIMARY KEY (id);


--
-- Name: feeds_url_key; Type: CONSTRAINT; Schema: public; Owner: aaronwishnick; Tablespace: 
--

ALTER TABLE ONLY feeds
    ADD CONSTRAINT feeds_url_key UNIQUE (url);


--
-- Name: songs_pkey; Type: CONSTRAINT; Schema: public; Owner: aaronwishnick; Tablespace: 
--

ALTER TABLE ONLY songs
    ADD CONSTRAINT songs_pkey PRIMARY KEY (id);


--
-- Name: songs_song_id_key; Type: CONSTRAINT; Schema: public; Owner: aaronwishnick; Tablespace: 
--

ALTER TABLE ONLY songs
    ADD CONSTRAINT songs_song_id_key UNIQUE (song_id);


--
-- Name: songs_feed_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aaronwishnick
--

ALTER TABLE ONLY songs
    ADD CONSTRAINT songs_feed_id_fkey FOREIGN KEY (feed_id) REFERENCES feeds(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: aaronwishnick
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM aaronwishnick;
GRANT ALL ON SCHEMA public TO aaronwishnick;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

