from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from schemas.schema_env import settings
# cria o motor que irá se conectar ao banco
engine = create_engine(settings.DATABASE_URL)

Base = declarative_base()
# cria uma pool de conexões para acessar o banco
Session = sessionmaker(bind=engine)

# função que injeta um sessão do banco a cada request
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

