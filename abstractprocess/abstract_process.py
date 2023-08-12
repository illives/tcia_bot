__author__ = 'William Souza Alves'
__version__ = '0.1.0'

from abc import ABC, abstractmethod


class AbstractProcess(ABC):
    
    @abstractmethod
    def do_login(self):
        raise NotImplementedError
    
    @abstractmethod
    def execute_process(self):
        raise NotImplementedError
    
    @abstractmethod
    def send_result_data(self):
        raise NotImplementedError
    
