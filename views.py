from accounts import *


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





