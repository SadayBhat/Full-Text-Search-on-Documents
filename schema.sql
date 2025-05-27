--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-05-27 12:45:55

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
-- TOC entry 218 (class 1259 OID 16751)
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents (
    id integer NOT NULL,
    filename character varying NOT NULL,
    content text NOT NULL,
    search_vector tsvector GENERATED ALWAYS AS (to_tsvector('english'::regconfig, content)) STORED
);


ALTER TABLE public.documents OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16750)
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.documents_id_seq OWNER TO postgres;

--
-- TOC entry 4862 (class 0 OID 0)
-- Dependencies: 217
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;


--
-- TOC entry 220 (class 1259 OID 16892)
-- Name: search_index; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.search_index (
    id integer NOT NULL,
    filename character varying NOT NULL,
    file_hash character varying NOT NULL,
    search_vector tsvector NOT NULL,
    file_path character varying
);


ALTER TABLE public.search_index OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16891)
-- Name: search_index_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.search_index_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.search_index_id_seq OWNER TO postgres;

--
-- TOC entry 4863 (class 0 OID 0)
-- Dependencies: 219
-- Name: search_index_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.search_index_id_seq OWNED BY public.search_index.id;


--
-- TOC entry 4700 (class 2604 OID 16754)
-- Name: documents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);


--
-- TOC entry 4702 (class 2604 OID 16895)
-- Name: search_index id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.search_index ALTER COLUMN id SET DEFAULT nextval('public.search_index_id_seq'::regclass);


--
-- TOC entry 4704 (class 2606 OID 16759)
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- TOC entry 4709 (class 2606 OID 16901)
-- Name: search_index search_index_filename_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.search_index
    ADD CONSTRAINT search_index_filename_key UNIQUE (filename);


--
-- TOC entry 4711 (class 2606 OID 16899)
-- Name: search_index search_index_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.search_index
    ADD CONSTRAINT search_index_pkey PRIMARY KEY (id);


--
-- TOC entry 4705 (class 1259 OID 16760)
-- Name: idx_documents_search_vector; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_documents_search_vector ON public.documents USING gin (search_vector);


--
-- TOC entry 4706 (class 1259 OID 16902)
-- Name: ix_search_index_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_search_index_id ON public.search_index USING btree (id);


--
-- TOC entry 4707 (class 1259 OID 16903)
-- Name: ix_search_vector_gin; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_search_vector_gin ON public.search_index USING gin (search_vector);


-- Completed on 2025-05-27 12:45:56

--
-- PostgreSQL database dump complete
--

