import logging
from extractors.euskadi import get_euskadi

logging.info('Euskadi Load')
euskadi, pro,loc = get_euskadi()

provinces = euskadi['provinces']
localities = euskadi['localities']
monuments = euskadi['monuments']
