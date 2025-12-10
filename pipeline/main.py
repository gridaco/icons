import click
from vendor_radix_ui_icons import process as process_radix
from vendor_heroicons import process as process_heroicons
from vendor_lucide_icons import process as process_lucide
from vendor_phosphor_icons import process as process_phosphor
from vendor_octicons import process as process_octicons
from vendor_svgl import process as process_svgl


@click.group()
def cli():
    """
    Icon Pipeline CLI.
    Extracts and processes icons from various vendors.
    """
    pass


# Register individual vendor commands
cli.add_command(process_radix, name="radix-ui-icons")
cli.add_command(process_heroicons, name="heroicons")
cli.add_command(process_lucide, name="lucide-icons")
cli.add_command(process_phosphor, name="phosphor-icons")
cli.add_command(process_octicons, name="octicons")
cli.add_command(process_svgl, name="svgl")


@cli.command(name="all")
@click.pass_context
def process_all(ctx):
    """
    Run all vendor processors.
    """
    click.echo("Running all processors...")
    ctx.invoke(process_radix)
    click.echo("-" * 20)
    ctx.invoke(process_heroicons)
    click.echo("-" * 20)
    ctx.invoke(process_lucide)
    click.echo("-" * 20)
    ctx.invoke(process_phosphor)
    click.echo("-" * 20)
    ctx.invoke(process_octicons)
    click.echo("-" * 20)
    ctx.invoke(process_svgl)
    click.echo("All processors finished.")


if __name__ == "__main__":
    cli()
