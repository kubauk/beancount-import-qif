import os
import re

from beancount.core import data
from beancount.ingest.importer import ImporterProtocol
from beancount.utils.defdict import ImmutableDictWithDefault
from qifparse.parser import QifParser

class Importer(ImporterProtocol):
    def __init__(self, file_name_mapping=ImmutableDictWithDefault({re.compile(".qif$"): "Expenses:QIF"})) -> None:
        super().__init__()
        self._file_name_mapping = file_name_mapping

    def name(self):
        return ImporterProtocol.name(self)

    def identify(self, file):
        for_file = self._mapping_for_file(file)
        return for_file is not None

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

                account = self.file_account(file)
                if account:
                    data.create_simple_posting(data_transaction, account, transaction.amount, "GBP")
                transactions.append(data_transaction)
        return transactions

    def file_account(self, file):
        return self._mapping_for_file(file)

    def file_name(self, file):
        pass

    def file_date(self, file):
       pass

    def _mapping_for_file(self, file):
        abspath = os.path.abspath(file.name)
        for mapping in self._file_name_mapping.keys():
            if mapping.search(abspath) is not None:
                return self._file_name_mapping[mapping]
        return None
