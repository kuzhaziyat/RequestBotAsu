import sqlite3
import threading
conn = sqlite3.connect('users.db', check_same_thread=False)
cur = conn.cursor();
lock = threading.Lock()

print("соединение с БД успешно")

def insert_record_users(userid,fname,lname,number):
    try:
        lock.acquire(True)
        cur.execute("""INSERT OR IGNORE INTO users 
            VALUES(?,?,?,?);""",(userid,fname,lname,number))
        conn.commit();
    finally:
        lock.release()

def insert_record_requests(userid,korpus,status):
    try:
        lock.acquire(True)
        cur.execute("""INSERT OR IGNORE INTO requests(userid,korpus,status)
            VALUES(?,?,?);""",(userid,korpus,status))
        conn.commit();
    finally:
        lock.release()
def select_user_phone(userid):
    try:
        lock.acquire(True)
        cur.execute("select number from users where userid=?", (userid,))
        list = cur.fetchall()
        number = [item[0] for item in list]
        return str(number[0])
    finally:
        lock.release()

def select_id_requests(userid, status):
    try:
        lock.acquire(True)
        cur.execute("select id from requests where userid=? AND status=?", (userid, status))
        list = cur.fetchall()
        id = [item[0] for item in list]
        return str(id[0])
    finally:
            lock.release()

def select_users_id(userid):
    try:
        lock.acquire(True)
        cur.execute("select userid from users where userid=?", (userid,))
        if cur.fetchone() is None:
            return 0
        else:
            return 1
    finally:
            lock.release()

def select_user(userid):
    try:
        lock.acquire(True)
        cur.execute("select * from users where userid=?", (userid,))
        return cur.fetchone()
    finally:
        lock.release()

def select_users():
    try:
        lock.acquire(True)
        cur.execute("select count (*) from users", ())
        return cur.fetchone()[0]
    finally:
        lock.release()

def select_requests():
    try:
        lock.acquire(True)
        cur.execute("select count (*) from requests", ())
        return cur.fetchone()[0]
    finally:
        lock.release()

def select_text_requests(userid, status):
    number = select_user_phone(userid)
    try:
        lock.acquire(True)
        cur.execute("select * from requests WHERE userid=? AND status=? ORDER BY id DESC LIMIT 1", (userid, status))
        list=cur.fetchall()
        id = [item[0] for item in list]
        request = [item[2] for item in list]
        status = [item[3] for item in list]
        korpus = [item[4] for item in list]
        otdel = [item[5] for item in list]
        user = '[Пользователь](tg://user?id=' + str(userid) + ')'
        return '№' + str(id[0]) + '\n' +'+'+ number + '\n'  + user +'\n\n'+ str(otdel[0])+'\n'+ str(korpus[0]) +'\n\n' + str(request[0]) + '\n\nСтатус заявки: ' + str(status[0])
    finally:
        lock.release()

def select_document_request(id):
    try:
        lock.acquire(True)
        cur.execute("select * from requests WHERE id=?", (id,))

        list=cur.fetchall()
        doc = [item[8] for item in list]
        photo = [item[6] for item in list]
        video = [item[7] for item in list]
        file = ''
        if not photo[0]:
            if not video[0]:
                if not doc[0]:
                    pass
                else:
                    file = str(doc[0])
            else:
                file = str(video[0])
        else:
            file = str(photo[0])
        return file
    finally:
        lock.release()
        return 0

def select_id_request_userid(id):
    try:
        lock.acquire(True)
        cur.execute("select userid from requests where id=?", (id,))
        row = [item[0] for item in cur.fetchall()]
        return str(row[0])
    finally:
            lock.release()

def update_status(status,id):
    try:
        lock.acquire(True)
        cur.execute("UPDATE requests SET status=? where id=?", (status, id))
        conn.commit();
    finally:
            lock.release()

def update_otdel(otdel, userid, status):
    try:
        lock.acquire(True)
        cur.execute("UPDATE requests SET otdel=? where userid=? AND status=?", (otdel, userid, status[0]))
        conn.commit();
    finally:
        lock.release()
def update_photo(photoid, userid, status):
    try:
        lock.acquire(True)
        cur.execute("UPDATE requests SET photoid=? where userid=? AND status=?", (photoid, userid, status[0]))
        conn.commit();
    finally:
        lock.release()
def update_video(videoid, userid, status):
    try:
        lock.acquire(True)
        cur.execute("UPDATE requests SET videoid=? where userid=? AND status=?", (videoid, userid, status[0]))
        conn.commit();
    finally:
        lock.release()
def update_document(documentid, userid, status):
    try:
        lock.acquire(True)
        cur.execute("UPDATE requests SET documentid=? where userid=? AND status=?", (documentid, userid, status[0]))
        conn.commit();
    finally:
        lock.release()

def update_request(request, userid, status):
    try:
        lock.acquire(True)
        cur.execute("UPDATE requests SET request=? WHERE userid=? AND status=?", (request, userid, status))
        conn.commit();
    finally:
        lock.release()

def undo_request(userid, status):
    try:
        lock.acquire(True)
        cur.execute("DELETE FROM requests WHERE userid=? AND status=?", (userid, status))
        conn.commit();
    finally:
        lock.release()

conn.commit();