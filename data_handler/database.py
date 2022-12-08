import sqlite3


def get_cursor():
    connection = sqlite3.connect("links.db")
    cursor = connection.cursor()
    return connection, cursor


def create_db():
    con, cur = get_cursor()
    try:
        cur.execute("CREATE TABLE links(title, url, xpath)")
    except sqlite3.OperationalError:
        print("table is already created")
    con.close()


def insert_data(data: list):
    con, cur = get_cursor()
    cur.executemany("INSERT INTO links VALUES(?, ?, ?)", data)
    con.commit()
    con.close()


if __name__ == "__main__":
    insert_data([['snk', 'snkn', 'xcklj']])
