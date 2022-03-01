CREATE TABLE IF NOT EXISTS public.events (
    id integer NOT NULL,
    eventname text NOT NULL,
    eventstartdate timestamp without time zone NOT NULL,
    eventpersoncreator character varying(60) NOT NULL,
    approved boolean DEFAULT false NOT NULL,
    eventstopdate timestamp without time zone,
    descr text,
    email text
);
CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE IF NOT EXISTS public.users (
    id integer NOT NULL,
    login text NOT NULL,
    hash text NOT NULL,
    role character varying(10) NOT NULL
);
CREATE SEQUENCE public.users_id_seq
    -- AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
Insert INTO public.users(id,login,hash,role) VALUES (1,'root','63a9f0ea7bb98050796b649e85481845','root');