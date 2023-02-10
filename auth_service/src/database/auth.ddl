CREATE SCHEMA IF NOT EXISTS auth;


CREATE TABLE IF NOT EXISTS auth.user
(
    id                  uuid                     NOT NULL PRIMARY KEY,
    login               varchar(128)             NOT NULL UNIQUE,
    password            TEXT                     NOT NULL,
    full_name           varchar(255)             NOT NULL,
    email               varchar(255)             NOT NULL UNIQUE,
    permitted_devices   text[]                   NOT NULL,
    active              BOOLEAN                  NOT NULL,
    registered_date     timestamp with time zone NOT NULL,
    updated_at          timestamp with time zone NOT NULL
);


CREATE TABLE IF NOT EXISTS auth.login_history
(
    id          uuid                     NOT NULL PRIMARY KEY,
    user_id     uuid                     NOT NULL REFERENCES auth.user (id) ON DELETE CASCADE,
    action      varchar(255)             NOT NULL,
    device      text[]                   NOT NULL
);



CREATE TABLE IF NOT EXISTS auth.role
(
    id          uuid        NOT NULL PRIMARY KEY,
    name        varchar(64) NOT NULL UNIQUE,
    permissions varchar[]   NOT NULL
);



CREATE TABLE IF NOT EXISTS auth.user_roles
(
    id      uuid NOT NULL PRIMARY KEY,
    user_id uuid NOT NULL UNIQUE REFERENCES auth.user (id) ON DELETE CASCADE,
    role_id uuid NOT NULL UNIQUE REFERENCES auth.roles (id) ON DELETE CASCADE
);
