from sqlite3 import ProgrammingError
from django.shortcuts import render
import pyodbc

conn_str = (
    r'DRIVER=ODBC Driver 17 for SQL Server;'
    r'SERVER=DESKTOP-BVT6U1A\MSSQLSERVER01;'
    r'DATABASE=cust_db;'
    r'Trusted_Connection=yes;'
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()


def existing_schema(request):
    if request.method == "POST":
        existing_schema = request.POST.get("existing_schema")
        present_schema = request.POST.get("present_schema")
        if existing_schema != "None" and present_schema != "None":
            tables_db = cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{}';".format(str(present_schema)))
            tables_lst = []  # TO GET FORMATTED TABLE NAMES
            for raw_table_names in tables_db:  # WILL OPT RAW DATA LIKE (TABLENAME,)
                for formatted_table_names in raw_table_names:
                    tables_lst.append(formatted_table_names)
            print(tables_lst)
        try:
            for table_name in tables_lst:
                if table_name == "Order":
                    temp = 'ALTER SCHEMA {} TRANSFER {}."{}"'.format(existing_schema, present_schema, table_name)
                    cursor.execute(temp)
                    cursor.commit()
                else:
                    temp = 'ALTER SCHEMA {} TRANSFER {}.{}'.format(existing_schema, present_schema, table_name)
                    cursor.execute(temp)
                    cursor.commit()
        except ProgrammingError:
            print("EXCEPTION HIT \n")
            # return HttpResponse("<h1>Error Detected</h1>")


    return render(request, 'data_update/existing_schema.html')


def migrate_to_new_schema(request):
    if request.method == "POST":
        old_schema = request.POST.get("old_schema")
        new_schema = request.POST.get("new_schema")
        if old_schema != "None" and new_schema != "None": 
            print("old_schema ", old_schema)
            print("new_schema ", new_schema)
            tables_db = cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{}';".format(str(old_schema)))
            tables_lst = []  # TO GET FORMATTED TABLE NAMES
            for raw_table_names in tables_db:  # WILL OPT RAW DATA LIKE (TABLENAME,)
                for formatted_table_names in raw_table_names:
                    tables_lst.append(formatted_table_names)  # STORE FORMATTED NAMES OF TABLE
            print("TABLES LIST ", tables_lst)
        try:
            cursor.execute('DROP SCHEMA IF EXISTS ' + new_schema + ';')
            cursor.execute('CREATE SCHEMA ' + new_schema)
            for table_name in tables_lst:
                cursor.execute('ALTER SCHEMA {} TRANSFER {}.{}'.format(new_schema, old_schema, table_name))
                cursor.commit()
        except ProgrammingError:
            print("EXCEPTION HIT \n")
            # return HttpResponse("<h1>Error Detected</h1>")
    return render(request, 'data_update/to_new_schema.html')


def insert_update_delete(request):
    if request.method == "POST":
        get_cud = request.POST.get("get_cud")
        cursor.execute(get_cud)
        cursor.commit()
    return render(request, 'data_update/insert_update_delete.html')

def delete_table_or_schema(request):
    if request.method == "POST":
        table__or_schema_delete = request.POST.get("table__or_schema_delete")
        cursor.execute(table__or_schema_delete)
        cursor.commit()
    return render(request, 'data_update/delete_table_or_schema.html')