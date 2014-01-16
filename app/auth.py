""" Module for net_id authentication """
import ldap


def auth_user(net_id, password):
    """ Authenticate using NetID and password via LDAP """
    # For debugging
    return True
    try:
        l = ldap.initialize("ldap://unrdc1.unr.edu")
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(net_id + "@unr.edu", password)
        return True
    except ldap.INVALID_CREDENTIALS:
        return False
