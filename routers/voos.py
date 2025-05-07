
from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas.voos import Voo
from models.database import get_db
from models.voos import Voos
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()


@router.get("/voos")
def get(db: Session = Depends(get_db)):
    try:
        all_voos = db.query(Voos).all()
    except:
        return "Não foi possível consultar o banco de dados"
    logging.info("GET_ALL_VOOS")
    voos = []
    for voo in all_voos:
        item = {"id": voo.id,
                "aeroporto de origem": voo.aeroporto_origem,
                "aeroporto de destino": voo.aeroporto_destino,
                "assentos disponíveis": voo.assentos_disponiveis,
                "data": voo.data,
                "preço": voo.preco,
                "id do avião": voo.id_aviao
                }
        voos.append(item)       
    logging.info(voos)
    return all_voos


@router.post("/voos")
def post(voo: Voo, db: Session = Depends(get_db)):
    novo_voo = Voos(**voo.model_dump())
    try:
        db.add(novo_voo)
        db.commit()
        db.refresh(novo_voo)
        logging.info("Voo criado com sucesso")
        return { "mensagem": "Voo criado com sucesso",
                 "voo": novo_voo}
    except Exception as e:
            logging.error(e)
            return { "mensagem": "Problemas para inserir o voo",
                 "voo": novo_voo}
 
 
@router.delete("/voos/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Voos).filter(Voos.id == id)
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Voo não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/voos/{id}")
def update(id: int, voo:Voo, db:Session = Depends(get_db)):
    updated_post = db.query(Voos).filter(Voos.id == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Voo: {id} não existe')
    else:
        updated_post.update(voo.model_dump(), synchronize_session=False)
        db.commit()
    return updated_post.first()


@router.get("/voos_na_data/{data}")
def get_voos_na_data(data: str, db: Session = Depends(get_db)):
    all_voos = db.query(Voos).filter(Voos.data == data).all()
    logging.info("GET_ALL_VOOS")
    voos = []
    for voo in all_voos:
        item = {"id": voo.id,
                "aeroporto de origem": voo.aeroporto_origem,
                "aeroporto de destino": voo.aeroporto_destino,
                "assentos disponíveis": voo.assentos_disponiveis,
                "data": voo.data,
                "preço": voo.preco,
                "id do avião": voo.id_aviao
                }
        voos.append(item)       
    logging.info(voos)
    return all_voos


@router.get("/pesquisar_voos/{data}/{assentos_comprados}")
def get_voos_por_preco(data: str, assentos_comprados:int, db: Session = Depends(get_db)):
    voo = db.query(Voos).filter(Voos.assentos_disponiveis >= assentos_comprados).filter(Voos.data == data).order_by(Voos.preco).all()
    if voo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Voo com {assentos_comprados} assentos disponíveis não existe")
    return voo