dbf_light
=========
https://github.com/idlesign/dbf_light

|release| |lic| |ci| |coverage| |health|

.. |release| image:: https://img.shields.io/pypi/v/dbf_light.svg
    :target: https://pypi.python.org/pypi/dbf_light

.. |lic| image:: https://img.shields.io/pypi/l/dbf_light.svg
    :target: https://pypi.python.org/pypi/dbf_light

.. |ci| image:: https://img.shields.io/travis/idlesign/dbf_light/master.svg
    :target: https://travis-ci.org/idlesign/dbf_light

.. |coverage| image:: https://img.shields.io/coveralls/idlesign/dbf_light/master.svg
    :target: https://coveralls.io/r/idlesign/dbf_light

.. |health| image:: https://landscape.io/github/idlesign/dbf_light/master/landscape.svg?style=flat
    :target: https://landscape.io/github/idlesign/dbf_light/master


Description
-----------

*Light and easy DBF reader*

No fancy stuff, just DBF reading for most common format versions.

* Python 2.7, 3.4+;
* Uses `namedtuple` for row representation and iterative row reading to minimize memory usage;
* Works fine with cyrillic (supports KLADR and CBRF databases).


API
---

.. code-block:: python

    from dbf_light import Dbf


    with Dbf.open('some.dbf') as dbf:

        for field in dbf.field:
            print('Field: %s' % field)

        print('Rows:')

        for row in dbf:
            print(row)

CLI
---

Requires `click` package (can be installed with: `pip install dbf_light[cli]`).

.. code-block:: bash

    $ dbf_light describe myfile.dbf
    $ dbf_light show myfile.dbf
