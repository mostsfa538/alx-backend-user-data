#!/usr/bin/env python3
""" Filtered Logger """
import re
from typing import (List)
import logging
import os
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    for f in fields:
        message = re.sub(r'({})=.*?{}'.format(f, separator),
                         r'\1={}{}'.format(redaction, separator), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ formats a record """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """ returns a  logging.Logger object with the right PII fields"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connect to secure database """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=db_name
    )
    return mydb


def main() -> None:
    """ The function will obtain a database connection using get_db()
        and retrieve all rows in the users table
        and display each row under a filtered format
    """

    mydb = get_db()
    logger = get_logger()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM users;")
    cols = cur.column_names
    for row in cur:
        message = "".join(f"{k}={v}; " for k, v in zip(cols, row))
        logger.info(message.strip())
    cur.close()
    mydb.close()


if __name__ == "__main__":
    main()
