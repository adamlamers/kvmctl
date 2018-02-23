import click
import libvirt
import sys
import time
from . import util

@click.group(name='machine')
def this():
    pass

@this.command()
@click.option('--running', is_flag=True)
@click.option('--stopped', is_flag=True)
@click.pass_context
def list(ctx, running, stopped):
    conn = ctx.obj['kvm']

    flags = 0

    if running:
        flags += libvirt.VIR_CONNECT_LIST_DOMAINS_RUNNING

    if stopped:
        flags += libvirt.VIR_CONNECT_LIST_DOMAINS_SHUTOFF

    template = '| {:<20} | {:<20} | {:<9} |'
    click.echo(template.format("Name", "State", "Autostart"))
    click.echo(template.format('-'*20, '-'*20, '-'*9))
    for vm in conn.listAllDomains(flags):
        state, _, _, _, _ = vm.info()
        if vm.autostart() == 1:
            autostart = 'Yes'
        else:
            autostart = 'No'
        click.echo(template.format(vm.name(), util.state_to_string(state), autostart))

@this.command()
@click.argument('name', type=click.STRING)
@click.pass_context
def info(ctx, name):
    conn = ctx.obj['kvm']

    vm = conn.lookupByName(name)

    click.echo("     ID: {}".format(vm.ID()))
    click.echo("   UUID: {}".format(vm.UUIDString()))
    click.echo("OS Type: {}".format(vm.OSType()))
    state, maxmem, mem, cpus, cput = vm.info()
    click.echo("  State: {}".format(util.state_to_string(state)))
    click.echo(" Memory: {}/{}MB".format(mem/1024, maxmem/1024))
    click.echo("  vCPUs: {}".format(cpus))

@this.command()
@click.argument('name', type=click.STRING)
@click.pass_context
def start(ctx, name):
    conn = ctx.obj['kvm']

    vm = conn.lookupByName(name)

    if vm.isActive():
        click.echo("{} is already running.".format(name))
        return

    click.echo("Starting {}...".format(name), nl=False)

    if vm.create() < 0:
        click.echo("Could not start VM.")
        ctx.abort()

    while not vm.isActive():
        click.echo(".", nl=False)
        time.sleep(0.25)
        i += 1
        if i % 40 == 0:
            sys.exit(1)

    click.echo("Started.")

@this.command()
@click.argument('name', type=click.STRING)
@click.option('--force', '-f', is_flag=True)
@click.pass_context
def stop(ctx, name, force):
    conn = ctx.obj['kvm']

    vm = conn.lookupByName(name)

    if not vm.isActive():
        click.echo("{} is not running.".format(name))
        return

    if force:
        vm.destroy()
        click.echo("Force stopped {}".format(name))
        return

    click.echo("Sending ACPI Shutdown signal to {}...".format(name), nl=False)
    result = vm.shutdownFlags(libvirt.VIR_DOMAIN_SHUTDOWN_ACPI_POWER_BTN)
    i = 0
    while vm.isActive():
        click.echo(".", nl=False)
        time.sleep(0.25)
        i += 1
        if i % 40 == 0:
            result = vm.shutdownFlags(libvirt.VIR_DOMAIN_SHUTDOWN_ACPI_POWER_BTN)
    click.echo("done.")

@this.command()
@click.argument('name', type=click.STRING)
@click.option('--quiet', '-q', is_flag=True)
@click.pass_context
def state(ctx, name, quiet):
    conn = ctx.obj['kvm']

    vm = conn.lookupByName(name)
    state, _, _, _, _ = vm.info()

    if quiet:
        sys.exit(state)

    click.echo("{}".format(util.state_to_string(state)))

@this.command()
@click.argument('name', type=click.STRING)
@click.option('--disable/--enable', is_flag=True)
@click.pass_context
def autostart(ctx, name, disable):
    conn = ctx.obj['kvm']

    vm = conn.lookupByName(name)

    if disable:
        pass

    click.echo(disable)
