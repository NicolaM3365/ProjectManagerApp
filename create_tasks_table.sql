-- Table: public.tasks

-- DROP TABLE IF EXISTS public.tasks;

CREATE TABLE IF NOT EXISTS public.tasks
(
    task_id integer NOT NULL,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    description character varying(100) COLLATE pg_catalog."default" NOT NULL,
    status character varying(100) COLLATE pg_catalog."default" NOT NULL,
    created_at date,
    project_id integer NOT NULL,
    managed_task_id integer NOT NULL,
    CONSTRAINT tasks_pkey PRIMARY KEY (task_id),
    CONSTRAINT tasks_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.projects2 (project_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tasks
    OWNER to postgres;