### arquivo models/reservas.py ###
from fastapi          import APIRouter, Depends, HTTPException, Response, status
from schemas.reservas   import Reserva
from models.database  import get_db
from models.reservas    import Reservas
from models.voos    import Voos
#import mensageria.pub as pub
from sqlalchemy.orm   import Session
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

@router.get("/reservas")
def get(db: Session = Depends(get_db)):
    all_reservas = db.query(Reservas).all()
    all_voos = db.query(Voos).all()
    logging.info("GET_ALL_RESERVAS")
    reservas = []
    for reserva in all_reservas:
        for voo in all_voos:
            if voo.id == reserva.id_voo:
                aeroporto_origem = voo.aeroporto_origem
                aeroporto_destino = voo.aeroporto_destino
                data = voo.data
                preco = voo.preco
        item = {"id": reserva.id,
                "nome do cliente": reserva.nome_cliente,
                "cpf": reserva.cpf,
                "id do voo": reserva.id_voo,
                "aeroporto de origem": aeroporto_origem,
                "aeroporto de destino": aeroporto_destino,
                "data": data,
                "preço": preco
                }
        reservas.append(item)       
    logging.info(reservas)
    return reservas


@router.post("/reservas")
def efetuar_reserva(reserva: Reserva, db: Session = Depends(get_db)):
    novo_reserva = Reservas(**reserva.model_dump())
    try:
        db.add(novo_reserva)
        db.commit()
        db.refresh(novo_reserva)
        logging.info("Reserva criado com sucesso")
        #pub.publish_message("reservas", "Reserva criada com sucesso: " + str(novo_reserva))
        return { "mensagem": "Reserva criada com sucesso",
                 "reserva": novo_reserva}
    except Exception as e:
            logging.error(e)
            return { "mensagem": "Problemas para inserir a reserva",
                 "reserva": novo_reserva}
 
 
@router.delete("/reservas/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Reservas).filter(Reservas.id == id)
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reserva não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/reservas/{id}")
def update(id: int, reserva:Reserva, db:Session = Depends(get_db)):
    updated_post = db.query(Reservas).filter(Reservas.id == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Reserva: {id} não existe')
    else:
        updated_post.update(reserva.model_dump(), synchronize_session=False)
        db.commit()
    return updated_post.first()