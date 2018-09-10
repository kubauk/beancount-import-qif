import os
import re

from beancount.ingest.importer import ImporterProtocol


class Importer(ImporterProtocol):
    _file_name_re = re.compile(".qif$")

    def name(self):
        return ImporterProtocol.name(self)

    def identify(self, file):
        abspath = os.path.abspath(file.name)
        return self._file_name_re.search(abspath) is not None

    def extract(self, file, existing_entries=None):
        pass

    def file_account(self, file):
        pass

    def file_name(self, file):
        pass

    def file_data(self, file):
       pass