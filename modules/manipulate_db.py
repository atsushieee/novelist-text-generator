''' database '''
import os
import sqlite3


def create_db(dbFile):
    """
    Create database if there is not dbFile(argument)
    :param dbFile: Name of database
    """
    if not os.path.isfile(dbFile):
        db_file = open(dbFile, 'w')
        db_file.close()


def create_table(dbFile, tableName, scheme):
    """
    :param dbFile: Name of database
    :param tableName: Name of table
    :param scheme: table scheme
    """
    conn = sqlite3.connect(dbFile)
    cur = conn.cursor()
    query = 'CREATE TABLE IF not EXISTS ' + tableName + ' ' + scheme
    cur.execute(query)
    conn.commit()
    conn.close()


def add_dict(dbFile, tableName, dictionary):
    """
    insert records of (word, counter) list
    :param dbFile: Name of database
    :param tableName: Name of table
    :param dictionary: Dictionary for insert
    """
    conn = sqlite3.connect(dbFile)
    cur = conn.cursor()
    values = ' VALUES (NULL, ?, ?)'

    for key, value in dictionary.items():
        temp_array = [key, value]
        query = 'INSERT INTO ' + tableName + values
        cur.execute(query, temp_array)
    conn.commit()
    conn.close()


def select_records(dbFile, tableName, columns, condition):
    """
    :param dbFile: Name of database
    :param tableName: Name of table
    :param column: extracted columns
    :param condition: conditional info for selection of records
    """
    conn = sqlite3.connect(dbFile)
    cur = conn.cursor()
    query = 'SELECT ' + columns + ' FROM ' + tableName + ' ' + condition
    cur.execute(query)
    return cur.fetchall()
