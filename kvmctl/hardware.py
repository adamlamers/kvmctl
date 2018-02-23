import libvirt
import click
from xml.dom import minidom

@click.group(name='hardware')
def this():
    pass

@this.command()
@click.argument('name', type=click.STRING)
@click.pass_context
def describe(ctx, name):
    conn = ctx.obj['kvm']

    dom = conn.lookupByName(name)

    raw_xml = dom.XMLDesc(0)
    xml = minidom.parseString(raw_xml)

    disks = xml.getElementsByTagName('disk')
    for disk in disks:
        disk_type = disk.getAttribute('type')
        print(disk_type)
    print(raw_xml)
