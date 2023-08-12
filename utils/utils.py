__author__ = 'William Souza Alves'
__version__ = '0.1.0'

import numpy as np
import pandas as pd


class Utils:

    def slice_serial_list(serial_list: list) -> list:
        return np.array_split(serial_list, np.ceil(len(serial_list)/2000))
    
    def concat_tables(table_list: list) -> dict:
        return pd.concat(table_list, ignore_index=True).to_dict()
    
    def is_repeated_class(class_in_use: str, last_used_class: str) -> bool:
        return class_in_use == last_used_class