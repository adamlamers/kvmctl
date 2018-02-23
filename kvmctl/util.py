import libvirt

def state_to_string(state):
    if state == libvirt.VIR_DOMAIN_NOSTATE:
        return 'No State'
    elif state == libvirt.VIR_DOMAIN_RUNNING:
        return 'Running'
    elif state == libvirt.VIR_DOMAIN_BLOCKED:
        return 'Blocked'
    elif state == libvirt.VIR_DOMAIN_PAUSED:
        return 'Paused'
    elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
        return 'Shutdown'
    elif state == libvirt.VIR_DOMAIN_SHUTOFF:
        return 'Shutoff'
    elif state == libvirt.VIR_DOMAIN_CRASHED:
        return 'Crashed'
    elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
        return 'Suspended'
