import os
import re
from typing import Optional

from beancount.core import data, flags
from beancount.utils.defdict import ImmutableDictWithDefault
from beangulp.importer import Importer
from beangulp import cache
from qifparse.parser import QifParser


class QIFImporter(Importer):
    def __init__(self, file_name_mapping=ImmutableDictWithDefault({re.compile(".qif$"): "Expenses:QIF"})) -> None:
        super().__init__()
        self._file_name_mapping = file_name_mapping

    def extract(self, filepath: str, existing_entries: data.Entries) -> data.Entries:
        file = cache.get_file(filepath)
        transactions = list()
        with open(file.name) as f:
            parser = QifParser.parse(f)
            for transaction in parser.get_transactions()[0]:
                data_transaction = data.Transaction(payee=None,
                                                    date=transaction.date.date(),
                                                    flag=flags.FLAG_OKAY,
                                                    narration=transaction.payee,
                                                    meta=data.new_metadata(file.name, 0),
                                                    tags=data.EMPTY_SET,
                                                    links=data.EMPTY_SET,
                                                    postings=[])

                account = self.account(filepath)
                if account:
                    data.create_simple_posting(data_transaction, account, transaction.amount, "GBP")
                transactions.append(data_transaction)
        return transactions

    def identify(self, filepath: str) -> bool:
        for_file = self._mapping_for_file(filepath)
        return for_file is not None

    def account(self, filepath: str) -> data.Account:
        return self._mapping_for_file(filepath)

    def _mapping_for_file(self, filepath: str) -> Optional[str]:
        abspath = os.path.abspath(filepath)
        for mapping in self._file_name_mapping.keys():
            if mapping.search(abspath) is not None:
                return self._file_name_mapping[mapping]
        return None
