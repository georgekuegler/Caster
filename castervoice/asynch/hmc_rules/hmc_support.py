from castervoice.lib import control, settings, printer


def kill():
    control.nexus().comm.get_com("hmc").kill()