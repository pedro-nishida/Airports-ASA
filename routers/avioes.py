### arquivo models/avioes.py ###
from fastapi          import APIRouter, Depends, HTTPException, Response, status
from schemas.avioes   import Aviao
from models.database  import get_db
from models.avioes    import Avioes
import mensageria.pub as pub
from sqlalchemy.orm   import Session
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

@router.get("/avioes")
def get(db: Session = Depends(get_db)):
    all_avioes = db.query(Avioes).all()
    logging.info("GET_ALL_AVIOES")
    avioes = []
    for aviao in all_avioes:
        item = {"id": aviao.id,
                "modelo": aviao.modelo,
                "quantidade de passageiros": aviao.qtd_passageiros,
                }
        avioes.append(item)       
    logging.info(avioes)
    return all_avioes


@router.post("/avioes")
def post(aviao: Aviao, db: Session = Depends(get_db)):
    novo_aviao = Avioes(**aviao.model_dump())
    try:
        db.add(novo_aviao)
        db.commit()
        db.refresh(novo_aviao)
        logging.info("Avião criado com sucesso")
        pub.publish_message("avioes", "Avião criado com sucesso: " + str(novo_aviao))
        return { "mensagem": "Avião criado com sucesso",
                 "aviao": novo_aviao}
    except Exception as e:
            logging.error(e)
            return { "mensagem": "Problemas para inserir o avião",
                 "aviao": novo_aviao}
 
 
@router.delete("/avioes/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Avioes).filter(Avioes.id == id)
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Avião não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/avioes/{id}")
def update(id: int, aviao:Aviao, db:Session = Depends(get_db)):
    updated_post = db.query(Avioes).filter(Avioes.id == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Avião: {id} não existe')
    else:
        updated_post.update(aviao.model_dump(), synchronize_session=False)
        db.commit()
    return updated_post.first()