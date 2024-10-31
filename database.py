from azure.cosmos import CosmosClient, exceptions
from dotenv import load_dotenv
import os

# Obtener las variables de entorno
COSMOS_ENDPOINT = 'https://acdbcncevaluacion.documents.azure.com:443/'
COSMOS_KEY = 'VRqqmuIC5pQMt4oLyXdqjlZj1Lk08chanLGEAA3fJSVQWkjEWgf8wpLCAjPFRuq2cMmZfGuXKEx0ACDb7jZxCw=='
DATABASE_NAME = 'GestorProyectosDB'
CONTAINER_USUARIOS = 'usuarios'
CONTAINER_PROYECTOS = 'proyectos'

# Inicializar el cliente de Cosmos DB
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

# Crear o obtener la base de datos
try:
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(DATABASE_NAME)

# Crear o obtener el contenedor
try:
    container_usuario = database.create_container_if_not_exists(
        id=CONTAINER_USUARIOS,
        partition_key={'paths': ['/id'], 'kind': 'Hash'},
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    container = database.get_container_client(CONTAINER_USUARIOS)

# Crear o obtener el contenedor
try:
    container_proyecto = database.create_container_if_not_exists(
        id=CONTAINER_PROYECTOS,
        partition_key={'paths': ['/id'], 'kind': 'Hash'},
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    container = database.get_container_client(CONTAINER_PROYECTOS)