import json
import re

import spacy
from rapidfuzz import process

from app.assets.questions import questions_data
from app.services.swapi_service import fetch_page

nlp = spacy.load('pt_core_news_sm')


def load_attribute_map(questions_data):
    data = json.loads(questions_data)
    attribute_map = {}

    for resource_type, questions in data.items():
        for question_data in questions:
            question = question_data['question']
            attribute = question_data['attribute']
            attribute_map[question] = {'attribute': attribute, 'resource_type': resource_type}

    return attribute_map


attribute_map = load_attribute_map(questions_data)


def preprocess_question(question: str) -> str:
    return re.sub(r'[^\w\s]', '', question.lower())


def extract_entities_from_question(question: str) -> list:
    doc = nlp(question)
    accepted_entities = ['PER', 'LOC', 'ORG', 'MISC']
    entities = [ent.text for ent in doc.ents if ent.label_ in accepted_entities]
    return entities


async def respond_to_question(question: str):
    cleaned_question = preprocess_question(question)

    entities = extract_entities_from_question(cleaned_question)

    if not entities:
        return {'error': f'Não consegui identificar a entidade na pergunta: {question}'}

    entity = entities[0]

    best_match, score, _ = process.extractOne(cleaned_question, attribute_map.keys())
    acceptable_score = 60
    if score > acceptable_score:
        attribute_info = attribute_map[best_match]
        try:
            response_page = await fetch_page(f'/{attribute_info["resource_type"]}', 1, entity)
            return {'message': response_page['results'][0][attribute_info['attribute']]}
        except Exception as e:
            return {'error': f'Ocorreu um erro ao buscar informações: {str(e)}'}

    return {'error': 'Não sei responder a essa pergunta. Tente perguntar de outra forma.'}
