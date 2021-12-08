CREATE TABLE tweets (
	tweet_id bigint NOT NULL,
	texto text,
	PRIMARY KEY (tweet_id)
);

CREATE TABLE retweets (
	tweet_id bigint NOT NULL,
	texto text,
	fecha_creacion DATETIME,
	ubicacion text,
	id_tweet_original bigint,
	longitud DOUBLE,
	latitude DOUBLE,
	PRIMARY KEY (tweet_id)
);

CREATE TABLE ubicaciones (
	nombre text,
	longitud DOUBLE,
	latitude DOUBLE
);

CREATE TABLE stemming (
	id bigint NOT NULL,
	tweet_id bigint,
	texto text,
	fecha_creacion DATETIME,
	cantidad_likes int,
	cantidad_rt int,
	id_usuario text,
	nombre_usuario text,
	ubicacion text,
	cantidad_seguidores int,
	id_tweet_original bigint,
	created_at TIME,
	updated_at TIME
);

ALTER TABLE stemming
ADD CONSTRAINT PK_stemming PRIMARY KEY (id);

CREATE TABLE comunidades (
	id bigint NOT NULL AUTO_INCREMENT,
	nombre_comunidades text,
	texto_comunidades text,
	created_at TIME,
	updated_at TIME,
	PRIMARY KEY(id)
);

CREATE TABLE rel_stemming_comunidades (
	id bigint NOT NULL AUTO_INCREMENT,
	grado double,
	comunidades_id bigint NOT NULL,
	stemming_id bigint NOT NULL,
	created_at TIME,
	updated_at TIME,
	PRIMARY KEY(id)
);

ALTER table rel_stemming_comunidades
ADD CONSTRAINT rel_rel_stemming_comunidades_stemming
FOREIGN KEY (stemming_id) REFERENCES stemming(id);

ALTER table rel_stemming_comunidades
ADD CONSTRAINT rel_rel_stemming_comunidades_comunidades
FOREIGN KEY (comunidades_id) REFERENCES comunidades(id);
