from fastapi import FastAPI, Form, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import Base, engine, SessionLocal
from models import Item

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Dependência de sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def listar_itens(request: Request, db: Session = Depends(get_db), q: str = None):
    if q:
        itens = db.execute(select(Item).where(Item.nome.like(f"%{q}%"))).scalars().all()
        msg = f"Resultados da busca por: '{q}'"
    else:
        itens = db.execute(select(Item)).scalars().all()
        msg = None
    return templates.TemplateResponse(
        "index.html", {"request": request, "itens": itens, "mensagem": msg}
    )


@app.get("/novo")
def form_criar_item(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.post("/criar")
def criar_item(
    request: Request, nome: str = Form(...), descricao: str = Form(...), db: Session = Depends(get_db)
):
    item = Item(nome=nome, descricao=descricao)
    db.add(item)
    db.commit()
    db.refresh(item)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "itens": db.execute(select(Item)).scalars().all(),
            "mensagem": f"✅ Item '{item.nome}' criado com sucesso!"
        },
    )


@app.get("/editar/{item_id}")
def editar_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return templates.TemplateResponse("edit.html", {"request": request, "item": item})


@app.post("/atualizar/{item_id}")
def atualizar_item(
    request: Request,
    item_id: int,
    nome: str = Form(...),
    descricao: str = Form(...),
    db: Session = Depends(get_db),
):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item.nome = nome
    item.descricao = descricao
    db.commit()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "itens": db.execute(select(Item)).scalars().all(),
            "mensagem": f"✏️ Item '{item.nome}' atualizado com sucesso!"
        },
    )


@app.get("/deletar/{item_id}")
def deletar_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    db.delete(item)
    db.commit()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "itens": db.execute(select(Item)).scalars().all(),
            "mensagem": f"🗑️ Item '{item.nome}' foi excluído!"
        },
    )
