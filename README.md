# dbf_light

<https://github.com/idlesign/dbf_light>

[![release](https://img.shields.io/pypi/v/dbf_light.svg)](https://pypi.python.org/pypi/dbf_light)
[![lic](https://img.shields.io/pypi/l/dbf_light.svg)](https://pypi.python.org/pypi/dbf_light)
[![coverage](https://img.shields.io/coveralls/idlesign/dbf_light/master.svg)](https://coveralls.io/r/idlesign/dbf_light)

## Description

*Light and easy DBF reader*

No fancy stuff, just DBF reading for most common format versions.

* Uses `namedtuple` for row representation and iterative row reading to minimize memory usage;
* Works fine with cyrillic (supports KLADR and CBRF databases);
* Reads .dbf from zip files.

## API

```python
from dbf_light import Dbf


with Dbf.open('some.dbf') as dbf:

    for field in dbf.fields:
        print('Field: %s' % field)

    print('Rows (%s):' % dbf.prolog.records_count)

    for row in dbf:
        print(row)

# Read `some.dbf` from zip (ignoring filename case):
with Dbf.open_zip('some.dbf', 'here/myarch.zip', case_sensitive=False) as dbf:
    ...
```

## CLI

Requires `click` package (can be installed with: `pip install dbf_light[cli]`).

```shell
$ dbf_light describe myfile.dbf
$ dbf_light show myfile.dbf
```
