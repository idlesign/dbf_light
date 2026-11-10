# Usage

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
