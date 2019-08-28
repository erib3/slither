import abc
from collections import OrderedDict

class IncorrectPrinterInitialization(Exception):
    pass


class AbstractPrinter(metaclass=abc.ABCMeta):
    ARGUMENT = ''  # run the printer with slither.py --ARGUMENT
    HELP = ''  # help information

    WIKI = ''

    def __init__(self, slither, logger):
        self.slither = slither
        self.contracts = slither.contracts
        self.filename = slither.filename
        self.logger = logger

        if not self.HELP:
            raise IncorrectPrinterInitialization('HELP is not initialized {}'.format(self.__class__.__name__))

        if not self.ARGUMENT:
            raise IncorrectPrinterInitialization('ARGUMENT is not initialized {}'.format(self.__class__.__name__))

        if not self.WIKI:
            raise IncorrectPrinterInitialization('WIKI is not initialized {}'.format(self.__class__.__name__))

    def info(self, info):
        if self.logger:
            self.logger.info(info)

    @staticmethod
    def _create_base_element(type, type_specific_fields={}, additional_fields={}):
        element = {'type': type}
        if type_specific_fields:
            element['type_specific_fields'] = type_specific_fields
        if additional_fields:
            element['additional_fields'] = additional_fields
        return element

    def add_file_to_json(self, filename, content, d, additional_fields={}):
        type_specific_fields = {
            'filename': filename,
            'content': content
        }
        element = self._create_base_element('file',
                                            type_specific_fields,
                                            additional_fields)

        d['elements'].append(element)

    def add_dictionary_to_json(self, content, d, additional_fields={}):
        type_specific_fields = {
            'dictionary': content,
        }
        element = self._create_base_element('dictionary',
                                            type_specific_fields,
                                            additional_fields)

        d['elements'].append(element)

    def add_pretty_table_to_json(self, content, name, d, additional_fields={}):
        type_specific_fields = {
            'content': content,
            'name': name
        }
        element = self._create_base_element('pretty_table',
                                            type_specific_fields,
                                            additional_fields)

        d['elements'].append(element)

    def generate_json_result(self, info, additional_fields={}):
        d = OrderedDict()
        d['printer'] = self.ARGUMENT
        d['description'] = info
        d['elements'] = []
        if additional_fields:
            d['additional_fields'] = additional_fields
        return d

    @abc.abstractmethod
    def output(self, filename):
        """TODO Documentation"""
        return
