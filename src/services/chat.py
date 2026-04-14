from fastapi import APIRouter, HTTPException, status
from google import genai
from google.genai import types

from schemas.schemas_routes import Message
from schemas.schema_env import settings

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

class Mensagem:
    def __init__(self):
        self.cliente = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.instrucao = """
    Você é o Guia Virtual Oficial do site 'Terê Verde'.
    Sua missão é ajudar turistas e moradores a explorarem os parques naturais, trilhas e a biodiversidade de Teresópolis.
    Principalmente nos seguintes parques : Parnaso, Três Picos e Parque Municipal Montanhas de Teresópolis.
    
    REGRAS DE COMPORTAMENTO:
    1. Seja amigável e use emojis de natureza (🌿, ⛰️, 🥾).
    2. Se o assunto não for Teresópolis ou natureza, recuse educadamente.
    3. Responda de forma curta e direta para caber num chat flutuante.
    """

    async def perguntar(self,mensagem: str):
        try:
            resposta = await self.cliente.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=mensagem,
                config=types.GenerateContentConfig(
                    system_instruction=self.instrucao,
                    temperature=0.7
                )
            )

            return {"resposta": resposta.text}

        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Erro na IA:{str(e)}")



@router.post('/', status_code=status.HTTP_200_OK)
async def get_message(data: Message):

    agente = Mensagem()

    return await agente.perguntar(data.mensagem)
