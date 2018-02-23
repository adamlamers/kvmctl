import click
from . import machine
from . import configure
from .config import Configuration
import libvirt

@click.group()
@click.option('-c', '--config-file', default='~/.config/kvmctl.conf')
@click.pass_context
def cli(ctx, **kwargs):
    ctx.obj = kwargs
    ctx.obj['CONFIG'] = Configuration(kwargs['config_file'])

    if ctx.obj['CONFIG']['KVM_URI']:
        ctx.obj['kvm']  = libvirt.open(name=ctx.obj['CONFIG']['KVM_URI'])
    elif ctx.invoked_subcommand == 'configure':
        pass
    else:
        click.echo("Missing KVM_URI")
        ctx.abort()

cli.add_command(machine.this)
cli.add_command(configure.this)

if __name__ == '__main__':
    cli()

