from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas.aeroportos import Aeroporto
from models.database import get_db
from models.aeroportos import Aeroportos
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

@router.get("/aeroportos")
def get(db: Session = Depends(get_db)):
    all_aeroportos = db.query(Aeroportos).all()
    logging.info("GET_ALL_AEROPORTOS")
    aeroportos = []
    for aeroporto in all_aeroportos:
        item = {"id": aeroporto.id,
                "nome": aeroporto.nome,
                "endereço": aeroporto.endereco,
                "sigla": aeroporto.sigla
                }
        aeroportos.append(item)
    logging.info(aeroportos)
    return all_aeroportos


@router.post("/aeroportos")
def post(aeroporto: Aeroporto, db: Session = Depends(get_db)):
    novo_aeroporto = Aeroportos(**aeroporto.model_dump())
    try:
        db.add(novo_aeroporto)
        db.commit()
        db.refresh(novo_aeroporto)
        logging.info("Aeroporto criado com sucesso")
        return { "mensagem": "Aeroporto criado com sucesso",
                 "aeroporto": novo_aeroporto}
    except Exception as e:
            logging.error(e)
            return { "mensagem": "Houve um problema ao inserir o aeroporto",
                 "aeroporto": novo_aeroporto}
 
 
@router.delete("/aeroportos/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Aeroportos).filter(Aeroportos.id == id)
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aeroporto não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/aeroportos/{id}")
def update(id: int, aeroporto:Aeroporto, db:Session = Depends(get_db)):
    updated_post = db.query(Aeroportos).filter(Aeroportos.id == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Aeroporto: {id} não existe')
    else:
        updated_post.update(aeroporto.model_dump(), synchronize_session=False)
        db.commit()
    return updated_post.first()


@router.get("/aeroportos_por_endereco/{endereco}")
def get_aeroportos_por_endereco(endereco: str, db: Session = Depends(get_db)):
    all_aeroportos = db.query(Aeroportos).filter(Aeroportos.endereco == endereco).all()
    logging.info("GET_ALL_AEROPORTOS")
    aeroportos = []
    for aeroporto in all_aeroportos:
        item = {"id": aeroporto.id,
                "nome": aeroporto.nome,
                "endereço": aeroporto.endereco,
                "sigla": aeroporto.sigla
                }
        aeroportos.append(item)
    logging.info(aeroportos)
    return all_aeroportos