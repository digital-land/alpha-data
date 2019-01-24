#! /usr/bin/env python

import os
import click

from datapackage import Package, Resource
from tableschema import Schema
from datapackage.exceptions import CastError


@click.command()
@click.option('--source', help='Path to data directory')
@click.option('--publisher', help='Three letter local authority code e.g. dac for Dacorum')
def make_package(source, publisher):

    os.chdir(source)
    files = [f for f in os.listdir('data') if f.endswith('.csv')]

    publisher = f"local-authority:{publisher}"
    package = Package({'publisher': publisher})

    for f in files:
        path = f"data/{f}"
        name = f.replace('.csv', '')
        schema = f"https://raw.githubusercontent.com/digital-land/alpha-data/master/schema/{name}-schema.json"
        resource = Resource({'path': path, 'schema': schema})
        package.add_resource(resource.descriptor)

    package.commit()
    package.infer()

    errors = False
    for r in package.resources:
        try:
            r.read(keyed=True)
        except CastError as e:
            print('Error in', os.path.join(source, r.descriptor['path']))
            print(e, e.errors)
            errors = True
    if not errors:
        package.save('datapackage.json')
        print('saved datapackage.json to', source)



if __name__ == '__main__':
    make_package()
