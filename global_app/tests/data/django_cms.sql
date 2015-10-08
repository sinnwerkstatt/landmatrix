--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: cms_aliaspluginmodel; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_aliaspluginmodel (
    cmsplugin_ptr_id integer NOT NULL,
    plugin_id integer,
    alias_placeholder_id integer
);


--
-- Name: cms_cmsplugin; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_cmsplugin (
    id integer NOT NULL,
    "position" smallint,
    language character varying(15) NOT NULL,
    plugin_type character varying(50) NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    changed_date timestamp with time zone NOT NULL,
    parent_id integer,
    placeholder_id integer,
    depth integer NOT NULL,
    numchild integer NOT NULL,
    path character varying(255) NOT NULL,
    CONSTRAINT cms_cmsplugin_depth_check CHECK ((depth >= 0)),
    CONSTRAINT cms_cmsplugin_numchild_check CHECK ((numchild >= 0)),
    CONSTRAINT cms_cmsplugin_position_check CHECK (("position" >= 0))
);


--
-- Name: cms_cmsplugin_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_cmsplugin_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cms_cmsplugin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_cmsplugin_id_seq OWNED BY cms_cmsplugin.id;


--
-- Name: cms_globalpagepermission; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_globalpagepermission (
    id integer NOT NULL,
    can_change boolean NOT NULL,
    can_add boolean NOT NULL,
    can_delete boolean NOT NULL,
    can_change_advanced_settings boolean NOT NULL,
    can_publish boolean NOT NULL,
    can_change_permissions boolean NOT NULL,
    can_move_page boolean NOT NULL,
    can_view boolean NOT NULL,
    can_recover_page boolean NOT NULL,
    group_id integer,
    user_id integer
);


--
-- Name: cms_globalpagepermission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_globalpagepermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cms_globalpagepermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_globalpagepermission_id_seq OWNED BY cms_globalpagepermission.id;


--
-- Name: cms_globalpagepermission_sites; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_globalpagepermission_sites (
    id integer NOT NULL,
    globalpagepermission_id integer NOT NULL,
    site_id integer NOT NULL
);


--
-- Name: cms_globalpagepermission_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_globalpagepermission_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cms_globalpagepermission_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_globalpagepermission_sites_id_seq OWNED BY cms_globalpagepermission_sites.id;


--
-- Name: cms_page; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_page (
    id integer NOT NULL,
    created_by character varying(255) NOT NULL,
    changed_by character varying(255) NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    changed_date timestamp with time zone NOT NULL,
    publication_date timestamp with time zone,
    publication_end_date timestamp with time zone,
    in_navigation boolean NOT NULL,
    soft_root boolean NOT NULL,
    reverse_id character varying(40),
    navigation_extenders character varying(80),
    template character varying(100) NOT NULL,
    login_required boolean NOT NULL,
    limit_visibility_in_menu smallint,
    is_home boolean NOT NULL,
    application_urls character varying(200),
    application_namespace character varying(200),
    publisher_is_draft boolean NOT NULL,
    languages character varying(255),
    revision_id integer NOT NULL,
    xframe_options integer NOT NULL,
    parent_id integer,
    publisher_public_id integer,
    site_id integer NOT NULL,
    depth integer NOT NULL,
    numchild integer NOT NULL,
    path character varying(255) NOT NULL,
    CONSTRAINT cms_page_depth_check CHECK ((depth >= 0)),
    CONSTRAINT cms_page_numchild_check CHECK ((numchild >= 0)),
    CONSTRAINT cms_page_revision_id_check CHECK ((revision_id >= 0))
);


--
-- Name: cms_page_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_page_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cms_page_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_page_id_seq OWNED BY cms_page.id;


--
-- Name: cms_page_placeholders; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_page_placeholders (
    id integer NOT NULL,
    page_id integer NOT NULL,
    placeholder_id integer NOT NULL
);


--
-- Name: cms_page_placeholders_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_page_placeholders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cms_page_placeholders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_page_placeholders_id_seq OWNED BY cms_page_placeholders.id;


--
-- Name: cms_pagepermission; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_pagepermission (
    id integer NOT NULL,
    can_change boolean NOT NULL,
    can_add boolean NOT NULL,
    can_delete boolean NOT NULL,
    can_change_advanced_settings boolean NOT NULL,
    can_publish boolean NOT NULL,
    can_change_permissions boolean NOT NULL,
    can_move_page boolean NOT NULL,
    can_view boolean NOT NULL,
    grant_on integer NOT NULL,
    group_id integer,
    page_id integer,
    user_id integer
);


--
-- Name: cms_pagepermission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_pagepermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cms_pagepermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_pagepermission_id_seq OWNED BY cms_pagepermission.id;


--
-- Name: cms_pageuser; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_pageuser (
    user_ptr_id integer NOT NULL,
    created_by_id integer NOT NULL
);


--
-- Name: cms_pageusergroup; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_pageusergroup (
    group_ptr_id integer NOT NULL,
    created_by_id integer NOT NULL
);


--
-- Name: cms_placeholder; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_placeholder (
    id integer NOT NULL,
    slot character varying(255) NOT NULL,
    default_width smallint,
    CONSTRAINT cms_placeholder_default_width_check CHECK ((default_width >= 0))
);


--
-- Name: cms_placeholder_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_placeholder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cms_placeholder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_placeholder_id_seq OWNED BY cms_placeholder.id;


--
-- Name: cms_placeholderreference; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_placeholderreference (
    cmsplugin_ptr_id integer NOT NULL,
    name character varying(255) NOT NULL,
    placeholder_ref_id integer
);


--
-- Name: cms_staticplaceholder; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_staticplaceholder (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    code character varying(255) NOT NULL,
    dirty boolean NOT NULL,
    creation_method character varying(20) NOT NULL,
    draft_id integer,
    public_id integer,
    site_id integer
);


--
-- Name: cms_staticplaceholder_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_staticplaceholder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cms_staticplaceholder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_staticplaceholder_id_seq OWNED BY cms_staticplaceholder.id;


--
-- Name: cms_title; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_title (
    id integer NOT NULL,
    language character varying(15) NOT NULL,
    title character varying(255) NOT NULL,
    page_title character varying(255),
    menu_title character varying(255),
    meta_description text,
    slug character varying(255) NOT NULL,
    path character varying(255) NOT NULL,
    has_url_overwrite boolean NOT NULL,
    redirect character varying(2048),
    creation_date timestamp with time zone NOT NULL,
    published boolean NOT NULL,
    publisher_is_draft boolean NOT NULL,
    publisher_state smallint NOT NULL,
    page_id integer NOT NULL,
    publisher_public_id integer
);


--
-- Name: cms_title_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_title_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cms_title_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_title_id_seq OWNED BY cms_title.id;


--
-- Name: cms_usersettings; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_usersettings (
    id integer NOT NULL,
    language character varying(10) NOT NULL,
    clipboard_id integer,
    user_id integer NOT NULL
);


--
-- Name: cms_usersettings_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_usersettings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cms_usersettings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_usersettings_id_seq OWNED BY cms_usersettings.id;


--
-- Name: djangocms_text_ckeditor_text; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE djangocms_text_ckeditor_text (
    cmsplugin_ptr_id integer NOT NULL,
    body text NOT NULL
);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_cmsplugin ALTER COLUMN id SET DEFAULT nextval('cms_cmsplugin_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_globalpagepermission ALTER COLUMN id SET DEFAULT nextval('cms_globalpagepermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_globalpagepermission_sites ALTER COLUMN id SET DEFAULT nextval('cms_globalpagepermission_sites_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_page ALTER COLUMN id SET DEFAULT nextval('cms_page_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_page_placeholders ALTER COLUMN id SET DEFAULT nextval('cms_page_placeholders_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_pagepermission ALTER COLUMN id SET DEFAULT nextval('cms_pagepermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_placeholder ALTER COLUMN id SET DEFAULT nextval('cms_placeholder_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_staticplaceholder ALTER COLUMN id SET DEFAULT nextval('cms_staticplaceholder_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_title ALTER COLUMN id SET DEFAULT nextval('cms_title_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_usersettings ALTER COLUMN id SET DEFAULT nextval('cms_usersettings_id_seq'::regclass);


--
-- Data for Name: cms_aliaspluginmodel; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_aliaspluginmodel (cmsplugin_ptr_id, plugin_id, alias_placeholder_id) FROM stdin;
\.


--
-- Data for Name: cms_cmsplugin; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_cmsplugin (id, "position", language, plugin_type, creation_date, changed_date, parent_id, placeholder_id, depth, numchild, path) FROM stdin;
1	0	en	MapPlugin	2015-09-17 14:14:13.705436+02	2015-09-17 14:14:20.591781+02	\N	65	1	0	0001
2	0	en	MapPlugin	2015-09-17 14:14:13.705436+02	2015-09-17 14:26:38.578165+02	\N	66	1	0	0002
3	0	en	OverviewPlugin	2015-09-21 12:38:23.732494+02	2015-09-21 12:38:27.835234+02	\N	82	1	0	0003
4	0	en	TransnationalDealsPlugin	2015-09-21 12:38:42.395653+02	2015-09-21 12:38:45.250843+02	\N	83	1	0	0004
10	0	en	OverviewPlugin	2015-09-21 12:38:23.732494+02	2015-09-21 13:01:13.95497+02	\N	84	1	0	0007
11	0	en	InvestorTargetCountriesPlugin	2015-09-22 14:38:01.367684+02	2015-09-22 14:38:04.984403+02	\N	98	1	0	0008
13	0	en	TransnationalDealsPlugin	2015-09-21 12:38:42.395653+02	2015-09-22 14:38:22.180331+02	\N	90	1	0	000A
14	0	en	InvestorTargetCountriesPlugin	2015-09-22 14:38:01.367684+02	2015-09-22 15:59:09.280462+02	\N	99	1	0	000B
15	0	en	AgriculturalProducePlugin	2015-09-22 15:59:18.641198+02	2015-09-22 15:59:21.246044+02	\N	100	1	0	000C
17	0	en	AgriculturalProducePlugin	2015-09-22 15:59:18.641198+02	2015-09-22 16:01:53.869259+02	\N	101	1	0	000D
18	0	en	PerspectivePlugin	2015-09-22 16:23:56.398426+02	2015-09-22 16:23:59.401861+02	\N	102	1	0	000E
19	0	en	PerspectivePlugin	2015-09-22 16:23:56.398426+02	2015-09-22 16:24:45.451941+02	\N	103	1	0	000F
\.


--
-- Name: cms_cmsplugin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_cmsplugin_id_seq', 19, true);


--
-- Data for Name: cms_globalpagepermission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_globalpagepermission (id, can_change, can_add, can_delete, can_change_advanced_settings, can_publish, can_change_permissions, can_move_page, can_view, can_recover_page, group_id, user_id) FROM stdin;
\.


--
-- Name: cms_globalpagepermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_globalpagepermission_id_seq', 1, false);


--
-- Data for Name: cms_globalpagepermission_sites; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_globalpagepermission_sites (id, globalpagepermission_id, site_id) FROM stdin;
\.


--
-- Name: cms_globalpagepermission_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_globalpagepermission_sites_id_seq', 1, false);


--
-- Data for Name: cms_page; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_page (id, created_by, changed_by, creation_date, changed_date, publication_date, publication_end_date, in_navigation, soft_root, reverse_id, navigation_extenders, template, login_required, limit_visibility_in_menu, is_home, application_urls, application_namespace, publisher_is_draft, languages, revision_id, xframe_options, parent_id, publisher_public_id, site_id, depth, numchild, path) FROM stdin;
11	landmatrix	landmatrix	2015-06-18 13:10:50.3667+02	2015-06-18 13:10:50.54436+02	2015-06-18 13:10:50.308796+02	\N	t	f	\N	\N	INHERIT	f	\N	f	\N	\N	f	en	0	0	9	4	1	2	0	000B0003
10	landmatrix	landmatrix	2015-06-15 15:57:18.136968+02	2015-06-15 15:57:18.21346+02	2015-06-15 15:56:59.780278+02	\N	t	f	\N		1-column.html	f	\N	f	GlobalApphook	\N	f	en	0	0	9	3	1	2	0	000B0002
12	landmatrix	landmatrix	2015-06-18 13:10:55.955338+02	2015-06-18 13:10:56.043118+02	2015-06-18 13:10:55.935268+02	\N	t	f	\N	\N	INHERIT	f	\N	f	\N	\N	f	en	0	0	9	5	1	2	0	000B0004
13	landmatrix	landmatrix	2015-06-18 13:11:00.335296+02	2015-06-18 13:11:00.421223+02	2015-06-18 13:11:00.318646+02	\N	t	f	\N	\N	INHERIT	f	\N	f	\N	\N	f	en	0	0	9	6	1	2	0	000B0005
23	landmatrix	landmatrix	2015-09-22 15:59:35.484157+02	2015-09-22 16:01:53.872616+02	2015-09-22 15:59:35.472031+02	\N	t	f	\N		base-gettheidea.html	f	\N	f		\N	f	en	0	0	2	22	1	3	0	000B00010004
22	landmatrix	landmatrix	2015-09-22 15:58:43.865228+02	2015-09-22 16:01:53.880986+02	2015-09-22 15:59:35.472031+02	\N	t	f	\N		base-gettheidea.html	f	\N	f		\N	t	en	0	0	1	23	1	3	0	000A00010004
9	landmatrix	landmatrix	2015-06-15 15:57:17.579306+02	2015-06-18 13:26:02.924202+02	2015-06-15 15:57:17.568023+02	\N	t	f	\N		start.html	f	\N	t		\N	f	en	0	0	\N	8	1	1	6	000B
15	landmatrix	landmatrix	2015-09-17 14:26:38.511564+02	2015-09-17 14:26:38.583063+02	2015-09-17 14:26:38.500749+02	\N	t	f	\N		fullwidth.html	f	\N	f		\N	f	en	0	0	9	14	1	2	0	000B0006
19	landmatrix	landmatrix	2015-09-21 12:47:23.2717+02	2015-09-22 14:38:22.18397+02	2015-09-21 12:47:23.259719+02	\N	t	f	\N		INHERIT	f	\N	f		\N	f	en	0	0	2	17	1	3	0	000B00010002
17	landmatrix	landmatrix	2015-09-21 12:37:39.123252+02	2015-09-22 14:38:22.195639+02	2015-09-21 12:47:23.259719+02	\N	t	f	\N		INHERIT	f	\N	f		\N	t	en	0	0	1	19	1	3	0	000A00010002
14	landmatrix	landmatrix	2015-09-17 14:11:53.992269+02	2015-09-17 14:26:38.590446+02	2015-09-17 14:26:38.500749+02	\N	t	f	\N		fullwidth.html	f	\N	f		\N	t	en	0	0	8	15	1	2	0	000A0007
6	script	landmatrix	2015-06-10 16:06:44.11944+02	2015-06-18 13:11:00.446074+02	2015-06-18 13:11:00.318646+02	\N	t	f	\N	\N	INHERIT	f	\N	f	\N	\N	t	en	0	0	8	13	1	2	0	000A0006
5	script	landmatrix	2015-06-10 16:06:29.594661+02	2015-06-18 13:10:56.066277+02	2015-06-18 13:10:55.935268+02	\N	t	f	\N	\N	INHERIT	f	\N	f	\N	\N	t	en	0	0	8	12	1	2	0	000A0005
4	script	landmatrix	2015-06-10 16:06:19.697265+02	2015-06-18 13:10:50.56914+02	2015-06-18 13:10:50.308796+02	\N	t	f	\N	\N	INHERIT	f	\N	f	\N	\N	t	en	0	0	8	11	1	2	0	000A0004
3	script	landmatrix	2015-06-10 16:06:04.9222+02	2015-06-15 15:57:18.23633+02	2015-06-15 15:56:59.780278+02	\N	t	f	\N		1-column.html	f	\N	f	GlobalApphook	\N	t	en	0	0	8	10	1	2	0	000A0003
8	landmatrix	landmatrix	2015-06-11 15:35:20.553448+02	2015-06-18 13:26:02.974494+02	2015-06-15 15:57:17.568023+02	\N	t	f	\N		start.html	f	\N	t		\N	t	en	0	0	\N	9	1	1	6	000A
1	script	landmatrix	2015-06-10 16:05:46.591449+02	2015-09-21 13:01:09.609213+02	2015-06-10 16:05:47.420797+02	\N	t	f	\N		base-gettheidea.html	f	\N	f		\N	t	en	0	0	8	2	1	2	5	000A0001
18	landmatrix	landmatrix	2015-09-21 12:47:18.167384+02	2015-09-21 13:01:13.958387+02	2015-09-21 12:47:18.157742+02	\N	t	f	\N		INHERIT	f	\N	f		\N	f	en	0	0	2	16	1	3	0	000B00010001
16	landmatrix	landmatrix	2015-09-21 12:36:43.027007+02	2015-09-21 13:01:13.967866+02	2015-09-21 12:47:18.157742+02	\N	t	f	\N		INHERIT	f	\N	f		\N	t	en	0	0	1	18	1	3	0	000A00010001
21	landmatrix	landmatrix	2015-09-22 14:38:10.132622+02	2015-09-22 15:59:09.283746+02	2015-09-22 14:38:10.118792+02	\N	t	f	\N		INHERIT	f	\N	f		\N	f	en	0	0	2	20	1	3	0	000B00010003
20	landmatrix	landmatrix	2015-09-22 14:37:12.608246+02	2015-09-22 15:59:09.292624+02	2015-09-22 14:38:10.118792+02	\N	t	f	\N		INHERIT	f	\N	f		\N	t	en	0	0	1	21	1	3	0	000A00010003
2	script	landmatrix	2015-06-10 16:05:47.428875+02	2015-09-21 13:01:09.600302+02	2015-06-10 16:05:47.420797+02	\N	t	f	\N		base-gettheidea.html	f	\N	f		\N	f	en	0	0	9	1	1	2	5	000B0001
25	landmatrix	landmatrix	2015-09-22 16:24:45.398739+02	2015-09-22 16:24:45.455611+02	2015-09-22 16:24:45.386334+02	\N	t	f	\N		base-gettheidea.html	f	\N	f		\N	f	en	0	0	2	24	1	3	0	000B00010005
24	landmatrix	landmatrix	2015-09-22 16:23:39.713702+02	2015-09-22 16:24:45.464179+02	2015-09-22 16:24:45.386334+02	\N	t	f	\N		base-gettheidea.html	f	\N	f		\N	t	en	0	0	1	25	1	3	0	000A00010005
\.


--
-- Name: cms_page_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_page_id_seq', 25, true);


--
-- Data for Name: cms_page_placeholders; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_page_placeholders (id, page_id, placeholder_id) FROM stdin;
2	6	3
3	1	4
4	3	5
5	8	6
6	2	7
7	4	8
8	5	9
9	9	10
10	10	11
11	11	12
12	12	13
13	13	14
14	8	15
15	8	16
16	8	17
17	8	18
18	8	19
19	1	20
20	1	21
21	1	22
22	1	23
23	1	24
24	9	25
25	9	26
26	9	27
27	9	28
28	9	29
29	2	30
30	2	31
31	2	32
32	2	33
33	2	34
34	4	35
35	4	36
36	4	37
37	4	38
38	4	39
39	5	40
40	5	41
41	5	42
42	5	43
43	5	44
44	6	45
45	6	46
46	6	47
47	6	48
48	6	49
49	12	50
50	12	51
51	12	52
52	12	53
53	12	54
54	11	55
55	11	56
56	11	57
57	11	58
58	11	59
59	14	60
60	14	61
61	14	62
62	14	63
63	14	64
64	14	65
65	15	66
66	15	67
67	15	68
68	15	69
69	15	70
70	15	71
71	16	72
72	16	73
73	16	74
74	16	75
75	16	76
76	17	77
77	17	78
78	17	79
79	17	80
80	17	81
81	16	82
82	17	83
83	18	84
84	18	88
85	18	89
86	18	85
87	18	86
88	18	87
89	19	90
90	19	91
91	19	92
92	19	93
93	19	94
94	19	95
95	1	96
96	2	97
97	20	98
98	21	99
99	22	100
100	23	101
101	24	102
102	25	103
\.


--
-- Name: cms_page_placeholders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_page_placeholders_id_seq', 102, true);


--
-- Data for Name: cms_pagepermission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_pagepermission (id, can_change, can_add, can_delete, can_change_advanced_settings, can_publish, can_change_permissions, can_move_page, can_view, grant_on, group_id, page_id, user_id) FROM stdin;
\.


--
-- Name: cms_pagepermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_pagepermission_id_seq', 1, false);


--
-- Data for Name: cms_pageuser; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_pageuser (user_ptr_id, created_by_id) FROM stdin;
\.


--
-- Data for Name: cms_pageusergroup; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_pageusergroup (group_ptr_id, created_by_id) FROM stdin;
\.


--
-- Data for Name: cms_placeholder; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_placeholder (id, slot, default_width) FROM stdin;
1	clipboard	\N
3	Content	\N
4	Content	\N
5	Content	\N
6	Content	\N
7	Content	\N
8	Content	\N
9	Content	\N
10	Content	\N
11	Content	\N
12	Content	\N
13	Content	\N
14	Content	\N
15	Left column1	\N
16	Right column	\N
17	Both columns	\N
18	Middle left	\N
19	Bottom left	\N
20	Left column1	\N
21	Right column	\N
22	Both columns	\N
23	Middle left	\N
24	Bottom left	\N
25	Left column1	\N
26	Right column	\N
27	Both columns	\N
28	Middle left	\N
29	Bottom left	\N
30	Left column1	\N
31	Right column	\N
32	Both columns	\N
33	Middle left	\N
34	Bottom left	\N
35	Left column1	\N
36	Right column	\N
37	Both columns	\N
38	Middle left	\N
39	Bottom left	\N
40	Left column1	\N
41	Right column	\N
42	Both columns	\N
43	Middle left	\N
44	Bottom left	\N
45	Left column1	\N
46	Right column	\N
47	Both columns	\N
48	Middle left	\N
49	Bottom left	\N
50	Left column1	\N
51	Right column	\N
52	Both columns	\N
53	Middle left	\N
54	Bottom left	\N
55	Left column1	\N
56	Right column	\N
57	Both columns	\N
58	Middle left	\N
59	Bottom left	\N
60	Left column1	\N
61	Right column	\N
62	Both columns	\N
63	Middle left	\N
64	Bottom left	\N
65	content	\N
66	content	\N
67	Left column1	\N
68	Right column	\N
69	Both columns	\N
70	Middle left	\N
71	Bottom left	\N
72	Left column1	\N
73	Right column	\N
74	Both columns	\N
75	Middle left	\N
76	Bottom left	\N
77	Left column1	\N
78	Right column	\N
79	Both columns	\N
80	Middle left	\N
81	Bottom left	\N
82	content	\N
83	content	\N
84	content	\N
85	Left column1	\N
86	Right column	\N
87	Both columns	\N
88	Middle left	\N
89	Bottom left	\N
90	content	\N
91	Left column1	\N
92	Right column	\N
93	Both columns	\N
94	Middle left	\N
95	Bottom left	\N
96	content	\N
97	content	\N
98	content	\N
99	content	\N
100	content	\N
101	content	\N
102	content	\N
103	content	\N
\.


--
-- Name: cms_placeholder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_placeholder_id_seq', 103, true);


--
-- Data for Name: cms_placeholderreference; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_placeholderreference (cmsplugin_ptr_id, name, placeholder_ref_id) FROM stdin;
\.


--
-- Data for Name: cms_staticplaceholder; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_staticplaceholder (id, name, code, dirty, creation_method, draft_id, public_id, site_id) FROM stdin;
\.


--
-- Name: cms_staticplaceholder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_staticplaceholder_id_seq', 1, false);


--
-- Data for Name: cms_title; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_title (id, language, title, page_title, menu_title, meta_description, slug, path, has_url_overwrite, redirect, creation_date, published, publisher_is_draft, publisher_state, page_id, publisher_public_id) FROM stdin;
10	en	Global				global	global	f		2015-06-10 16:06:04.948261+02	t	f	0	10	3
3	en	Global				global	global	f		2015-06-10 16:06:04.948261+02	t	t	0	3	10
11	en	Continent				continent	continent	f	\N	2015-06-10 16:06:19.723709+02	t	f	0	11	4
4	en	Continent				continent	continent	f	\N	2015-06-10 16:06:19.723709+02	t	t	0	4	11
12	en	Region				region	region	f	\N	2015-06-10 16:06:29.623414+02	t	f	0	12	5
5	en	Region				region	region	f	\N	2015-06-10 16:06:29.623414+02	t	t	0	5	12
13	en	Get Involved				get-involved	get-involved	f	\N	2015-06-10 16:06:44.150871+02	t	f	0	13	6
6	en	Get Involved				get-involved	get-involved	f	\N	2015-06-10 16:06:44.150871+02	t	t	0	6	13
9	en	Home				home		f		2015-06-11 15:35:20.655715+02	t	f	0	9	8
8	en	Home				home		f		2015-06-11 15:35:20.655715+02	t	t	0	8	9
15	en	Map				map	map	f		2015-09-17 14:11:54.05232+02	t	f	0	15	14
14	en	Map				map	map	f		2015-09-17 14:11:54.05232+02	t	t	0	14	15
19	en	Web of Transnational Deals				transnational	idea/transnational	f		2015-09-21 12:37:39.168423+02	t	f	0	19	17
17	en	Web of Transnational Deals				transnational	idea/transnational	f		2015-09-21 12:37:39.168423+02	t	t	0	17	19
21	en	Global Map of Investments				investments	idea/investments	f		2015-09-22 14:37:12.715071+02	t	f	0	21	20
20	en	Global Map of Investments				investments	idea/investments	f		2015-09-22 14:37:12.715071+02	t	t	0	20	21
23	en	Agricultural Drivers				agricultural	idea/agricultural	f		2015-09-22 15:58:43.904011+02	t	f	0	23	22
22	en	Agricultural Drivers				agricultural	idea/agricultural	f		2015-09-22 15:58:43.904011+02	t	t	0	22	23
25	en	It's a big deal				area	idea/area	f		2015-09-22 16:23:39.749391+02	t	f	0	25	24
24	en	It's a big deal				area	idea/area	f		2015-09-22 16:23:39.749391+02	t	t	0	24	25
2	en	Idea		Get the idea		idea	idea	f		2015-06-10 16:05:47.363732+02	t	f	0	2	1
1	en	Idea		Get the idea		idea	idea	f		2015-06-10 16:05:47.363732+02	t	t	0	1	2
18	en	Overview				overview	idea/overview	f		2015-09-21 12:36:43.160795+02	t	f	0	18	16
16	en	Overview				overview	idea/overview	f		2015-09-21 12:36:43.160795+02	t	t	0	16	18
\.


--
-- Name: cms_title_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_title_id_seq', 25, true);


--
-- Data for Name: cms_usersettings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_usersettings (id, language, clipboard_id, user_id) FROM stdin;
1	en	1	1
\.


--
-- Name: cms_usersettings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_usersettings_id_seq', 1, true);


--
-- Data for Name: djangocms_text_ckeditor_text; Type: TABLE DATA; Schema: public; Owner: -
--

COPY djangocms_text_ckeditor_text (cmsplugin_ptr_id, body) FROM stdin;
\.


--
-- Name: cms_aliaspluginmodel_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_aliaspluginmodel
    ADD CONSTRAINT cms_aliaspluginmodel_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cms_cmsplugin_path_141f52fcc960f65c_uniq; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmsplugin_path_141f52fcc960f65c_uniq UNIQUE (path);


--
-- Name: cms_cmsplugin_path_67ba0705db370bca_uniq; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmsplugin_path_67ba0705db370bca_uniq UNIQUE (path);


--
-- Name: cms_cmsplugin_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmsplugin_pkey PRIMARY KEY (id);


--
-- Name: cms_globalpagepermission_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_globalpagepermission
    ADD CONSTRAINT cms_globalpagepermission_pkey PRIMARY KEY (id);


--
-- Name: cms_globalpagepermission_site_globalpagepermission_id_site__key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_globalpagepermission_sites
    ADD CONSTRAINT cms_globalpagepermission_site_globalpagepermission_id_site__key UNIQUE (globalpagepermission_id, site_id);


--
-- Name: cms_globalpagepermission_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_globalpagepermission_sites
    ADD CONSTRAINT cms_globalpagepermission_sites_pkey PRIMARY KEY (id);


--
-- Name: cms_page_path_42dd834e2f623039_uniq; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_path_42dd834e2f623039_uniq UNIQUE (path);


--
-- Name: cms_page_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_pkey PRIMARY KEY (id);


--
-- Name: cms_page_placeholders_page_id_placeholder_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_page_placeholders
    ADD CONSTRAINT cms_page_placeholders_page_id_placeholder_id_key UNIQUE (page_id, placeholder_id);


--
-- Name: cms_page_placeholders_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_page_placeholders
    ADD CONSTRAINT cms_page_placeholders_pkey PRIMARY KEY (id);


--
-- Name: cms_page_publisher_is_draft_602b80a2c150bf8a_uniq; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_publisher_is_draft_602b80a2c150bf8a_uniq UNIQUE (publisher_is_draft, site_id, application_namespace);


--
-- Name: cms_page_publisher_public_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_publisher_public_id_key UNIQUE (publisher_public_id);


--
-- Name: cms_page_reverse_id_995f17b534f872a_uniq; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_reverse_id_995f17b534f872a_uniq UNIQUE (reverse_id, site_id, publisher_is_draft);


--
-- Name: cms_pagepermission_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_pagepermission
    ADD CONSTRAINT cms_pagepermission_pkey PRIMARY KEY (id);


--
-- Name: cms_pageuser_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_pageuser
    ADD CONSTRAINT cms_pageuser_pkey PRIMARY KEY (user_ptr_id);


--
-- Name: cms_pageusergroup_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_pageusergroup
    ADD CONSTRAINT cms_pageusergroup_pkey PRIMARY KEY (group_ptr_id);


--
-- Name: cms_placeholder_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_placeholder
    ADD CONSTRAINT cms_placeholder_pkey PRIMARY KEY (id);


--
-- Name: cms_placeholderreference_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_placeholderreference
    ADD CONSTRAINT cms_placeholderreference_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cms_staticplaceholder_code_652026c01edb1289_uniq; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplaceholder_code_652026c01edb1289_uniq UNIQUE (code, site_id);


--
-- Name: cms_staticplaceholder_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplaceholder_pkey PRIMARY KEY (id);


--
-- Name: cms_title_language_36047e46db89b4c3_uniq; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_language_36047e46db89b4c3_uniq UNIQUE (language, page_id);


--
-- Name: cms_title_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_pkey PRIMARY KEY (id);


--
-- Name: cms_title_publisher_public_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_publisher_public_id_key UNIQUE (publisher_public_id);


--
-- Name: cms_usersettings_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_usersettings
    ADD CONSTRAINT cms_usersettings_pkey PRIMARY KEY (id);


--
-- Name: cms_usersettings_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_usersettings
    ADD CONSTRAINT cms_usersettings_user_id_key UNIQUE (user_id);


--
-- Name: djangocms_text_ckeditor_text_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY djangocms_text_ckeditor_text
    ADD CONSTRAINT djangocms_text_ckeditor_text_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cms_aliaspluginmodel_921abf5c; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_aliaspluginmodel_921abf5c ON cms_aliaspluginmodel USING btree (alias_placeholder_id);


--
-- Name: cms_aliaspluginmodel_b25eaab4; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_aliaspluginmodel_b25eaab4 ON cms_aliaspluginmodel USING btree (plugin_id);


--
-- Name: cms_cmsplugin_667a6151; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_cmsplugin_667a6151 ON cms_cmsplugin USING btree (placeholder_id);


--
-- Name: cms_cmsplugin_6be37982; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_cmsplugin_6be37982 ON cms_cmsplugin USING btree (parent_id);


--
-- Name: cms_cmsplugin_8512ae7d; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_cmsplugin_8512ae7d ON cms_cmsplugin USING btree (language);


--
-- Name: cms_cmsplugin_b5e4cf8f; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_cmsplugin_b5e4cf8f ON cms_cmsplugin USING btree (plugin_type);


--
-- Name: cms_cmsplugin_language_c08bb60796a6f87_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_cmsplugin_language_c08bb60796a6f87_like ON cms_cmsplugin USING btree (language varchar_pattern_ops);


--
-- Name: cms_cmsplugin_language_d848ffd6b1e975f_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_cmsplugin_language_d848ffd6b1e975f_like ON cms_cmsplugin USING btree (language varchar_pattern_ops);


--
-- Name: cms_cmsplugin_plugin_type_2ff5635080222f80_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_cmsplugin_plugin_type_2ff5635080222f80_like ON cms_cmsplugin USING btree (plugin_type varchar_pattern_ops);


--
-- Name: cms_cmsplugin_plugin_type_4a27a6689bff9c44_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_cmsplugin_plugin_type_4a27a6689bff9c44_like ON cms_cmsplugin USING btree (plugin_type varchar_pattern_ops);


--
-- Name: cms_globalpagepermission_0e939a4f; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_globalpagepermission_0e939a4f ON cms_globalpagepermission USING btree (group_id);


--
-- Name: cms_globalpagepermission_e8701ad4; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_globalpagepermission_e8701ad4 ON cms_globalpagepermission USING btree (user_id);


--
-- Name: cms_globalpagepermission_sites_9365d6e7; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_globalpagepermission_sites_9365d6e7 ON cms_globalpagepermission_sites USING btree (site_id);


--
-- Name: cms_globalpagepermission_sites_a3d12ecd; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_globalpagepermission_sites_a3d12ecd ON cms_globalpagepermission_sites USING btree (globalpagepermission_id);


--
-- Name: cms_page_1d85575d; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_1d85575d ON cms_page USING btree (soft_root);


--
-- Name: cms_page_2247c5f0; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_2247c5f0 ON cms_page USING btree (publication_end_date);


--
-- Name: cms_page_3d9ef52f; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_3d9ef52f ON cms_page USING btree (reverse_id);


--
-- Name: cms_page_4fa1c803; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_4fa1c803 ON cms_page USING btree (is_home);


--
-- Name: cms_page_6be37982; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_6be37982 ON cms_page USING btree (parent_id);


--
-- Name: cms_page_7b8acfa6; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_7b8acfa6 ON cms_page USING btree (navigation_extenders);


--
-- Name: cms_page_9365d6e7; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_9365d6e7 ON cms_page USING btree (site_id);


--
-- Name: cms_page_93b83098; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_93b83098 ON cms_page USING btree (publication_date);


--
-- Name: cms_page_application_urls_53789416f667385e_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_application_urls_53789416f667385e_like ON cms_page USING btree (application_urls varchar_pattern_ops);


--
-- Name: cms_page_b7700099; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_b7700099 ON cms_page USING btree (publisher_is_draft);


--
-- Name: cms_page_cb540373; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_cb540373 ON cms_page USING btree (limit_visibility_in_menu);


--
-- Name: cms_page_db3eb53f; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_db3eb53f ON cms_page USING btree (in_navigation);


--
-- Name: cms_page_e721871e; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_e721871e ON cms_page USING btree (application_urls);


--
-- Name: cms_page_navigation_extenders_811061878532a9e_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_navigation_extenders_811061878532a9e_like ON cms_page USING btree (navigation_extenders varchar_pattern_ops);


--
-- Name: cms_page_placeholders_1a63c800; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_placeholders_1a63c800 ON cms_page_placeholders USING btree (page_id);


--
-- Name: cms_page_placeholders_667a6151; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_placeholders_667a6151 ON cms_page_placeholders USING btree (placeholder_id);


--
-- Name: cms_page_reverse_id_70f7094a94441bf9_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_page_reverse_id_70f7094a94441bf9_like ON cms_page USING btree (reverse_id varchar_pattern_ops);


--
-- Name: cms_pagepermission_0e939a4f; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_pagepermission_0e939a4f ON cms_pagepermission USING btree (group_id);


--
-- Name: cms_pagepermission_1a63c800; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_pagepermission_1a63c800 ON cms_pagepermission USING btree (page_id);


--
-- Name: cms_pagepermission_e8701ad4; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_pagepermission_e8701ad4 ON cms_pagepermission USING btree (user_id);


--
-- Name: cms_pageuser_e93cb7eb; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_pageuser_e93cb7eb ON cms_pageuser USING btree (created_by_id);


--
-- Name: cms_pageusergroup_e93cb7eb; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_pageusergroup_e93cb7eb ON cms_pageusergroup USING btree (created_by_id);


--
-- Name: cms_placeholder_5e97994e; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_placeholder_5e97994e ON cms_placeholder USING btree (slot);


--
-- Name: cms_placeholder_slot_3ec71fba17de961_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_placeholder_slot_3ec71fba17de961_like ON cms_placeholder USING btree (slot varchar_pattern_ops);


--
-- Name: cms_placeholder_slot_505fd670e00a4031_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_placeholder_slot_505fd670e00a4031_like ON cms_placeholder USING btree (slot varchar_pattern_ops);


--
-- Name: cms_placeholderreference_328d0afc; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_placeholderreference_328d0afc ON cms_placeholderreference USING btree (placeholder_ref_id);


--
-- Name: cms_staticplaceholder_1ee2744d; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_staticplaceholder_1ee2744d ON cms_staticplaceholder USING btree (public_id);


--
-- Name: cms_staticplaceholder_5cb48773; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_staticplaceholder_5cb48773 ON cms_staticplaceholder USING btree (draft_id);


--
-- Name: cms_staticplaceholder_9365d6e7; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_staticplaceholder_9365d6e7 ON cms_staticplaceholder USING btree (site_id);


--
-- Name: cms_title_1268de9a; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_title_1268de9a ON cms_title USING btree (has_url_overwrite);


--
-- Name: cms_title_1a63c800; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_title_1a63c800 ON cms_title USING btree (page_id);


--
-- Name: cms_title_2dbcba41; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_title_2dbcba41 ON cms_title USING btree (slug);


--
-- Name: cms_title_8512ae7d; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_title_8512ae7d ON cms_title USING btree (language);


--
-- Name: cms_title_b7700099; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_title_b7700099 ON cms_title USING btree (publisher_is_draft);


--
-- Name: cms_title_d6fe1d0b; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_title_d6fe1d0b ON cms_title USING btree (path);


--
-- Name: cms_title_f7202fc0; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_title_f7202fc0 ON cms_title USING btree (publisher_state);


--
-- Name: cms_title_language_336ae6853ef2c6ba_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_title_language_336ae6853ef2c6ba_like ON cms_title USING btree (language varchar_pattern_ops);


--
-- Name: cms_title_path_32ae1d46fa794b91_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_title_path_32ae1d46fa794b91_like ON cms_title USING btree (path varchar_pattern_ops);


--
-- Name: cms_title_slug_1cb2ca8d93f80037_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_title_slug_1cb2ca8d93f80037_like ON cms_title USING btree (slug varchar_pattern_ops);


--
-- Name: cms_usersettings_2655b062; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX cms_usersettings_2655b062 ON cms_usersettings USING btree (clipboard_id);


--
-- Name: D95650a885fa84f2f12837f15586d742; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_globalpagepermission_sites
    ADD CONSTRAINT "D95650a885fa84f2f12837f15586d742" FOREIGN KEY (globalpagepermission_id) REFERENCES cms_globalpagepermission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_alias_cmsplugin_ptr_id_7fab4de01c1233ab_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_aliaspluginmodel
    ADD CONSTRAINT cms_alias_cmsplugin_ptr_id_7fab4de01c1233ab_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_alias_placeholder_id_72aa2f8a1eefc7b9_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_aliaspluginmodel
    ADD CONSTRAINT cms_alias_placeholder_id_72aa2f8a1eefc7b9_fk_cms_placeholder_id FOREIGN KEY (alias_placeholder_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_aliaspluginmo_plugin_id_d6b763b9848949c_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_aliaspluginmodel
    ADD CONSTRAINT cms_aliaspluginmo_plugin_id_d6b763b9848949c_fk_cms_cmsplugin_id FOREIGN KEY (plugin_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_cmspl_placeholder_id_266752f6b674e50c_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmspl_placeholder_id_266752f6b674e50c_fk_cms_placeholder_id FOREIGN KEY (placeholder_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_cmspl_placeholder_id_61217ad51efd7fdb_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmspl_placeholder_id_61217ad51efd7fdb_fk_cms_placeholder_id FOREIGN KEY (placeholder_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_cmsplugin_parent_id_3bc2041e4b72452d_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmsplugin_parent_id_3bc2041e4b72452d_fk_cms_cmsplugin_id FOREIGN KEY (parent_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_cmsplugin_parent_id_6019c91b715ba839_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmsplugin_parent_id_6019c91b715ba839_fk_cms_cmsplugin_id FOREIGN KEY (parent_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_globalpagepermis_group_id_3548edf35c3031f4_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_globalpagepermission
    ADD CONSTRAINT cms_globalpagepermis_group_id_3548edf35c3031f4_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_globalpagepermis_site_id_773d87af54fab686_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_globalpagepermission_sites
    ADD CONSTRAINT cms_globalpagepermis_site_id_773d87af54fab686_fk_django_site_id FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_globalpagepermissi_user_id_1af2acd0f8938da5_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_globalpagepermission
    ADD CONSTRAINT cms_globalpagepermissi_user_id_1af2acd0f8938da5_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_p_placeholder_ref_id_66e6811bed966bf6_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_placeholderreference
    ADD CONSTRAINT cms_p_placeholder_ref_id_66e6811bed966bf6_fk_cms_placeholder_id FOREIGN KEY (placeholder_ref_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page__placeholder_id_5287666e5e8ad301_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_page_placeholders
    ADD CONSTRAINT cms_page__placeholder_id_5287666e5e8ad301_fk_cms_placeholder_id FOREIGN KEY (placeholder_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page_parent_id_67a606802cf82a88_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_parent_id_67a606802cf82a88_fk_cms_page_id FOREIGN KEY (parent_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page_placeholders_page_id_fb9517cb96c7f1b_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_page_placeholders
    ADD CONSTRAINT cms_page_placeholders_page_id_fb9517cb96c7f1b_fk_cms_page_id FOREIGN KEY (page_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page_publisher_public_id_2165b58969f3b8a1_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_publisher_public_id_2165b58969f3b8a1_fk_cms_page_id FOREIGN KEY (publisher_public_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page_site_id_773d29cc9574dafe_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_site_id_773d29cc9574dafe_fk_django_site_id FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pagepermission_group_id_3e8b5fece99e5d3e_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_pagepermission
    ADD CONSTRAINT cms_pagepermission_group_id_3e8b5fece99e5d3e_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pagepermission_page_id_4eed52d739cc312a_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_pagepermission
    ADD CONSTRAINT cms_pagepermission_page_id_4eed52d739cc312a_fk_cms_page_id FOREIGN KEY (page_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pagepermission_user_id_5ed8f0e7748d130d_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_pagepermission
    ADD CONSTRAINT cms_pagepermission_user_id_5ed8f0e7748d130d_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pageuser_created_by_id_eadbc8f0a9562b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_pageuser
    ADD CONSTRAINT cms_pageuser_created_by_id_eadbc8f0a9562b_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pageuser_user_ptr_id_5bba5ebeb8e4b6c1_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_pageuser
    ADD CONSTRAINT cms_pageuser_user_ptr_id_5bba5ebeb8e4b6c1_fk_auth_user_id FOREIGN KEY (user_ptr_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pageusergrou_created_by_id_59b8b4de51158667_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_pageusergroup
    ADD CONSTRAINT cms_pageusergrou_created_by_id_59b8b4de51158667_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pageusergrou_group_ptr_id_4b37171ee57872b4_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_pageusergroup
    ADD CONSTRAINT cms_pageusergrou_group_ptr_id_4b37171ee57872b4_fk_auth_group_id FOREIGN KEY (group_ptr_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_placeh_cmsplugin_ptr_id_dff2e641f7c2bb4_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_placeholderreference
    ADD CONSTRAINT cms_placeh_cmsplugin_ptr_id_dff2e641f7c2bb4_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_staticplac_public_id_651472a4631d7212_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplac_public_id_651472a4631d7212_fk_cms_placeholder_id FOREIGN KEY (public_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_staticplace_draft_id_7def6c9af7e4304f_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplace_draft_id_7def6c9af7e4304f_fk_cms_placeholder_id FOREIGN KEY (draft_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_staticplaceholde_site_id_269af061d2bc1d6f_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplaceholde_site_id_269af061d2bc1d6f_fk_django_site_id FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_title_page_id_5087aa7946b7b022_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_page_id_5087aa7946b7b022_fk_cms_page_id FOREIGN KEY (page_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_title_publisher_public_id_3f17c2bc1b7e4937_fk_cms_title_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_publisher_public_id_3f17c2bc1b7e4937_fk_cms_title_id FOREIGN KEY (publisher_public_id) REFERENCES cms_title(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_userset_clipboard_id_749172e7f5082f45_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_usersettings
    ADD CONSTRAINT cms_userset_clipboard_id_749172e7f5082f45_fk_cms_placeholder_id FOREIGN KEY (clipboard_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_usersettings_user_id_1c22e825455ecdf1_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_usersettings
    ADD CONSTRAINT cms_usersettings_user_id_1c22e825455ecdf1_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_1895cc8f336e8cde_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY djangocms_text_ckeditor_text
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_1895cc8f336e8cde_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

