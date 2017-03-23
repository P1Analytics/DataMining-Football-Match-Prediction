import os
import sqlite3
import logging

from src.util import util
import src.util.Cache as Cache

sqllite_connections = dict()
log = logging.getLogger(__name__)


class SQLiteConnection(object):
    def __init__(self, database_path="data/db/database.sqlite"):
        self.connection = sqlite3.connect(util.get_project_directory()+database_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def getTableNameDataBase(self):
        tables = []
        for row in self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';"):
            tables.append(row[0])
        return tables

    def getColumnFromTable(self, table_name):
        try:
            return Cache.get_element(table_name, "SQLLITE_COLUMN_TABLE")
        except KeyError:
            pass

        columns = []
        for r in self.cursor.execute("PRAGMA table_info("+table_name+");"):
            columns.append(r[1])

        Cache.add_element(table_name, columns, "SQLLITE_COLUMN_TABLE")
        return columns

    def list_constraints(self):
        for l in self.cursor.execute("select sql from sqlite_master where type='table'"):
            print(str(l))


    def select(self, table_name, column_filter='*', **id):
        id_condition = ""
        if len(id) > 0:
            id_condition = "WHERE "

            for attrbiute, value in id.items():
                id_condition += attrbiute+"='"+str(value).replace("'","''")+"' AND "
            id_condition = id_condition[0:-4]

        if column_filter=='*':
            column_names = self.getColumnFromTable(table_name)
        else:
            column_names = column_filter.split(",")

        row_results = []
        select = "SELECT "+column_filter+" FROM "+table_name+" "+id_condition+";"
        log.debug("select ["+select+"]")
        for sqllite_row in self.cursor.execute(select):
            if sqllite_row is None:
                continue
            row = {}
            for i, name in enumerate(column_names):
                row[name] = sqllite_row[i]
            row_results.append(row)

        log.debug("Rows found: "+str(len(row_results)))
        return row_results

    def select_or(self, table_name, column_filter='*', **or_conditions):
        or_condition = ""
        if len(or_conditions) > 0:
            or_condition = "WHERE "

            for attrbiute, value in or_conditions.items():
                or_condition += attrbiute+"='"+str(value).replace("'","''")+"' OR "
            or_condition = or_condition[0:-3]

        if column_filter == '*':
            column_names = self.getColumnFromTable(table_name)
        else:
            column_names = column_filter.split(",")

        row_results = []
        select = "SELECT "+column_filter+" FROM "+table_name+" "+or_condition+";"
        log.debug("select ["+select+"]")
        for sqllite_row in self.cursor.execute(select):
            if sqllite_row is None:
                continue
            row = {}
            for i, name in enumerate(column_names):
                row[name] = sqllite_row[i]
            row_results.append(row)

        log.debug("Rows found: "+str(len(row_results)))
        return row_results

    def select_like(self, table_name, column_filter='*', columns_order=None, **id):
        id_condition = ""
        if len(id) > 0:
            id_condition = "WHERE "

            for attrbiute, value in id.items():
                id_condition += attrbiute+" like '%"+str(value).replace("'","''")+"%' AND "
            id_condition = id_condition[0:-4]

        if column_filter=='*':
            column_names = self.getColumnFromTable(table_name)
        else:
            column_names = column_filter.split(",")

        if util.is_None(columns_order):
            order_by = ""
        else:
            order_by = " ORDER BY "+columns_order


        row_results = []
        select_like = "SELECT "+column_filter+" FROM "+table_name+" "+id_condition+order_by+";"
        log.debug("Select like ["+select_like+"]")
        for sqllite_row in self.cursor.execute(select_like):
            if sqllite_row is None:
                continue
            row = {}
            for i, name in enumerate(column_names):
                row[name] = sqllite_row[i]
            row_results.append(row)
        return row_results

    def insert(self, table_name, attributes):
        insert = "INSERT INTO "+table_name+" "

        columns = "("
        values  = "VALUES ("
        for column, value in attributes.items():
            columns += column+","
            values += "'"+str(value).replace("'","''")+"',"

        columns = columns[:-1]+")"
        values = values[:-1] + ")"

        insert += columns+" "+values+";"

        log.debug("Begin transaction insert [" + insert + "]")

        old_isolation_level = self.connection.isolation_level
        self.connection.isolation_level = None
        try:
            self.cursor.execute("begin")
            self.cursor.execute(insert)
            self.cursor.execute("commit")
        except Exception as e:
            print("Errror during transaction --> rolling back!")
            self.cursor.execute("rollback")
            raise e
        self.connection.isolation_level = old_isolation_level

        log.debug("Rows inserted: " + str(self.cursor.rowcount))

    def execute_select(self, query):
        rows = []
        for row in self.cursor.execute(query):
            rows.append(row)
        return rows

    def execute_update(self, query):
        log.debug("Transaction update [" + query + "]")
        old_isolation_level = self.connection.isolation_level
        self.connection.isolation_level = None

        try:
            self.cursor.execute("begin")
            self.cursor.execute(query)
            self.cursor.execute("commit")
        except Exception as e:
            print("Errror during transaction --> rolling back!")
            self.cursor.execute("rollback")
            raise e

        self.connection.isolation_level = old_isolation_level
        log.debug("Rows updated: " + str(self.cursor.rowcount))


    def execute_create(self, query):
        log.debug("Transaction create [" + query + "]")
        old_isolation_level = self.connection.isolation_level
        self.connection.isolation_level = None

        try:
            self.cursor.execute("begin")
            self.cursor.execute(query)
            self.cursor.execute("commit")
        except Exception as e:
            print("Errror during transaction --> rolling back!")
            self.cursor.execute("rollback")
            raise e

        self.connection.isolation_level = old_isolation_level

    def delete(self, table_name, object):
        delete = "DELETE FROM " + table_name + " WHERE ID = '" + str(object.id) + "';"
        log.debug("Transaction delete [" + delete + "]")

        old_isolation_level = self.connection.isolation_level
        self.connection.isolation_level = None
        try:
            self.cursor.execute("begin")
            self.cursor.execute(delete)
            self.cursor.execute("commit")
        except Exception as e:
            print("Errror during transaction --> rolling back!")
            self.cursor.execute("rollback")
            raise e

        self.connection.isolation_level = old_isolation_level
        log.debug("Rows deleted: " + str(self.cursor.rowcount))


    def update(self, table_name, object):
        column_names = self.getColumnFromTable(table_name)
        update = "UPDATE "+table_name+" SET "

        for column in column_names:
            value = str(object.__getattribute__(column)).replace("'", "''")
            if util.is_None(value):
                continue
            update += column+"='"+value+"',"

        update = update[:-1]

        update += " WHERE id = '"+str(object.id)+"'"
        self.execute_update(update)

    def create_table(self, table_name, create_stmt):
        for db_table_name in self.getTableNameDataBase():
            if db_table_name == table_name:
                # table already in
                return
        self.execute_create(create_stmt)


def get_connection():
    global sqllite_connections
    try:
        return sqllite_connections[os.getpid()]
    except KeyError:
        log.debug("creating new connection for process "+str(os.getpid()))
        sqllite_connections[os.getpid()] = SQLiteConnection()
        return sqllite_connections[os.getpid()]


def init_database():
    print("> Initialization DB")
    try:
        get_connection().create_table("Match_Event", "CREATE TABLE Match_Event(id INTEGER PRIMARY KEY AUTOINCREMENT, match_id INTEGER)")
        get_connection().create_table("Bet_Event",
                                     "CREATE TABLE Bet_Event(id INTEGER PRIMARY KEY AUTOINCREMENT, match_event_id INTEGER, event_name STRING, bet_value STRING, date STRING)")
        return True
    except sqlite3.OperationalError:
        return False


def read_all(table_name, column_filter='*'):
    return get_connection().select(table_name, column_filter=column_filter)
