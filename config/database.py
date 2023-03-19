import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Se guarda el nombre de la base de datos
sqlite_file_name = "database.sqlite" 

#Luego se leera el directorio actual del archivo database                                       
base_dir = os.path.dirname(os.path.realpath(__file__))

#"sqlite:///" es la forma en la que se conecta a una base de datos, se usa el metodo join para unir las URLs
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

#Engine representa el motor de la base de datos, con el comando "echo" mostrará en consola lo que esta haciendo
engine = create_engine(database_url, echo=True)

#Se crea una sesion para conectarse con la base de datos, se enlaza en engine con bind 
Session = sessionmaker(bind=engine)

#Con la base podemos manipular todas las tablas de la database
Base = declarative_base()