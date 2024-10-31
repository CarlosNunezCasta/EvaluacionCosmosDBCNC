from azure.cosmos import CosmosClient, exceptions
from dotenv import load_dotenv
import os

# Obtener las variables de entorno
COSMOS_ENDPOINT = ''
COSMOS_KEY = ''
DATABASE_NAME = 'GestorProyectosDB'
USUARIOS_CONTAINER = 'Usuarios'
PROYECTOS_CONTAINER = 'Proyectos'

# Inicializar el cliente de Cosmos DB
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

# Crear o obtener la base de datos
try:
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(DATABASE_NAME)

# Crear o obtener el contenedor usuarios
try:
    container = database.create_container_if_not_exists(
        id=USUARIOS_CONTAINER,
        partition_key={'paths': ['/id'], 'kind': 'Hash'},
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    container = database.get_container_client(USUARIOS_CONTAINER)

# Crear o obtener el contenedor proyectos
try:
    container = database.create_container_if_not_exists(
        id=PROYECTOS_CONTAINER,
        partition_key={'paths': ['/id'], 'kind': 'Hash'},
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    container = database.get_container_client(PROYECTOS_CONTAINER)
