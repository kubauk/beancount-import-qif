import os
import re

from beancount.core import data
from beancount.ingest.importer import ImporterProtocol
from qifparse.parser import QifParser


class Importer(ImporterProtocol):
    _file_name_re = re.compile(".qif$")

    def name(self):
        return ImporterProtocol.name(self)

    def identify(self, file):
        abspath = os.path.abspath(file.name)
        return self._file_name_re.search(abspath) is not None

    def extract(self, file, existing_entries=None):
        transactions = list()
        with open(file.name) as f:
            parser = QifParser.parse(f)
            for transaction in parser.get_transactions()[0]:
                data_transaction = data.Transaction(payee=None,
                                                date=transaction.date.date(),
                                                flag=ImporterProtocol.FLAG,
                                                narration=transaction.payee,
                                                meta=data.new_metadata(file.name, 0),
                                                tags=data.EMPTY_SET,
                                                links=data.EMPTY_SET,
                                                postings=[])
                data.create_simple_posting(data_transaction, self.file_account(file), transaction.amount, "GBP")
                transactions.append(data_transaction)
        return transactions

    def file_account(self, file):
        return None

    def file_name(self, file):
        pass

    def file_data(self, file):
       pass