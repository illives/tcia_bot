__author__ = 'William Souza Alves'
__version__ = '0.1.0'

from webscraper.web_scrapper_serial_consult import WebScrapperSerialConsult
from webscraper.web_scrapper_serial_movement import WebScrapperSerialMovement
from sapinvoicedownloader.sap_invoice_downloader import SapInvoiceDownloader


CLASS_HANDLER = {
    'atlasconsult': WebScrapperSerialConsult,
    'atlasmove': WebScrapperSerialMovement,
    'sapinvoice': SapInvoiceDownloader
    }


class ClassHandler:

    def define_classes_based_on_config (value: str) -> object:
        return CLASS_HANDLER.get(value.lower())

