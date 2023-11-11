-- Table: public.projects

-- DROP TABLE IF EXISTS public.projects;


CREATE TABLE IF NOT EXISTS public.projects
(
    project_id SERIAL PRIMARY KEY,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    description character varying(100) COLLATE pg_catalog."default" NOT NULL,
    status character varying(100) COLLATE pg_catalog."default" NOT NULL,
    created_at date,
    managed_project_id integer NOT NULL
)
TABLESPACE pg_default;


ALTER TABLE IF EXISTS public.projects
    OWNER to postgres;
