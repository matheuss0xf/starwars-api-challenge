import logging
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Query

from app.services.question_processing_service import respond_to_question
from app.services.swapi_service import fetch_page

logger = logging.getLogger(__name__)

router = APIRouter()

VALID_RESOURCES = {
    'people': 'name',
    'planets': 'name',
    'species': 'name',
    'films': 'title',
    'starships': 'name',
    'vehicles': 'name',
}


@router.get(
    '/{resource}',
    summary='Busca de recursos do Star Wars',
    description='Resource deve ser preenchido com uma das opções: people, films, '
    'planets, species, starships e vehicles do universo Star Wars.',
)
async def get_starwars(
    resource: str,
    page: int = Query(1, description='Número da página', ge=1),
    search: Optional[str] = Query(None, description='Filtrar por nome/título'),
):
    if resource not in VALID_RESOURCES:
        raise HTTPException(status_code=404, detail='Recurso não encontrado')

    try:
        response = await fetch_page(resource, page, search)

        if 'error' in response:
            raise HTTPException(status_code=502, detail=response['error'])

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f'Erro de filtro: {str(e)}')

    except Exception as e:
        logger.error(f'Erro interno inesperado: {str(e)}')
        raise HTTPException(status_code=500, detail='Erro interno no servidor')


@router.post('/ask', summary='Pergunte e receba uma resposta sobre o universo Star Wars')
async def ask_question(question: str = Body(..., embed=True)):
    response = await respond_to_question(question)
    return response
