__author__ = 'William Souza Alves'
__version__ = '0.1.0'

import logging
from utils.utils import Utils
from apiconnector.api_connector import ApiConnector
from classhandler.class_handler import ClassHandler


logger = logging.getLogger('TCIA_CONSULT_BOT')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('log.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


if __name__=='__main__':
    logger.info('Initiating...')
    process_data = ApiConnector.get_config_data()
    logger.info('Data has been got with sucess.')
    last_used_class_name = ''
    status_session = False
    driver_session = None
    for data in process_data:
        handler_class = ClassHandler.define_classes_based_on_config(data['process'])
        repeated_class = Utils.is_repeated_class(str(handler_class).split('.')[-1], last_used_class_name)
        logger.info('Selecting Class %s for id %s.', str(handler_class), data["env"]["ID"])
        if not status_session or not repeated_class:
            handler = handler_class(logger, data, status_session, driver_session)
        handler.execute_process()
        driver_session = handler.driver
        status_session = handler.session
        last_used_class_name = str(handler_class).split('.')[-1]
        


