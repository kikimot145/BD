import pymysql.cursors
import sys
from datetime import datetime

login = "root"
password = ""
db_name = "blog"

conn = pymysql.connect(host = "localhost", user = login, password = password, db = db_name,
                             charset = "utf8mb4", cursorclass = pymysql.cursors.DictCursor)

class WorkBlog():
    @classmethod
    def add_user(cls, email, name, us_name, password):
        sql_add_user = 'INSERT INTO users (email, fullname, username, password) ' \
                       'VALUES ("{}", "{}", "{}", "{}");'.format(email, name, us_name, password)
        sql_all_user = 'SELECT * FROM users;'
        return cursor.execute(sql_add_user), cursor.execute(sql_all_user)

    @classmethod
    def authoriz_user(cls, us_name, passw):
        sql_auth_user = 'UPDATE users SET is_authorization=1 WHERE username = "{}" AND password = "{}" ' \
                        'AND is_authorization = "1";'
        sql_user = 'SELECT id FROM users WHERE is_authorization = "1";'.format(us_name, passw)
        return cursor.execute(sql_auth_user), cursor.execute(sql_user)

    @classmethod
    def all_list_user(cls):
        sql_all_user = 'SELECT * FROM users;'
        return cursor.execute(sql_all_user)

    @classmethod
    def add_new_blog(cls, title, auth):
        sql_new_bl = 'INSERT INTO blog (title, author) VALUES ("{}","{}");'.format(title, auth)
        sql_pr = 'SELECT * FROM blog'
        return cursor.execute(sql_new_bl), cursor.execute(sql_pr)

    @classmethod
    def change_blog(cls, title):
        sql_chang_bl = 'UPDATE blog SET title = "{}";'.format(title)
        return cursor.execute(sql_chang_bl)

    @classmethod
    def delete_blog(cls, title):
        sql_del_bl = 'DELETE FROM blog WHERE title = "{}";'.format(title)
        return cursor.execute(sql_del_bl)

    @classmethod
    def all_list_blog_not_delete(cls):
        sql_all_bl_nd = 'SELECT title FROM blog;'
        return cursor.execute(sql_all_bl_nd)

    @classmethod
    def all_list_blog_auth(cls):
        sql_all_bl_au = 'SELECT title FROM blog, users WHERE blog.author = users.id AND users.is_authorization = 1;'
        return cursor.execute(sql_all_bl_au)

    @classmethod
    def add_post(cls, title, author, descrip, id_post, *args):
        list_execute = list()
        time = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")

        list_execute.append(cursor.execute('INSERT INTO post (title, author, description, time_created) VALUES ' \
                       '("{}", "{}", "{}", "{}");'.format(title, author, descrip, time)))

        for arg in args:
            list_execute.append(cursor.execute('INSERT INTO connect_blog_post (post_id, blog_id) ' \
                              'VALUES ("{}", "{}");'.format(id_post, arg)))

        return list_execute

    @classmethod
    def change_post(cls, id, title = None, descrip = None, *args):
        list_execute = list()
        time = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")

        if title != None and descrip != None:
            list_execute.append(cursor.execute('UPDATE post SET title="{}",decrip="{}",time_created="{}"'
                                               'WHERE id="{}";'.format(title,descrip,time,id)))
        elif title != None:
            list_execute.append(cursor.execute('UPDATE post SET title="{}",time_created="{}" '
                                               'WHERE id="{}";'.format(title,time,id)))
        elif descrip != None:
            list_execute.append(cursor.execute('UPDATE post SET decrip="{}",time_created="{}" '
                                               'WHERE id="{}";'.format(descrip,time,id)))

        for idx in args.count()/2:
            list_execute.append(cursor.execute('UPDATE connect_blog_post SET blog_id="{}" '
                                'WHERE post_id="{}" AND blog_id="{}";').format(args[idx*2], id, args[idx*2 + 1]))

        return list_execute

    @classmethod
    def del_post(cls, id):
        sql_del_post = 'DELETE FROM post WHERE id = "{}";'.format(id)
        sql_del_post_in_blog_post = 'DELETE FROM connect_blog_post WHERE post_id="{}";'.format(id)
        return cursor.execute(sql_del_post), cursor.execute(sql_del_post_in_blog_post)

    @classmethod
    def add_comment(cls, author, descrip, post_id = None, comment_id = None):
        time = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
        sql_add_comment = 'INSERT INTO comments (author, time_created, post_id, comment_id, description) ' \
                          'VALUES ("{}","{}","{}","{}","{}");'.format(author,time,post_id,comment_id,descrip)
        return cursor.execute(sql_add_comment)


    @classmethod
    def all_list_comment_user_post(cls, id, post_id):
        sql_all_comment_user = 'SELECT description FROM comments WHERE id="{}" AND post_id="{}";'.format(id, post_id)
        return cursor.execute(sql_all_comment_user)


cursor = conn.cursor()
#WorkBlog.all_list_blog_auth()
#WorkBlog.all_list_blog_not_delete()
#WorkBlog.add_user("bn9", "blo", "kol", "123")
WorkBlog.add_new_blog('mama', '37')
result = cursor.fetchall()
print(result)
for user in cursor:
    print('{}'. format(user))

cursor.close()
