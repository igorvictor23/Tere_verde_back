from fastapi import APIRouter, status
import httpx

from schemas.schemas_routes import (
    WeatherReq,
    WeatherResponse
)

router = APIRouter(
    prefix="/weather",
    tags=["weather"]
)

class Clima:
    def __init__(self):
        self.lat = -22.4172064
        self.lon = -42.9874811

    async def busca_clima(self, data):
        async with httpx.AsyncClient() as client:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&start_date={data}&end_date={data}&daily=weathercode,temperature_2m_max&timezone=America/Sao_Paulo"

            resposta = await client.get(url)
            resposta.raise_for_status()


            dados = resposta.json()


            temperatura = dados["daily"]["temperature_2m_max"][0]
            codigo_wmo = dados["daily"]["weathercode"][0]

            tabela_clima = {
                0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
                45: "🌫️", 48: "🌫️", 51: "🌦️", 53: "🌧️",
                55: "🌧️", 61: "🌧️", 63: "🌧️", 65: "⛈️",
                71: "🌨️", 80: "🌦️", 95: "🌩️"
            }

            emoji_clima = tabela_clima.get(codigo_wmo, "🌍")


            return {
                "temperatura": temperatura,
                "emoji": emoji_clima
            }




@router.post("/", response_model=WeatherResponse,status_code=status.HTTP_200_OK)
async def get_weather(data : WeatherReq):
    wf = Clima()

    response =  await wf.busca_clima(data.data)

    return response








