--
-- PostgreSQL database dump
--

\restrict kg7MWrTgaivWcPtI6J8aocfjPzRIvjYs8OaRkb8Mg939hBifToNWxoiL6BRefWJ

-- Dumped from database version 18.2
-- Dumped by pg_dump version 18.2

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
-- Name: States; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."States" (
    state_id integer NOT NULL,
    state_name character varying
);


ALTER TABLE public."States" OWNER TO postgres;

--
-- Name: States_state_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."States_state_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."States_state_id_seq" OWNER TO postgres;

--
-- Name: States_state_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."States_state_id_seq" OWNED BY public."States".state_id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audit_logs (
    id integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    "user" character varying NOT NULL,
    user_role character varying,
    action character varying NOT NULL,
    module character varying NOT NULL,
    resource character varying,
    detail text,
    ip_address character varying
);


ALTER TABLE public.audit_logs OWNER TO postgres;

--
-- Name: audit_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.audit_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.audit_logs_id_seq OWNER TO postgres;

--
-- Name: audit_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.audit_logs_id_seq OWNED BY public.audit_logs.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    category_name character varying NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: contact_messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contact_messages (
    id integer NOT NULL,
    name character varying,
    email character varying,
    company character varying,
    subject character varying,
    message text,
    is_read boolean,
    created_at character varying
);


ALTER TABLE public.contact_messages OWNER TO postgres;

--
-- Name: contact_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contact_messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contact_messages_id_seq OWNER TO postgres;

--
-- Name: contact_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contact_messages_id_seq OWNED BY public.contact_messages.id;


--
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    id integer NOT NULL,
    customer_id character varying NOT NULL,
    age integer,
    gender character varying,
    income_bracket character varying,
    purchase_frequency integer,
    average_spend double precision,
    preferred_categories character varying,
    last_purchase_date date,
    total_spend double precision,
    clv double precision,
    csat double precision,
    nps integer
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- Name: customers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customers_id_seq OWNER TO postgres;

--
-- Name: customers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customers_id_seq OWNED BY public.customers.id;


--
-- Name: inventory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.inventory (
    id integer NOT NULL,
    site_id character varying NOT NULL,
    product_id character varying NOT NULL,
    beginning_inventory integer,
    ending_inventory integer,
    replenishment integer,
    stockout_flag character varying
);


ALTER TABLE public.inventory OWNER TO postgres;

--
-- Name: inventory_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.inventory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.inventory_id_seq OWNER TO postgres;

--
-- Name: inventory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.inventory_id_seq OWNED BY public.inventory.id;


--
-- Name: logistics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logistics (
    id integer NOT NULL,
    shipment_id character varying NOT NULL,
    site_id character varying,
    product_id character varying,
    shipment_date date,
    quantity integer,
    delivery_status character varying,
    transportation_type character varying,
    delivery_date character varying,
    so_id integer,
    so_number character varying(50),
    estimated_delivery date,
    tracking_status_updated timestamp without time zone,
    tracking_notes text
);


ALTER TABLE public.logistics OWNER TO postgres;

--
-- Name: logistics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.logistics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.logistics_id_seq OWNER TO postgres;

--
-- Name: logistics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.logistics_id_seq OWNED BY public.logistics.id;


--
-- Name: managers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.managers (
    id integer NOT NULL,
    user_id integer NOT NULL,
    site_id character varying
);


ALTER TABLE public.managers OWNER TO postgres;

--
-- Name: managers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.managers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.managers_id_seq OWNER TO postgres;

--
-- Name: managers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.managers_id_seq OWNED BY public.managers.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer NOT NULL,
    product_id character varying NOT NULL,
    product_name character varying,
    category character varying,
    subcategory character varying,
    unit_cost double precision,
    unit_price double precision,
    supplier character varying,
    shelf_life integer,
    uom character varying(30) DEFAULT 'Unit'::character varying,
    reorder_point integer DEFAULT 0,
    reorder_qty integer DEFAULT 0,
    default_warehouse character varying(20),
    status character varying(20) DEFAULT 'Active'::character varying,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: promotions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.promotions (
    id integer NOT NULL,
    promotion_id character varying NOT NULL,
    product_id character varying,
    site_id character varying,
    start_date date,
    end_date date,
    discount_type character varying,
    discount_amount double precision
);


ALTER TABLE public.promotions OWNER TO postgres;

--
-- Name: promotions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.promotions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.promotions_id_seq OWNER TO postgres;

--
-- Name: promotions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.promotions_id_seq OWNED BY public.promotions.id;


--
-- Name: purchase_orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.purchase_orders (
    id integer NOT NULL,
    po_number character varying NOT NULL,
    supplier character varying,
    product_name character varying,
    product_id character varying,
    quantity integer,
    unit_cost double precision,
    total_cost double precision,
    status character varying,
    site character varying,
    expected_delivery character varying,
    created_at character varying,
    created_by character varying,
    approved_at character varying,
    role character varying,
    manager_user_id integer,
    notes text DEFAULT ''::text,
    rejection_reason text DEFAULT ''::text,
    received_at character varying(20) DEFAULT ''::character varying,
    cancelled_at character varying(20) DEFAULT ''::character varying,
    cancel_reason text DEFAULT ''::text,
    supplier_id integer,
    supplier_approval_token character varying(128),
    supplier_token_expiry timestamp without time zone,
    supplier_action character varying(20),
    supplier_actioned_at timestamp without time zone,
    supplier_reject_reason text,
    approved_by character varying(100) DEFAULT ''::character varying
);


ALTER TABLE public.purchase_orders OWNER TO postgres;

--
-- Name: purchase_orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.purchase_orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.purchase_orders_id_seq OWNER TO postgres;

--
-- Name: purchase_orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.purchase_orders_id_seq OWNED BY public.purchase_orders.id;


--
-- Name: purchase_returns; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.purchase_returns (
    id integer NOT NULL,
    return_number character varying(50) NOT NULL,
    po_number character varying(50) NOT NULL,
    supplier character varying(150),
    site character varying(50),
    return_reason text,
    product_name character varying(200),
    product_id character varying(50),
    quantity integer,
    unit_cost double precision,
    total_credit double precision,
    status character varying(30),
    notes text,
    created_at character varying(20),
    created_by character varying(80),
    approved_at character varying(20),
    approved_by character varying(80),
    role character varying(20),
    manager_user_id integer
);


ALTER TABLE public.purchase_returns OWNER TO postgres;

--
-- Name: purchase_returns_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.purchase_returns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.purchase_returns_id_seq OWNER TO postgres;

--
-- Name: purchase_returns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.purchase_returns_id_seq OWNED BY public.purchase_returns.id;


--
-- Name: sales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sales (
    id integer NOT NULL,
    date date,
    site_id character varying,
    product_id character varying,
    units_sold integer,
    revenue double precision,
    discounts double precision,
    returns integer,
    customer_id character varying
);


ALTER TABLE public.sales OWNER TO postgres;

--
-- Name: sales_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sales_id_seq OWNER TO postgres;

--
-- Name: sales_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sales_id_seq OWNED BY public.sales.id;


--
-- Name: sales_orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sales_orders (
    id integer NOT NULL,
    so_number character varying NOT NULL,
    customer character varying,
    state character varying,
    site character varying,
    items_json text,
    total_amount double precision,
    status character varying,
    dispatch_type character varying,
    created_at character varying,
    created_by character varying,
    confirmed_at character varying,
    dispatched_at character varying,
    role character varying,
    manager_user_id integer,
    customer_id character varying(50) DEFAULT ''::character varying,
    customer_email character varying(120) DEFAULT ''::character varying,
    notes text DEFAULT ''::text,
    cancelled_at character varying(20) DEFAULT ''::character varying,
    cancel_reason text DEFAULT ''::text
);


ALTER TABLE public.sales_orders OWNER TO postgres;

--
-- Name: sales_orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sales_orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sales_orders_id_seq OWNER TO postgres;

--
-- Name: sales_orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sales_orders_id_seq OWNED BY public.sales_orders.id;


--
-- Name: sales_returns; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sales_returns (
    id integer NOT NULL,
    return_number character varying(50) NOT NULL,
    so_number character varying(50) NOT NULL,
    customer character varying(150),
    site character varying(50),
    return_reason text,
    items_json text,
    total_refund double precision,
    status character varying(30),
    notes text,
    created_at character varying(20),
    created_by character varying(80),
    approved_at character varying(20),
    approved_by character varying(80),
    role character varying(20),
    manager_user_id integer
);


ALTER TABLE public.sales_returns OWNER TO postgres;

--
-- Name: sales_returns_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sales_returns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sales_returns_id_seq OWNER TO postgres;

--
-- Name: sales_returns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sales_returns_id_seq OWNED BY public.sales_returns.id;


--
-- Name: seasonal_planning; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seasonal_planning (
    id integer NOT NULL,
    month character varying,
    site_id character varying,
    product_category character varying,
    forecasted_sales double precision,
    actual_sales double precision,
    seasonal_adjustments double precision
);


ALTER TABLE public.seasonal_planning OWNER TO postgres;

--
-- Name: seasonal_planning_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seasonal_planning_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seasonal_planning_id_seq OWNER TO postgres;

--
-- Name: seasonal_planning_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.seasonal_planning_id_seq OWNED BY public.seasonal_planning.id;


--
-- Name: sites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sites (
    id integer NOT NULL,
    site_id character varying NOT NULL,
    site_name character varying,
    site_format character varying,
    region character varying,
    city character varying,
    state_id integer,
    store_size integer,
    open_date date,
    status character varying
);


ALTER TABLE public.sites OWNER TO postgres;

--
-- Name: sites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sites_id_seq OWNER TO postgres;

--
-- Name: sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sites_id_seq OWNED BY public.sites.id;


--
-- Name: stock_levels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stock_levels (
    id integer NOT NULL,
    site_id character varying(20) NOT NULL,
    product_id character varying(50) NOT NULL,
    qty_on_hand integer NOT NULL,
    reorder_point integer,
    updated_at timestamp without time zone
);


ALTER TABLE public.stock_levels OWNER TO postgres;

--
-- Name: stock_levels_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stock_levels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stock_levels_id_seq OWNER TO postgres;

--
-- Name: stock_levels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stock_levels_id_seq OWNED BY public.stock_levels.id;


--
-- Name: stock_movements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stock_movements (
    id integer NOT NULL,
    site_id character varying(20) NOT NULL,
    product_id character varying(50) NOT NULL,
    movement_type character varying(30) NOT NULL,
    qty_change integer NOT NULL,
    reference_id character varying(50),
    remarks text,
    created_by integer,
    created_at timestamp without time zone
);


ALTER TABLE public.stock_movements OWNER TO postgres;

--
-- Name: stock_movements_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stock_movements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stock_movements_id_seq OWNER TO postgres;

--
-- Name: stock_movements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stock_movements_id_seq OWNED BY public.stock_movements.id;


--
-- Name: subcategories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subcategories (
    id integer NOT NULL,
    category_id integer NOT NULL,
    subcategory_name character varying NOT NULL
);


ALTER TABLE public.subcategories OWNER TO postgres;

--
-- Name: subcategories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subcategories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subcategories_id_seq OWNER TO postgres;

--
-- Name: subcategories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subcategories_id_seq OWNED BY public.subcategories.id;


--
-- Name: suppliers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.suppliers (
    id integer NOT NULL,
    supplier_id character varying NOT NULL,
    supplier_name character varying NOT NULL,
    email character varying,
    phone character varying,
    address text,
    contact_person character varying(150),
    category character varying(100),
    status character varying(20) DEFAULT 'Active'::character varying,
    notes text,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.suppliers OWNER TO postgres;

--
-- Name: suppliers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.suppliers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.suppliers_id_seq OWNER TO postgres;

--
-- Name: suppliers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.suppliers_id_seq OWNED BY public.suppliers.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(100),
    email character varying(120),
    password character varying(255),
    role character varying(20),
    is_first_login boolean,
    is_active boolean DEFAULT true NOT NULL,
    phone character varying(20),
    department character varying(100),
    employee_id character varying(50),
    photo_url character varying(500),
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: States state_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."States" ALTER COLUMN state_id SET DEFAULT nextval('public."States_state_id_seq"'::regclass);


--
-- Name: audit_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_logs ALTER COLUMN id SET DEFAULT nextval('public.audit_logs_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: contact_messages id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contact_messages ALTER COLUMN id SET DEFAULT nextval('public.contact_messages_id_seq'::regclass);


--
-- Name: customers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_id_seq'::regclass);


--
-- Name: inventory id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventory ALTER COLUMN id SET DEFAULT nextval('public.inventory_id_seq'::regclass);


--
-- Name: logistics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logistics ALTER COLUMN id SET DEFAULT nextval('public.logistics_id_seq'::regclass);


--
-- Name: managers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.managers ALTER COLUMN id SET DEFAULT nextval('public.managers_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: promotions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promotions ALTER COLUMN id SET DEFAULT nextval('public.promotions_id_seq'::regclass);


--
-- Name: purchase_orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_orders ALTER COLUMN id SET DEFAULT nextval('public.purchase_orders_id_seq'::regclass);


--
-- Name: purchase_returns id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_returns ALTER COLUMN id SET DEFAULT nextval('public.purchase_returns_id_seq'::regclass);


--
-- Name: sales id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales ALTER COLUMN id SET DEFAULT nextval('public.sales_id_seq'::regclass);


--
-- Name: sales_orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales_orders ALTER COLUMN id SET DEFAULT nextval('public.sales_orders_id_seq'::regclass);


--
-- Name: sales_returns id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales_returns ALTER COLUMN id SET DEFAULT nextval('public.sales_returns_id_seq'::regclass);


--
-- Name: seasonal_planning id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seasonal_planning ALTER COLUMN id SET DEFAULT nextval('public.seasonal_planning_id_seq'::regclass);


--
-- Name: sites id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sites ALTER COLUMN id SET DEFAULT nextval('public.sites_id_seq'::regclass);


--
-- Name: stock_levels id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_levels ALTER COLUMN id SET DEFAULT nextval('public.stock_levels_id_seq'::regclass);


--
-- Name: stock_movements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_movements ALTER COLUMN id SET DEFAULT nextval('public.stock_movements_id_seq'::regclass);


--
-- Name: subcategories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subcategories ALTER COLUMN id SET DEFAULT nextval('public.subcategories_id_seq'::regclass);


--
-- Name: suppliers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers ALTER COLUMN id SET DEFAULT nextval('public.suppliers_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: States; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."States" (state_id, state_name) FROM stdin;
1	Maharashtra
2	Gujarat
3	Tamil Nadu
4	Delhi
5	Karnataka
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
75aabbde05e5
\.


--
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audit_logs (id, "timestamp", "user", user_role, action, module, resource, detail, ip_address) FROM stdin;
1	2026-04-30 13:14:06.044036	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
2	2026-04-30 13:17:17.187374	Admin	admin	CREATE	Purchase Orders	PO PO-YFXG25	Supplier: Supplier 3, Qty: 100	127.0.0.1
3	2026-04-30 13:17:22.603504	Admin	admin	UPDATE	Purchase Orders	PO PO-YFXG25	Approved, inventory +100	127.0.0.1
4	2026-04-30 13:18:19.217145	Admin	admin	CREATE	Sales Orders	SO SO-10001	Customer: CUST200003, Total: 498.11	127.0.0.1
5	2026-04-30 13:18:21.221456	Admin	admin	UPDATE	Sales Orders	SO SO-10001	Status → Confirmed, inventory decremented	127.0.0.1
6	2026-04-30 13:18:29.037772	Admin	admin	UPDATE	Sales Orders	SO SO-10001	Dispatched via Truck	127.0.0.1
7	2026-04-30 15:28:36.856948	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
8	2026-05-02 05:03:32.152316	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
9	2026-05-02 05:06:28.237636	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
10	2026-05-02 05:06:37.702336	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
11	2026-05-02 05:06:47.498007	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
12	2026-05-02 05:06:59.630925	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
13	2026-05-02 05:13:31.415914	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
14	2026-05-02 05:13:41.024516	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
15	2026-05-02 06:06:18.799901	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
16	2026-05-02 06:23:48.740966	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
17	2026-05-02 14:41:30.607692	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
18	2026-05-03 06:20:11.88003	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
19	2026-05-03 06:29:19.78783	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
20	2026-05-03 06:48:49.856872	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
21	2026-05-03 06:49:00.096742	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
22	2026-05-04 04:35:46.196205	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
23	2026-05-04 05:28:38.61428	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
24	2026-05-04 05:28:49.716781	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
25	2026-05-04 05:38:07.70651	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
26	2026-05-04 05:38:16.662858	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
27	2026-05-04 05:42:55.751511	Admin	admin	CREATE	Purchase Orders	PO PO-0ZR6SC	Supplier: Supplier 1, Qty: 45	127.0.0.1
28	2026-05-04 05:43:00.604662	Admin	admin	UPDATE	Purchase Orders	PO PO-0ZR6SC	Approved, inventory +45	127.0.0.1
29	2026-05-04 05:47:23.562451	Admin	admin	CREATE	Sales Orders	SO SO-10002	Customer: CUST200000, Total: 270306.30	127.0.0.1
30	2026-05-04 05:47:33.793452	Admin	admin	UPDATE	Sales Orders	SO SO-10002	Status → Cancelled	127.0.0.1
31	2026-05-04 09:24:34.165559	Admin	admin	UPDATE	Shipments	Shipment SHP-J5M6T3RN	Status: Dispatched → Delivered	127.0.0.1
32	2026-05-04 09:25:04.069184	Admin	admin	UPDATE	Shipments	Shipment SHP-UDOVQQNB	Status: In Transit → Delivered	127.0.0.1
33	2026-05-04 09:25:14.974615	Admin	admin	UPDATE	Shipments	Shipment SHP-MIN6JNAG	Status: In Transit → Out for Delivery	127.0.0.1
34	2026-05-04 09:55:37.153385	Admin	admin	CREATE	Sales Orders	SO SO-10003	Customer: CUST200000, Total: 25867.20	127.0.0.1
35	2026-05-04 09:55:42.677261	Admin	admin	UPDATE	Sales Orders	SO SO-10003	Status → Confirmed, inventory decremented	127.0.0.1
36	2026-05-04 09:55:46.775609	Admin	admin	UPDATE	Sales Orders	SO SO-10003	Dispatched via Train	127.0.0.1
37	2026-05-04 09:56:29.348983	Admin	admin	CREATE	Sales Orders	SO SO-10004	Customer: CUST200001, Total: 72305.64	127.0.0.1
38	2026-05-04 09:56:38.701825	Admin	admin	UPDATE	Sales Orders	SO SO-10004	Status → Cancelled	127.0.0.1
39	2026-05-04 13:12:05.438961	Admin	admin	CREATE	Users	User Arjun	Role: analyst, Email: nanisudheer4555@gmail.com	127.0.0.1
40	2026-05-04 13:12:17.805379	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
41	2026-05-04 13:12:23.968275	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
42	2026-05-05 01:07:07.61296	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
43	2026-05-05 01:09:57.351197	Admin	admin	UPDATE	Shipments	Shipment SHP90142	Status: Cancelled → Delivered	127.0.0.1
44	2026-05-05 01:11:19.506114	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
45	2026-05-05 01:14:21.335161	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
46	2026-05-05 01:27:46.779511	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
47	2026-05-05 01:29:42.38884	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
48	2026-05-05 01:30:00.62423	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
49	2026-05-05 02:37:37.792272	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
50	2026-05-05 02:38:46.793407	Admin	admin	UPDATE	Shipments	Shipment SHP-I98W3ITO	Status: Dispatched → Delivered	127.0.0.1
51	2026-05-05 02:39:41.058564	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
52	2026-05-05 02:39:55.869032	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
53	2026-05-05 02:52:25.560059	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
54	2026-05-05 02:52:32.377101	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
55	2026-05-05 02:57:13.702966	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
56	2026-05-05 02:57:37.295101	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
57	2026-05-05 02:57:46.599976	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
58	2026-05-05 02:58:36.370657	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
59	2026-05-05 02:59:25.193657	Admin	admin	UPDATE	Shipments	Shipment SHP-MIN6JNAG	Status: Out for Delivery → Delivered	127.0.0.1
60	2026-05-05 03:00:01.589999	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
61	2026-05-05 03:00:24.354519	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
62	2026-05-05 03:02:09.082861	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
63	2026-05-05 03:02:22.797031	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
64	2026-05-05 04:38:33.026336	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
65	2026-05-05 04:39:56.847336	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
66	2026-05-05 04:40:12.55668	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
67	2026-05-05 04:40:55.493938	Admin	admin	CREATE	Users	User Miller	Role: manager, Email: 31msdhoni@gmail.com	127.0.0.1
68	2026-05-05 04:41:09.967676	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
69	2026-05-05 04:41:28.121137	Miller	manager	LOGIN	Auth	User Miller	Role: manager	127.0.0.1
70	2026-05-05 04:50:13.300457	Miller	manager	LOGOUT	Auth	User Miller	Logged out	127.0.0.1
71	2026-05-05 04:50:34.128462	Miller	manager	LOGIN	Auth	User Miller	Role: manager	127.0.0.1
149	2026-05-06 05:21:08.046963	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
72	2026-05-05 05:28:09.523852	Miller	manager	LOGOUT	Auth	User Miller	Logged out	127.0.0.1
73	2026-05-05 05:28:20.533689	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
74	2026-05-05 05:30:55.996247	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
75	2026-05-05 05:31:10.567413	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
77	2026-05-05 05:34:12.306063	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
76	2026-05-05 05:33:52.115122	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
78	2026-05-05 05:50:34.923636	Admin	admin	DELETE	Suppliers	Supplier Supplier 9	ID: 9	127.0.0.1
79	2026-05-05 05:50:41.569659	Admin	admin	DELETE	Suppliers	Supplier Supplier 2	ID: 4	127.0.0.1
80	2026-05-05 05:50:45.712863	Admin	admin	DELETE	Suppliers	Supplier Supplier 3	ID: 6	127.0.0.1
81	2026-05-05 05:50:48.83638	Admin	admin	DELETE	Suppliers	Supplier Supplier 5	ID: 7	127.0.0.1
82	2026-05-05 05:51:01.329161	Admin	admin	DELETE	Suppliers	Supplier Supplier 4	ID: 2	127.0.0.1
83	2026-05-05 05:51:04.248844	Admin	admin	DELETE	Suppliers	Supplier Supplier 6	ID: 10	127.0.0.1
84	2026-05-05 05:51:07.221479	Admin	admin	DELETE	Suppliers	Supplier Supplier 7	ID: 8	127.0.0.1
85	2026-05-05 08:48:36.467592	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
86	2026-05-05 09:05:59.643891	Admin	admin	CREATE	Sales Orders	SO SO-10005	Customer: CUST200000, Total: 5472.90	127.0.0.1
87	2026-05-05 09:06:05.737628	Admin	admin	UPDATE	Sales Orders	SO SO-10005	Status → Confirmed, inventory decremented	127.0.0.1
88	2026-05-05 09:06:11.363259	Admin	admin	UPDATE	Sales Orders	SO SO-10005	Dispatched via Truck	127.0.0.1
89	2026-05-05 10:02:46.831142	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
90	2026-05-05 10:04:43.648714	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
91	2026-05-05 10:22:33.867016	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
92	2026-05-05 10:22:47.542536	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
93	2026-05-05 10:40:51.334589	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
94	2026-05-05 10:40:58.140691	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
95	2026-05-05 11:26:22.37605	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
96	2026-05-05 11:26:50.722419	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
97	2026-05-05 11:27:08.710896	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
98	2026-05-05 11:27:50.742481	Ishan	manager	CREATE	Purchase Orders	PO PO-N78EYL	Product: PRD10015, Qty: 45, Site: OTOH - Digital Ahmedabad	127.0.0.1
99	2026-05-05 11:28:16.058517	Ishan	manager	UPDATE	Purchase Orders	PO PO-N78EYL	Approved, inventory +45	127.0.0.1
100	2026-05-05 11:30:12.361548	Ishan	manager	CREATE	Sales Orders	SO SO-9X2URJ	Product: PRD10016, Qty: 50, Site: M5K8 - Digital Surat	127.0.0.1
101	2026-05-05 11:30:16.656257	Ishan	manager	UPDATE	Sales Orders	SO SO-9X2URJ	Confirmed, logistics created, inventory decremented	127.0.0.1
102	2026-05-05 11:52:50.430757	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
103	2026-05-05 11:52:55.492589	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
104	2026-05-05 12:27:19.342176	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
105	2026-05-05 12:27:25.458439	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
106	2026-05-05 16:44:06.040432	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
107	2026-05-05 16:55:11.39901	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
108	2026-05-05 16:55:41.603429	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
109	2026-05-05 16:57:55.309392	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
110	2026-05-05 16:58:03.367027	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
111	2026-05-05 16:58:16.265445	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
112	2026-05-05 16:58:29.800492	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
113	2026-05-05 16:58:47.445621	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
114	2026-05-05 17:01:47.82804	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
115	2026-05-05 17:02:14.509303	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
116	2026-05-05 17:02:34.242159	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
117	2026-05-05 17:07:47.919848	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
118	2026-05-05 17:07:56.200209	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
119	2026-05-05 17:10:54.021034	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
120	2026-05-05 17:11:08.659452	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
121	2026-05-05 17:31:14.02905	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
122	2026-05-05 17:31:30.776006	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
123	2026-05-06 02:47:15.533852	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
124	2026-05-06 02:47:33.055382	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
125	2026-05-06 02:47:43.123171	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
126	2026-05-06 03:17:54.185867	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
127	2026-05-06 03:18:29.310214	Admin	admin	UPDATE	Shipments	Shipment SHP-4DS7F19M	Status: Dispatched → Cancelled	127.0.0.1
128	2026-05-06 03:19:04.520754	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
129	2026-05-06 03:19:11.038209	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
130	2026-05-06 04:42:52.03063	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
131	2026-05-06 05:01:34.494657	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
132	2026-05-06 05:01:57.675531	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
133	2026-05-06 05:02:28.364562	Admin	admin	UPDATE	Shipments	Shipment SHP-24QXZGTL	Status: Dispatched → Out for Delivery	127.0.0.1
134	2026-05-06 05:02:39.664975	Admin	admin	UPDATE	Shipments	Shipment SHP-24QXZGTL	Status: Out for Delivery → In Transit	127.0.0.1
135	2026-05-06 05:02:48.243751	Admin	admin	UPDATE	Shipments	Shipment SHP-24QXZGTL	Status: In Transit → Out for Delivery	127.0.0.1
136	2026-05-06 05:02:54.922229	Admin	admin	UPDATE	Shipments	Shipment SHP-24QXZGTL	Status: Out for Delivery → Delivered	127.0.0.1
137	2026-05-06 05:03:46.029964	Admin	admin	CREATE	Sales Orders	SO SO-10007	Customer: CUST200002, Total: 10777.00	127.0.0.1
138	2026-05-06 05:03:47.499258	Admin	admin	UPDATE	Sales Orders	SO SO-10007	Status → Confirmed, inventory decremented	127.0.0.1
139	2026-05-06 05:03:49.266544	Admin	admin	UPDATE	Sales Orders	SO SO-10007	Dispatched via Air	127.0.0.1
140	2026-05-06 05:05:09.092426	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
141	2026-05-06 05:05:47.270354	Miller	manager	LOGIN	Auth	User Miller	Role: manager	127.0.0.1
142	2026-05-06 05:06:33.875255	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
143	2026-05-06 05:06:38.446769	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
144	2026-05-06 05:06:53.29731	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
145	2026-05-06 05:18:17.630645	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
146	2026-05-06 05:18:19.961418	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
147	2026-05-06 05:20:21.320499	Admin	admin	CREATE	Purchase Orders	PO PO-N9V7CD	Supplier: Arjun, Qty: 24	127.0.0.1
148	2026-05-06 05:20:22.684156	Admin	admin	UPDATE	Purchase Orders	PO PO-N9V7CD	Approved, inventory +24	127.0.0.1
150	2026-05-06 05:21:13.139081	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
152	2026-05-06 05:46:06.109161	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
151	2026-05-06 05:45:58.826563	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
153	2026-05-06 06:07:46.153483	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
154	2026-05-06 06:09:44.124627	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
155	2026-05-06 06:10:18.930062	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
156	2026-05-06 08:49:04.219866	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
157	2026-05-06 08:50:33.906788	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
158	2026-05-06 08:52:42.229511	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
159	2026-05-06 10:24:33.571513	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
160	2026-05-06 10:24:49.005288	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
161	2026-05-06 10:24:57.007918	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
162	2026-05-06 10:29:35.296884	Ishan	manager	CREATE	Sales Orders	SO SO-J7W9VZ	Product: PRD10013, Qty: 120	127.0.0.1
163	2026-05-06 10:29:42.142785	Ishan	manager	UPDATE	Sales Orders	SO SO-J7W9VZ	Status → Cancelled	127.0.0.1
164	2026-05-06 10:36:52.792648	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
165	2026-05-06 10:37:02.152539	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
166	2026-05-06 10:41:26.815622	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
167	2026-05-06 10:41:39.608993	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
168	2026-05-07 01:54:06.480225	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
169	2026-05-07 01:56:07.990395	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
170	2026-05-07 01:56:14.375304	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
171	2026-05-07 01:56:56.141518	Ishan	manager	CREATE	Sales Orders	SO SO-0F9E40	Product: PRD10015, Qty: 10	127.0.0.1
172	2026-05-07 01:58:04.875312	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
173	2026-05-07 01:58:39.821086	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
174	2026-05-07 02:03:07.020339	Arjun	analyst	LOGOUT	Auth	User Arjun		127.0.0.1
175	2026-05-07 02:03:18.275326	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
176	2026-05-07 02:04:45.747149	Admin	admin	LOGOUT	Auth	User Admin		127.0.0.1
177	2026-05-07 02:04:53.548176	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
178	2026-05-07 02:08:41.143543	Ishan	manager	UPDATE	Sales Orders	SO SO-0F9E40	Confirmed by Ishan. Shipments: 1	127.0.0.1
179	2026-05-07 02:08:43.567197	Ishan	manager	UPDATE	Sales Orders	SO SO-0F9E40	Dispatched via Truck	127.0.0.1
180	2026-05-07 02:08:52.314871	Ishan	manager	UPDATE	Sales Orders	SO SO-9X2URJ	Dispatched via Truck	127.0.0.1
181	2026-05-07 02:09:31.161484	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
182	2026-05-07 02:09:39.314082	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
183	2026-05-07 02:10:08.836596	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
184	2026-05-07 02:10:15.341126	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
185	2026-05-07 05:17:03.023985	Ishan	manager	CREATE_SALES_ORDER	Sales Orders	SO SO-W7LGQP	Items: 1, Total: 6812.4, Site: OTOH	127.0.0.1
186	2026-05-07 05:17:06.700556	Ishan	manager	UPDATE	Sales Orders	SO SO-W7LGQP	Confirmed by Ishan. Shipments: 1	127.0.0.1
187	2026-05-07 05:17:08.623706	Ishan	manager	UPDATE	Sales Orders	SO SO-W7LGQP	Dispatched via Truck	127.0.0.1
188	2026-05-07 05:19:09.832908	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
189	2026-05-07 05:19:17.557295	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
190	2026-05-07 05:19:43.641991	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
191	2026-05-07 05:19:50.64566	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
192	2026-05-07 05:27:41.975041	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
193	2026-05-07 05:27:51.26157	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
194	2026-05-07 05:29:58.094994	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
195	2026-05-07 05:30:05.700419	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
196	2026-05-07 06:18:45.81603	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
197	2026-05-07 06:18:57.067484	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
198	2026-05-07 06:19:29.81249	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
199	2026-05-07 06:21:42.240066	Ishan	manager	CREATE	Purchase Orders	PO PO-2R6YVP	Product: PRD10010, Qty: 139	127.0.0.1
200	2026-05-07 06:21:48.290653	Ishan	manager	UPDATE	Purchase Orders	PO PO-2R6YVP	Approved, inventory +139	127.0.0.1
201	2026-05-07 06:22:19.103671	Ishan	manager	CREATE_SALES_ORDER	Sales Orders	SO SO-CXYKY9	Items: 1, Total: 6466.2, Site: OTOH	127.0.0.1
202	2026-05-07 06:22:22.897253	Ishan	manager	UPDATE	Sales Orders	SO SO-CXYKY9	Confirmed by Ishan. Shipments: 1	127.0.0.1
203	2026-05-07 06:22:28.052863	Ishan	manager	UPDATE	Sales Orders	SO SO-CXYKY9	Dispatched via Truck	127.0.0.1
204	2026-05-07 08:43:12.693742	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
205	2026-05-07 08:46:30.215951	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
206	2026-05-07 08:57:25.881996	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
207	2026-05-07 09:01:50.932182	Admin	admin	CREATE_USER	Users	User maru	Role: manager, Email: flubuds32@gmail.com, EmpID: EMP1005	127.0.0.1
208	2026-05-07 09:13:53.288144	Admin	admin	CREATE	Purchase Orders	PO PO-WXJA1K	Supplier: Kishan, Qty: 45	127.0.0.1
209	2026-05-07 09:14:42.928761	Admin	admin	UPDATE	Purchase Orders	PO PO-WXJA1K	Approved, inventory +45	127.0.0.1
210	2026-05-07 09:17:39.949972	Admin	admin	CREATE	Sales Orders	SO SO-10012	Customer: CUST200002, Total: 729.90	127.0.0.1
211	2026-05-07 09:17:46.000178	Admin	admin	UPDATE	Sales Orders	SO SO-10012	Status → Confirmed, inventory decremented	127.0.0.1
212	2026-05-07 09:17:48.279227	Admin	admin	UPDATE	Sales Orders	SO SO-10012	Dispatched via Truck	127.0.0.1
213	2026-05-07 09:20:11.36969	Admin	admin	CREATE	Sales Orders	SO SO-10013	Customer: CUST200001, Total: 5656.32	127.0.0.1
214	2026-05-07 09:20:13.900003	Admin	admin	UPDATE	Sales Orders	SO SO-10013	Status → Confirmed, inventory decremented	127.0.0.1
215	2026-05-07 09:20:27.029229	Admin	admin	UPDATE	Sales Orders	SO SO-10013	Dispatched via Truck	127.0.0.1
216	2026-05-07 09:21:32.192246	Admin	admin	UPDATE	Shipments	Shipment SHP-FITWG6EP	Status: Dispatched → Delivered	127.0.0.1
217	2026-05-07 09:21:42.135268	Admin	admin	UPDATE	Shipments	Shipment SHP-7MRM2RVW	Status: Dispatched → Delivered	127.0.0.1
218	2026-05-07 09:21:59.397423	Admin	admin	UPDATE	Shipments	Shipment SHP-IZGEUETZ	Status: Dispatched → Delivered	127.0.0.1
219	2026-05-07 09:23:30.913606	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
220	2026-05-07 09:24:10.409441	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
221	2026-05-07 09:24:18.136356	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
222	2026-05-07 09:24:27.779562	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
223	2026-05-07 09:35:24.800314	Ishan	manager	CREATE	Purchase Orders	PO PO-HBLHHU	Product: PRD10014, Qty: 45	127.0.0.1
224	2026-05-07 09:35:29.488267	Ishan	manager	UPDATE	Purchase Orders	PO PO-HBLHHU	Approved, inventory +45	127.0.0.1
225	2026-05-07 10:53:11.325806	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
226	2026-05-07 11:18:26.597831	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
227	2026-05-07 11:18:31.426987	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
228	2026-05-07 11:18:34.073568	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
229	2026-05-07 11:18:39.290378	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
230	2026-05-07 11:18:47.527668	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
231	2026-05-07 15:55:39.359229	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
232	2026-05-07 15:58:54.643645	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
233	2026-05-07 16:03:05.830324	Admin	admin	DELETE	Users	User maru	Email: flubuds32@gmail.com, Role: manager	127.0.0.1
234	2026-05-07 17:12:45.260576	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
235	2026-05-07 17:32:21.505475	Admin	admin	CREATE	Sales Orders	SO SO-10014	Customer: CUST200001, Total: 121.62	127.0.0.1
236	2026-05-07 17:32:29.478647	Admin	admin	UPDATE	Sales Orders	SO SO-10014	Status → Confirmed, inventory decremented	127.0.0.1
237	2026-05-07 17:32:46.629591	Admin	admin	UPDATE	Sales Orders	SO SO-10014	Dispatched via Air	127.0.0.1
238	2026-05-07 17:37:38.218641	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
239	2026-05-07 17:37:44.254914	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
240	2026-05-07 17:45:58.545176	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
241	2026-05-07 17:46:04.672569	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
242	2026-05-07 17:47:56.953214	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
243	2026-05-07 17:48:01.609369	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
244	2026-05-07 17:48:48.966282	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
245	2026-05-08 02:28:44.148082	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
246	2026-05-08 02:30:15.298185	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
247	2026-05-08 02:30:23.126812	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
248	2026-05-08 02:31:54.324769	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
249	2026-05-08 02:32:00.920535	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
250	2026-05-08 02:52:14.875359	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
251	2026-05-08 03:11:48.370343	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
252	2026-05-08 03:11:54.612667	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
253	2026-05-08 03:12:22.530726	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
254	2026-05-08 03:12:27.044802	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
255	2026-05-08 04:43:06.518801	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
256	2026-05-08 04:48:49.214042	Admin	admin	CREATE_USER	Users	User Arjun	Role: manager, Email: ganeshgani5110@gmail.com, EmpID: EMP1005	127.0.0.1
257	2026-05-08 04:58:52.113811	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
258	2026-05-08 05:16:55.441074	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
259	2026-05-08 05:17:01.849293	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
260	2026-05-08 05:17:05.418358	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
261	2026-05-08 05:17:21.460001	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
262	2026-05-08 05:18:18.264533	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
263	2026-05-08 05:18:26.778874	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
264	2026-05-08 05:23:58.587705	Admin	admin	UPDATE	Shipments	Shipment SHP-XGNR8WGQ	Status: Dispatched → In Transit	127.0.0.1
265	2026-05-08 05:25:40.968457	Admin	admin	CREATE	Sales Orders	SO SO-10015	Customer: CUST200000, Total: 76851.00	127.0.0.1
266	2026-05-08 05:25:48.859312	Admin	admin	UPDATE	Sales Orders	SO SO-10015	Status → Confirmed, inventory decremented	127.0.0.1
267	2026-05-08 05:25:55.332257	Admin	admin	DISPATCH	Sales Orders	SO SO-10015	Dispatched via Train. Customer: CUST200000 <>. Supplier notification sent.	127.0.0.1
268	2026-05-08 06:17:41.396417	Admin	admin	CREATE	Sales Orders	SO SO-10016	Customer: CUST200000, Total: 14253.80	127.0.0.1
269	2026-05-08 06:17:43.812639	Admin	admin	UPDATE	Sales Orders	SO SO-10016	Status → Confirmed, inventory decremented	127.0.0.1
270	2026-05-08 06:17:47.804894	Admin	admin	DISPATCH	Sales Orders	SO SO-10016	Dispatched via Truck. Customer: CUST200000 <>. Supplier notification sent.	127.0.0.1
271	2026-05-08 06:18:34.396985	Admin	admin	CREATE	Purchase Orders	PO PO-TRJ2JC	Supplier: Nithesh, Qty: 63	127.0.0.1
272	2026-05-08 06:18:36.391465	Admin	admin	UPDATE	Purchase Orders	PO PO-TRJ2JC	Approved, inventory +63	127.0.0.1
273	2026-05-08 06:44:13.850433	Admin	admin	UPDATE	Shipments	Shipment SHP-5VL7ANMD	Status: In Transit → In Transit	127.0.0.1
274	2026-05-08 06:44:19.731657	Admin	admin	UPDATE	Shipments	Shipment SHP-5VL7ANMD	Status: In Transit → In Transit	127.0.0.1
275	2026-05-08 06:44:27.822626	Admin	admin	UPDATE	Shipments	Shipment SHP-0QVGOEU8	Status: Dispatched → In Transit	127.0.0.1
276	2026-05-08 06:48:17.399975	Admin	admin	UPDATE	Shipments	Shipment SHP-0QVGOEU8	Status: In Transit → In Transit	127.0.0.1
277	2026-05-08 06:51:09.458848	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
278	2026-05-08 06:52:02.219079	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
279	2026-05-08 06:52:35.516822	Admin	admin	UPDATE	Shipments	Shipment SHP-0QVGOEU8	Status: In Transit → In Transit	127.0.0.1
280	2026-05-08 07:49:10.618048	Admin	admin	UPDATE	Shipments	Shipment SHP-0QVGOEU8	Status: In Transit → In Transit	127.0.0.1
313	2026-05-08 15:54:01.009047	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
314	2026-05-08 15:56:12.503981	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
315	2026-05-08 15:56:17.833133	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
316	2026-05-08 16:01:26.027668	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
317	2026-05-08 16:01:30.925418	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
318	2026-05-08 16:01:50.975838	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
319	2026-05-08 16:01:56.733138	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
320	2026-05-08 16:02:04.696013	Admin	admin	UPDATE	Shipments	Shipment SHP-0QVGOEU8	Status: In Transit → In Transit	127.0.0.1
321	2026-05-08 16:03:37.178025	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
322	2026-05-08 16:03:41.60485	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
323	2026-05-08 16:21:58.018062	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
324	2026-05-08 16:22:02.979889	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
325	2026-05-08 16:23:19.58282	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
326	2026-05-08 16:23:38.152332	Admin	admin	UPDATE	Shipments	Shipment SHP-0QVGOEU8	Status: In Transit → In Transit	127.0.0.1
327	2026-05-09 02:28:21.159513	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
328	2026-05-09 02:29:50.934334	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
329	2026-05-09 02:30:03.07904	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
330	2026-05-09 02:33:50.435277	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
331	2026-05-09 02:36:57.706447	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
332	2026-05-09 02:37:13.390462	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
333	2026-05-09 02:38:03.068643	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
334	2026-05-09 02:38:13.64337	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
335	2026-05-09 02:38:46.087575	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
336	2026-05-09 02:38:59.141698	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
337	2026-05-09 02:44:33.797107	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
338	2026-05-09 02:44:40.537782	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
339	2026-05-09 02:45:18.700652	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
340	2026-05-09 02:45:28.774204	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
341	2026-05-09 03:01:00.301537	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
342	2026-05-09 03:01:07.421157	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
343	2026-05-09 04:40:13.153287	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
344	2026-05-09 05:06:05.513827	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
345	2026-05-09 05:20:22.436104	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
346	2026-05-09 05:20:28.513055	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
347	2026-05-09 05:31:36.353008	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
348	2026-05-09 05:31:43.68272	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
349	2026-05-09 05:43:45.226193	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
350	2026-05-09 05:43:47.391962	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
351	2026-05-09 05:43:50.499275	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
352	2026-05-09 05:43:55.833813	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
353	2026-05-09 05:44:02.31743	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
354	2026-05-09 05:44:06.355339	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
355	2026-05-09 06:52:34.892916	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
356	2026-05-09 07:05:51.463888	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
357	2026-05-09 07:06:45.164567	Admin	admin	UPDATE	Shipments	Shipment SHP-XGNR8WGQ	Status: In Transit → In Transit	127.0.0.1
358	2026-05-09 07:07:41.201612	Admin	admin	UPDATE	Shipments	Shipment SHP-N4JHG1YA	Status: Dispatched → Out for Delivery	127.0.0.1
359	2026-05-09 07:08:39.167627	Admin	admin	UPDATE	Shipments	Shipment SHP-N4JHG1YA	Status: Out for Delivery → Dispatched	127.0.0.1
360	2026-05-09 07:08:53.737415	Admin	admin	UPDATE	Shipments	Shipment SHP-N4JHG1YA	Status: Dispatched → Dispatched	127.0.0.1
361	2026-05-09 07:09:00.61962	Admin	admin	UPDATE	Shipments	Shipment SHP-N4JHG1YA	Status: Dispatched → Dispatched	127.0.0.1
362	2026-05-09 07:10:24.083397	Admin	admin	UPDATE	Shipments	Shipment SHP-N4JHG1YA	Status: Dispatched → In Transit	127.0.0.1
363	2026-05-09 07:10:38.29945	Admin	admin	UPDATE	Shipments	Shipment SHP-0QVGOEU8	Status: In Transit → In Transit	127.0.0.1
364	2026-05-09 07:25:53.536197	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
365	2026-05-09 07:26:07.898464	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
366	2026-05-09 07:30:01.189984	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
367	2026-05-09 07:30:09.229008	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
368	2026-05-09 12:16:05.791698	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
369	2026-05-09 12:17:52.333957	Admin	admin	UPDATE	Shipments	Shipment SHP-0QVGOEU8	Status: In Transit → Delivered	127.0.0.1
370	2026-05-09 12:18:00.666158	Admin	admin	UPDATE	Shipments	Shipment SHP-0QVGOEU8	Status: Delivered → In Transit	127.0.0.1
371	2026-05-09 12:18:35.344789	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
372	2026-05-09 12:18:41.279361	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
373	2026-05-09 12:19:43.267844	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
374	2026-05-09 12:19:48.57059	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
375	2026-05-09 12:30:30.834656	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
376	2026-05-09 12:30:33.741168	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
377	2026-05-09 15:49:49.343547	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
378	2026-05-09 15:49:55.798229	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
379	2026-05-09 15:51:16.628879	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
380	2026-05-09 15:51:19.968637	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
381	2026-05-09 15:51:24.01483	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
384	2026-05-09 15:52:46.44072	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
385	2026-05-09 15:52:55.958197	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
382	2026-05-09 15:51:37.609936	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
383	2026-05-09 15:52:41.117617	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
386	2026-05-09 15:54:26.016762	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
387	2026-05-09 15:55:16.950673	Admin	admin	UPDATE	Shipments	Shipment SHP-0QVGOEU8	Status: In Transit → Out for Delivery	127.0.0.1
388	2026-05-09 15:55:23.86744	Admin	admin	UPDATE	Shipments	Shipment SHP-0QVGOEU8	Status: Out for Delivery → Delivered	127.0.0.1
389	2026-05-09 15:55:31.037288	Admin	admin	UPDATE	Shipments	Shipment SHP-5VL7ANMD	Status: In Transit → Delivered	127.0.0.1
390	2026-05-09 15:55:45.133192	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
391	2026-05-09 15:55:51.014611	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
392	2026-05-10 05:53:15.060934	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
393	2026-05-10 05:56:07.336917	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
394	2026-05-10 05:56:14.895954	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
395	2026-05-10 05:57:12.139888	Ishan	manager	CREATE_SALES_ORDER	Sales Orders	SO SO-P13M18	Items: 1, Total: 6082.5, Site: OTOH	127.0.0.1
396	2026-05-10 05:57:14.90936	Ishan	manager	UPDATE	Sales Orders	SO SO-P13M18	Order moved to Processing by Ishan. Shipments: 1	127.0.0.1
397	2026-05-10 05:57:17.662282	Ishan	manager	UPDATE	Sales Orders	SO SO-P13M18	Dispatched via Air	127.0.0.1
398	2026-05-10 05:58:22.414769	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
399	2026-05-10 05:58:31.90965	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
400	2026-05-10 08:36:24.344678	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
401	2026-05-10 13:52:45.841635	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
402	2026-05-10 14:02:24.268449	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
403	2026-05-10 14:02:30.327466	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
404	2026-05-10 14:23:21.061597	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
405	2026-05-10 14:23:25.662193	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
406	2026-05-10 14:31:57.632462	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
407	2026-05-10 14:32:08.161274	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
408	2026-05-10 14:33:05.898604	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
409	2026-05-10 14:33:12.413615	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
410	2026-05-10 14:33:44.17851	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
411	2026-05-10 14:33:46.906086	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
412	2026-05-10 14:33:49.324106	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
413	2026-05-10 14:33:54.933852	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
414	2026-05-11 02:43:11.038304	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
415	2026-05-11 02:45:14.552806	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
416	2026-05-11 02:45:22.292224	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
417	2026-05-11 02:48:04.928615	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
418	2026-05-11 02:48:11.952558	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
419	2026-05-11 02:48:58.155724	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
420	2026-05-11 02:49:04.674456	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
421	2026-05-11 02:49:28.012344	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
422	2026-05-11 02:49:33.14388	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
423	2026-05-11 02:50:00.078482	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
424	2026-05-11 03:00:47.137493	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
425	2026-05-11 03:02:20.274219	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
426	2026-05-11 03:02:25.894313	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
427	2026-05-11 04:35:21.976366	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
428	2026-05-11 04:35:47.942672	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
429	2026-05-11 04:35:51.971414	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
430	2026-05-11 04:37:06.411686	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
431	2026-05-11 04:37:42.046911	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
432	2026-05-11 04:39:25.6191	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
433	2026-05-11 04:50:52.344947	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
434	2026-05-11 04:51:01.248188	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
435	2026-05-11 04:54:59.367267	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
436	2026-05-11 04:55:06.348566	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
437	2026-05-11 04:55:08.959519	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
438	2026-05-11 04:55:15.387145	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
439	2026-05-11 04:55:18.386268	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
440	2026-05-11 05:05:24.804023	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
441	2026-05-11 05:05:31.166278	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
442	2026-05-11 05:05:35.84301	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
443	2026-05-11 05:11:59.792469	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
444	2026-05-11 05:12:04.765782	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
445	2026-05-11 05:15:53.749501	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
446	2026-05-11 05:15:57.875004	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
447	2026-05-11 05:17:38.697245	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
448	2026-05-11 05:18:19.894496	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
449	2026-05-11 05:25:01.391787	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
450	2026-05-11 05:25:06.37063	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
451	2026-05-11 05:26:05.863848	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
452	2026-05-11 05:26:09.43436	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
453	2026-05-11 05:26:11.869098	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
456	2026-05-11 05:33:11.028581	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
454	2026-05-11 05:26:20.149939	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
455	2026-05-11 05:33:01.300691	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
457	2026-05-11 05:40:36.413341	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
458	2026-05-11 05:49:41.997263	Admin	admin	CREATE_USER	Users	User kanakadri	Role: manager, Email: kurubakanakadri9@gmail.com, EmpID: EMP1006	127.0.0.1
459	2026-05-11 05:50:03.623629	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
460	2026-05-11 05:50:21.752764	kanakadri	manager	LOGIN	Auth	User kanakadri	Role: manager	127.0.0.1
461	2026-05-11 05:54:51.159763	kanakadri	manager	CREATE	Purchase Orders	PO PO-W5IB9L	Product: PRD10009, Qty: 123	127.0.0.1
462	2026-05-11 05:55:03.613735	kanakadri	manager	UPDATE	Purchase Orders	PO PO-W5IB9L	Approved, inventory +123	127.0.0.1
463	2026-05-11 05:56:15.740434	kanakadri	manager	CREATE_SALES_ORDER	Sales Orders	SO SO-GV9377	Items: 1, Total: 5565.4, Site: W1Q5	127.0.0.1
464	2026-05-11 05:56:20.289328	kanakadri	manager	UPDATE	Sales Orders	SO SO-GV9377	Order moved to Processing by kanakadri. Shipments: 1	127.0.0.1
465	2026-05-11 05:56:25.601633	kanakadri	manager	UPDATE	Sales Orders	SO SO-GV9377	Dispatched via Air	127.0.0.1
466	2026-05-11 06:02:23.786659	kanakadri	manager	LOGOUT	Auth	User kanakadri	Logged out	127.0.0.1
467	2026-05-11 06:02:26.973781	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
468	2026-05-11 06:05:42.979327	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
469	2026-05-11 06:05:48.425959	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
470	2026-05-11 06:08:10.999231	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
471	2026-05-11 06:08:17.496253	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
472	2026-05-11 06:27:43.423836	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
473	2026-05-11 06:27:49.02464	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
474	2026-05-11 06:33:32.817819	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
475	2026-05-11 06:33:36.694749	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
476	2026-05-11 06:40:33.517826	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
477	2026-05-11 06:41:03.465388	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
478	2026-05-11 06:41:30.960741	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
479	2026-05-11 06:41:36.844418	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
480	2026-05-11 12:08:09.547223	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
481	2026-05-13 09:03:01.569222	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
482	2026-05-13 09:32:07.784905	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
483	2026-05-13 09:32:13.000386	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
484	2026-05-13 09:32:24.653026	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
485	2026-05-13 09:32:30.546907	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
486	2026-05-13 10:37:19.287939	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
487	2026-05-13 10:37:34.318831	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
488	2026-05-13 10:43:19.82409	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
489	2026-05-13 10:43:25.060827	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
490	2026-05-13 10:53:34.894076	Ishan	manager	CREATE_SALES_ORDER	Sales Orders	SO SO-2JTE03	Items: 1, Total: 6466.2, Site: OTOH	127.0.0.1
491	2026-05-13 10:53:40.627396	Ishan	manager	UPDATE	Sales Orders	SO SO-2JTE03	Order moved to Processing by Ishan. Shipments: 1	127.0.0.1
492	2026-05-13 10:53:42.300122	Ishan	manager	UPDATE	Sales Orders	SO SO-2JTE03	Dispatched via Truck	127.0.0.1
493	2026-05-13 11:06:17.019428	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
494	2026-05-13 11:06:23.144164	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
495	2026-05-13 11:16:47.708141	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
496	2026-05-13 11:16:49.853506	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
497	2026-05-13 11:17:14.032728	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
498	2026-05-13 11:17:16.178007	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
499	2026-05-13 11:17:22.214508	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
500	2026-05-13 11:17:27.370874	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
501	2026-05-14 05:02:58.77399	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
502	2026-05-14 05:19:46.780172	Admin	admin	CREATE	Sales Orders	SO SO-10020	Customer: CUST200004, Total: 5977.32	127.0.0.1
503	2026-05-14 05:19:53.603785	Admin	admin	UPDATE	Sales Orders	SO SO-10020	Status → Processing, inventory decremented	127.0.0.1
504	2026-05-14 05:19:56.394316	Admin	admin	DISPATCH	Sales Orders	SO SO-10020	Dispatched via Air. Customer: CUST200004 <>. Supplier notification sent.	127.0.0.1
505	2026-05-14 05:30:23.170294	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
506	2026-05-14 05:30:30.280491	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
507	2026-05-14 05:31:46.144298	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
508	2026-05-14 05:32:01.287816	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
509	2026-05-14 05:32:06.579291	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
510	2026-05-14 08:53:11.814169	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
511	2026-05-14 11:48:05.211619	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
512	2026-05-14 11:48:09.715141	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
513	2026-05-14 11:50:07.517048	Admin	admin	CREATE_USER	Users	User Arjun	Role: manager, Email: arjunak12@gmail.com, EmpID: EMP1007	127.0.0.1
514	2026-05-14 11:56:48.796326	Admin	admin	DELETE	Users	User Arjun	Email: arjunak12@gmail.com, Role: manager	127.0.0.1
515	2026-05-14 12:01:11.406687	Admin	admin	CREATE	Purchase Orders	PO PO-UXMUOE	Supplier: Nithesh, Qty: 45	127.0.0.1
516	2026-05-14 12:01:14.175439	Admin	admin	UPDATE	Purchase Orders	PO PO-UXMUOE	Approved, inventory +45	127.0.0.1
517	2026-05-14 12:14:40.885154	Admin	admin	CREATE	Purchase Orders	PO PO-RA7NKK	Supplier: Arjun, Qty: 55	127.0.0.1
518	2026-05-14 12:14:42.796484	Admin	admin	UPDATE	Purchase Orders	PO PO-RA7NKK	Approved, inventory +55	127.0.0.1
519	2026-05-14 12:16:27.96158	Admin	admin	CREATE	Sales Orders	SO SO-10021	Customer: CUST200003, Total: 30565.00	127.0.0.1
520	2026-05-14 12:16:30.296215	Admin	admin	UPDATE	Sales Orders	SO SO-10021	Status → Processing, inventory decremented	127.0.0.1
524	2026-05-14 12:21:40.671231	Ishan	manager	CREATE	Purchase Orders	PO PO-EKA3MN	Product: PRD10014, Qty: 45	127.0.0.1
530	2026-05-14 12:23:22.558897	Ishan	manager	UPDATE	Sales Orders	SO SO-DAXM7X	Dispatched via Air	127.0.0.1
535	2026-05-14 13:16:00.734822	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
521	2026-05-14 12:16:31.912537	Admin	admin	DISPATCH	Sales Orders	SO SO-10021	Dispatched via Truck. Customer: CUST200003 <>. Supplier notification sent.	127.0.0.1
525	2026-05-14 12:21:52.195803	Ishan	manager	UPDATE	Purchase Orders	PO PO-EKA3MN	Status → Cancelled	127.0.0.1
528	2026-05-14 12:23:12.227756	Ishan	manager	CREATE_SALES_ORDER	Sales Orders	SO SO-DAXM7X	Items: 1, Total: 2189.7, Site: OTOH	127.0.0.1
532	2026-05-14 12:25:11.017118	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
533	2026-05-14 12:50:45.149775	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
522	2026-05-14 12:18:04.560018	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
527	2026-05-14 12:22:37.246446	Ishan	manager	UPDATE	Purchase Orders	PO PO-IFK1IO	Status → Cancelled	127.0.0.1
531	2026-05-14 12:25:06.033893	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
536	2026-05-14 13:16:05.092183	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
523	2026-05-14 12:18:09.465238	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
529	2026-05-14 12:23:19.638962	Ishan	manager	UPDATE	Sales Orders	SO SO-DAXM7X	Order moved to Processing by Ishan. Shipments: 1	127.0.0.1
526	2026-05-14 12:22:26.537637	Ishan	manager	CREATE	Purchase Orders	PO PO-IFK1IO	Product: PRD10005, Qty: 55	127.0.0.1
534	2026-05-14 12:50:49.326296	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
537	2026-05-15 02:35:24.912155	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
538	2026-05-15 02:48:56.609598	Admin	admin	CREATE	Purchase Returns	Return PR-W44FY5	PO: PO-RA7NKK, Credit: 427.80	127.0.0.1
539	2026-05-15 02:49:05.452592	Admin	admin	UPDATE	Purchase Returns	Return PR-W44FY5	Status: Approved	127.0.0.1
540	2026-05-15 02:51:25.45586	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
541	2026-05-15 02:51:32.407312	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
542	2026-05-15 02:53:01.47662	Ishan	manager	CREATE	Purchase Orders	PO PO-E12V7F	Product: PRD10011, Qty: 55, Cost: 229.08	127.0.0.1
543	2026-05-15 02:53:09.532996	Ishan	manager	UPDATE	Purchase Orders	PO PO-E12V7F	Approved, inventory +55	127.0.0.1
544	2026-05-15 02:54:45.124022	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
545	2026-05-15 02:54:51.430084	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
546	2026-05-15 02:56:23.687261	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
547	2026-05-15 02:56:28.681933	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
548	2026-05-15 03:03:28.971712	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
549	2026-05-15 04:43:32.153219	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
550	2026-05-15 04:44:31.375301	Admin	admin	CREATE_USER	Users	User Rohit	Role: manager, Email: sudheernani3345@gmail.com, EmpID: EMP1007	127.0.0.1
551	2026-05-15 04:45:23.96014	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
552	2026-05-15 04:47:42.058486	system		LOGOUT	Auth	User ?	Logged out	127.0.0.1
553	2026-05-15 04:47:59.020457	Rohit	manager	LOGIN	Auth	User Rohit	Role: manager	127.0.0.1
554	2026-05-15 05:30:39.875466	Rohit	manager	LOGOUT	Auth	User Rohit	Logged out	127.0.0.1
555	2026-05-15 05:30:44.985088	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
556	2026-05-15 05:35:50.003211	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
557	2026-05-15 05:35:55.020423	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
558	2026-05-15 05:43:27.824199	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
559	2026-05-15 05:43:32.844426	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
560	2026-05-15 08:32:43.609013	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
561	2026-05-15 08:54:17.836288	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
562	2026-05-15 10:40:39.781702	Rohit	manager	LOGIN	Auth	User Rohit	Role: manager	127.0.0.1
563	2026-05-15 10:40:46.22293	Rohit	manager	LOGOUT	Auth	User Rohit	Logged out	127.0.0.1
564	2026-05-15 10:40:58.771954	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
565	2026-05-15 10:41:03.691962	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
566	2026-05-15 10:41:11.605343	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
567	2026-05-15 10:41:16.842595	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
568	2026-05-15 11:03:21.756269	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
569	2026-05-15 11:03:26.767162	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
570	2026-05-15 11:05:30.80655	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
571	2026-05-15 11:05:36.693186	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
572	2026-05-15 11:10:03.277446	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
573	2026-05-15 11:10:09.334339	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
574	2026-05-15 11:16:48.904979	Ishan	manager	CREATE_SALES_ORDER	Sales Orders	SO SO-2OOEJS	Items: 2, Total: 11724.8, Site: OTOH	127.0.0.1
575	2026-05-15 11:16:51.037194	Ishan	manager	UPDATE	Sales Orders	SO SO-2OOEJS	Order moved to Processing by Ishan. Shipments: 2	127.0.0.1
576	2026-05-15 11:16:53.094494	Ishan	manager	UPDATE	Sales Orders	SO SO-2OOEJS	Dispatched via Truck	127.0.0.1
577	2026-05-15 11:47:37.109566	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
578	2026-05-15 11:48:21.706362	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
579	2026-05-15 11:48:52.945846	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
580	2026-05-15 11:48:57.266534	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
581	2026-05-15 12:14:48.257084	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
582	2026-05-15 12:14:56.187263	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
583	2026-05-15 12:16:03.144379	Admin	admin	UPDATE	Shipments	Shipment SHP-BWSVYET9	Status: In Transit → Delivered	127.0.0.1
584	2026-05-15 12:18:04.194352	Admin	admin	CREATE	Sales Returns	Return SR-MHAG4U	SO: SO-10020, Refund: 5977.32	127.0.0.1
585	2026-05-15 12:18:10.655631	Admin	admin	UPDATE	Sales Returns	Return SR-MHAG4U	Status: Approved	127.0.0.1
586	2026-05-15 12:20:05.097784	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
587	2026-05-15 12:20:09.772731	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
588	2026-05-15 12:20:18.342554	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
589	2026-05-15 12:20:24.931817	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
590	2026-05-15 12:27:15.117376	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
591	2026-05-15 12:27:22.755358	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
592	2026-05-15 12:28:30.197275	Admin	admin	CREATE	Sales Returns	Return SR-J2U6GX	SO: SO-10016, Refund: 14253.80	127.0.0.1
593	2026-05-15 12:29:52.471692	Admin	admin	UPDATE	Sales Returns	Return SR-J2U6GX	Status: Approved	127.0.0.1
594	2026-05-16 08:57:14.585441	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
595	2026-05-16 09:27:10.98357	Admin	admin	DELETE	Products	Product Men Item 4	ID: PRD10004	127.0.0.1
596	2026-05-16 09:32:12.141585	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
597	2026-05-16 09:32:14.501498	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
598	2026-05-16 09:39:54.492963	Admin	admin	DELETE	Users	User kanakadri	Email: kurubakanakadri9@gmail.com, Role: manager	127.0.0.1
599	2026-05-16 10:45:53.817508	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
600	2026-05-16 10:46:00.996038	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
601	2026-05-16 10:46:08.532332	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
602	2026-05-16 10:56:51.998542	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
603	2026-05-16 10:56:57.688157	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
604	2026-05-16 11:12:14.124887	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
605	2026-05-16 11:12:19.109234	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
606	2026-05-16 11:12:22.012676	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
607	2026-05-16 11:12:27.737671	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
608	2026-05-16 11:24:24.409703	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
609	2026-05-16 11:24:30.881234	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
610	2026-05-16 11:32:06.295105	Admin	admin	DELETE	Users	User Arjun	Email: ganeshgani5110@gmail.com, Role: manager	127.0.0.1
611	2026-05-16 11:32:11.088967	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
612	2026-05-16 11:32:18.212029	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
613	2026-05-16 11:33:27.940361	Ishan	manager	CREATE_SALES_ORDER	Sales Orders	SO SO-YOYUA9	Items: 1, Total: 5839.2, Site: OTOH	127.0.0.1
614	2026-05-16 11:33:29.587007	Ishan	manager	UPDATE	Sales Orders	SO SO-YOYUA9	Order moved to Processing by Ishan. Shipments: 1	127.0.0.1
615	2026-05-16 11:33:31.904311	Ishan	manager	UPDATE	Sales Orders	SO SO-YOYUA9	Dispatched via Truck	127.0.0.1
616	2026-05-16 11:41:18.35626	Ishan	manager	CREATE	Purchase Orders	PO PO-IDDI7P	Product: PRD10009, Qty: 45, Cost: 447.96	127.0.0.1
617	2026-05-16 11:44:55.288251	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
618	2026-05-16 11:55:38.227572	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
619	2026-05-16 11:57:02.335103	Admin	admin	CREATE_USER	Users	User Nani Sudheer	Role: manager, Email: nanisudheer455@gmail.com, EmpID: EMP1006	127.0.0.1
620	2026-05-16 12:00:02.748684	Admin	admin	UPDATE	Shipments	Shipment SHP-WG4B11BV	Status: In Transit → Delivered	127.0.0.1
621	2026-05-16 12:13:34.261578	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
622	2026-05-16 12:13:38.71533	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
623	2026-05-16 12:14:34.123972	Ishan	manager	UPDATE	Purchase Orders	PO PO-IDDI7P	Approved, inventory +45	127.0.0.1
624	2026-05-16 12:16:10.057871	Ishan	manager	CREATE	Purchase Orders	PO PO-NTKUKF	Product: PRD10008, Qty: 55, Cost: 427.8	127.0.0.1
625	2026-05-16 12:16:16.138224	Ishan	manager	UPDATE	Purchase Orders	PO PO-NTKUKF	Approved, inventory +55	127.0.0.1
626	2026-05-16 12:18:34.187447	Ishan	manager	CREATE	Purchase Returns	Return PR-1M5ZK6	PO: PO-NTKUKF, Credit: 427.80	127.0.0.1
627	2026-05-16 12:18:41.791511	Ishan	manager	UPDATE	Purchase Returns	Return PR-1M5ZK6	Status: Approved	127.0.0.1
628	2026-05-16 12:19:13.310559	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
629	2026-05-16 12:19:20.801544	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
630	2026-05-16 12:19:23.161397	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
631	2026-05-16 12:19:27.381388	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
632	2026-05-16 12:20:46.848177	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
633	2026-05-16 12:20:53.845895	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
634	2026-05-16 12:23:00.670268	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
635	2026-05-16 12:41:29.114123	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
636	2026-05-16 12:41:59.776793	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
637	2026-05-16 12:42:02.152659	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
638	2026-05-18 12:10:57.081296	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
639	2026-05-18 12:11:21.248738	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
640	2026-05-18 12:11:29.84278	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
641	2026-05-18 12:14:21.566026	Admin	admin	DELETE	Users	User Nani Sudheer	Email: nanisudheer455@gmail.com, Role: manager	127.0.0.1
642	2026-05-18 12:20:32.528448	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
643	2026-05-18 19:50:30.378203	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
644	2026-05-18 19:51:35.694966	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
645	2026-05-18 19:55:32.837028	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
646	2026-05-18 19:56:10.294896	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
647	2026-05-18 19:56:17.389857	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
648	2026-05-18 19:56:48.727623	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
649	2026-05-18 19:56:51.15937	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
650	2026-05-18 20:00:27.978861	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
651	2026-05-18 20:00:33.232485	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
652	2026-05-18 20:04:23.145727	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
653	2026-05-18 20:05:03.473877	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
654	2026-05-18 20:05:14.625663	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
655	2026-05-18 20:09:58.879757	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
656	2026-05-19 02:05:27.776319	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
657	2026-05-19 02:06:04.569212	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
658	2026-05-19 02:06:11.773027	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
659	2026-05-19 02:06:59.468321	Ishan	manager	CREATE	Sales Returns	Return SR-9GQPC4	SO: SO-2JTE03, Refund: 6466.20	127.0.0.1
660	2026-05-19 02:07:05.653301	Ishan	manager	UPDATE	Sales Returns	Return SR-9GQPC4	Status: Approved	127.0.0.1
661	2026-05-19 02:07:47.467841	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
662	2026-05-19 02:07:50.725958	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
663	2026-05-19 02:07:53.42802	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
664	2026-05-19 02:07:59.588839	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
665	2026-05-19 02:16:37.517154	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
666	2026-05-19 02:17:02.771418	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
667	2026-05-19 02:17:52.277765	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
668	2026-05-19 02:17:58.662418	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
669	2026-05-19 02:24:56.668347	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
670	2026-05-19 02:25:01.796791	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
671	2026-05-19 02:25:40.139098	Admin	admin	CREATE	Purchase Returns	Return PR-8PSHNC	PO: PO-TRJ2JC, Credit: 475.07	127.0.0.1
672	2026-05-19 02:25:48.923727	Admin	admin	UPDATE	Purchase Returns	Return PR-8PSHNC	Status: Approved	127.0.0.1
673	2026-05-19 02:25:52.665996	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
674	2026-05-19 02:26:12.312336	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
675	2026-05-19 02:30:21.563303	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
676	2026-05-19 02:30:45.310003	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
677	2026-05-19 02:30:49.027728	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
678	2026-05-19 02:38:34.226409	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
679	2026-05-19 02:39:03.008587	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
680	2026-05-19 02:39:07.688817	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
681	2026-05-19 02:41:30.238168	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
682	2026-05-19 02:41:35.393192	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
683	2026-05-19 02:52:09.11355	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
684	2026-05-19 02:52:25.712885	Admin	admin	LOGOUT	Auth	User Admin	Logged out	127.0.0.1
685	2026-05-19 02:52:30.895733	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
686	2026-05-19 02:53:46.645422	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
687	2026-05-19 02:53:53.023338	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
688	2026-05-19 02:54:02.236612	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
689	2026-05-19 02:54:08.030175	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
690	2026-05-19 03:02:22.649871	Arjun	analyst	LOGOUT	Auth	User Arjun	Logged out	127.0.0.1
691	2026-05-19 03:02:30.915772	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
692	2026-05-19 10:24:20.737485	Ishan	manager	LOGIN	Auth	User Ishan	Role: manager	127.0.0.1
693	2026-05-19 10:26:05.774902	Ishan	manager	LOGOUT	Auth	User Ishan	Logged out	127.0.0.1
694	2026-05-19 10:26:11.434972	Arjun	analyst	LOGIN	Auth	User Arjun	Role: analyst	127.0.0.1
695	2026-05-19 12:34:43.473165	Admin	admin	LOGIN	Auth	User Admin	Role: admin	127.0.0.1
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, category_name) FROM stdin;
1	Dairy
2	Bakery
3	Electronics
4	Apparel
\.


--
-- Data for Name: contact_messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contact_messages (id, name, email, company, subject, message, is_read, created_at) FROM stdin;
1	Ik Ishan	ishankishanik32@gmail.com	Mani_Products	General Inquiry	Tell me what type of products are available.	t	2026-05-08
\.


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customers (id, customer_id, age, gender, income_bracket, purchase_frequency, average_spend, preferred_categories, last_purchase_date, total_spend, clv, csat, nps) FROM stdin;
1	CUST200000	29	Female	10 LPA	9	2248.08	\N	\N	\N	\N	\N	\N
2	CUST200001	56	Male	20+ LPA	7	1335.89	\N	\N	\N	\N	\N	\N
3	CUST200002	58	Other	10 LPA	9	1250.89	\N	\N	\N	\N	\N	\N
4	CUST200003	36	Male	10 LPA	6	4288.93	\N	\N	\N	\N	\N	\N
5	CUST200004	57	Male	10-20 LPA	1	2680.74	\N	\N	\N	\N	\N	\N
6	CUST200005	30	Female	20+ LPA	7	3581.14	\N	\N	\N	\N	\N	\N
7	CUST200006	44	Other	20+ LPA	8	1252.64	\N	\N	\N	\N	\N	\N
8	CUST200007	54	Male	10 LPA	5	647.13	\N	\N	\N	\N	\N	\N
9	CUST200008	32	Other	10-20 LPA	3	4013.33	\N	\N	\N	\N	\N	\N
10	CUST200009	54	Other	20+ LPA	9	2798.63	\N	\N	\N	\N	\N	\N
11	CUST200010	54	Male	10-20 LPA	9	4204.77	\N	\N	\N	\N	\N	\N
12	CUST200011	41	Other	1-5 LPA	12	2486.15	\N	\N	\N	\N	\N	\N
13	CUST200012	31	Female	1-5 LPA	12	4235.32	\N	\N	\N	\N	\N	\N
14	CUST200013	66	Male	10-20 LPA	1	2523.8	\N	\N	\N	\N	\N	\N
15	CUST200014	40	Male	20+ LPA	2	3990.34	\N	\N	\N	\N	\N	\N
16	CUST200015	33	Male	10-20 LPA	12	3246.18	\N	\N	\N	\N	\N	\N
17	CUST200016	45	Male	10 LPA	4	4160.88	\N	\N	\N	\N	\N	\N
18	CUST200017	69	Male	10-20 LPA	9	1764.88	\N	\N	\N	\N	\N	\N
19	CUST200018	52	Male	10-20 LPA	12	1816.86	\N	\N	\N	\N	\N	\N
20	CUST200019	54	Female	1-5 LPA	3	4832.47	\N	\N	\N	\N	\N	\N
21	CUST200020	68	Female	1-5 LPA	5	4401.71	\N	\N	\N	\N	\N	\N
22	CUST200021	26	Other	10 LPA	4	1158.1	\N	\N	\N	\N	\N	\N
23	CUST200022	38	Male	20+ LPA	8	1139.77	\N	\N	\N	\N	\N	\N
24	CUST200023	58	Female	20+ LPA	7	2533.96	\N	\N	\N	\N	\N	\N
25	CUST200024	58	Male	20+ LPA	9	3874.11	\N	\N	\N	\N	\N	\N
26	CUST200025	62	Female	20+ LPA	8	1972.8	\N	\N	\N	\N	\N	\N
27	CUST200026	18	Other	1-5 LPA	12	4874.68	\N	\N	\N	\N	\N	\N
28	CUST200027	58	Other	10-20 LPA	2	4080.55	\N	\N	\N	\N	\N	\N
29	CUST200028	43	Male	20+ LPA	4	2726.22	\N	\N	\N	\N	\N	\N
30	CUST200029	38	Female	10-20 LPA	9	3100.7	\N	\N	\N	\N	\N	\N
31	CUST200030	54	Female	10-20 LPA	11	3930.14	\N	\N	\N	\N	\N	\N
32	CUST200031	20	Male	20+ LPA	1	1059.07	\N	\N	\N	\N	\N	\N
33	CUST200032	28	Female	20+ LPA	1	4963.27	\N	\N	\N	\N	\N	\N
34	CUST200033	45	Male	10 LPA	11	1858.39	\N	\N	\N	\N	\N	\N
35	CUST200034	35	Male	10-20 LPA	5	870.89	\N	\N	\N	\N	\N	\N
36	CUST200035	60	Other	10 LPA	1	2283.54	\N	\N	\N	\N	\N	\N
37	CUST200036	37	Other	10 LPA	7	3449.68	\N	\N	\N	\N	\N	\N
38	CUST200037	63	Male	1-5 LPA	4	2645.63	\N	\N	\N	\N	\N	\N
39	CUST200038	26	Other	10 LPA	9	3559.92	\N	\N	\N	\N	\N	\N
40	CUST200039	18	Male	10-20 LPA	2	4946.7	\N	\N	\N	\N	\N	\N
41	CUST200040	45	Other	10 LPA	8	818.73	\N	\N	\N	\N	\N	\N
42	CUST200041	42	Male	1-5 LPA	2	1910.08	\N	\N	\N	\N	\N	\N
43	CUST200042	37	Male	20+ LPA	3	3387.09	\N	\N	\N	\N	\N	\N
44	CUST200043	61	Male	1-5 LPA	9	3034.81	\N	\N	\N	\N	\N	\N
45	CUST200044	57	Other	10 LPA	8	2080.34	\N	\N	\N	\N	\N	\N
46	CUST200045	31	Other	10 LPA	7	3272.34	\N	\N	\N	\N	\N	\N
47	CUST200046	46	Male	1-5 LPA	2	1130.06	\N	\N	\N	\N	\N	\N
48	CUST200047	25	Other	20+ LPA	6	4834.62	\N	\N	\N	\N	\N	\N
49	CUST200048	38	Male	10 LPA	5	3400.79	\N	\N	\N	\N	\N	\N
50	CUST200049	33	Other	10-20 LPA	12	620.71	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: inventory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.inventory (id, site_id, product_id, beginning_inventory, ending_inventory, replenishment, stockout_flag) FROM stdin;
1	A11D	PRD10087	222	233	42	No
2	AM14	PRD10082	428	442	72	No
3	ZYTJ	PRD10093	457	502	55	No
4	0T0P	PRD10092	329	378	72	No
5	BVM2	PRD10082	80	153	77	No
6	CX19	PRD10085	74	78	10	No
7	0T0P	PRD10080	168	182	18	No
8	JI0Y	PRD10027	308	329	68	No
9	30T9	PRD10079	376	393	95	No
11	BVM2	PRD10070	260	271	11	No
12	58KX	PRD10092	190	232	78	No
13	VUZZ	PRD10064	466	479	99	No
14	FKHM	PRD10022	104	110	22	No
15	FFYV	PRD10030	148	170	89	No
16	4CIY	PRD10045	186	241	60	No
17	CXUL	PRD10051	285	336	82	No
18	KJLT	PRD10028	203	290	97	No
19	A11D	PRD10083	438	451	14	No
20	SEMC	PRD10048	243	263	80	No
21	30T9	PRD10081	54	132	99	No
23	4ZKL	PRD10012	320	328	15	No
24	IUC0	PRD10088	340	376	70	No
25	PKH1	PRD10009	400	411	45	No
26	4ZKL	PRD10084	66	78	32	No
27	VUZZ	PRD10026	350	354	28	No
28	OTOH	PRD10050	89	127	48	No
29	4ZKL	PRD10030	340	356	59	No
30	BVM2	PRD10042	246	248	27	No
31	KJLT	PRD10092	90	120	74	No
32	30T9	PRD10012	273	308	39	No
33	GHC0	PRD10077	443	455	88	No
34	SEMC	PRD10099	217	220	13	No
35	GDPP	PRD10057	301	318	39	No
36	PS3Y	PRD10048	271	280	33	No
37	MYZY	PRD10098	366	398	47	No
39	EXQ7	PRD10091	451	523	91	No
40	NY20	PRD10049	212	262	56	No
41	MYZY	PRD10000	207	227	66	No
42	XDP5	PRD10034	102	126	26	No
43	5JSG	PRD10055	279	289	81	No
44	I3QK	PRD10052	102	114	13	No
45	8CGV	PRD10070	97	107	86	No
46	HOCN	PRD10049	56	77	47	No
47	EXQ7	PRD10099	93	143	81	No
48	4ZKL	PRD10066	136	185	97	No
49	ZYTJ	PRD10017	187	218	48	No
52	CXUL	PRD10032	176	203	90	No
54	0T0P	PRD10038	53	92	60	No
55	WM31	PRD10048	461	485	52	No
56	GHC0	PRD10055	467	484	93	No
57	0T0P	PRD10038	214	276	87	No
58	ID25	PRD10040	140	180	60	No
59	M5IG	PRD10094	405	434	91	No
60	4ZKL	PRD10031	216	257	58	No
61	SEMC	PRD10046	108	165	82	No
62	P7Y6	PRD10069	142	169	97	No
63	VUZZ	PRD10093	286	360	100	No
64	A1WJ	PRD10037	475	565	98	No
65	93TY	PRD10086	305	312	27	No
66	P5TB	PRD10030	179	254	94	No
67	OTOH	PRD10054	454	508	58	No
68	A1WJ	PRD10076	295	328	84	No
69	BVM2	PRD10064	495	540	98	No
70	BVM2	PRD10004	454	466	56	No
71	BVM2	PRD10076	376	393	20	No
72	M5K8	PRD10031	386	436	95	No
73	ZYTJ	PRD10082	363	366	15	No
74	XDP5	PRD10042	457	509	65	No
75	JI0Y	PRD10012	182	188	38	No
76	NY20	PRD10066	335	346	84	No
77	SV87	PRD10057	241	272	60	No
78	M5K8	PRD10086	351	385	98	No
79	FFYV	PRD10044	62	120	71	No
80	M5IG	PRD10053	93	94	24	No
81	FFYV	PRD10044	209	233	53	No
82	IUC0	PRD10066	297	321	54	No
83	J7YH	PRD10056	419	461	99	No
85	VUZZ	PRD10043	381	383	23	No
86	ZYTJ	PRD10094	174	228	76	No
87	PS3Y	PRD10020	219	246	81	No
88	T4UF	PRD10029	458	479	61	No
89	5JSG	PRD10023	377	416	94	No
90	SEMC	PRD10003	427	490	88	No
91	A1WJ	PRD10075	269	328	59	No
92	OTOH	PRD10027	155	155	45	No
93	CX19	PRD10073	102	157	78	No
94	CXUL	PRD10041	150	204	68	No
95	4CIY	PRD10085	491	496	72	No
96	W1Q5	PRD10040	355	375	59	No
97	SEMC	PRD10075	108	140	54	No
98	T4UF	PRD10079	138	144	96	No
99	P5TB	PRD10078	352	368	20	No
100	HOCN	PRD10015	172	214	49	No
107	OTOH	PRD10014	45	45	45	No
102	0T0P	PRD10011	100	100	100	No
10	ID25	PRD10084	299	263	12	No
22	MYZY	PRD10063	482	355	65	No
104	OTOH	PRD10015	45	25	45	No
103	VUZZ	PRD10013	45	0	45	Yes
106	OTOH	PRD10010	139	139	139	No
110	OTOH	PRD10008	55	55	55	No
101	OTOH	PRD10013	450	425	450	No
50	0L72	PRD10018	82	70	31	No
53	2VLP	PRD10078	150	159	68	No
51	GDPP	PRD10053	203	210	71	No
105	VUZZ	PRD10015	87	87	87	No
108	0T0P	PRD10015	45	45	45	No
84	HOCN	PRD10008	258	270	70	No
109	OTOH	PRD10011	55	55	55	No
38	OTOH	PRD10009	182	217	134	No
\.


--
-- Data for Name: logistics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logistics (id, shipment_id, site_id, product_id, shipment_date, quantity, delivery_status, transportation_type, delivery_date, so_id, so_number, estimated_delivery, tracking_status_updated, tracking_notes) FROM stdin;
1	SHP90000	7EEQ	PRD10038	2024-07-15	76	Cancelled	Rail	\N	\N	\N	\N	\N	\N
2	SHP90001	NY20	PRD10050	2024-08-30	92	Delivered	Rail	\N	\N	\N	\N	\N	\N
3	SHP90002	0L72	PRD10049	2024-05-28	40	Delayed	Truck	\N	\N	\N	\N	\N	\N
4	SHP90003	58KX	PRD10001	2024-10-02	50	Delivered	Ship	\N	\N	\N	\N	\N	\N
5	SHP90004	4ZKL	PRD10053	2024-10-05	79	Cancelled	Rail	\N	\N	\N	\N	\N	\N
6	SHP90005	XDP5	PRD10060	2024-05-08	12	Cancelled	Truck	\N	\N	\N	\N	\N	\N
7	SHP90006	JI0Y	PRD10033	2024-07-20	15	Delivered	Ship	\N	\N	\N	\N	\N	\N
8	SHP90007	I3QK	PRD10036	2025-02-16	74	Delayed	Ship	\N	\N	\N	\N	\N	\N
9	SHP90008	KJLT	PRD10051	2024-05-13	91	Cancelled	Rail	\N	\N	\N	\N	\N	\N
10	SHP90009	GDPP	PRD10010	2024-09-06	20	Cancelled	Rail	\N	\N	\N	\N	\N	\N
11	SHP90010	FFYV	PRD10068	2024-09-15	60	Cancelled	Truck	\N	\N	\N	\N	\N	\N
12	SHP90011	P5TB	PRD10089	2024-11-10	40	Delivered	Rail	\N	\N	\N	\N	\N	\N
13	SHP90012	MYZY	PRD10055	2024-05-30	68	Cancelled	Truck	\N	\N	\N	\N	\N	\N
14	SHP90013	P5TB	PRD10085	2025-03-03	32	Delivered	Truck	\N	\N	\N	\N	\N	\N
15	SHP90014	OTOH	PRD10017	2025-03-26	11	Delivered	Ship	\N	\N	\N	\N	\N	\N
16	SHP90015	8CGV	PRD10066	2024-12-21	43	Delivered	Air	\N	\N	\N	\N	\N	\N
17	SHP90016	0T0P	PRD10095	2024-08-16	25	Delivered	Air	\N	\N	\N	\N	\N	\N
18	SHP90017	FKHM	PRD10034	2024-12-25	18	Delayed	Truck	\N	\N	\N	\N	\N	\N
19	SHP90018	0L72	PRD10058	2024-12-18	56	Delivered	Ship	\N	\N	\N	\N	\N	\N
20	SHP90019	4ZKL	PRD10021	2024-10-06	30	Delayed	Truck	\N	\N	\N	\N	\N	\N
21	SHP90020	4ZKL	PRD10086	2024-05-30	39	Cancelled	Truck	\N	\N	\N	\N	\N	\N
22	SHP90021	PKH1	PRD10001	2024-08-04	15	Delayed	Air	\N	\N	\N	\N	\N	\N
23	SHP90022	EXQ7	PRD10019	2024-07-01	14	Cancelled	Ship	\N	\N	\N	\N	\N	\N
24	SHP90023	SV87	PRD10041	2024-08-06	63	Cancelled	Air	\N	\N	\N	\N	\N	\N
25	SHP90024	GDPP	PRD10009	2025-01-18	57	Delivered	Truck	\N	\N	\N	\N	\N	\N
26	SHP90025	5JSG	PRD10028	2024-12-21	15	Delayed	Truck	\N	\N	\N	\N	\N	\N
27	SHP90026	T4UF	PRD10036	2024-09-07	51	Delivered	Ship	\N	\N	\N	\N	\N	\N
28	SHP90027	JI0Y	PRD10047	2024-07-12	47	Cancelled	Air	\N	\N	\N	\N	\N	\N
29	SHP90028	NY20	PRD10079	2024-08-03	69	Delayed	Ship	\N	\N	\N	\N	\N	\N
30	SHP90029	M5K8	PRD10099	2024-07-10	79	Delivered	Rail	\N	\N	\N	\N	\N	\N
31	SHP90030	JI0Y	PRD10052	2024-04-13	39	Cancelled	Air	\N	\N	\N	\N	\N	\N
32	SHP90031	W1Q5	PRD10088	2024-04-05	52	Delivered	Ship	\N	\N	\N	\N	\N	\N
33	SHP90032	NY20	PRD10093	2024-09-05	23	Delivered	Rail	\N	\N	\N	\N	\N	\N
34	SHP90033	93TY	PRD10062	2024-05-01	28	Cancelled	Air	\N	\N	\N	\N	\N	\N
35	SHP90034	MYZY	PRD10005	2024-07-28	76	Delayed	Air	\N	\N	\N	\N	\N	\N
36	SHP90035	T4UF	PRD10095	2024-05-14	84	Delivered	Rail	\N	\N	\N	\N	\N	\N
37	SHP90036	W1Q5	PRD10050	2024-05-09	85	Cancelled	Truck	\N	\N	\N	\N	\N	\N
38	SHP90037	FKHM	PRD10084	2024-06-06	40	Delayed	Air	\N	\N	\N	\N	\N	\N
39	SHP90038	HOCN	PRD10050	2025-03-25	51	Delayed	Ship	\N	\N	\N	\N	\N	\N
40	SHP90039	GDPP	PRD10029	2024-05-09	35	Delivered	Truck	\N	\N	\N	\N	\N	\N
41	SHP90040	FFYV	PRD10013	2024-06-24	67	Delayed	Air	\N	\N	\N	\N	\N	\N
42	SHP90041	93TY	PRD10015	2024-12-31	55	Delivered	Ship	\N	\N	\N	\N	\N	\N
43	SHP90042	P5TB	PRD10059	2024-08-14	25	Delivered	Rail	\N	\N	\N	\N	\N	\N
44	SHP90043	0RJI	PRD10038	2025-03-27	99	Cancelled	Truck	\N	\N	\N	\N	\N	\N
45	SHP90044	IUC0	PRD10041	2024-06-15	21	Cancelled	Rail	\N	\N	\N	\N	\N	\N
46	SHP90045	8CGV	PRD10050	2024-12-19	16	Cancelled	Air	\N	\N	\N	\N	\N	\N
47	SHP90046	4CIY	PRD10022	2024-04-16	61	Delayed	Rail	\N	\N	\N	\N	\N	\N
48	SHP90047	J7YH	PRD10059	2024-05-23	27	Delivered	Truck	\N	\N	\N	\N	\N	\N
49	SHP90048	30T9	PRD10099	2024-07-23	26	Delivered	Ship	\N	\N	\N	\N	\N	\N
50	SHP90049	CXUL	PRD10087	2025-02-17	92	Delivered	Air	\N	\N	\N	\N	\N	\N
51	SHP90050	CX19	PRD10002	2024-05-04	35	Cancelled	Ship	\N	\N	\N	\N	\N	\N
52	SHP90051	0T0P	PRD10011	2024-09-17	25	Delivered	Ship	\N	\N	\N	\N	\N	\N
53	SHP90052	30T9	PRD10021	2025-01-19	65	Cancelled	Ship	\N	\N	\N	\N	\N	\N
54	SHP90053	0L72	PRD10003	2024-10-13	97	Delayed	Rail	\N	\N	\N	\N	\N	\N
55	SHP90054	8CGV	PRD10027	2024-07-05	45	Delayed	Ship	\N	\N	\N	\N	\N	\N
56	SHP90055	FFYV	PRD10004	2025-02-09	89	Cancelled	Rail	\N	\N	\N	\N	\N	\N
57	SHP90056	A11D	PRD10037	2024-12-12	62	Cancelled	Ship	\N	\N	\N	\N	\N	\N
58	SHP90057	30T9	PRD10011	2024-08-22	59	Delivered	Ship	\N	\N	\N	\N	\N	\N
59	SHP90058	T2TA	PRD10082	2024-12-26	41	Cancelled	Truck	\N	\N	\N	\N	\N	\N
60	SHP90059	EXQ7	PRD10091	2024-10-01	71	Cancelled	Ship	\N	\N	\N	\N	\N	\N
61	SHP90060	8CGV	PRD10072	2024-12-14	51	Delayed	Air	\N	\N	\N	\N	\N	\N
62	SHP90061	5JSG	PRD10003	2024-09-11	86	Delivered	Truck	\N	\N	\N	\N	\N	\N
63	SHP90062	M5K8	PRD10035	2024-04-30	70	Cancelled	Air	\N	\N	\N	\N	\N	\N
64	SHP90063	M5K8	PRD10074	2024-07-29	30	Delivered	Rail	\N	\N	\N	\N	\N	\N
65	SHP90064	7EEQ	PRD10030	2024-08-15	78	Cancelled	Truck	\N	\N	\N	\N	\N	\N
66	SHP90065	XDP5	PRD10028	2025-01-20	59	Delayed	Rail	\N	\N	\N	\N	\N	\N
67	SHP90066	5JSG	PRD10030	2025-01-29	50	Cancelled	Air	\N	\N	\N	\N	\N	\N
68	SHP90067	P7Y6	PRD10003	2025-03-27	99	Delayed	Rail	\N	\N	\N	\N	\N	\N
69	SHP90068	4ZKL	PRD10024	2024-12-09	79	Delayed	Rail	\N	\N	\N	\N	\N	\N
70	SHP90069	0L72	PRD10004	2024-05-17	17	Delivered	Rail	\N	\N	\N	\N	\N	\N
71	SHP90070	VUZZ	PRD10067	2024-12-01	10	Delayed	Rail	\N	\N	\N	\N	\N	\N
72	SHP90071	0T0P	PRD10043	2024-06-30	51	Delivered	Truck	\N	\N	\N	\N	\N	\N
73	SHP90072	FFYV	PRD10075	2025-03-27	28	Delivered	Air	\N	\N	\N	\N	\N	\N
74	SHP90073	CX19	PRD10047	2025-03-27	94	Delayed	Truck	\N	\N	\N	\N	\N	\N
75	SHP90074	GHC0	PRD10038	2024-09-13	27	Delivered	Ship	\N	\N	\N	\N	\N	\N
76	SHP90075	W1Q5	PRD10062	2025-02-27	50	Delivered	Air	\N	\N	\N	\N	\N	\N
77	SHP90076	SV87	PRD10085	2025-01-27	32	Delayed	Air	\N	\N	\N	\N	\N	\N
78	SHP90077	AM14	PRD10088	2024-08-29	26	Delivered	Truck	\N	\N	\N	\N	\N	\N
79	SHP90078	KJLT	PRD10073	2024-10-18	82	Delivered	Rail	\N	\N	\N	\N	\N	\N
80	SHP90079	2VLP	PRD10040	2025-02-08	38	Cancelled	Truck	\N	\N	\N	\N	\N	\N
81	SHP90080	0L72	PRD10018	2024-09-17	19	Delivered	Air	\N	\N	\N	\N	\N	\N
82	SHP90081	HOCN	PRD10021	2025-02-20	21	Cancelled	Air	\N	\N	\N	\N	\N	\N
83	SHP90082	A1WJ	PRD10001	2024-08-14	36	Delivered	Truck	\N	\N	\N	\N	\N	\N
84	SHP90083	8CGV	PRD10032	2024-05-26	10	Delivered	Ship	\N	\N	\N	\N	\N	\N
85	SHP90084	A1WJ	PRD10093	2024-11-01	31	Delayed	Ship	\N	\N	\N	\N	\N	\N
86	SHP90085	EXQ7	PRD10044	2025-01-05	58	Delivered	Ship	\N	\N	\N	\N	\N	\N
87	SHP90086	4ZKL	PRD10083	2025-03-18	38	Delivered	Ship	\N	\N	\N	\N	\N	\N
88	SHP90087	CX19	PRD10004	2024-08-29	12	Delayed	Air	\N	\N	\N	\N	\N	\N
89	SHP90088	J7YH	PRD10009	2024-09-23	31	Delayed	Rail	\N	\N	\N	\N	\N	\N
90	SHP90089	AM14	PRD10009	2025-01-06	21	Delayed	Ship	\N	\N	\N	\N	\N	\N
91	SHP90090	OTOH	PRD10003	2024-11-07	93	Delivered	Ship	\N	\N	\N	\N	\N	\N
92	SHP90091	ZYTJ	PRD10006	2024-05-22	52	Delivered	Rail	\N	\N	\N	\N	\N	\N
93	SHP90092	93TY	PRD10089	2025-01-09	79	Delayed	Air	\N	\N	\N	\N	\N	\N
94	SHP90093	P5TB	PRD10030	2024-05-20	16	Delayed	Ship	\N	\N	\N	\N	\N	\N
95	SHP90094	FFYV	PRD10006	2024-10-02	10	Delayed	Truck	\N	\N	\N	\N	\N	\N
96	SHP90095	M5IG	PRD10084	2025-02-15	86	Delayed	Rail	\N	\N	\N	\N	\N	\N
97	SHP90096	J7YH	PRD10003	2024-07-15	31	Cancelled	Air	\N	\N	\N	\N	\N	\N
98	SHP90097	MYZY	PRD10060	2024-05-30	49	Delayed	Ship	\N	\N	\N	\N	\N	\N
99	SHP90098	0L72	PRD10084	2024-08-14	21	Cancelled	Ship	\N	\N	\N	\N	\N	\N
100	SHP90099	5JSG	PRD10047	2024-10-13	57	Delivered	Ship	\N	\N	\N	\N	\N	\N
101	SHP90100	PKH1	PRD10033	2024-11-12	69	Delayed	Rail	\N	\N	\N	\N	\N	\N
102	SHP90101	GDPP	PRD10072	2024-05-02	29	Cancelled	Truck	\N	\N	\N	\N	\N	\N
103	SHP90102	MYZY	PRD10085	2024-09-24	79	Delayed	Rail	\N	\N	\N	\N	\N	\N
104	SHP90103	PS3Y	PRD10007	2024-10-16	76	Delayed	Ship	\N	\N	\N	\N	\N	\N
105	SHP90104	4ZKL	PRD10030	2024-11-30	48	Delivered	Ship	\N	\N	\N	\N	\N	\N
106	SHP90105	OTOH	PRD10004	2024-12-14	83	Cancelled	Rail	\N	\N	\N	\N	\N	\N
107	SHP90106	H75L	PRD10096	2024-11-16	32	Delivered	Rail	\N	\N	\N	\N	\N	\N
108	SHP90107	T2TA	PRD10016	2024-04-22	64	Delivered	Ship	\N	\N	\N	\N	\N	\N
109	SHP90108	T2TA	PRD10080	2024-06-15	86	Delayed	Air	\N	\N	\N	\N	\N	\N
110	SHP90109	AM14	PRD10008	2024-05-15	59	Cancelled	Ship	\N	\N	\N	\N	\N	\N
111	SHP90110	PS3Y	PRD10041	2024-08-20	76	Delayed	Truck	\N	\N	\N	\N	\N	\N
112	SHP90111	KJLT	PRD10079	2025-01-26	76	Delayed	Truck	\N	\N	\N	\N	\N	\N
113	SHP90112	93TY	PRD10019	2024-06-15	82	Cancelled	Truck	\N	\N	\N	\N	\N	\N
114	SHP90113	J7YH	PRD10072	2024-05-22	46	Cancelled	Air	\N	\N	\N	\N	\N	\N
115	SHP90114	93TY	PRD10033	2024-10-14	93	Delayed	Ship	\N	\N	\N	\N	\N	\N
116	SHP90115	PKH1	PRD10022	2024-08-20	61	Delivered	Ship	\N	\N	\N	\N	\N	\N
117	SHP90116	PKH1	PRD10050	2024-09-17	98	Delivered	Truck	\N	\N	\N	\N	\N	\N
118	SHP90117	NY20	PRD10060	2024-08-16	57	Delivered	Air	\N	\N	\N	\N	\N	\N
119	SHP90118	P5TB	PRD10039	2024-08-22	72	Cancelled	Truck	\N	\N	\N	\N	\N	\N
120	SHP90119	SV87	PRD10017	2024-09-01	66	Delayed	Air	\N	\N	\N	\N	\N	\N
121	SHP90120	AM14	PRD10053	2025-02-04	92	Delivered	Rail	\N	\N	\N	\N	\N	\N
122	SHP90121	A1WJ	PRD10027	2024-10-26	72	Cancelled	Air	\N	\N	\N	\N	\N	\N
123	SHP90122	30T9	PRD10065	2024-06-21	18	Delayed	Ship	\N	\N	\N	\N	\N	\N
124	SHP90123	0T0P	PRD10099	2024-12-25	82	Delivered	Rail	\N	\N	\N	\N	\N	\N
125	SHP90124	T2TA	PRD10025	2024-04-30	41	Delivered	Ship	\N	\N	\N	\N	\N	\N
126	SHP90125	30T9	PRD10046	2025-03-27	35	Delayed	Air	\N	\N	\N	\N	\N	\N
127	SHP90126	T4UF	PRD10064	2024-10-21	91	Delivered	Truck	\N	\N	\N	\N	\N	\N
128	SHP90127	EIMV	PRD10047	2024-12-07	86	Delayed	Rail	\N	\N	\N	\N	\N	\N
129	SHP90128	ID25	PRD10075	2025-01-08	54	Delayed	Rail	\N	\N	\N	\N	\N	\N
130	SHP90129	4CIY	PRD10095	2025-03-19	21	Delayed	Truck	\N	\N	\N	\N	\N	\N
131	SHP90130	EXQ7	PRD10006	2024-06-23	83	Delivered	Rail	\N	\N	\N	\N	\N	\N
132	SHP90131	A11D	PRD10028	2025-03-13	36	Delayed	Ship	\N	\N	\N	\N	\N	\N
133	SHP90132	I3QK	PRD10002	2025-03-16	11	Delayed	Rail	\N	\N	\N	\N	\N	\N
134	SHP90133	A11D	PRD10022	2025-02-02	11	Delivered	Air	\N	\N	\N	\N	\N	\N
135	SHP90134	2VLP	PRD10039	2025-03-31	100	Cancelled	Air	\N	\N	\N	\N	\N	\N
136	SHP90135	FKHM	PRD10048	2024-09-26	68	Delayed	Rail	\N	\N	\N	\N	\N	\N
137	SHP90136	T4UF	PRD10038	2025-03-13	76	Cancelled	Ship	\N	\N	\N	\N	\N	\N
138	SHP90137	P7Y6	PRD10013	2024-04-04	75	Cancelled	Air	\N	\N	\N	\N	\N	\N
139	SHP90138	PS3Y	PRD10082	2025-01-30	87	Delayed	Air	\N	\N	\N	\N	\N	\N
140	SHP90139	0RJI	PRD10013	2024-12-03	18	Delayed	Air	\N	\N	\N	\N	\N	\N
141	SHP90140	W1Q5	PRD10041	2024-08-20	43	Cancelled	Air	\N	\N	\N	\N	\N	\N
142	SHP90141	T2TA	PRD10019	2024-12-21	40	Delivered	Ship	\N	\N	\N	\N	\N	\N
144	SHP90143	A11D	PRD10063	2024-08-30	43	Delayed	Ship	\N	\N	\N	\N	\N	\N
145	SHP90144	EXQ7	PRD10094	2024-04-19	84	Cancelled	Rail	\N	\N	\N	\N	\N	\N
146	SHP90145	GHC0	PRD10092	2024-07-23	97	Cancelled	Ship	\N	\N	\N	\N	\N	\N
147	SHP90146	7EEQ	PRD10045	2024-12-16	48	Delivered	Rail	\N	\N	\N	\N	\N	\N
148	SHP90147	M5IG	PRD10012	2024-11-28	26	Cancelled	Air	\N	\N	\N	\N	\N	\N
149	SHP90148	AM14	PRD10071	2024-07-03	97	Delayed	Truck	\N	\N	\N	\N	\N	\N
150	SHP90149	SV87	PRD10045	2024-07-24	49	Delayed	Air	\N	\N	\N	\N	\N	\N
153	SHP-J5M6T3RN	FKHM	PRD10014	2026-04-30	1	Delivered	Truck	2026-05-04	\N	\N	\N	\N	\N
152	SHP-UDOVQQNB	OTOH	PRD10008	2026-04-30	15	Delivered	Truck	2026-05-04	\N	\N	\N	\N	\N
157	SHP-75XP6H8A	OTOH	PRD10015	2026-05-06	20	Dispatched	Air		\N	\N	\N	\N	\N
143	SHP90142	7EEQ	PRD10040	2025-03-15	27	Delivered	Truck	2026-05-05	\N	\N	\N	\N	\N
154	SHP-I98W3ITO	ID25	PRD10084	2026-05-04	48	Delivered	Train	2026-05-05	\N	\N	\N	\N	\N
151	SHP-MIN6JNAG	OTOH	PRD10013	2026-04-30	10	Delivered	Truck	2026-05-05	\N	\N	\N	\N	\N
156	SHP-4DS7F19M	M5K8	PRD10016	2026-05-05	50	Dispatched	Truck		\N	\N	\N	\N	\N
155	SHP-24QXZGTL	2VLP	PRD10078	2026-05-05	45	Delivered	Truck	2026-05-06	\N	\N	\N	\N	\N
161	SHP-92Z3ON0X	OTOH	PRD10013	2026-05-07	15	Dispatched	Truck		\N	\N	\N	\N	\N
159	SHP-FITWG6EP	VUZZ	PRD10013	2026-05-07	140	Delivered	Truck	2026-05-07	10	SO-W7LGQP	\N	\N	\N
160	SHP-7MRM2RVW	ID25	PRD10015	2026-05-07	12	Delivered	Truck	2026-05-07	11	SO-CXYKY9	\N	\N	\N
162	SHP-IZGEUETZ	0L72	PRD10018	2026-05-07	16	Delivered	Truck	2026-05-07	\N	\N	\N	\N	\N
163	SHP-N4JHG1YA	2VLP	PRD10078	2026-05-07	1	In Transit	Air		\N	\N	\N	\N	\N
158	SHP-XGNR8WGQ		PRD10015	2026-05-07	10	In Transit	Truck		9	SO-0F9E40	\N	\N	\N
164	SHP-0QVGOEU8	MYZY	PRD10063	2026-05-08	150	Delivered	Train	2026-05-09	\N	\N	\N	\N	\N
165	SHP-5VL7ANMD	GDPP	PRD10053	2026-05-08	55	Delivered	Truck	2026-05-09	\N	\N	\N	\N	\N
166	SHP-Z72OE256	MYZY	PRD10013	2026-05-10	125	In Transit	Air		17	SO-P13M18	\N	\N	\N
167	SHP-CLFUVLSJ	W1Q5	PRD10005	2026-05-11	10	In Transit	Air		18	SO-GV9377	\N	\N	\N
168	SHP-BGOHAU12	GDPP	PRD10015	2026-05-13	12	In Transit	Truck		19	SO-2JTE03	\N	\N	\N
169	SHP-8NG5ELF2	ID25	PRD10014	2026-05-14	12	In Transit	Air		\N	\N	\N	\N	\N
171	SHP-84KOETEO	VUZZ	PRD10013	2026-05-14	45	In Transit	Air		22	SO-DAXM7X	\N	\N	\N
170	SHP-WG4B11BV	H75L	PRD10008	2026-05-14	50	Delivered	Truck	2026-05-16	\N	\N	\N	\N	\N
173	SHP-22WLF7PN	MYZY	PRD10010	2026-05-15	16	In Transit	Truck		23	SO-2OOEJS	\N	\N	\N
172	SHP-BWSVYET9	MYZY	PRD10013	2026-05-15	120	Delivered	Truck	2026-05-15	23	SO-2OOEJS	\N	\N	\N
174	SHP-N4QKZU10	GDPP	PRD10013	2026-05-16	120	In Transit	Truck		24	SO-YOYUA9	\N	\N	\N
\.


--
-- Data for Name: managers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.managers (id, user_id, site_id) FROM stdin;
1	2	OTOH
2	4	8CGV
7	9	\N
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (id, product_id, product_name, category, subcategory, unit_cost, unit_price, supplier, shelf_life, uom, reorder_point, reorder_qty, default_warehouse, status, created_at, updated_at) FROM stdin;
1	PRD10000	Cheese Item 0	Dairy	Cheese	127.63	143.9	Supplier 1	12	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
2	PRD10001	Bread Item 1	Bakery	Bread	422.83	570.2	Supplier 4	37	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
3	PRD10002	Accessories Item 2	Electronics	Accessories	74.91	110.8	Supplier 8	70	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
4	PRD10003	Men Item 3	Apparel	Men	310.83	461.74	Supplier 2	46	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
6	PRD10005	Laptop Item 5	Electronics	Laptop	471.91	556.54	Supplier 10	165	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
7	PRD10006	Bread Item 6	Bakery	Bread	354.65	432.9	Supplier 10	35	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
8	PRD10007	Cheese Item 7	Dairy	Cheese	275.72	376.25	Supplier 2	134	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
9	PRD10008	Men Item 8	Apparel	Men	427.8	611.3	Supplier 2	115	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
10	PRD10009	Kids Item 9	Apparel	Kids	447.96	575.13	Supplier 3	116	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
11	PRD10010	Cookies Item 10	Bakery	Cookies	270.44	367.85	Supplier 10	142	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
12	PRD10011	Laptop Item 11	Electronics	Laptop	229.08	318.97	Supplier 5	87	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
13	PRD10012	Bread Item 12	Bakery	Bread	153.89	197.03	Supplier 8	150	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
14	PRD10013	Laptop Item 13	Electronics	Laptop	33.78	48.66	Supplier 3	129	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
15	PRD10014	Cakes Item 14	Bakery	Cakes	402.96	498.11	Supplier 10	75	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
16	PRD10015	Yogurt Item 15	Dairy	Yogurt	475.07	538.85	Supplier 7	130	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
17	PRD10016	Cookies Item 16	Bakery	Cookies	248.52	344.13	Supplier 8	9	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
18	PRD10017	Cheese Item 17	Dairy	Cheese	126.37	173.98	Supplier 5	174	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
19	PRD10018	Women Item 18	Apparel	Women	285.67	353.52	Supplier 9	89	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
20	PRD10019	Kids Item 19	Apparel	Kids	237.8	290.75	Supplier 4	35	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
21	PRD10020	Cakes Item 20	Bakery	Cakes	77.39	101.72	Supplier 3	54	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
22	PRD10021	Cookies Item 21	Bakery	Cookies	252.42	350.82	Supplier 9	157	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
23	PRD10022	Men Item 22	Apparel	Men	419.66	511.36	Supplier 6	50	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
24	PRD10023	Men Item 23	Apparel	Men	359.85	414.06	Supplier 1	18	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
25	PRD10024	Kids Item 24	Apparel	Kids	473.16	641.2	Supplier 8	31	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
26	PRD10025	Yogurt Item 25	Dairy	Yogurt	156.48	202.09	Supplier 6	52	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
27	PRD10026	Cheese Item 26	Dairy	Cheese	471.71	609.02	Supplier 2	107	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
28	PRD10027	Mobile Item 27	Electronics	Mobile	296.97	408.21	Supplier 3	43	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
29	PRD10028	Men Item 28	Apparel	Men	497.08	570.34	Supplier 7	160	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
30	PRD10029	Cookies Item 29	Bakery	Cookies	202.58	296.46	Supplier 5	155	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
31	PRD10030	Laptop Item 30	Electronics	Laptop	292.94	329.29	Supplier 2	58	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
32	PRD10031	Cakes Item 31	Bakery	Cakes	337.01	391.88	Supplier 3	146	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
33	PRD10032	Milk Item 32	Dairy	Milk	21.28	27.24	Supplier 10	125	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
34	PRD10033	Men Item 33	Apparel	Men	131.11	181.3	Supplier 8	23	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
35	PRD10034	Cakes Item 34	Bakery	Cakes	398.16	537.53	Supplier 4	113	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
36	PRD10035	Yogurt Item 35	Dairy	Yogurt	127.91	148.32	Supplier 5	41	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
37	PRD10036	Milk Item 36	Dairy	Milk	99.64	121.86	Supplier 10	78	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
38	PRD10037	Mobile Item 37	Electronics	Mobile	244.98	299.28	Supplier 7	74	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
39	PRD10038	Laptop Item 38	Electronics	Laptop	58.61	65.41	Supplier 7	87	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
40	PRD10039	Men Item 39	Apparel	Men	63.84	94.79	Supplier 10	155	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
41	PRD10040	Yogurt Item 40	Dairy	Yogurt	414.28	551.2	Supplier 3	125	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
42	PRD10041	Laptop Item 41	Electronics	Laptop	107.11	142.9	Supplier 8	28	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
43	PRD10042	Laptop Item 42	Electronics	Laptop	216.01	265.35	Supplier 2	46	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
44	PRD10043	Women Item 43	Apparel	Women	352.96	428.95	Supplier 7	145	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
45	PRD10044	Cheese Item 44	Dairy	Cheese	62.27	74.78	Supplier 2	108	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
46	PRD10045	Yogurt Item 45	Dairy	Yogurt	437.3	561.84	Supplier 1	53	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
47	PRD10046	Kids Item 46	Apparel	Kids	383.09	517.23	Supplier 1	57	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
48	PRD10047	Kids Item 47	Apparel	Kids	82.89	100.73	Supplier 8	36	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
49	PRD10048	Yogurt Item 48	Dairy	Yogurt	312.26	373.38	Supplier 3	84	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
50	PRD10049	Yogurt Item 49	Dairy	Yogurt	215.84	256.82	Supplier 2	123	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
51	PRD10050	Yogurt Item 50	Dairy	Yogurt	419.43	544.99	Supplier 5	135	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
52	PRD10051	Women Item 51	Apparel	Women	420.67	627.68	Supplier 4	121	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
53	PRD10052	Cakes Item 52	Bakery	Cakes	111.49	149.37	Supplier 3	22	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
54	PRD10053	Women Item 53	Apparel	Women	183.14	259.16	Supplier 5	5	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
55	PRD10054	Kids Item 54	Apparel	Kids	163.31	217.98	Supplier 8	43	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
56	PRD10055	Accessories Item 55	Electronics	Accessories	252.48	311.3	Supplier 9	101	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
57	PRD10056	Laptop Item 56	Electronics	Laptop	437.41	652.75	Supplier 4	151	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
58	PRD10057	Mobile Item 57	Electronics	Mobile	430.89	544.78	Supplier 6	126	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
59	PRD10058	Laptop Item 58	Electronics	Laptop	494.44	700.6	Supplier 3	131	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
60	PRD10059	Milk Item 59	Dairy	Milk	261.1	348.85	Supplier 2	117	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
61	PRD10060	Yogurt Item 60	Dairy	Yogurt	457.01	505.52	Supplier 3	109	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
62	PRD10061	Bread Item 61	Bakery	Bread	245.36	365.02	Supplier 6	164	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
63	PRD10062	Accessories Item 62	Electronics	Accessories	58.55	72.1	Supplier 9	102	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
64	PRD10063	Kids Item 63	Apparel	Kids	364.98	512.34	Supplier 9	14	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
65	PRD10064	Milk Item 64	Dairy	Milk	322.96	474.23	Supplier 4	28	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
66	PRD10065	Mobile Item 65	Electronics	Mobile	384.98	531.87	Supplier 2	118	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
67	PRD10066	Cookies Item 66	Bakery	Cookies	163.74	182.01	Supplier 6	19	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
68	PRD10067	Women Item 67	Apparel	Women	199.92	231.55	Supplier 9	110	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
69	PRD10068	Bread Item 68	Bakery	Bread	104.03	139.8	Supplier 7	163	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
70	PRD10069	Cakes Item 69	Bakery	Cakes	458.16	530.2	Supplier 8	168	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
71	PRD10070	Women Item 70	Apparel	Women	142.56	157.35	Supplier 8	78	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
72	PRD10071	Bread Item 71	Bakery	Bread	232.03	287.31	Supplier 10	81	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
73	PRD10072	Accessories Item 72	Electronics	Accessories	140.05	201.41	Supplier 4	103	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
74	PRD10073	Mobile Item 73	Electronics	Mobile	133.86	177.87	Supplier 10	80	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
75	PRD10074	Men Item 74	Apparel	Men	489.41	667.21	Supplier 5	7	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
76	PRD10075	Yogurt Item 75	Dairy	Yogurt	377.68	541.27	Supplier 5	63	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
77	PRD10076	Men Item 76	Apparel	Men	325.58	439	Supplier 3	165	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
78	PRD10077	Yogurt Item 77	Dairy	Yogurt	330.24	404.07	Supplier 8	13	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
79	PRD10078	Kids Item 78	Apparel	Kids	83.08	121.62	Supplier 6	111	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
80	PRD10079	Bread Item 79	Bakery	Bread	83.44	109.79	Supplier 6	140	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
81	PRD10080	Men Item 80	Apparel	Men	143.35	204.97	Supplier 8	80	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
82	PRD10081	Men Item 81	Apparel	Men	244.8	276.65	Supplier 4	178	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
83	PRD10082	Accessories Item 82	Electronics	Accessories	195.57	276.98	Supplier 1	72	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
84	PRD10083	Cheese Item 83	Dairy	Cheese	196.92	275.61	Supplier 5	154	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
85	PRD10084	Accessories Item 84	Electronics	Accessories	471.34	538.9	Supplier 4	125	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
86	PRD10085	Yogurt Item 85	Dairy	Yogurt	444.43	588.68	Supplier 10	61	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
87	PRD10086	Yogurt Item 86	Dairy	Yogurt	415.45	608.12	Supplier 5	171	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
88	PRD10087	Mobile Item 87	Electronics	Mobile	87.09	128.76	Supplier 5	131	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
89	PRD10088	Milk Item 88	Dairy	Milk	132.7	174.5	Supplier 7	121	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
90	PRD10089	Kids Item 89	Apparel	Kids	475.7	655.8	Supplier 9	112	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
91	PRD10090	Cakes Item 90	Bakery	Cakes	334.36	479.3	Supplier 10	109	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
92	PRD10091	Men Item 91	Apparel	Men	351.33	417	Supplier 8	65	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
93	PRD10092	Men Item 92	Apparel	Men	490.85	612.06	Supplier 6	20	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
94	PRD10093	Laptop Item 93	Electronics	Laptop	111.11	127.65	Supplier 8	28	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
95	PRD10094	Cookies Item 94	Bakery	Cookies	326.96	486.66	Supplier 1	90	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
96	PRD10095	Bread Item 95	Bakery	Bread	397.75	470.17	Supplier 9	58	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
97	PRD10096	Bread Item 96	Bakery	Bread	177.71	205.97	Supplier 10	5	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
98	PRD10097	Men Item 97	Apparel	Men	494.01	650.16	Supplier 3	33	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
99	PRD10098	Milk Item 98	Dairy	Milk	27.13	38.42	Supplier 4	155	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
100	PRD10099	Men Item 99	Apparel	Men	103.64	116.18	Supplier 7	139	Unit	0	0	\N	Active	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
101	PRD10101	shirt	Apparel	Men	450	550	Kishan	0	Unit	0	0	\N	Active	2026-05-07 09:07:02.749009	2026-05-07 09:07:02.749019
\.


--
-- Data for Name: promotions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.promotions (id, promotion_id, product_id, site_id, start_date, end_date, discount_type, discount_amount) FROM stdin;
1	PROMO10000	PRD10033	CXUL	2024-08-29	2024-12-25	Percentage	20
2	PROMO10001	PRD10081	30T9	2024-05-07	2025-01-03	Percentage	21
3	PROMO10002	PRD10087	H75L	2024-10-13	2025-02-25	Flat	23.59
4	PROMO10003	PRD10017	FFYV	2024-07-12	2025-01-03	Flat	49.42
5	PROMO10004	PRD10018	T4UF	2024-09-09	2025-03-11	Percentage	29
6	PROMO10005	PRD10062	MYZY	2024-09-18	2025-02-26	Percentage	15
7	PROMO10006	PRD10007	W1Q5	2024-04-03	2024-11-20	Flat	14.42
8	PROMO10007	PRD10021	M5K8	2024-06-21	2025-02-26	Percentage	9
9	PROMO10008	PRD10055	WM31	2024-11-06	2025-02-17	Flat	48.44
10	PROMO10009	PRD10000	EXQ7	2024-04-20	2025-01-18	Percentage	28
11	PROMO10010	PRD10001	CXUL	2024-09-12	2025-03-24	Percentage	5
12	PROMO10011	PRD10000	0RJI	2024-08-06	2024-10-02	Flat	19.04
13	PROMO10012	PRD10049	J7YH	2024-12-14	2025-02-27	Flat	12.52
14	PROMO10013	PRD10038	PKH1	2024-08-27	2024-12-21	Flat	24.51
15	PROMO10014	PRD10017	0RJI	2024-09-23	2025-01-26	Flat	38.76
16	PROMO10015	PRD10051	ZYTJ	2024-04-10	2024-08-04	Percentage	28
17	PROMO10016	PRD10027	0T0P	2024-04-12	2025-02-07	Percentage	8
18	PROMO10017	PRD10091	CXUL	2024-04-20	2024-10-29	Flat	39.71
19	PROMO10018	PRD10006	WM31	2024-04-25	2025-03-29	Percentage	25
20	PROMO10019	PRD10006	VUZZ	2024-05-30	2024-12-29	Flat	22.11
21	PROMO10020	PRD10032	PS3Y	2024-11-29	2025-02-26	Percentage	11
22	PROMO10021	PRD10087	KJLT	2024-04-05	2024-09-06	Flat	34.77
23	PROMO10022	PRD10066	7EEQ	2024-08-17	2025-01-23	Percentage	18
24	PROMO10023	PRD10065	J7YH	2024-05-31	2024-10-22	Percentage	30
25	PROMO10024	PRD10063	J7YH	2024-07-11	2024-10-21	Flat	42.42
26	PROMO10025	PRD10045	T2TA	2024-10-27	2025-01-10	Percentage	6
27	PROMO10026	PRD10063	PS3Y	2024-07-16	2025-03-19	Flat	15.55
28	PROMO10027	PRD10085	JI0Y	2024-05-16	2024-07-11	Flat	11.71
29	PROMO10028	PRD10099	MYZY	2024-12-18	2024-12-27	Percentage	13
30	PROMO10029	PRD10029	A11D	2024-11-20	2025-02-03	Flat	25.89
31	PROMO10030	PRD10022	J7YH	2024-04-21	2024-09-16	Flat	41.07
32	PROMO10031	PRD10054	HOCN	2024-05-30	2024-07-17	Percentage	5
33	PROMO10032	PRD10084	0T0P	2024-06-27	2024-12-12	Flat	45.25
34	PROMO10033	PRD10034	WM31	2024-05-18	2024-11-24	Flat	13.23
35	PROMO10034	PRD10051	SEMC	2024-11-20	2025-01-28	Flat	36.05
36	PROMO10035	PRD10053	ID25	2024-06-25	2024-08-21	Percentage	27
37	PROMO10036	PRD10007	AM14	2024-06-21	2024-08-13	Flat	46.01
38	PROMO10037	PRD10072	ID25	2024-11-11	2024-12-27	Flat	40.06
39	PROMO10038	PRD10003	WM31	2024-06-06	2025-02-08	Flat	10.08
40	PROMO10039	PRD10056	93TY	2024-04-24	2024-05-26	Flat	34.47
41	PROMO10040	PRD10090	JI0Y	2024-12-25	2025-03-30	Percentage	26
42	PROMO10041	PRD10066	GHC0	2024-12-24	2025-03-22	Percentage	18
43	PROMO10042	PRD10093	7EEQ	2024-08-06	2024-12-07	Flat	34.87
44	PROMO10043	PRD10049	A11D	2024-06-16	2025-03-28	Percentage	5
45	PROMO10044	PRD10020	A11D	2024-12-15	2025-02-13	Flat	44.12
46	PROMO10045	PRD10096	CX19	2024-12-08	2025-01-18	Percentage	15
47	PROMO10046	PRD10006	GDPP	2024-12-16	2025-01-13	Flat	23.15
48	PROMO10047	PRD10010	EIMV	2024-11-22	2025-03-15	Flat	8.96
49	PROMO10048	PRD10057	0L72	2024-09-09	2024-10-09	Flat	38.54
50	PROMO10049	PRD10013	VUZZ	2024-10-24	2025-02-06	Percentage	22
\.


--
-- Data for Name: purchase_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.purchase_orders (id, po_number, supplier, product_name, product_id, quantity, unit_cost, total_cost, status, site, expected_delivery, created_at, created_by, approved_at, role, manager_user_id, notes, rejection_reason, received_at, cancelled_at, cancel_reason, supplier_id, supplier_approval_token, supplier_token_expiry, supplier_action, supplier_actioned_at, supplier_reject_reason, approved_by) FROM stdin;
1	PO-YFXG25	Supplier 3	Laptop Item 11	PRD10011	100	229.08	22908	Approved	0T0P - Digital Bangalore	2026-05-10	2026-04-30	Admin	2026-04-30	admin	0						\N	\N	\N	\N	\N	\N	
2	PO-0ZR6SC	Supplier 1	Laptop Item 13	PRD10013	45	33.78	1520.1000000000001	Approved	VUZZ - Digital Ahmedabad	2026-05-06	2026-05-04	Admin	2026-05-04	admin	0						\N	\N	\N	\N	\N	\N	
3	PO-N78EYL	Kishan	Yogurt Item 15	PRD10015	45	475.07	21378.15	Approved	OTOH - Digital Ahmedabad	2026-05-09	2026-05-05	Ishan	2026-05-05	manager	2						\N	\N	\N	\N	\N	\N	
4	PO-N9V7CD	Arjun	Yogurt Item 15	PRD10015	24	475.07	11401.68	Approved	VUZZ - Digital Ahmedabad	2026-05-09	2026-05-06	Admin	2026-05-06	admin	0						\N	\N	\N	\N	\N	\N	
5	PO-2R6YVP			PRD10010	139	0	0	Approved	OTOH		2026-05-07	Ishan	2026-05-07	manager	2						\N	\N	\N	\N	\N	\N	
6	PO-WXJA1K	Kishan	Kids Item 9	PRD10009	45	447.96	20158.2	Approved	OTOH - Digital Ahmedabad	2026-05-08	2026-05-07	Admin	2026-05-07	admin	0						\N	\N	\N	\N	\N	\N	
7	PO-HBLHHU			PRD10014	45	0	0	Approved	OTOH		2026-05-07	Ishan	2026-05-07	manager	2						\N	\N	\N	\N	\N	\N	
8	PO-TRJ2JC	Nithesh	Yogurt Item 15	PRD10015	63	475.07	29929.41	Approved	VUZZ - Digital Ahmedabad	2026-05-11	2026-05-08	Admin	2026-05-08	admin	0						\N	\N	\N	\N	\N	\N	
9	PO-W5IB9L			PRD10009	123	0	0	Approved			2026-05-11	kanakadri	2026-05-11	manager	7						\N	\N	\N	\N	\N	\N	
10	PO-UXMUOE	Nithesh	Yogurt Item 15	PRD10015	45	475.07	21378.15	Approved	0T0P - Digital Bangalore	2026-05-16	2026-05-14	Admin	2026-05-14	admin	0						\N	\N	\N	\N	\N	\N	
11	PO-RA7NKK	Arjun	Men Item 8	PRD10008	55	427.8	23529	Approved	HOCN - Digital Coimbatore	2026-05-22	2026-05-14	Admin	2026-05-14	admin	0						\N	\N	\N	\N	\N	\N	
12	PO-EKA3MN			PRD10014	45	0	0	Cancelled	OTOH		2026-05-14	Ishan		manager	2						\N	\N	\N	\N	\N	\N	
13	PO-IFK1IO			PRD10005	55	0	0	Cancelled	OTOH		2026-05-14	Ishan		manager	2						\N	\N	\N	\N	\N	\N	
14	PO-E12V7F	Supplier 5	Laptop Item 11	PRD10011	55	229.08	12599.4	Approved	OTOH		2026-05-15	Ishan	2026-05-15	manager	2						\N	\N	\N	\N	\N	\N	
15	PO-IDDI7P	Supplier 3	Kids Item 9	PRD10009	45	447.96	20158.2	Approved	OTOH		2026-05-16	Ishan	2026-05-16	manager	2						\N	\N	\N	\N	\N	\N	
16	PO-NTKUKF	Supplier 2	Men Item 8	PRD10008	55	427.8	23529	Approved	OTOH		2026-05-16	Ishan	2026-05-16	manager	2						\N	\N	\N	\N	\N	\N	
\.


--
-- Data for Name: purchase_returns; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.purchase_returns (id, return_number, po_number, supplier, site, return_reason, product_name, product_id, quantity, unit_cost, total_credit, status, notes, created_at, created_by, approved_at, approved_by, role, manager_user_id) FROM stdin;
1	PR-W44FY5	PO-RA7NKK	Arjun	HOCN - Digital Coimbatore	Defective / Damaged	Men Item 8	PRD10008	1	427.8	427.8	Approved	asdf	2026-05-15	Admin	2026-05-15	Admin	admin	0
2	PR-1M5ZK6	PO-NTKUKF	Supplier 2	OTOH	Wrong Item Supplied	Men Item 8	PRD10008	1	427.8	427.8	Approved		2026-05-16	Ishan	2026-05-16	Ishan	manager	0
3	PR-8PSHNC	PO-TRJ2JC	Nithesh	VUZZ - Digital Ahmedabad	Defective / Damaged	Yogurt Item 15	PRD10015	1	475.07	475.07	Approved		2026-05-19	Admin	2026-05-19	Admin	admin	0
\.


--
-- Data for Name: sales; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sales (id, date, site_id, product_id, units_sold, revenue, discounts, returns, customer_id) FROM stdin;
1	2024-02-04	XDP5	PRD10002	20	4844.84	764.83	3	CUST200026
2	2024-03-04	PS3Y	PRD10020	27	9001.49	1639.15	3	CUST200048
3	2024-09-04	8CGV	PRD10008	23	3122.03	463.83	0	CUST200025
4	2024-09-04	4CIY	PRD10070	38	11323.57	1275.45	1	CUST200048
5	2024-01-05	ZYTJ	PRD10056	27	6815.89	549.38	4	CUST200012
6	2024-01-05	M5K8	PRD10011	42	12414.53	1617.28	5	CUST200000
7	2024-02-05	OTOH	PRD10017	34	4063.82	401.33	5	CUST200036
8	2024-02-05	PS3Y	PRD10064	13	3833.66	277.86	2	CUST200016
9	2024-05-05	MYZY	PRD10010	6	1363.8	220.51	2	CUST200010
10	2024-05-05	58KX	PRD10069	33	13116.77	1654.59	0	CUST200023
11	2024-05-05	EIMV	PRD10099	42	8225.18	883.62	4	CUST200039
12	2024-08-05	A1WJ	PRD10059	44	11806.64	817.61	4	CUST200002
13	2024-09-05	5JSG	PRD10098	41	10544.22	1720.47	4	CUST200036
14	2024-09-05	7EEQ	PRD10081	26	5054.12	860.03	5	CUST200037
15	2024-10-05	4ZKL	PRD10017	34	6668.62	647.91	2	CUST200041
16	2024-12-05	HOCN	PRD10077	10	515.27	47.02	5	CUST200004
17	2024-12-05	GDPP	PRD10056	43	9611.66	1355.83	3	CUST200022
18	2024-02-06	93TY	PRD10045	43	20284.92	2301.13	5	CUST200012
19	2024-02-06	GDPP	PRD10057	16	1401.94	80.74	3	CUST200015
20	2024-03-06	58KX	PRD10019	20	1980.71	194.9	5	CUST200004
21	2024-06-06	PS3Y	PRD10007	38	18208.83	2444.58	5	CUST200011
22	2024-06-06	EXQ7	PRD10068	46	6000.84	802.96	5	CUST200027
23	2024-06-06	XDP5	PRD10047	33	9556.56	935.28	3	CUST200014
24	2024-10-06	PKH1	PRD10036	31	10977.55	777.42	5	CUST200016
25	2024-11-06	ID25	PRD10041	16	372.46	40.05	3	CUST200008
26	2024-03-07	0T0P	PRD10008	46	18058.28	2142.65	2	CUST200028
27	2024-08-07	SV87	PRD10017	10	570.39	100.77	0	CUST200003
28	2024-09-07	M5K8	PRD10044	23	8490.27	1467.48	1	CUST200034
29	2024-10-07	GHC0	PRD10029	25	7337.47	637.33	4	CUST200049
30	2024-01-08	EIMV	PRD10006	43	19543	1638.7	1	CUST200046
31	2024-02-08	4ZKL	PRD10053	12	4066.78	255.56	2	CUST200022
32	2024-02-08	IUC0	PRD10008	7	2135.65	249.8	5	CUST200029
33	2024-02-08	SV87	PRD10038	46	4107.29	490.63	0	CUST200037
34	2024-06-08	H75L	PRD10003	48	5246.55	669.78	4	CUST200042
35	2024-09-08	M5IG	PRD10041	8	189.68	30.74	1	CUST200026
36	2024-09-08	JI0Y	PRD10095	14	4166.25	236.62	2	CUST200020
37	2024-02-09	ID25	PRD10031	44	9456.67	1116.19	5	CUST200011
38	2024-02-09	FFYV	PRD10084	34	4287.42	407.63	0	CUST200033
39	2024-05-09	0L72	PRD10002	6	2842.27	357.6	1	CUST200018
40	2024-06-09	A11D	PRD10089	43	8950.01	1246.34	0	CUST200049
41	2024-06-09	PS3Y	PRD10048	42	16799.91	2889.21	5	CUST200000
42	2024-08-09	7EEQ	PRD10032	24	11465.39	1754.47	3	CUST200009
43	2024-08-09	4ZKL	PRD10054	37	7922.55	1156.86	2	CUST200029
44	2024-08-09	T2TA	PRD10097	11	2850.84	362.65	3	CUST200017
45	2024-09-09	FFYV	PRD10056	5	1225.41	177.33	2	CUST200038
46	2024-02-10	KJLT	PRD10030	4	1362.15	163.2	1	CUST200010
47	2024-03-10	VUZZ	PRD10046	20	2130.52	174.98	3	CUST200002
48	2024-05-10	XDP5	PRD10018	13	4019.37	442.97	0	CUST200025
49	2024-06-10	H75L	PRD10097	18	5320.22	910.2	4	CUST200015
50	2024-07-10	HOCN	PRD10052	3	870.04	72.38	1	CUST200047
51	2024-10-10	MYZY	PRD10087	43	18910.79	1322.78	2	CUST200024
52	2024-01-11	ZYTJ	PRD10025	39	3370.82	294.95	5	CUST200010
53	2024-10-11	MYZY	PRD10028	29	12894.05	2444.34	3	CUST200013
54	2024-12-11	EXQ7	PRD10043	12	3098.13	386.12	4	CUST200032
55	2024-01-12	58KX	PRD10048	21	10063.39	1197.04	4	CUST200037
56	2024-01-12	A11D	PRD10025	49	23651.26	2321.97	5	CUST200049
57	2024-02-12	IUC0	PRD10042	20	9587.39	501.42	1	CUST200042
58	2024-03-12	CXUL	PRD10070	7	2530.31	322.33	0	CUST200011
59	2024-07-12	HOCN	PRD10061	23	6647.78	1264.23	5	CUST200041
60	2024-09-12	0T0P	PRD10064	30	4528.85	775.89	2	CUST200004
61	2024-10-12	5JSG	PRD10095	19	8375.9	430.44	4	CUST200002
62	2025-01-01	7EEQ	PRD10027	49	6800.39	1109.9	0	CUST200014
63	2025-04-01	ID25	PRD10032	3	1144.74	90.05	2	CUST200030
64	2025-05-01	M5IG	PRD10041	7	409.03	61	2	CUST200034
65	2025-08-01	GDPP	PRD10016	41	6779.59	881.49	4	CUST200006
66	2025-09-01	4ZKL	PRD10047	30	12172.73	1615.89	4	CUST200049
67	2025-11-01	P7Y6	PRD10094	12	3845.72	438.72	3	CUST200034
68	2025-03-02	J7YH	PRD10042	19	4523.66	661.34	4	CUST200003
69	2025-04-02	GHC0	PRD10072	3	1248.34	67.73	0	CUST200008
70	2025-09-02	2VLP	PRD10064	25	6052.54	805.88	5	CUST200041
71	2025-10-02	93TY	PRD10031	11	4515.16	858.16	5	CUST200016
72	2025-11-02	0T0P	PRD10076	25	2351.03	181.33	5	CUST200005
73	2025-11-02	W1Q5	PRD10003	32	14294.99	1884.6	5	CUST200010
74	2025-12-02	M5K8	PRD10048	10	4143.97	357.75	4	CUST200033
75	2025-03-03	2VLP	PRD10019	22	1300.66	194.5	2	CUST200048
76	2025-08-03	8CGV	PRD10090	5	1419.99	132.85	2	CUST200046
77	2025-11-03	ID25	PRD10036	35	837.38	55.37	1	CUST200020
78	2025-03-05	2VLP	PRD10019	22	1300.66	194.5	2	CUST200048
79	2025-08-05	8CGV	PRD10090	5	1419.99	132.85	2	CUST200046
80	2025-11-05	ID25	PRD10036	35	837.38	55.37	1	CUST200020
81	2025-03-05	W1Q5	PRD10003	39	9664.33	1885.13	4	CUST200031
82	2025-08-05	CXUL	PRD10011	28	11909.87	1030.17	4	CUST200031
83	2025-11-05	IUC0	PRD10052	33	12935.56	2432.9	5	CUST200035
84	2025-03-05	GDPP	PRD10003	12	1814.04	298.16	2	CUST200017
85	2025-08-05	H75L	PRD10024	2	463.4	52.28	3	CUST200034
86	2025-11-05	CX19	PRD10069	4	1874.4	113.13	3	CUST200021
\.


--
-- Data for Name: sales_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sales_orders (id, so_number, customer, state, site, items_json, total_amount, status, dispatch_type, created_at, created_by, confirmed_at, dispatched_at, role, manager_user_id, customer_id, customer_email, notes, cancelled_at, cancel_reason) FROM stdin;
6	SO-9X2URJ	CUST200001	Gujarat	M5K8 - Digital Surat	[{"product_id": "PRD10016", "quantity": 50, "unit_price": 344.13, "shipment_id": "SHP-4DS7F19M"}]	17206.5	Dispatched	Truck	2026-05-05	Ishan	2026-05-05	2026-05-07	manager	2					
1	SO-10001	CUST200003	Maharashtra	FKHM	[{"product_id": "PRD10014", "product_name": "Cakes Item 14", "quantity": 1, "unit_price": 498.11, "shipment_id": "SHP-J5M6T3RN"}]	498.11	Dispatched	Truck	2026-04-30	Admin	2026-04-30	2026-04-30	admin	0					
2	SO-10002	CUST200000	Delhi	93TY	[{"product_id": "PRD10013", "product_name": "Laptop Item 13", "quantity": 5555, "unit_price": 48.66}]	270306.3	Cancelled	Truck	2026-05-04	Admin			admin	0					
10	SO-W7LGQP			VUZZ	[{"product_id": "PRD10013", "product_name": "Laptop Item 13", "quantity": 140, "unit_price": 48.66, "discount": 0.0, "line_total": 6812.4, "shipment_id": "SHP-FITWG6EP"}]	6812.4	Dispatched	Truck	2026-05-07	Ishan	2026-05-07	2026-05-07	manager	2					
3	SO-10003	CUST200000	Karnataka	ID25	[{"product_id": "PRD10084", "product_name": "Accessories Item 84 (311 in stock) | Sold: 0 | PO: 0", "quantity": 48, "unit_price": 538.9, "shipment_id": "SHP-I98W3ITO"}]	25867.199999999997	Dispatched	Train	2026-05-04	Admin	2026-05-04	2026-05-04	admin	0					
4	SO-10004	CUST200001	Gujarat	GDPP	[{"product_id": "PRD10053", "product_name": "Women Item 53 (265 in stock) | Sold: 0 | PO: 0", "quantity": 279, "unit_price": 259.16}]	72305.64000000001	Cancelled	Truck	2026-05-04	Admin			admin	0					
14	SO-10014	CUST200001	Karnataka	2VLP	[{"product_id": "PRD10078", "product_name": "Kids Item 78 (160 in stock) | Sold: 0 | PO: 0", "quantity": 1, "unit_price": 121.62, "shipment_id": "SHP-N4JHG1YA"}]	121.62	Dispatched	Air	2026-05-07	Admin	2026-05-07	2026-05-07	admin	0					
5	SO-10005	CUST200000	Karnataka	2VLP	[{"product_id": "PRD10078", "product_name": "Kids Item 78 (205 in stock) | Sold: 0 | PO: 0", "quantity": 45, "unit_price": 121.62, "shipment_id": "SHP-24QXZGTL"}]	5472.900000000001	Dispatched	Truck	2026-05-05	Admin	2026-05-05	2026-05-05	admin	0					
11	SO-CXYKY9			ID25	[{"product_id": "PRD10015", "product_name": "Yogurt Item 15", "quantity": 12, "unit_price": 538.85, "discount": 0.0, "line_total": 6466.2, "shipment_id": "SHP-7MRM2RVW"}]	6466.2	Dispatched	Truck	2026-05-07	Ishan	2026-05-07	2026-05-07	manager	2					
7	SO-10007	CUST200002	Gujarat	OTOH	[{"product_id": "PRD10015", "product_name": "Yogurt Item 15 (45 in stock) | Sold: 0 | PO: 45", "quantity": 20, "unit_price": 538.85, "shipment_id": "SHP-75XP6H8A"}]	10777	Dispatched	Air	2026-05-06	Admin	2026-05-06	2026-05-06	admin	0					
8	SO-J7W9VZ				[{"product_id": "PRD10013", "quantity": 120, "customer_id": "CUST200000", "discount": 0.0, "notes": ""}]	0	Cancelled	Truck	2026-05-06	Ishan			manager	2					
17	SO-P13M18			MYZY	[{"product_id": "PRD10013", "product_name": "Laptop Item 13", "quantity": 125, "unit_price": 48.66, "discount": 0.0, "line_total": 6082.5, "shipment_id": "SHP-Z72OE256"}]	6082.5	Dispatched	Air	2026-05-10	Ishan	2026-05-10	2026-05-10	manager	2					
9	SO-0F9E40				[{"product_id": "PRD10015", "quantity": 10, "customer_id": "CUST200001", "discount": 0.0, "notes": "", "shipment_id": "SHP-XGNR8WGQ"}]	0	Dispatched	Truck	2026-05-07	Ishan	2026-05-07	2026-05-07	manager	2					
12	SO-10012	CUST200002	Gujarat	OTOH	[{"product_id": "PRD10013", "product_name": "Laptop Item 13 (440 in stock) | Sold: 0 | PO: 0", "quantity": 15, "unit_price": 48.66, "shipment_id": "SHP-92Z3ON0X"}]	729.9	Dispatched	Truck	2026-05-07	Admin	2026-05-07	2026-05-07	admin	0					
15	SO-10015	CUST200000	Karnataka	MYZY	[{"product_id": "PRD10063", "product_name": "Kids Item 63 (505 in stock) | Sold: 0 | PO: 0", "quantity": 150, "unit_price": 512.34, "shipment_id": "SHP-0QVGOEU8"}]	76851	Dispatched	Train	2026-05-08	Admin	2026-05-08	2026-05-08	admin	0					
13	SO-10013	CUST200001	Tamil Nadu	0L72	[{"product_id": "PRD10018", "product_name": "Women Item 18 (86 in stock) | Sold: 0 | PO: 0", "quantity": 16, "unit_price": 353.52, "shipment_id": "SHP-IZGEUETZ"}]	5656.32	Dispatched	Truck	2026-05-07	Admin	2026-05-07	2026-05-07	admin	0					
21	SO-10021	CUST200003	Tamil Nadu	H75L	[{"product_id": "PRD10008", "product_name": "Men Item 8", "quantity": 50, "unit_price": 611.3, "shipment_id": "SHP-WG4B11BV"}]	30564.999999999996	Dispatched	Truck	2026-05-14	Admin	2026-05-14	2026-05-14	admin	0					
18	SO-GV9377			W1Q5	[{"product_id": "PRD10005", "product_name": "Laptop Item 5", "quantity": 10, "unit_price": 556.54, "discount": 0.0, "line_total": 5565.4, "shipment_id": "SHP-CLFUVLSJ"}]	5565.4	Dispatched	Air	2026-05-11	kanakadri	2026-05-11	2026-05-11	manager	7					
16	SO-10016	CUST200000	Gujarat	GDPP	[{"product_id": "PRD10053", "product_name": "Women Item 53 (265 in stock) | Sold: 0 | PO: 0", "quantity": 55, "unit_price": 259.16, "shipment_id": "SHP-5VL7ANMD"}]	14253.800000000001	Dispatched	Truck	2026-05-08	Admin	2026-05-08	2026-05-08	admin	0					
19	SO-2JTE03			GDPP	[{"product_id": "PRD10015", "product_name": "Yogurt Item 15", "quantity": 12, "unit_price": 538.85, "discount": 0.0, "line_total": 6466.2, "shipment_id": "SHP-BGOHAU12"}]	6466.2	Dispatched	Truck	2026-05-13	Ishan	2026-05-13	2026-05-13	manager	2					
20	SO-10020	CUST200004	Karnataka	ID25	[{"product_id": "PRD10014", "product_name": "Cakes Item 14", "quantity": 12, "unit_price": 498.11, "shipment_id": "SHP-8NG5ELF2"}]	5977.32	Dispatched	Air	2026-05-14	Admin	2026-05-14	2026-05-14	admin	0					
22	SO-DAXM7X			VUZZ	[{"product_id": "PRD10013", "product_name": "Laptop Item 13", "quantity": 45, "unit_price": 48.66, "discount": 0.0, "line_total": 2189.7, "shipment_id": "SHP-84KOETEO"}]	2189.7	Dispatched	Air	2026-05-14	Ishan	2026-05-14	2026-05-14	manager	2					
23	SO-2OOEJS			MYZY	[{"product_id": "PRD10013", "product_name": "Laptop Item 13", "quantity": 120, "unit_price": 48.66, "discount": 0.0, "line_total": 5839.2, "shipment_id": "SHP-BWSVYET9"}, {"product_id": "PRD10010", "product_name": "Cookies Item 10", "quantity": 16, "unit_price": 367.85, "discount": 0.0, "line_total": 5885.6, "shipment_id": "SHP-22WLF7PN"}]	11724.8	Dispatched	Truck	2026-05-15	Ishan	2026-05-15	2026-05-15	manager	2					
24	SO-YOYUA9			GDPP	[{"product_id": "PRD10013", "product_name": "Laptop Item 13", "quantity": 120, "unit_price": 48.66, "discount": 0.0, "line_total": 5839.2, "shipment_id": "SHP-N4QKZU10"}]	5839.2	Dispatched	Truck	2026-05-16	Ishan	2026-05-16	2026-05-16	manager	2					
\.


--
-- Data for Name: sales_returns; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sales_returns (id, return_number, so_number, customer, site, return_reason, items_json, total_refund, status, notes, created_at, created_by, approved_at, approved_by, role, manager_user_id) FROM stdin;
1	SR-MHAG4U	SO-10020	CUST200004	ID25	Customer Changed Mind	[{"product_id": "PRD10014", "product_name": "Cakes Item 14", "quantity": 12, "unit_price": 498.11}]	5977.32	Approved		2026-05-15	Admin	2026-05-15	Admin	admin	0
2	SR-J2U6GX	SO-10016	CUST200000	GDPP	Damaged in Transit	[{"product_id": "PRD10053", "product_name": "Women Item 53 (265 in stock) | Sold: 0 | PO: 0", "quantity": 55, "unit_price": 259.16}]	14253.8	Approved		2026-05-15	Admin	2026-05-15	Admin	admin	0
3	SR-9GQPC4	SO-2JTE03		GDPP	Defective Product	[{"product_id": "PRD10015", "product_name": "Yogurt Item 15", "quantity": 12, "unit_price": 538.85}]	6466.2	Approved		2026-05-19	Ishan	2026-05-19	Ishan	manager	0
\.


--
-- Data for Name: seasonal_planning; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.seasonal_planning (id, month, site_id, product_category, forecasted_sales, actual_sales, seasonal_adjustments) FROM stdin;
1	May-2024	PS3Y	Dairy	81260.5	96315.51088834292	0.1853
2	Dec-2024	W1Q5	Apparel	60609.93	64357.95069676382	0.0618
3	Sep-2024	T4UF	Apparel	84277.99	94950.57326459214	0.1266
4	Dec-2024	T4UF	Apparel	79067.48	82228.63427072395	0.04
5	Mar-2025	OTOH	Apparel	50727.92	42559.44698938204	-0.161
6	Apr-2024	7EEQ	Bakery	40722.14	46095.571109819226	0.132
7	Mar-2025	M5IG	Apparel	19569	22675.59533416437	0.1588
8	Mar-2025	0L72	Bakery	76825.98	74035.99097992641	-0.0363
9	Jul-2024	4CIY	Bakery	20867.12	23806.83288759106	0.1409
10	Jul-2024	IUC0	Electronics	74510.91	62820.61755888844	-0.1569
11	Feb-2025	93TY	Dairy	85371.96	88404.75134040613	0.0355
12	Nov-2024	M5K8	Electronics	69261.1	81899.59739406133	0.1825
13	Apr-2024	0T0P	Electronics	57732.79	47307.90172316384	-0.1806
14	Dec-2024	FKHM	Electronics	80297.33	93471.92127052066	0.1641
15	Mar-2025	KJLT	Bakery	83371.97	70150.9750960701	-0.1586
16	Dec-2024	7EEQ	Apparel	89325.15	86419.03648852394	-0.0325
17	Aug-2024	2VLP	Bakery	45808.3	42928.95161775372	-0.0629
18	Jun-2024	M5IG	Electronics	22436.2	23356.30362313169	0.041
19	Mar-2025	NY20	Apparel	59302.54	54888.31499294167	-0.0744
20	Jul-2024	NY20	Bakery	28874.14	31350.207638245025	0.0858
21	Feb-2025	0RJI	Apparel	21940.46	23786.93790268634	0.0842
22	Mar-2025	5JSG	Apparel	20386.47	19181.53015711015	-0.0591
23	Feb-2025	ID25	Electronics	77308.19	87865.06562208563	0.1366
24	Apr-2024	M5IG	Electronics	57045.7	46213.2267953441	-0.1899
25	Feb-2025	FFYV	Dairy	15094.43	13687.497919859215	-0.0932
26	Feb-2025	ZYTJ	Apparel	32550.49	36969.30774317217	0.1358
27	Jul-2024	KJLT	Apparel	77823.46	63264.44580960157	-0.1871
28	Jan-2025	A1WJ	Dairy	88123.18	96565.11557556738	0.0958
29	Jul-2024	SV87	Electronics	55983.01	62630.06642877465	0.1187
30	Mar-2025	KJLT	Apparel	69804.42	81712.62995297847	0.1706
31	Feb-2025	EXQ7	Electronics	38138.86	38934.04909114794	0.0208
32	Jul-2024	JI0Y	Apparel	65850.55	73250.17348182727	0.1124
33	Feb-2025	A1WJ	Bakery	73416.62	77752.08829984715	0.0591
34	Mar-2025	XDP5	Bakery	96786.08	88817.78740671491	-0.0823
35	Jun-2024	5JSG	Dairy	96622.77	105708.38244401183	0.094
36	Apr-2024	H75L	Electronics	48565.7	49665.2006512987	0.0226
37	Jan-2025	0T0P	Bakery	86141.28	69107.53569693965	-0.1977
38	Apr-2024	T4UF	Bakery	23833.3	22142.37531658449	-0.0709
39	Nov-2024	30T9	Apparel	81091.74	82718.77050088192	0.0201
40	Dec-2024	CX19	Apparel	29796.58	26028.73210969605	-0.1265
41	Oct-2024	CX19	Bakery	58877.21	56602.59653498792	-0.0386
42	Jul-2024	8CGV	Bakery	69700.1	64990.228283384575	-0.0676
43	Jan-2025	M5IG	Bakery	57744.9	69216.06488075171	0.1987
44	May-2024	XDP5	Dairy	70204.46	68678.69934604154	-0.0217
45	Apr-2024	A11D	Bakery	71429.62	66313.45948178273	-0.0716
46	Aug-2024	H75L	Electronics	58621.36	53529.0161168362	-0.0869
47	Dec-2024	58KX	Apparel	82253.51	80462.25549199371	-0.0218
48	Feb-2025	PKH1	Apparel	27326.11	27477.985241639708	0.0056
49	Dec-2024	J7YH	Bakery	57988.52	60932.78448594479	0.0508
50	Feb-2025	IUC0	Bakery	48178.85	40545.90966006275	-0.1584
51	Feb-2025	BVM2	Electronics	83507.89	69215.3640869851	-0.1712
52	Apr-2024	0RJI	Bakery	51330.27	47875.0319143549	-0.0673
53	Apr-2024	MYZY	Dairy	26019.29	23437.21893244596	-0.0992
54	Aug-2024	CX19	Bakery	46686.95	45774.23252277396	-0.0195
55	Sep-2024	SEMC	Electronics	11520.19	12318.763729269756	0.0693
56	Feb-2025	BVM2	Dairy	74825.71	61753.28705091357	-0.1747
57	Mar-2025	NY20	Dairy	86342.61	81427.99343074743	-0.0569
58	Aug-2024	I3QK	Dairy	80820.27	74398.31429374166	-0.0795
59	Nov-2024	MYZY	Apparel	44327.22	50038.735667584726	0.1288
60	Jun-2024	VUZZ	Electronics	58012.1	49574.38996591349	-0.1454
61	Feb-2025	SEMC	Apparel	22966.8	24595.504820122267	0.0709
62	Apr-2024	AM14	Apparel	59817.18	61134.82675500711	0.022
63	Apr-2024	H75L	Dairy	61544.67	58937.18729323406	-0.0424
64	Aug-2024	PS3Y	Dairy	28904.76	31696.15606757996	0.0966
65	Jul-2024	AM14	Apparel	47138.9	49890.52022126744	0.0584
66	Jun-2024	I3QK	Bakery	26559.35	27801.105034423388	0.0468
67	May-2024	4CIY	Bakery	26322.22	29477.30714248664	0.1199
68	Feb-2025	30T9	Electronics	59469.81	54489.87156536506	-0.0837
69	May-2024	CX19	Apparel	27767.58	28662.75850147128	0.0322
70	Jun-2024	GHC0	Apparel	70416.6	62939.28231880079	-0.1062
71	Jul-2024	M5IG	Dairy	38600.73	37838.68949226424	-0.0197
72	Mar-2025	WM31	Apparel	62575.29	64216.06436189781	0.0262
73	Oct-2024	CXUL	Apparel	25177.56	23296.441573929813	-0.0747
74	Aug-2024	SV87	Electronics	85609.91	73087.09208910969	-0.1463
75	Nov-2024	AM14	Apparel	51656.35	48737.59270333628	-0.0565
76	Dec-2024	P5TB	Electronics	19794.94	20947.414107881952	0.0582
77	Jun-2024	MYZY	Apparel	90216.73	79261.9625332098	-0.1214
78	Mar-2025	AM14	Dairy	16786	13553.891251883422	-0.1925
79	Jan-2025	I3QK	Dairy	62101.07	68788.11954948754	0.1077
80	Dec-2024	IUC0	Dairy	33455.47	38727.863845451	0.1576
81	Feb-2025	BVM2	Electronics	79767.75	75486.41161255974	-0.0537
82	Jun-2024	SV87	Apparel	51823.1	52038.93270890174	0.0042
83	Dec-2024	SEMC	Apparel	10953.25	9809.20846892493	-0.1044
84	Dec-2024	WM31	Bakery	22633.36	19548.18332189136	-0.1363
85	Mar-2025	4ZKL	Bakery	75880.4	89210.3177070485	0.1757
86	Nov-2024	PKH1	Bakery	30857.49	27948.95081425808	-0.0943
87	Feb-2025	SV87	Dairy	28609.67	33275.633583560746	0.1631
88	Nov-2024	CXUL	Electronics	92611.17	106745.56016228149	0.1526
89	May-2024	PKH1	Apparel	73336.26	73963.22354179726	0.0085
90	Jan-2025	GDPP	Apparel	58991.51	51295.47327415957	-0.1305
91	Sep-2024	A11D	Electronics	62891.09	72909.05241766498	0.1593
92	Oct-2024	CX19	Apparel	97540.67	86729.23305187684	-0.1108
93	Sep-2024	SEMC	Apparel	53817.54	53432.4236150159	-0.0072
94	Dec-2024	2VLP	Dairy	89383.08	87234.26430462347	-0.024
95	Dec-2024	SV87	Dairy	67912.93	60076.24251478969	-0.1154
96	Sep-2024	5JSG	Bakery	64181.82	72318.92144280329	0.1268
97	Oct-2024	7EEQ	Bakery	83005.54	90318.51596118836	0.0881
98	Nov-2024	ID25	Electronics	28963.36	25038.781389221916	-0.1355
99	Jul-2024	93TY	Dairy	13882.99	14291.07500089537	0.0294
100	Feb-2025	ZYTJ	Bakery	56137.85	64913.26642451202	0.1563
101	Jun-2024	FFYV	Dairy	33243.37	28988.7178168098	-0.128
102	Mar-2025	SEMC	Dairy	75517.69	85223.3235079069	0.1285
103	Nov-2024	MYZY	Bakery	64587.33	63848.798551610365	-0.0114
104	Jul-2024	ID25	Bakery	84732.72	88150.45542134567	0.0403
105	Jan-2025	P7Y6	Bakery	69368.39	62834.46199190484	-0.0942
106	Nov-2024	AM14	Apparel	63688	52704.18657070512	-0.1725
107	Jun-2024	EXQ7	Electronics	19771.31	17417.326356829013	-0.1191
108	Jun-2024	I3QK	Electronics	64495.99	56173.99977020345	-0.129
109	Dec-2024	WM31	Dairy	55299.63	46839.14952100576	-0.153
110	Jan-2025	ID25	Bakery	58535.74	46856.69397409946	-0.1995
111	Dec-2024	M5K8	Electronics	47861.56	55037.43030357713	0.1499
112	Jul-2024	KJLT	Electronics	94457.95	93782.51701335116	-0.0072
113	Sep-2024	M5K8	Electronics	63014.33	69098.84353616292	0.0966
114	Oct-2024	XDP5	Dairy	22049.48	21847.870465002747	-0.0091
115	Aug-2024	SV87	Dairy	63846.31	64963.13575350036	0.0175
116	Apr-2024	4CIY	Bakery	73823.4	82369.86067208166	0.1158
117	Dec-2024	4ZKL	Dairy	10647.46	11305.669455762883	0.0618
118	Oct-2024	KJLT	Apparel	42604.28	36721.11599370323	-0.1381
119	Aug-2024	A11D	Apparel	86947.92	84289.45421652491	-0.0306
120	Feb-2025	CXUL	Apparel	45770.87	40345.99043450216	-0.1185
\.


--
-- Data for Name: sites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sites (id, site_id, site_name, site_format, region, city, state_id, store_size, open_date, status) FROM stdin;
1	JI0Y	Smart Mumbai	Digital	North	Mumbai	1	6041	2015-03-05	Active
3	PKH1	Smart Mumbai	Smart	North	Mumbai	1	17449	2016-01-02	Inactive
4	30T9	Digital Hubli	Smart	South	Hubli	5	23089	\N	Inactive
5	CX19	Fresh New Delhi	Smart	North	New Delhi	4	17455	2018-12-02	Inactive
6	MYZY	Smart Bangalore	Fresh	South	Bangalore	5	22502	2023-06-03	Active
7	J7YH	Trends Surat	Smart	South	Surat	2	12505	2015-12-05	Inactive
8	H75L	Digital Coimbatore	Digital	West	Coimbatore	3	26064	\N	Active
9	0T0P	Digital Bangalore	Trends	West	Bangalore	5	12186	\N	Inactive
10	FFYV	Digital Mumbai	Digital	West	Mumbai	1	24526	2020-01-04	Inactive
11	ZYTJ	Trends New Delhi	Smart	North	New Delhi	4	14617	\N	Active
12	5JSG	Smart Chennai	Trends	North	Chennai	3	25937	2020-10-09	Active
13	T2TA	Trends Surat	Digital	West	Surat	2	5638	2016-03-04	Inactive
14	IUC0	Smart Bangalore	Fresh	West	Bangalore	5	9207	\N	Inactive
15	SV87	Fresh New Delhi	Trends	South	New Delhi	4	18074	\N	Inactive
16	EIMV	Fresh Madurai	Fresh	South	Madurai	3	5235	\N	Active
17	4CIY	Fresh Ahmedabad	Fresh	West	Ahmedabad	2	28702	\N	Inactive
18	GDPP	Digital Surat	Smart	South	Surat	2	27064	\N	Active
19	M5IG	Digital Pune	Fresh	North	Pune	1	18824	\N	Inactive
20	P5TB	Smart Chennai	Smart	West	Chennai	3	29692	\N	Active
21	HOCN	Digital Coimbatore	Trends	South	Coimbatore	3	19909	\N	Inactive
22	GHC0	Smart New Delhi	Trends	West	New Delhi	4	6873	\N	Inactive
23	8CGV	Fresh New Delhi	Digital	West	New Delhi	4	8928	\N	Active
24	CXUL	Trends New Delhi	Fresh	North	New Delhi	4	26945	2023-12-01	Inactive
25	EXQ7	Smart Surat	Smart	South	Surat	2	20017	\N	Active
26	SEMC	Fresh Nagpur	Trends	West	Nagpur	1	14338	2016-08-10	Inactive
27	93TY	Trends New Delhi	Smart	North	New Delhi	4	9400	\N	Active
28	FKHM	Trends Nagpur	Digital	North	Nagpur	1	13228	\N	Active
29	A1WJ	Digital Coimbatore	Digital	West	Coimbatore	3	23379	2015-09-02	Active
30	T4UF	Fresh Nagpur	Smart	West	Nagpur	1	15101	2019-02-02	Active
31	ID25	Digital Bangalore	Fresh	North	Bangalore	5	12757	\N	Active
32	0L72	Fresh Chennai	Trends	West	Chennai	3	10216	\N	Active
33	I3QK	Fresh Chennai	Fresh	South	Chennai	3	5775	\N	Active
34	58KX	Digital Coimbatore	Trends	South	Coimbatore	3	5904	\N	Inactive
35	BVM2	Digital Vadodara	Smart	South	Vadodara	2	17622	\N	Active
36	PS3Y	Fresh Bangalore	Trends	North	Bangalore	5	19132	\N	Inactive
37	4ZKL	Digital New Delhi	Trends	North	New Delhi	4	18185	\N	Inactive
38	P7Y6	Trends New Delhi	Digital	West	New Delhi	4	22954	2015-02-01	Inactive
39	2VLP	Fresh Bangalore	Digital	South	Bangalore	5	29115	\N	Active
40	WM31	Trends Hubli	Fresh	North	Hubli	5	11525	\N	Active
41	W1Q5	Fresh Mumbai	Digital	South	Mumbai	1	21199	\N	Active
42	A11D	Digital Vadodara	Fresh	North	Vadodara	2	10763	\N	Inactive
43	7EEQ	Trends Nagpur	Digital	West	Nagpur	1	25075	\N	Inactive
44	0RJI	Trends New Delhi	Digital	West	New Delhi	4	25537	2017-06-09	Inactive
45	KJLT	Fresh Chennai	Fresh	North	Chennai	3	12577	\N	Active
46	OTOH	Digital Ahmedabad	Digital	South	Ahmedabad	2	24139	\N	Active
47	AM14	Digital New Delhi	Fresh	South	New Delhi	4	20998	\N	Inactive
48	NY20	Digital Coimbatore	Fresh	West	Coimbatore	3	25390	\N	Active
49	XDP5	Fresh Madurai	Smart	North	Madurai	3	13524	2019-02-04	Inactive
50	M5K8	Digital Surat	Trends	South	Surat	2	7683	2020-10-04	Active
2	VUZZ	Digital Ahmedabad	Fresh	North	Ahmedabad	2	19719	2021-10-08	Active
\.


--
-- Data for Name: stock_levels; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stock_levels (id, site_id, product_id, qty_on_hand, reorder_point, updated_at) FROM stdin;
\.


--
-- Data for Name: stock_movements; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stock_movements (id, site_id, product_id, movement_type, qty_change, reference_id, remarks, created_by, created_at) FROM stdin;
1		PRD10015	SaleOut	-10	SO-0F9E40	\N	2	2026-05-07 02:08:41.117741
2	VUZZ	PRD10013	SaleOut	-140	SO-W7LGQP	\N	2	2026-05-07 05:17:06.689022
3	ID25	PRD10015	SaleOut	-12	SO-CXYKY9	\N	2	2026-05-07 06:22:22.886096
4	MYZY	PRD10013	SaleOut	-125	SO-P13M18	\N	2	2026-05-10 05:57:14.889975
6	GDPP	PRD10015	SaleOut	-12	SO-2JTE03	\N	2	2026-05-13 10:53:40.619999
7	VUZZ	PRD10013	SaleOut	-45	SO-DAXM7X	\N	2	2026-05-14 12:23:19.630222
8	MYZY	PRD10013	SaleOut	-120	SO-2OOEJS	\N	2	2026-05-15 11:16:51.015195
9	MYZY	PRD10010	SaleOut	-16	SO-2OOEJS	\N	2	2026-05-15 11:16:51.035262
5	W1Q5	PRD10005	SaleOut	-10	SO-GV9377	\N	\N	2026-05-11 05:56:20.268176
10	GDPP	PRD10013	SaleOut	-120	SO-YOYUA9	\N	2	2026-05-16 11:33:29.573142
\.


--
-- Data for Name: subcategories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subcategories (id, category_id, subcategory_name) FROM stdin;
1	1	Cheese
2	2	Bread
3	3	Accessories
4	4	Men
5	3	Laptop
6	4	Kids
7	2	Cookies
8	2	Cakes
9	1	Yogurt
10	4	Women
11	3	Mobile
12	1	Milk
\.


--
-- Data for Name: suppliers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.suppliers (id, supplier_id, supplier_name, email, phone, address, contact_person, category, status, notes, created_at, updated_at) FROM stdin;
5	SUP010	Nithesh	kurubakanakadri9@gmail.com	7865765456	\N	\N	\N	Active	\N	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
11	SUP001	Kishan	ishankishanik32@gmail.com	9182627361	\N	\N	\N	Active	\N	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
3	SUP008	Arjun	arjunak63@gmail.com		\N	\N	\N	Active	\N	2026-05-07 07:23:38.82112	2026-05-07 07:23:38.82112
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, password, role, is_first_login, is_active, phone, department, employee_id, photo_url, created_at) FROM stdin;
1	Admin	admin@inventory.com	scrypt:32768:8:1$xdNCDDcXnJIXmZ3Q$8cc4b49db12d442b78c1c92744bc49d27ece513d207cf8c0eb91f0b2a8d1b81be23124f565fd09a63c88d5015448f56f210ca503ba2ec09d3076d0e98b3847da	admin	f	t	\N	\N	\N	\N	2026-05-07 07:23:38.82112
2	Ishan	ishankishanik32@gmail.com	scrypt:32768:8:1$fd9Rhx2Uxuy6s0Lf$d1bd586d92984110427f533c553d2bb89393396b9156284c8205feb2c560c7153272ee12476337df567370ceaafa9bb295b2ca017489d895104a913a69b17647	manager	f	t	\N	\N	\N	\N	2026-05-07 07:23:38.82112
3	Arjun	nanisudheer4555@gmail.com	scrypt:32768:8:1$CCiKT4rBklRtP6G9$2559a4c72ad942eae256aac6b147bf8dd58cf5c53ece0549b145fcb2b618a08c4da75455c91539fbbe4fb77cfa90436b7e8da9caa09865e416ae0bf6854c3646	analyst	f	t	\N	\N	\N	\N	2026-05-07 07:23:38.82112
4	Miller	31msdhoni@gmail.com	scrypt:32768:8:1$SbQGgba5WC5tt6hm$bc369dade44910bc6410b43902f7e0ee897a6002f8cf31320e925e6f9b7008db6dda32fe7e0cc412b2948078d124fe383fb811fb0bcb6a466e1260ee52420b3f	manager	f	t	\N	\N	\N	\N	2026-05-07 07:23:38.82112
9	Rohit	sudheernani3345@gmail.com	scrypt:32768:8:1$Y9E5HQiFnpGXARy6$20430e2175491b71c890867badf27f46d412036753f33b6c75a4de6aa31c8ea107c0e4ce7bddaccbe83e205e222511369a659004f104e36b19523b3e082e5b1e	manager	f	t			EMP1007		2026-05-15 04:44:31.275655
\.


--
-- Name: States_state_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."States_state_id_seq"', 1, false);


--
-- Name: audit_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.audit_logs_id_seq', 695, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 4, true);


--
-- Name: contact_messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contact_messages_id_seq', 1, true);


--
-- Name: customers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customers_id_seq', 50, true);


--
-- Name: inventory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.inventory_id_seq', 110, true);


--
-- Name: logistics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.logistics_id_seq', 174, true);


--
-- Name: managers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.managers_id_seq', 8, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 102, true);


--
-- Name: promotions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.promotions_id_seq', 50, true);


--
-- Name: purchase_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.purchase_orders_id_seq', 16, true);


--
-- Name: purchase_returns_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.purchase_returns_id_seq', 3, true);


--
-- Name: sales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sales_id_seq', 86, true);


--
-- Name: sales_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sales_orders_id_seq', 24, true);


--
-- Name: sales_returns_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sales_returns_id_seq', 3, true);


--
-- Name: seasonal_planning_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.seasonal_planning_id_seq', 120, true);


--
-- Name: sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sites_id_seq', 50, true);


--
-- Name: stock_levels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stock_levels_id_seq', 1, false);


--
-- Name: stock_movements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stock_movements_id_seq', 10, true);


--
-- Name: subcategories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subcategories_id_seq', 12, true);


--
-- Name: suppliers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.suppliers_id_seq', 11, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- Name: States States_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."States"
    ADD CONSTRAINT "States_pkey" PRIMARY KEY (state_id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: categories categories_category_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_category_name_key UNIQUE (category_name);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: contact_messages contact_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contact_messages
    ADD CONSTRAINT contact_messages_pkey PRIMARY KEY (id);


--
-- Name: customers customers_customer_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_customer_id_key UNIQUE (customer_id);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- Name: inventory inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (id);


--
-- Name: logistics logistics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logistics
    ADD CONSTRAINT logistics_pkey PRIMARY KEY (id);


--
-- Name: logistics logistics_shipment_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logistics
    ADD CONSTRAINT logistics_shipment_id_key UNIQUE (shipment_id);


--
-- Name: managers managers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.managers
    ADD CONSTRAINT managers_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: products products_product_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_product_id_key UNIQUE (product_id);


--
-- Name: promotions promotions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promotions
    ADD CONSTRAINT promotions_pkey PRIMARY KEY (id);


--
-- Name: promotions promotions_promotion_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promotions
    ADD CONSTRAINT promotions_promotion_id_key UNIQUE (promotion_id);


--
-- Name: purchase_orders purchase_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_orders
    ADD CONSTRAINT purchase_orders_pkey PRIMARY KEY (id);


--
-- Name: purchase_orders purchase_orders_po_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_orders
    ADD CONSTRAINT purchase_orders_po_number_key UNIQUE (po_number);


--
-- Name: purchase_orders purchase_orders_supplier_approval_token_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_orders
    ADD CONSTRAINT purchase_orders_supplier_approval_token_key UNIQUE (supplier_approval_token);


--
-- Name: purchase_returns purchase_returns_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_returns
    ADD CONSTRAINT purchase_returns_pkey PRIMARY KEY (id);


--
-- Name: purchase_returns purchase_returns_return_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_returns
    ADD CONSTRAINT purchase_returns_return_number_key UNIQUE (return_number);


--
-- Name: sales_orders sales_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales_orders
    ADD CONSTRAINT sales_orders_pkey PRIMARY KEY (id);


--
-- Name: sales_orders sales_orders_so_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales_orders
    ADD CONSTRAINT sales_orders_so_number_key UNIQUE (so_number);


--
-- Name: sales sales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_pkey PRIMARY KEY (id);


--
-- Name: sales_returns sales_returns_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales_returns
    ADD CONSTRAINT sales_returns_pkey PRIMARY KEY (id);


--
-- Name: sales_returns sales_returns_return_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales_returns
    ADD CONSTRAINT sales_returns_return_number_key UNIQUE (return_number);


--
-- Name: seasonal_planning seasonal_planning_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seasonal_planning
    ADD CONSTRAINT seasonal_planning_pkey PRIMARY KEY (id);


--
-- Name: sites sites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sites
    ADD CONSTRAINT sites_pkey PRIMARY KEY (id);


--
-- Name: sites sites_site_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sites
    ADD CONSTRAINT sites_site_id_key UNIQUE (site_id);


--
-- Name: stock_levels stock_levels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_levels
    ADD CONSTRAINT stock_levels_pkey PRIMARY KEY (id);


--
-- Name: stock_movements stock_movements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_movements
    ADD CONSTRAINT stock_movements_pkey PRIMARY KEY (id);


--
-- Name: subcategories subcategories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subcategories
    ADD CONSTRAINT subcategories_pkey PRIMARY KEY (id);


--
-- Name: suppliers suppliers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (id);


--
-- Name: suppliers suppliers_supplier_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_supplier_id_key UNIQUE (supplier_id);


--
-- Name: stock_levels uq_stock_site_product; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_levels
    ADD CONSTRAINT uq_stock_site_product UNIQUE (site_id, product_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_employee_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_employee_id_key UNIQUE (employee_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_logistics_delivery_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_logistics_delivery_status ON public.logistics USING btree (delivery_status);


--
-- Name: ix_logistics_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_logistics_product_id ON public.logistics USING btree (product_id);


--
-- Name: ix_logistics_product_site; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_logistics_product_site ON public.logistics USING btree (product_id, site_id);


--
-- Name: ix_logistics_shipment_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_logistics_shipment_date ON public.logistics USING btree (shipment_date);


--
-- Name: ix_logistics_site_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_logistics_site_id ON public.logistics USING btree (site_id);


--
-- Name: ix_logistics_status_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_logistics_status_date ON public.logistics USING btree (delivery_status, shipment_date);


--
-- Name: ix_logistics_transportation_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_logistics_transportation_type ON public.logistics USING btree (transportation_type);


--
-- Name: logistics logistics_so_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logistics
    ADD CONSTRAINT logistics_so_id_fkey FOREIGN KEY (so_id) REFERENCES public.sales_orders(id);


--
-- Name: managers managers_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.managers
    ADD CONSTRAINT managers_site_id_fkey FOREIGN KEY (site_id) REFERENCES public.sites(site_id);


--
-- Name: managers managers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.managers
    ADD CONSTRAINT managers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: purchase_orders purchase_orders_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_orders
    ADD CONSTRAINT purchase_orders_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.suppliers(id);


--
-- Name: stock_movements stock_movements_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_movements
    ADD CONSTRAINT stock_movements_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: subcategories subcategories_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subcategories
    ADD CONSTRAINT subcategories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- PostgreSQL database dump complete
--

\unrestrict kg7MWrTgaivWcPtI6J8aocfjPzRIvjYs8OaRkb8Mg939hBifToNWxoiL6BRefWJ

