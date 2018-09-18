from unittest.mock import Mock

from hamcrest.core import assert_that
from hamcrest.core.core import is_
from pytest import fixture

from beancount_qif.importer import Importer


@fixture
def importer():
    return Importer()


@fixture
def file_provider():
    def fake_file(filename):
        file = Mock()
        file.name = filename
        return file
    return fake_file


def test_identify_correctly_handles_qif_files(importer, file_provider):
    assert_that(importer.identify(file_provider("download.qif")), is_(True))
    assert_that(importer.identify(file_provider("download.csv")), is_(False))
