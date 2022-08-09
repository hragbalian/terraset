"""Console script for terraset."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for terraset."""
    click.echo("Replace this message by putting your code into "
               "terraset.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0

@click.command()
@click.option("--host", default="<host>", help="Number of greetings.")
@click.option("--username", prompt="<username>", help="The person to greet.")
def create_superset_profile(host, username):
    """Console script for terraset."""
    click.echo(f"host value is {host}")
    click.echo(f"username value is {username}")
    return 0

if __name__ == "__main__":
    create_superset_profile()  # pragma: no cover
