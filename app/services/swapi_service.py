import asyncio
import logging
from typing import Any, Dict, Optional

import httpx

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch_resource_name(resource_url: str, name_field: str) -> Optional[str]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(resource_url)
            response.raise_for_status()

        resource_data = response.json()
        return resource_data.get(name_field)

    except httpx.HTTPStatusError as http_err:
        logger.error(f'Erro HTTP ao acessar {resource_url}: {http_err}')
    except httpx.RequestError as req_err:
        logger.error(f'Erro de conexão ao acessar {resource_url}: {req_err}')
    except Exception as e:
        logger.exception(f'Erro inesperado ao buscar dados do recurso: {e}')

    return None


async def process_links_in_result(result: Dict[str, Any]) -> Dict[str, Any]:
    for field, value in result.items():
        if isinstance(value, list):
            result[field] = [
                await fetch_resource_name(item_url, 'title' if 'films' in field else 'name')
                if item_url.startswith(settings.SWAPI_BASE_URL)
                else item_url
                for item_url in value
            ]

        elif field == 'homeworld':
            result[field] = await fetch_resource_name(value, 'name') or value

    return result


async def fetch_page(
    endpoint: str,
    page: int,
    search: Optional[str] = None,
) -> Dict[str, Any]:
    url = f'{settings.SWAPI_BASE_URL}{endpoint}/'
    params = {'page': page}
    if search:
        params['search'] = search

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

        data = response.json()

        if 'results' not in data:
            logger.warning(f'Resposta inesperada da API: {data}')
            return {'error': 'Formato inesperado da API externa'}

        results = data.get('results', [])

        if not results:
            logger.info(f"Nenhum resultado encontrado para endpoint '{endpoint}' (page={page}, search={search})")
            return {'error': 'Nenhum resultado encontrado'}

        results = await asyncio.gather(*[process_links_in_result(result) for result in results])

        return {
            'page': page,
            'total_items': data.get('count', 0),
            'next': data.get('next'),
            'previous': data.get('previous'),
            'results': results,
        }

    except httpx.HTTPStatusError as http_err:
        logger.error(f'Erro HTTP ao acessar {url}: {http_err}')
        return {'error': f'Falha na requisição: {http_err.response.status_code}'}

    except httpx.RequestError as req_err:
        logger.error(f'Erro de conexão ao acessar {url}: {req_err}')
        return {'error': 'Falha de conexão com a API externa'}

    except Exception as e:
        logger.exception(f'Erro inesperado ao buscar dados: {e}')
        return {'error': 'Erro interno ao processar a solicitação'}
