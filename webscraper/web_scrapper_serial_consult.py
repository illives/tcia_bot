__author__ = 'William Souza Alves'
__version__ = '0.1.0'

from abstractprocess.abstract_process import AbstractProcess
from apiconnector.api_connector import ApiConnector
from utils.utils import Utils

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebScrapperSerialConsult(AbstractProcess):
    
    def __init__(self, logger, process_data, status_session, driver_session):
        self.logger = logger
        self.process_data = process_data['env']
        self.session = status_session
        self.driver = driver_session if self.session else None
        self.start_webdriver()
        
    @staticmethod
    def send_result_data(table: dict, id: str):
        consult_data = {
            "id": id,
            "data_table": table
        }
        ApiConnector.post_result_data(consult_data)
        
    def start_webdriver(self):
        self.logger.info('Starting webdriver.')
        if not self.session:
            try:
                self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                self.set_webdriver()
                self.logger.info('Latest webdriver version has been instaled. Initiating session.')
            except ValueError:
                self.logger.warning('Error on instaling latest webdriver version. Initiating with last stable version: %s', self.process_data['CHROMEDRIVER_STABLE'])
                self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(version=self.process_data['CHROMEDRIVER_STABLE']).install()))
                self.set_webdriver()
        self.session = True

    def set_webdriver(self):
        self.logger.info('Setting web Session configuration.')
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(220)
        self.logger.info('Setting web Session configuration Done.')

    def execute_selection(self, tag_type: str, constant_name: str, index: str):
        self.logger.info('Selecting by %s the option %s:  tag_name %s', tag_type, str(index), constant_name)
        selection = self.driver.find_element(tag_type, constant_name)
        select_option = Select(selection)
        select_option.select_by_index(str(index))
        self.logger.info('Selection Done.')

    def get_table(self, html_content: str) -> pd.DataFrame:
        self.logger.info('Getting table datas.')
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find(name = 'table')
        return pd.read_html(str(table))[0]

    def do_login(self):
        self.driver.switch_to.frame(self.process_data['IFRAME_PRINCIPAL'])
        self.driver.find_element('id', self.process_data['LOGIN']).send_keys(self.process_data['_user'])
        self.driver.find_element('id', self.process_data['SENHA']).send_keys(self.process_data['_password'])
        self.execute_selection('id', self.process_data['OPERADORA'], self.process_data['OPERADORA_ID'])
        self.driver.find_element('xpath', self.process_data['CONFIRMAR_BUTTON']).click()
        self.logger.info('Login has been Done.')
    
    def is_logged(self):
        self.logger.info('Searching for session element.')
        for element in self.process_data['LOGGED_SESSION']:
            try:
                self.driver.find_element('xpath', element)
                self.logger.info('Session element has been found: %s', str(element))
                return True
            except NoSuchElementException as error:
                self.logger.warning('Not found: %s', error)
        self.logger.info('No element has been found. Session is not logged.')
        return False
    
    def verify_web_session(self):
        if not self.is_logged():
            self.logger.info('Initiating new web session.')
            self.driver.get(self.process_data['URL'])
            self.do_login()
    
    def execute_process(self):
        result_table = []
        self.verify_web_session()
        self.driver.get(self.process_data['URL_RELATORIO'])
        self.driver.find_element('id', self.process_data['ABA_EQUIPAMENTO']).click()
        chunks_serial_lists = Utils.slice_serial_list(self.process_data["SERIAIS_EQUIPAMENTO"])
        for serial_list in chunks_serial_lists:
            self.driver.find_element('xpath', self.process_data["SERIAL_TEXT_AREA"]).clear()
            stacked_serials = '\n'.join(serial_list)
            self.driver.find_element('xpath', self.process_data["SERIAL_TEXT_AREA"]).send_keys(stacked_serials)
            self.driver.find_element('xpath', self.process_data["GERAR_RELATORIO_BUTTON"]).click()
            element = self.driver.find_element('xpath', self.process_data["TABELA_RESULTADO"])
            html_content_table = element.get_attribute('outerHTML')
            result_table.append(self.get_table(html_content_table))
        self.send_result_data(Utils.concat_tables(result_table), self.process_data["ID"] )




         