import sqlite3
import os
from models import Item, Elem, Block, Mob

con = None

SELECT_ALL_TEMPLATE = "SELECT * FROM {};"
SELECT_WITH_ID_TEMPLATE = "SELECT * FROM {0} WHERE ID = ?;"

INSERT_TEMPLATE = "INSERT INTO {0} ({1}) VALUES ({2});"

def connect():
    global con
    con = sqlite3.connect("table.sql")


def fetchFromId(model, id):
    cur = con.cursor()
    
    query = SELECT_WITH_ID_TEMPLATE.format(model.table_name)
    one = cur.execute(query, (id,)).fetchone()

    if one[3]:
        return model(one[1], one[2], True, one[0])
    else:
        return model(one[1], one[2], False, one[0])


def fetchAllFromModel(model):
    cur = con.cursor()

    query = SELECT_ALL_TEMPLATE.format(model.table_name)
    all_row = cur.execute(query)

    retval = []

    for row in all_row:
        instance = None
        if row[3]:
            instance = model(row[1], row[2], True, row[0])
        else:
            instance = model(row[1], row[2], False, row[0])

        retval.append(instance)

    return retval

        

def insertModelInstance(model):
    cur = con.cursor()

    table = model.table_name
    columns = []
    values = []
    for column in model.__dict__:
        if column != "id":
            columns.append('"'+column+'"')
            val = model.__dict__[column]
            values.append(val)
        
    query = INSERT_TEMPLATE.format(table, formatColumn(columns), formatValues(values))
    print("Executing insert into table {0}: {1}".format(table, query))
    cur.execute(query)
    con.commit()


def formatValues(values):
    string = ""
    for value in values:
        if type(value) == type(""):
            string += "'"+value+"', "

        if type(value) == type(1):
            string += str(value) + ", "

        if type(value) == type(True):
            if value:
                string += "true, "
            else:
                string += "false, "
    
    return string[:-2]


def formatColumn(columns):
    string = ""
    for column in columns:
        string += column + ", "

    return string[:-2]

connect()

def blocks():
    file_name = "blocks.txt"
    treat(file_name, Block)

def items():
    treat("items.txt", Item)

def mobs():
    treat("mobs.txt", Mob)
    

def treat(file_name, elem):
    
    tmp_file_name = file_name+".tmp"
    lines_to_remove = []
    treated_file = open(file_name, "r")

    nb_of_lines = 1
    for name in treated_file.readlines():
        name = name[:-1]
        entry = input("Save this {} '{}' ? y/n\n".format(elem.table_name, name))
        if entry == ".e":
            print("ok, bye")
            break
        elif(entry != "n"):
            level = 1
            try:
                level = int(input("What level for this {} ? [1-2-3]\n".format(elem.table_name)))
            except Exception as ex:
                pass

            isNewFeature = input("Is new feature ? y/n\n")
            if isNewFeature == "y":
                isNewFeature = True
            else:
                isNewFeature = False

            instance = elem(name, level, isNewFeature)
            insertModelInstance(instance)
            print("saved : {}".format(instance.__dict__))
            lines_to_remove.append(nb_of_lines)

        nb_of_lines += 1

    print("removing lines {} from file '{}'".format(lines_to_remove, file_name))
    treated_file.close()
    removeTmpFile(file_name, tmp_file_name, lines_to_remove)


def removeTmpFile(file_name, tmp_file_name, lines_to_remove):
    with open(file_name, "r") as old_file:
        nb_of_lines =1
        with open(tmp_file_name, "w") as tmp:
            for line in old_file.readlines():
                if not nb_of_lines in lines_to_remove:
                    tmp.write(line)
                nb_of_lines += 1

    os.remove(file_name)
    os.rename(tmp_file_name, file_name)


def fill_db():
    entry = input("[b]locks, [i]tems or [m]obs ?\n")

    if entry == 'm':
        mobs()
    elif entry == 'b':
        blocks()
    elif entry == 'i':
        items()
    else:
        print("Bye")
    

if __name__ == '__main__':
    fill_db()