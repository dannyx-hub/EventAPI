CREATE TABLE IF NOT EXISTS public.events (
    id SERIAL NOT NULL,
    eventname text NOT NULL,
    eventstartdate timestamp without time zone NOT NULL,
    eventpersoncreator character varying(60) NOT NULL,
    approved boolean DEFAULT false NOT NULL,
    eventstopdate timestamp without time zone,
    descr text,
    email text
);

CREATE TABLE IF NOT EXISTS public.users (
    id SERIAL NOT NULL,
    login text NOT NULL,
    hash text NOT NULL,
    role character varying(10) NOT NULL
);
CREATE TABLE IF NOT EXISTS public.log(
    id serial NOT NULL,
    ip text NOT NULL,
    path text NOT NULL,
    data TIMESTAMP NOT NULL

);
Insert INTO public.users(id,login,hash,role) VALUES (1,'root','63a9f0ea7bb98050796b649e85481845','root');