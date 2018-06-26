# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import struct
from collections import namedtuple
from contextlib import contextmanager
from functools import partial

from .definitions import get_format_description, Field
from .exceptions import DbfException


class Dbf(object):
    """Represents data from .dbf file."""

    def __init__(self, fileobj, encoding=None, fieldnames_lower=True):
        """
        :param fileobj: Python file-like object containing .dbf file data.

        :param str|unicode encoding: Encoding used by DB.
            This will be used if there's no encoding information in the DB itself.

        :param bool fieldnames_lower: Lowercase field names.

        """
        self._fileobj = fileobj
        self._lower = fieldnames_lower

        cls_prolog = get_format_description(fileobj)

        self.cls_prolog = cls_prolog
        self.cls_field = cls_prolog.cls_field

        prolog = self.cls_prolog.from_file(fileobj)
        self.prolog = prolog

        if encoding is None:
            encoding = prolog.encoding

        self._encoding = encoding or 'cp866'

        self.fields, self.cls_row = self._read_fields()

    def __iter__(self):
        return iter(self.iter_rows())

    @classmethod
    @contextmanager
    def open(cls, filepath, encoding=None, fieldnames_lower=True):
        """Context manager. Allows opening a .dbf file.

        .. code-block::

            with Dbf.open('some.dbf') as dbf:
                ...

        :param str|unicode filepath: .dbf filepath

        :param encoding:

        :param str|unicode encoding: Encoding used by DB.
            This will be used if there's no encoding information in the DB itself.

        :param bool fieldnames_lower: Lowercase field names.

        :rtype: Dbf
        """
        with open(filepath, 'rb') as f:
            yield cls(f, encoding=encoding, fieldnames_lower=fieldnames_lower)

    def iter_rows(self):
        """Generator reading .dbf row one by one.

        Yields named tuple Row object.

        :rtype: Row
        """
        fileobj = self._fileobj
        cls_row = self.cls_row
        fields = self.fields

        for idx in range(self.prolog.records_count):
            data = fileobj.read(1)

            marker = struct.unpack('<1s', data)[0]
            is_deleted = marker == b'*'

            if is_deleted:
                continue

            row_values = []
            for field in fields:
                val = field.cast(fileobj.read(field.len))
                row_values.append(val)

            yield cls_row(*row_values)

    def _read_fields(self):
        fh = self._fileobj
        field_from_file = partial(self.cls_field.from_file, name_lower=self._lower, encoding=self._encoding)

        fields = []
        field_names = []
        for idx in range(self.prolog.fields_count):
            field = field_from_file(fh)  # type: Field
            name = field.name

            if name in field_names:
                # Handle duplicates.
                name = name + '_'
                field.set_name(name)

            fields.append(field)
            field_names.append(name)

        terminator = struct.unpack('<c', fh.read(1))[0]

        if terminator != b'\r':
            raise DbfException(
                'Header termination byte not found. '
                'Seems to be an unsupported format. Signature: %s' % self.prolog.signature)

        cls_row = namedtuple('Row', field_names)

        return fields, cls_row
