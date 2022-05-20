import sqlite3 as sql

# operation_records

db_name = "db_oper_records.db"
db_table_name = "records"


'''
操作记录表(操作人,动作,执行时间)
'''


def db_init():
    # 数据库或表不存在时会自动创建
    db = sql.connect(db_name)
    db.execute(f"CREATE TABLE IF NOT EXISTS {db_table_name} (operator TEXT, operation INT, time TEXT DEFAULT (datetime('now','localtime')))")
    db.close()


def db_list(cnt):
    # @param: cnt: 取出条数
    db = sql.connect(db_name)
    db.row_factory = sql.Row
    cur = db.cursor()
    cur.execute(f"select * from {db_table_name} order by time desc")  # 降序排序
    data = cur.fetchall()[:cnt]
    db.close()
    return data


def db_append(operator, operation):
    db = sql.connect(db_name)
    cur = db.cursor()
    cur.execute(f"INSERT INTO {db_table_name} (name,score) VALUES (?,?)", (operator, int(operation)))   # 添加数据
    db.commit()
    db.close()
