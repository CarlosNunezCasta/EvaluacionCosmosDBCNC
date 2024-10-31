from fastapi import FastAPI, HTTPException, Query, Path
from typing import List, Optional
from models import Usuario, Proyecto
from azure.cosmos import exceptions
from datetime import datetime
from database import container

app = FastAPI(title='API de Gestion de Usuarios y Proyectos')

### Endpoint de Users

@app.get("/")
def home():
    return "Hola Mundo"

#Crear usuario
@app.post("/users/", response_model=Usuario, status_code=201)
def create_event(event: Usuario):
    try:
        container.create_item(body=event.dict())
        return event
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=400, detail="El evento con este ID ya existe")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Obtener evento
@app.get("/events/{event_id}",response_model=Evento)
def get_event(event_id: str = Path(...,description="ID del evento a recuperar")):
    try:
        event = container.read_item(item=event_id,partition_key=event_id)
        return event
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=400, detail="Evento no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Listar eventos
@app.get("/events/", response_model=List[Evento])
def list_event():
    query = "SELECT * FROM c WHERE 1=1"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return items

#Actualizar evento
@app.put("/events/{event_id}",response_model=Evento)
def update_event(event_id: str,updated_event: Evento):
    existing_event = container.read_item(item=event_id,partition_key=event_id)
    existing_event.update(update_event.dict(exclude_unset=True))

##Endpoint de Participante

@app.post("/events/{event_id}/participants/",response_model=Participante, status_code=201)
def add_participant(event_id: str, participant: Participante):
    try:
        event = container.read_item(item=event_id, partition_key=event_id)

        if len(event['participants']) >= event['capacity']:
            raise HTTPException(status_code=400, detail='Capacidad maxima del evento alcanzado')
        
        if any( p['id'] == participant.id for p in event['participants'] ):
            raise HTTPException(status_code=400, detail='El participante con este ID ya esta inscrito')

        event['participants'].append(participant.dict())

        container.replace_item(item=event_id, body=event)

        return participant
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=400, detail="Evento no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/events/{event_id}/participants/{participant_id}")
def get_participant(event_id: str, participant_id: str):

    try:
        event = container.read_item(item=event_id, partition_key=event_id)

        participant = next((p for p in event['participants'] if p['id'] == participant_id), None)

        if participant:
            return participant
        else:
            raise HTTPException(status_code=400, detail='Participante no encontrado')
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=400, detail="Evento no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/events/{event_id}/participants/", response_model=List[Participante])
def list_participante(event_id: str):
    try:
        event = container.read_item(item=event_id, partition_key=event_id)

        participants = event.get('participants',[])

        return participants
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=400, detail="Evento no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/events/{event_id}/participants/{participant_id}", response_model=Participante)
def update_participant(event_id: str, participant_id: str, updated_participant: Participante):
 
    try:
        event = container.read_item(item=event_id, partition_key=event_id)
        participant = next((p for p in event['participants'] if p['id'] == participant_id), None)
 
        if not participant:
            raise HTTPException(status_code=404, detail= "Participante no encontrado")
        
        participant.update(updated_participant.dict(exclude_unset=True))
 
        # for p in event['participants']:
 
        #     if p['id'] != participant_id:
        #         lista_nueva.append(p)
        #     else:
        #         lista_nueva.append(participant)
 
 
        event['participants'] = [ p if p['id'] != participant_id else participant for p in event['participants']]
 
        container.replace_item(item=event_id, body=event)
 
        return participant
        
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Evento no encotrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
@app.delete("/events/{event_id}/participants/{participant_id}", status_code=204)
def delete_participant(event_id: str, participant_id: str):
 
    try:
 
        event = container.read_item(item=event_id, partition_key=event_id)
        participant = next((p for p in event['participants'] if p['id'] == participant_id), None)
 
        if not participant:
            raise HTTPException(status_code=404, detail='Participante no encontrado')
        
        event['participants'] = [ p for p in event['participants'] if p['id'] != participant_id]
 
        container.replace_item(item=event_id, body=event)
        return
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Evento no encotrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))