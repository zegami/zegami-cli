# Copyright 2018 Zegami Ltd

"""SQL driver wrappers."""

try:
    import sqlalchemy
except ImportError:
    have_driver = False
else:
    have_driver = True


def create_engine(conn_str, verbose):
    """Give engine from url connection string."""
    return sqlalchemy.create_engine(conn_str, echo=verbose)


def create_statement(query_str):
    """Give statement from string query."""
    return sqlalchemy.text(query_str)
