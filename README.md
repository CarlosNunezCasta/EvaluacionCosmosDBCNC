# EvaluacionCosmosDBCNC
# Repositorio GitHub: CarlosNunezCasta/EvaluacionCosmosDBCNC
# Base de Datos Cosmos: acdbcncevaluacion
# En database.py Reemplazar los valores de:
#    COSMOS_ENDPOINT por URI de la BD Cosmos
#    COSMOS_KEY por Primary Key de la BD Cosmos
# Al abrir el navegador al final del url añadir /docs
# Instrucciones de Ejecucion:
# Usuarios:
# GET /usuarios/: Obtener la lista completa de usuarios - Sin Parametros
# POST /usuarios/: Crear un nuevo usuario - Valores de campos de Usuario
# PUT /usuarios/{id}: Actualizar la información de un usuario - usuario_id y campos
# DELETE /usuarios/{id}: Eliminar un usuario - usuario_id
# Proyectos:
# GET /proyectos/: Obtener la lista de todos los proyectos - Sin Parametros
# POST /proyectos/: Crear un nuevo proyecto asociado a un usuario - Valores de campos de Proyecto
# GET /usuarios/{id_usuario}/proyectos: Obtener proyectos de usuario especifico - id_usuario
# PUT /proyectos/{id}: Actualizar la información de un proyecto - proyect_id
# DELETE /proyectos/{id}: Eliminar un proyecto - proyect_id
