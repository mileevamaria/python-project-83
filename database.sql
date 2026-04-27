--
-- PostgreSQL database dump
--

\restrict ippbTULVwvVWvBxcfDDtfYlcexsU9xJkbgY0XaDxJjDZz5Sozqx9KdDR0bCdJkw

-- Dumped from database version 18.3 (Homebrew)
-- Dumped by pg_dump version 18.3 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: url_checks; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.url_checks (
    id integer NOT NULL,
    url_id integer NOT NULL,
    status_code integer,
    h1 text,
    title text,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.url_checks OWNER TO myuser;

--
-- Name: url_checks_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.url_checks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.url_checks_id_seq OWNER TO myuser;

--
-- Name: url_checks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.url_checks_id_seq OWNED BY public.url_checks.id;


--
-- Name: urls; Type: TABLE; Schema: public; Owner: mariamileeva
--

CREATE TABLE public.urls (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.urls OWNER TO mariamileeva;

--
-- Name: urls_id_seq; Type: SEQUENCE; Schema: public; Owner: mariamileeva
--

CREATE SEQUENCE public.urls_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.urls_id_seq OWNER TO mariamileeva;

--
-- Name: urls_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mariamileeva
--

ALTER SEQUENCE public.urls_id_seq OWNED BY public.urls.id;


--
-- Name: url_checks id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.url_checks ALTER COLUMN id SET DEFAULT nextval('public.url_checks_id_seq'::regclass);


--
-- Name: urls id; Type: DEFAULT; Schema: public; Owner: mariamileeva
--

ALTER TABLE ONLY public.urls ALTER COLUMN id SET DEFAULT nextval('public.urls_id_seq'::regclass);


--
-- Data for Name: url_checks; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.url_checks (id, url_id, status_code, h1, title, description, created_at) FROM stdin;
\.


--
-- Data for Name: urls; Type: TABLE DATA; Schema: public; Owner: mariamileeva
--

COPY public.urls (id, name, created_at) FROM stdin;
\.


--
-- Name: url_checks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.url_checks_id_seq', 1, false);


--
-- Name: urls_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mariamileeva
--

SELECT pg_catalog.setval('public.urls_id_seq', 6, true);


--
-- Name: url_checks url_checks_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.url_checks
    ADD CONSTRAINT url_checks_pkey PRIMARY KEY (id);


--
-- Name: urls urls_name_key; Type: CONSTRAINT; Schema: public; Owner: mariamileeva
--

ALTER TABLE ONLY public.urls
    ADD CONSTRAINT urls_name_key UNIQUE (name);


--
-- Name: urls urls_pkey; Type: CONSTRAINT; Schema: public; Owner: mariamileeva
--

ALTER TABLE ONLY public.urls
    ADD CONSTRAINT urls_pkey PRIMARY KEY (id);


--
-- Name: url_checks url_checks_url_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.url_checks
    ADD CONSTRAINT url_checks_url_id_fkey FOREIGN KEY (url_id) REFERENCES public.urls(id) ON DELETE CASCADE;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO myuser;


--
-- Name: TABLE urls; Type: ACL; Schema: public; Owner: mariamileeva
--

GRANT ALL ON TABLE public.urls TO myuser;


--
-- Name: SEQUENCE urls_id_seq; Type: ACL; Schema: public; Owner: mariamileeva
--

GRANT ALL ON SEQUENCE public.urls_id_seq TO myuser;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: mariamileeva
--

ALTER DEFAULT PRIVILEGES FOR ROLE mariamileeva IN SCHEMA public GRANT ALL ON SEQUENCES TO myuser;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: mariamileeva
--

ALTER DEFAULT PRIVILEGES FOR ROLE mariamileeva IN SCHEMA public GRANT ALL ON TABLES TO myuser;


--
-- PostgreSQL database dump complete
--

\unrestrict ippbTULVwvVWvBxcfDDtfYlcexsU9xJkbgY0XaDxJjDZz5Sozqx9KdDR0bCdJkw

