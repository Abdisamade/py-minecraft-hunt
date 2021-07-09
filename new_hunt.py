import sqlite3


class NewHunt:
    _con = None
    _SELECT_RAND_TEMPLATE = "SELECT * FROM {} WHERE not isNewFeature AND level = ? ORDER BY RANDOM() LIMIT ?;"
    _SELECT_RAND_TEMPLATE_ALL = "SELECT * FROM {} WHERE not isNewFeature ORDER BY RANDOM() LIMIT ?;"
    _SELECT_RAND_TEMPLATE_NO_3 = "SELECT * FROM {} WHERE not isNewFeature AND level != 3 ORDER BY RANDOM() LIMIT ?;"

    def __init__(self):
        pass

    def connect(self):
        self._con = sqlite3.connect("table.sql")

    def getList(self, model, amount, level):
        cur = self._con.cursor()

        alist = []
        rows = None
        if level == 0:
            query = self._SELECT_RAND_TEMPLATE_ALL.format(model.table_name)
            rows = cur.execute(query, (amount, ))
        elif level == 4:
            query = self._SELECT_RAND_TEMPLATE_NO_3.format(model.table_name)
            rows = cur.execute(query, (amount, ))
        else:
            query = self._SELECT_RAND_TEMPLATE.format(model.table_name)
            rows = cur.execute(query, (level, amount))

        for row in rows:
            alist.append(model(row[1], row[2], row[3], row[0]))

        return alist



    
