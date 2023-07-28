import sqlite3
import hashlib
from datetime import datetime

from tabulate import tabulate
# from views import *


def show_courses():
    con = conn()
    cur = con.cursor()
    query = """
        select * from courses
    """
    cur.execute(query)
    return cur.fetchall()


def reader(arr: list):
    arr1 = []
    for i in arr:
        arr1.append(list(i))
    header = ['course id', 'name', 'number of students', 'is active']
    print(tabulate(arr1, headers=header, tablefmt='fancy_grid'))
    return arr1


def show_active_courses():
    con = conn()
    cur = con.cursor()
    query = """
        select * from courses where is_active = ?
    """
    val = (True,)
    cur.execute(query, val)
    return cur.fetchall()


def reg_for_course(user_id: int):
    course_id = int(input('ID: '))

    if course_id in check_course_status(user_id):
        print('You have already registered for this course')
    else:
        con = conn()
        cur = con.cursor()
        query = """
            insert into lists(
                user_id,
                course_id,
                datetime
            ) 
            values(?, ?, ?)
        """
        val = (user_id, course_id, datetime.now())
        cur.execute(query, val)
        con.commit()


def check_course_status(user_id):
    con = conn()
    cur = con.cursor()
    query = """
        select * from lists where user_id = ?
    """
    val = (user_id, )
    cur.execute(query, val)
    con.commit()
    arr = []
    for i in cur.fetchall():
        arr.append(i[2])
    return arr


def show_reg_course(course_id: int):
    con = conn()
    cur = con.cursor()
    query = """
        select * from courses where course_id = ?
    """
    value = (course_id, )
    cur.execute(query, value)
    con.commit()
    return cur.fetchone()


def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_password = sha256.hexdigest()
    return hashed_password


def conn():
    con = sqlite3.connect("database.db")
    return con


def add_course():
    name = input("Course Name: ")
    number = input("Number of students: ")
    is_active = input("Is active: ")
    con = conn()
    cur = con.cursor()
    query = """
        insert into courses (name, number_of_students, is_active)
        values (?, ?, ?)
    """
    val = (name, number, is_active)
    cur.execute(query, val)
    con.commit()


def add_user(data: dict):
    con = conn()
    cur = con.cursor()
    query = """
        insert into users (
        first_name, 
        last_name, 
        birth_day, 
        phone,
        username,
        password
        )
        values (?, ?, ?, ?, ?, ?)
    """
    val = (
        data['name'],
        data['last_name'],
        data['birth_day'],
        data['phone'],
        data['username'],
        hash_password(data['password'])
    )
    cur.execute(query, val)
    con.commit()


def is_active(user_id):
    con = conn()
    cur = con.cursor()
    query = """
        select * from users where user_id = ?
    """
    val = (user_id,)
    cur.execute(query, val)
    con.commit()
    return cur.fetchone()[7]


def register_user():
    data = {
        'name': input('Name: '),
        'last_name': input('Lastname: '),
        'birth_day': input('Birth_day (yyyy-mm-dd): '),
        'phone': input('Phone:  '),
        'username': input('Username: '),
        'password': input('Password: ')
    }
    password1 = input('Confirm password: ')
    if password1 == data['password']:
        return add_user(data)
    else:
        print('Failed: ')


def login_user(username, hashed_password):
    con = conn()
    cur = con.cursor()
    query = """
            select * from users where username = ? and password = ?
        """
    value = (username, hashed_password)
    cur.execute(query, value)
    return cur.fetchone()[0]


def login():
    username = input('Username: ')
    password = input('Password: ')
    hashed_password = hash_password(password)
    if is_active(user_id=login_user(username, hashed_password)):
        admin_page()
    else:
        user_page(login_user(username, hashed_password))


def admin_page():
    while True:
        print('1. Add Course ')
        print('2. Show list of courses ')
        print('3. Show list of active students ')
        print('4. Exit ')
        x = input('Enter: ')
        if x == '1':
            add_course()
        elif x == '2':
            arr = reader(show_courses())
        elif x == '3':
            pass
        elif x == '4':
            break
        else:
            print('Command is wrong!!!')


def user_page(user_id):
    while True:
        print('1. Show list of active courses ')
        print('2. Registration for active courses ')
        print('3. Show list of registration courses')
        print("4. Exit")
        x = input('Enter: ')
        if x == '1':
            reader(show_active_courses())
        elif x == '2':
            reg_for_course(user_id)
        elif x == '3':
            arr = []
            for i in check_course_status(user_id):
                arr.append(show_reg_course(i))
            reader(arr)
        elif x == '4':
            break
        else:
            print("Command is false: ")


def main():
    print('1. Login')
    print('2. Register')
    x = input('Enter: ')
    if x == '1':
        login()
    elif x == '2':
        register_user()
        print("Register completed successfully ")
        print("Please entry login in account")
        login()
    else:
        print("Enter failed !!! ")


main()



