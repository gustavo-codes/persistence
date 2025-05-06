import logging.config
import yaml
import logging
import json
from jsonschema import validate, ValidationError

userschema = {
    'type' : 'object',
    'properties' : {
        'id':{'type':'number'},
        'name':{'type':'string'},
        'age':{'type':'number'}
    },
    'required': ['id','name','age']
}

with open('config.yaml','rt') as file:
    config = yaml.safe_load(file.read())

logging.config.dictConfig(config)

logger = logging.getLogger()

with open('data.json','r') as file:
    data = json.load(file)
    logger.info(f'Arquivo JSON {file.name} carregado com succeso')

for u in data:
    try:
        validate(instance=u,schema=userschema)
        logger.info(f'Processando registro {u}')
    except ValidationError as e:
        logger.warning(f'Erro no registro: {u} erro: {e.message}')
