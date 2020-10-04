import psycopg2



# conn = psycopg2.connect(host="database-2.c2xa1utqjm6r.us-east-2.rds.amazonaws.com",database="postgres",user="jakemarsh",password="Sephiroth!1")

def connect():
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="database-2.c2xa1utqjm6r.us-east-2.rds.amazonaws.com",database="postgres",user="jakemarsh",password="Sephiroth!1")

        cur = conn.cursor()

        print('PostgreSQL database version:')
        # cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
       
	    # close the communication with the PostgreSQL
        print('create sample vendor table before closing')
        t_name_tbl = "turkeys"
        s = ""
        s += "CREATE TABLE " + t_name_tbl + "("
        s += " id serial NOT NULL"
        s += ", id_session int4 NULL DEFAULT 0"
        s += ", t_name_turkey varchar(64) NULL"
        s += ", t_contents text NULL"
        s += ", d_created date NULL DEFAULT now()"
        s += ", CONSTRAINT turkeys_pkey PRIMARY KEY (id)"
        s += " ); "
        s += "CREATE UNIQUE INDEX turkeys_id_idx ON public.turkeys USING btree (id);"
        cur.execute(s)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
# def drop_specific_table():
#     commands=(
#         DROP TABLE vendors ()
#     )