from pathlib import Path
from decimal import Decimal

from contextlib import contextmanager

import pytest

from dbf_light import Dbf, open_db

try:
    sting_types = basestring
except NameError:
    sting_types = str


@pytest.fixture
def dir_fixtures(request):
    return Path(request.module.__file__).resolve().parent / 'fixtures'


@pytest.fixture
def read_db(dir_fixtures):

    @contextmanager
    def read_db_(name):
        with Dbf.open(dir_fixtures / name) as dbf:
            yield dbf

    return read_db_


def test_basic(read_db):

    fnames = [
        'bik_swif.dbf',
        'dbase_03.dbf',  # dBase III without memo file
        # todo uncomment after implementation.
        # 'dbase_30.dbf',  # Visual FoxPro
        # 'dbase_31.dbf',  # Visual FoxPro with AutoIncrement field
        'dbase_83.dbf',  # dBase III with memo file
        'dbase_8b.dbf',  # dBase IV with memo file
        'dbase_f5.dbf',  # FoxPro with memo file
    ]

    for fname in fnames:
        with read_db(fname) as dbf:
            for _row in dbf:
                pass  # check no exception on iteration


def test_cast(read_db):
    with read_db('dbase_83.dbf') as dbf:

        assert len(dbf.fields) == 15
        assert f'{dbf.fields[-1]}' == 'active'

        for row in dbf:
            assert isinstance(row.id, int)
            assert isinstance(row.desc, int)
            assert isinstance(row.cost, Decimal)
            assert isinstance(row.image, sting_types)
            break


def test_cyrillic(read_db):

    with read_db('bik_swif.dbf') as dbf:
        for row in dbf:
            assert row.name_srus == '"СИБСОЦБАНК" ООО'
            break


def test_archive(dir_fixtures):

    with Dbf.open_zip('bik_swif.dbf', dir_fixtures / 'bik_swift-bik.zip', case_sensitive=False) as dbf:

        assert dbf.prolog.records_count == 369

        for row in dbf:
            assert row.name_srus == '"СИБСОЦБАНК" ООО'
            break


def test_open_db(dir_fixtures):

    with open_db('bik_swif.dbf', dir_fixtures / 'bik_swift-bik.zip', case_sensitive=False) as dbf:
        assert dbf.prolog.records_count == 369

    with open_db( dir_fixtures / 'bik_swif.dbf', case_sensitive=False) as dbf:
        assert dbf.prolog.records_count == 369


def test_deleted_rows(dir_fixtures, tmp_path):
    # A copy of the fixture with the second record marked as deleted.
    src = dir_fixtures / "dbase_03.dbf"
    data = bytearray(src.read_bytes())

    header_len = int.from_bytes(data[8:10], "little")
    record_len = int.from_bytes(data[10:12], "little")

    data[header_len + record_len] = ord("*")  # Marker of the second record.

    modified = tmp_path / "modified.dbf"
    modified.write_bytes(data)

    with Dbf.open(src) as dbf:
        rows_expected = [tuple(row) for row in dbf]

    with Dbf.open(modified) as dbf:
        rows_actual = [tuple(row) for row in dbf]

    # The second record is skipped, and the following records stay in sync.
    assert rows_actual == rows_expected[:1] + rows_expected[2:]
