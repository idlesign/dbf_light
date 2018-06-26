#!/usr/bin/env python
import click

from dbf_light import VERSION_STR, Dbf

arg_db = click.argument('dbfile', type=click.Path(exists=True, dir_okay=False))
opt_encoding = click.option('--encoding', help='Encoding used by DB')


@click.group()
@click.version_option(version=VERSION_STR)
def entry_point():
    """dbf_light command line utilities."""


@entry_point.command()
@arg_db
@opt_encoding
def show(dbfile, encoding):
    """Show .dbf file contents (rows)."""

    with Dbf.open(dbfile, encoding=encoding) as dbf:
        for row in dbf:
            click.secho('')
            for key, val in row._asdict().items():
                click.secho('    %s: %s' % (key, val))


@entry_point.command()
@arg_db
def describe(dbfile):
    """Show .dbf file statistics."""

    with Dbf.open(dbfile) as dbf:
        click.secho('Rows count: %s' % (dbf.prolog.records_count))
        click.secho('Fields:')
        for field in dbf.fields:
            click.secho('    %s: %s' % (field.type, field))


def main():
    entry_point(obj={})


if __name__ == '__main__':
    main()
