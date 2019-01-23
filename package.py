#! /usr/bin/env python

import os
import click

from datapackage import Package


@click.command()
@click.option('--source', help='Path to data directory')
def make_package(source):

    os.chdir(source)
    package = Package()
    package.infer('**/*.csv')
    package.commit()

    print(package.valid)

    package.save('datapackage.json')


if __name__ == '__main__':
    make_package()
