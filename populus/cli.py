import os

import click

from populus import utils
from populus.client import Client


@click.group()
def main():
    pass


@main.command()
def compile():
    """
    Compile contracts.
    """
    click.echo('Compiling!')
    contract_source_paths = utils.get_contract_files(os.getcwd())

    compiled_sources = {}

    for source_path in contract_source_paths:
        try:
            compiler = utils.get_compiler_for_file(source_path)
        except ValueError:
            raise click.ClickException("No compiler available for {0}".format(source_path))
        with open(source_path) as source_file:
            source_code = source_file.read()

        compiled_sources.update(utils._compile_rich(compiler, source_code))

    click.echo(compiled_sources)
    utils.write_compiled_sources(os.getcwd(), compiled_sources)


@main.command()
def deploy():
    """
    Deploy contract(s).
    """
    contracts = utils.load_contracts(os.getcwd())
    client = Client('127.0.0.1', '8545')

    deployed_contracts = utils.deployed_contracts(client, contracts)

    name_padding = max(len(n) + 1 for n in deployed_contracts.keys())
    for name, info in deployed_contracts.items():
        click.echo("{name} @ {addr} via txn:{txn_hash}".format(
            name=name.ljust(name_padding),
            addr=info.get('addr', '<pending>').ljust(42),
            txn_hash=info['txn'].ljust(66),
        ))
