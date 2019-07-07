import sqlite3
from sqlite3 import Error


class SQLite(object):
    database = "database.db"
    graph = "graph.sql"
    metrics = "metrics.sql"
    complicated_metrics = "complicatedmetrics.sql"

    @staticmethod
    def create_connection(db_file):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return None

    @staticmethod
    def create_table(connection, create_table_sql):
        """ create a table from the create_table_sql statement
        :param connection: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """

        try:
            c = connection.cursor()

            with open(create_table_sql) as f:
                schema = f.read()

            c.execute(schema)
        except Error as e:
            print("Error: ", e)

    @staticmethod
    def create_graph(conn, graph):
        """
        Create a new graph into the graph table
        :param conn:
        :param graph:
        :return: graph id
        """
        sql = ''' INSERT INTO graph(uri,metrics)
                  VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, graph)
        return cur.lastrowid

    @staticmethod
    def create_metrics(conn, metrics):
        """
        Create a new metric into the metrics table
        :param conn:
        :param metrics:
        :return: metrics id
        """
        sql = ''' INSERT INTO metrics(nodes,in_degree,out_degree)
                  VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, metrics)
        return cur.lastrowid

    @staticmethod
    def create_complicated_metrics(conn, complicated_metrics):
        """
        Create a new complicated_metric into the complicated_metrics table
        :param conn:
        :param complicated_metrics:
        :return: complicated_metrics id
        """
        sql = ''' INSERT INTO complicated_metrics(minimum,maximum,mean)
                  VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, complicated_metrics)
        return cur.lastrowid

    @staticmethod
    def update_graph(conn, task):
        """
        Update a row of the graph table
        :param conn:
        :param task:
        """
        sql = ''' UPDATE graph
                  SET uri = ? ,
                      metrics = ?
                  WHERE id = ?'''
        cur = conn.cursor()
        cur.execute(sql, task)

    @staticmethod
    def select_all_graphs(conn):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        graphs_dict = {}
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM graph LIMIT 1000")

        rows = cur.fetchall()

        for row in rows:
            graphs_dict[row[0]] = {
                "uri": row[1],
                "metrics": row[2]
            }

        return graphs_dict

    @staticmethod
    def select_metrics_by_id(conn, metrics_id):
        """
        Query tasks by priority
        :param conn: the Connection object
        :param metrics_id:
        :return:
        """
        metrics_dict = {}
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM metrics WHERE id=?", (metrics_id,))
        tuple_list = cur.fetchall()

        for item in tuple_list:
            metrics_dict = {
                "nodes": item[1],
                "in_degree": item[2],
                "out_degree": item[3],
            }

        return metrics_dict

    @staticmethod
    def select_complicated_metrics_by_id(conn, complicated_metrics_id):
        """
        Query tasks by priority
        :param conn: the Connection object
        :param complicated_metrics_id:
        :return:
        """
        complicated_metrics_dict = {}
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM complicated_metrics WHERE id=?", (complicated_metrics_id,))
        tuple_list = cur.fetchall()

        for item in tuple_list:
            complicated_metrics_dict = {
                "min": item[1],
                "max": item[2],
                "mean": item[3],
            }

        return complicated_metrics_dict
