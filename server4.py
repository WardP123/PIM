###############################################################################
# Web Technology at VU University Amsterdam
# Assignment 3
#
# The assignment description is available on Canvas.
# This is a template for you to quickly get started with Assignment 3.
# Read through the code and try to understand it.
#
# Have you looked at the documentation of bottle.py?
# http://bottle.readthedocs.org/en/stable/index.html
#
# Once you are familiar with bottle.py and the assignment, start implementing
# an API according to your design by adding routes.
###############################################################################

# Include more methods/decorators as you use them
# See http://bottle.readthedocs.org/en/stable/api.html#bottle.Bottle.route

from bottle import get, post, route, request, delete, error, put, response
import json
import sqlite3
import random

    # TODO: add code that checks for errors so you know what went wrong.
    # TODO: set the appropriate HTTP headers and HTTP response codes here.

MAX_GAME_CODE = 99
MIN_GAME_CODE = 10


# GET
## acutually put
@post('/new-game')
def make_new_game(db):
   if request.json is not None:
       item = request.json
       while True:
           gamecode = random.randint(MIN_GAME_CODE, MAX_GAME_CODE)
           gamecode_str = str(gamecode)
           db.execute("SELECT * FROM games WHERE gameid=?", (gamecode_str,))
           if not db.fetchall():
               break
       db.execute("INSERT INTO games (gameid, groupname) VALUES (?, ?)",(str(gamecode), item['groupname']))
   return json.dumps(gamecode)

@get('/make-test-group/groupid=<groupid>&groupname=<groupname>')
def make_test_group(db, groupid, groupname):
    db.execute("INSERT INTO games (gameid, groupname) VALUES (?, ?)", (groupid, groupname))



# @post('/new-game')
# def make_new_game(db):
#     response.headers['Access-Control-Allow-Methods'] = 'POST'
#     response.headers['Accept'] = 'json'
#     response.headers['Access-Control-Allow-Origin'] = 'http://create-group.html'
#     response.content_type = 'application/json; charset=UTF-8'
#
#     body = request.forms
#     game_name = body['groupname']
#
#     gamecode = random.randint(MIN_GAME_CODE, MAX_GAME_CODE)
#     gamecode_str = str(gamecode)
#
#     db.execute("SELECT * FROM games")
#     games = db.fetchall()
#     for game in games:
#         if game['gameid'] == gamecode_str:
#             return json.dumps("Game ID bestaat al")
#
#     db.executescript("""
#         INSERT INTO games
#         (gameid, groupname)
#         VALUES ('%s', '%s');
#         """ % (gamecode_str, game_name))
#     return json.dumps(gamecode)
#
#     currentstatus = response.status
#     return json.dumps(currentstatus)

@get('/all-gamecodes')
def get_all_gamecodes(db):
    db.execute("SELECT * FROM games")
    all_games = db.fetchall()
    return json.dumps(all_games)

@get('/all-announcements')
def get_all_announcements(db):
    db.execute("SELECT * FROM announcements")
    all_announcements = db.fetchall()
    return json.dumps(all_announcements)

@get('/announcement/gameid=<gameid>')
def get_announcement_by_gameid(db, gameid):
    db.execute("SELECT * FROM announcements WHERE gameid=?", (gameid,))
    gameid_announcements = db.fetchall()
    return json.dumps(gameid_announcements)
## acutually put

@get('/new-announcement/gameid=<gameid>&title=<announcement>&decription=<description>')
def new_announcement(db, gameid, announcement, description):
    db.execute("SELECT * FROM users WHERE gameid=?", (str(gameid),))
    all_users = db.fetchall()
    for user in all_users:
        new_unreadmessages =  (user['unreadannouncements'] + 1)
        db.execute("UPDATE users SET unreadannouncements=? WHERE id=?", (new_unreadmessages, user['id']))
    db.execute("INSERT INTO announcements (gameid, announcementtitle, announcementdecription) VALUES (?, ?, ?)", (gameid, announcement, description))

## acutually delete
@get('/DELETE-ALL')
def delete_all_games(db):
    db.execute("DELETE FROM games")

@post('/new-appointment')
def new_appointment(db):
    appointment = request.json
    db.execute("INSERT INTO appointments (gameid, type, title, description, times) VALUES (?, ?, ?, ?, ?)", (appointment['gameid'], "appointment", appointment['title'], appointment['description'], appointment['times']))

@post('/new-quiz')
def new_appointment(db):
    appointment = request.json
    db.execute("INSERT INTO appointments (gameid, type, title, times) VALUES (?, ?, ?, ?)", (appointment['gameid'], "quiz", appointment['title'], appointment['times']))

@get('/getuserdata/authkey=<key>')
def getuserinfo(db, key):
    # authentication = request.get_cookie("account",)
    authentication = key
    db.execute("SELECT * FROM users WHERE activesessionCoockie=?", (str(authentication),))
    user = db.fetchall()
    return json.dumps(user)

@post('/announcements')
def getannouncements(db):
    item = request.json;
    authentication = item['authkey']
    # authentication = key
    db.execute("SELECT * FROM users WHERE activesessionCoockie=?", (str(authentication),))
    user = db.fetchall()
    if not user:
        return "ERROR NO LOGIN."
    db.execute("SELECT * FROM users WHERE gameid=?", (str(user[0]['gameid']),))
    all_users = db.fetchall()
    for userx in all_users:
        new_unreadmessages = 0
        db.execute("UPDATE users SET unreadannouncements=? WHERE id=?", (new_unreadmessages, userx['id']))
    db.execute("SELECT * FROM announcements WHERE gameid=?", (str(user[0]['gameid']),))
    announcements = db.fetchall();
    return json.dumps(announcements)

@post('/getuserdata')
def getuserinfo(db):
    item = request.json;
    authentication = item['authkey']
    print(authentication)
    db.execute("SELECT * FROM users WHERE activesessionCoockie=?", (str(authentication),))
    user = db.fetchall()
    return json.dumps(user)

@post('/home')
def home(db):
    item = request.json;
    authentication = item['authkey']
    print(authentication)
    # authentication = key
    db.execute("SELECT * FROM users WHERE activesessionCoockie=?", (str(authentication),))
    user = db.fetchall()
    if not user:
        return "ERROR NO LOGIN."
    db.execute("SELECT * FROM appointments WHERE gameid=?", (str(user[0]['gameid']),))
    appointments = db.fetchall();
    return json.dumps(appointments)


# @get('/home')
# def home(db):
#     print(request.get_cookie("account"))
#     authentication = request.get_cookie("account")
#     # authentication = key
#     print(authentication)
#     db.execute("SELECT * FROM users WHERE activesessionCoockie=?", (str(authentication),))
#     user = db.fetchall()
#     if not user:
#         return "ERROR NO LOGIN."
#     db.execute("SELECT * FROM appointments WHERE gameid=?", (str(user[0]['gameid']),))
#     appointments = db.fetchall();
#     return json.dumps(appointments)

@post('/make_new_game')
def make_new_game(db):
    item = request.json
    if not item:
        return 'no data sumbmitted'
    db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
    currentadmin = db.fetchall()
    if not currentadmin:
        return 'error no login'
    while True:
        gamecode = random.randint(MIN_GAME_CODE, MAX_GAME_CODE)
        gamecode_str = str(gamecode)
        print("Test")
        db.execute("SELECT * FROM games WHERE gameid=?", (gamecode_str,))
        if not db.fetchall():
            break
    db.execute("INSERT INTO games (gameid, groupname, lockstatus) VALUES (?, ?, ?)",(str(gamecode), item['groupname'], 'unlocked'))
    db.execute("SELECT id FROM games WHERE gameid=?", (str(gamecode),))
    currentgroup = db.fetchall()
    db.execute("INSERT into adminsgroup (gameid, adminid) VALUES (?, ?)", (str(currentgroup[0]['id']), str(currentadmin[0]['id'])))
    return_string = {"gameid": gamecode}
    return json.dumps(return_string)

@post('/groups')
def groups(db):
    item = request.json
    if not item:
        return 'no data sumbmitted'
    db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
    currentadmin = db.fetchall()
    if not currentadmin:
        return 'error no login'
    db.execute(""" SELECT games.gameid, games.groupname FROM ((admins
    INNER JOIN adminsgroup on adminsgroup.adminid = admins.id)
    INNER JOIN games on games.id = adminsgroup.gameid)
    WHERE admins.id = ?
    """, (str(currentadmin[0]['id']),))
    currentgroups = db.fetchall()
    for group in currentgroups:
        db.execute("SELECT COUNT(id) FROM users WHERE gameid=?", (str(group['gameid']),))
        count = db.fetchall()
        group['joinedusers'] = count[0]['COUNT(id)']
    return json.dumps(currentgroups)

@delete('/group')
def delete_group(db):
    item = request.json
    if not item:
        return 'no data sumbmitted'
    db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
    currentadmin = db.fetchall()
    if not currentadmin:
        return 'error no login'
    db.execute("SELECT id FROM games WHERE gameid=?", (str(item['gameid']),))
    currentgame = db.fetchall()
    db.execute("DELETE FROM games WHERE gameid=?", (str(item['gameid']),))
    db.execute("DELETE FROM adminsgroup WHERE gameid=?", (str(currentgame[0]['id']),))
    db.execute("DELETE FROM users WHERE gameid=?", (str(item['gameid']),))
    db.execute("DELETE FROM announcements WHERE gameid=?", (str(item['gameid']),))
    db.execute("DELETE FROM quiz WHERE gameid=?", (str(item['gameid']),))
    db.execute("DELETE FROM appointments WHERE gameid=?", (str(item['gameid']),))
    return "succes"

@post('/new-announcement')
def new_announcement(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
    	db.execute("SELECT * FROM users WHERE gameid=?", (item['gameid'],))
    	all_users = db.fetchall()
    	for user in all_users:
    		new_unreadmessages =  (user['unreadannouncements'] + 1)
    		db.execute("UPDATE users SET unreadannouncements=? WHERE id=?", (new_unreadmessages, user['id']))
    	db.execute("INSERT INTO announcements (gameid, announcementtitle, announcementdecription, date) VALUES (?, ?, ?, ?)", (item['gameid'], item['announcementtitle'], item['announcementdescription'], item['date'],))
    	return(item['gameid'])

@post('/new-appointment')
def new_appointment(db):
    if request.json is not None:
    	item = request.json
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
    	db.execute("INSERT INTO appointments (gameid, type, title, description, times) VALUES (?, ?, ?, ?, ?)", (item['gameid'], "appointment", item['title'], item['description'], item['time']))
    	return json.dumps(item['gameid'])

@post('/new-quiz')
def new_quiz(db):
    if request.json is not None:
        item = request.json
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("INSERT INTO appointments (gameid, type, title, times) VALUES (?, ?, ?, ?)", (item['gameid'], "quiz" , item['title'],  item['time']))
        return json.dumps(item['gameid'])

@post('/delete-user')
def delete_user(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("DELETE FROM users WHERE gameid=? AND username=?", (item['gameid'], item['username']))
	return json.dumps(item)

@post('/announcement-title')
def announcement_title(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("SELECT * FROM announcements WHERE id=?", (item['id'],))
        announcements = db.fetchall()
        return json.dumps(announcements)

@post('/delete-announcement')
def delete_announcement(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("SELECT * FROM announcements WHERE id=?", (item['id'],))
        announcement = db.fetchall()
        db.execute("DELETE FROM announcements WHERE id=?", (item['id'],))
        return json.dumps(announcement)

@post('/appointment-title')
def appointment_title(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("SELECT * FROM appointments WHERE id=?", (item['id'],))
        appointments = db.fetchall()
        return json.dumps(appointments)

@post('/delete-appointment')
def delete_appointment(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("SELECT * FROM appointments WHERE id=?", (item['id'],))
        appointment = db.fetchall()
        db.execute("DELETE FROM appointments WHERE id=?", (item['id'],))
        return json.dumps(appointment)

@post('/retrieve-users')
def retrieve_users(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("SELECT * FROM users WHERE gameid=?", (item['gameid'],))
        users = db.fetchall()
        return json.dumps(users)

@post('/retrieve-announcements')
def retrieve_announcements(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("SELECT * FROM announcements WHERE gameid=?", (item['gameid'],))
        announcements = db.fetchall()
        return json.dumps(announcements)

@post('/retrieve-appointments')
def retrieve_appointments(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("SELECT * FROM appointments WHERE gameid=?", (item['gameid'],))
        appointments = db.fetchall()
        return json.dumps(appointments)

@post('/announcement-title')
def announcement_title(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("SELECT * FROM announcements WHERE id=?", (item['id'],))
        announcements = db.fetchall()
        return json.dumps(announcements)

@post('/update-announcement')
def update_announcement(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("UPDATE announcements SET announcementtitle=? WHERE id=?", (item['title'], item['id'],))
        db.execute("UPDATE announcements SET announcementdecription=? WHERE id=?", (item['description'], item['id'],))
        db.execute("UPDATE announcements SET date=? WHERE id=?", (item['date'], item['id'],))
        return json.dumps(item)

@post('/update-appointment')
def update_appointment(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("UPDATE appointments SET title=? WHERE id=?", (item['title'], item['id'],))
        db.execute("UPDATE appointments SET description=? WHERE id=?", (item['description'], item['id'],))
        db.execute("UPDATE appointments SET times=? WHERE id=?", (item['time'], item['id'],))
        return json.dumps(item)

@post('/lock-group')
def lock_group(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("UPDATE games SET lockstatus=? WHERE gameid=?", (item['lockstatus'], item['gameid'],))
        db.execute("SELECT * FROM games WHERE gameid=?", (item['gameid'],))
        game = db.fetchall()
        return json.dumps(game)

@post('/check-lock')
def check_lock(db):
    item = request.json
    if item is not None:
        db.execute("SELECT id FROM admins WHERE authkey=?", (str(item['authkey']),))
        currentadmin = db.fetchall()
        if not currentadmin:
            return 'error no login'
        db.execute("SELECT * FROM games WHERE gameid=?", (item['gameid'],))
        game = db.fetchall()
        return json.dumps(game)

@post('/appointment')
def appointment(db):
    item = request.json;
    authentication = item['authkey']
    print(authentication)
    db.execute("SELECT * FROM users WHERE activesessionCoockie=?", (str(authentication),))
    user = db.fetchall()
    if not user:
        return "ERROR NO LOGIN."
    db.execute("SELECT * FROM appointments WHERE id=?", (str(item['id']),))
    appointments = db.fetchall();
    return json.dumps(appointments)

## allow_login
@post('/get_group_info')
def getgroupinfo(db):
    item = request.json;
    if not item:
        return "empty json"
    db.execute("SELECT * FROM games WHERE gameid=?", (str(item['gameid']),))
    group = db.fetchall()
    return json.dumps(group)

@post('/check_authkey')
def check_authkey(db):
    item = request.json;
    if not item:
        return "empty json"
    authentication = item['authkey']
    db.execute("SELECT * FROM users WHERE activesessionCoockie=?", (str(authentication),))
    user = db.fetchall()
    if user:
        return_string = {"valid": "yes"}
        return json.dumps(return_string)
    else:
        return_string = {"valid": "no"}
        return json.dumps(return_string)

@post('/check_login')
def check_login(db):
    item = request.json;
    db.execute("SELECT * FROM users WHERE username=? AND encpin=? AND gameid=?", (str(item['username']), str(item['PIN']), str(item['gameid'])))
    user = db.fetchall()
    if not user:
        return_string = {"valid": "no"}
        return json.dumps(return_string)
    else:
        return_string = {"valid": "yes", "authkey": user[0]['activesessionCoockie']}
        return json.dumps(return_string)

@post('/check_gameid')
def check_name(db):
    print(request.json)
    if request.json is not None:
        item = request.json
        db.execute("SELECT * FROM games WHERE gameid=?", (item['gameid'],))
        if not db.fetchall():
            return_string = {"exists": "no"}
            print(return_string)
            return json.dumps(return_string)
        return_string = {"exists": "yes"}
        print(return_string)
        return json.dumps(return_string)
    return "ERRORORORRrx"

@post('/check_username')
def check_name(db):
    print(request.json)
    if request.json is not None:
        item = request.json
        db.execute("SELECT * FROM games WHERE gameid=?", (item['gameid'],))
    else:
        return "empty"
    if not db.fetchall():
        return_string = {"gamenumber_exists": "no", "username_exists": "no"}
        return json.dumps(return_string)
    db.execute("SELECT * FROM users WHERE gameid=? AND username=?", (item['gameid'], item['username']))
    if not db.fetchall():
        return_string = {"gamenumber_exists": "yes", "username_exists": "no"}
        return json.dumps(return_string)
    return_string = {"gamenumber_exists": "yes", "username_exists": "yes"}
    return json.dumps(return_string)

@post('/login')
def login(db):
    if request.json is not None:
        item = request.json
        db.execute("SELECT * FROM games WHERE gameid=?", (item['gameid'],))
        if not db.fetchall():
            return "ERROR"
        db.execute("SELECT * FROM users WHERE gameid=? AND username=?", (item['gameid'], item['username']))
        if not db.fetchall():
            authentication = str(random.getrandbits(128))
            # response.set_cookie("account", authentication)
            db.execute("INSERT INTO users (gameid, username, encpin, correctanswers, wronganswers, activesessionCoockie, unreadannouncements) VALUES (?, ?, ?, ?, ?, ?, ?)", (item['gameid'], item['username'], item['pin'], str(0), str(0), str(authentication), str(0)))
            # db.execute("INSERT INTO activesessions (gameid, userid, activesessionCoockie, status, expires) VALUES (?, (SELECT  id FROM users WHERE gameid, username VALUES (?,?)), ?, ?, ?)", (item['gameid'], item['gameid'], item['username'], item['pin'], 'active', 'beta'))
            return_string = authentication
            return json.dumps(return_string)
        return "LOGIN FALSE"



@get('/log-in/gameid=<gameid>&username=<username>&pinhash=<pin>')
def login2(db, gameid, username, pin):
        db.execute("SELECT * FROM games WHERE gameid=?", (gameid,))
        if not db.fetchall():
            return False
        db.execute("SELECT * FROM users WHERE gameid=? AND username=?", (gameid, username))
        if not db.fetchall():
            authentication = str(random.getrandbits(128))
            response.set_cookie("account", authentication)
            db.execute("INSERT INTO users (gameid, username, encpin, correctanswers, wronganswers, activesessionCoockie) VALUES (?, ?, ?, ?, ?, ?)", (gameid, username, pin, str(0), str(0), str(authentication)))
            # db.execute("INSERT INTO activesessions (gameid, userid, activesessionCoockie, status, expires) VALUES (?, SELECT  id FROM users WHERE gameid, username VALUES (?,?), ?, ?, ?)", (gameid, gameid, username, pin, active, "beta"))
            return "LOGIN OKAY"
        return False

## admin logins

@post('/createnewadmin')
def newadmin(db):
    item = request.json
    # db.execute("SELECT * FROM admins WHERE name=?", (item['name'],))
    # if db.fetchall():
    #     return_string = {"username_exists": "yes", "email_exists": "unknown", "authkey":"unknown"}
    #     return json.dumps(return_string)
    db.execute("SELECT * FROM admins WHERE email=?", (item['email'],))
    if db.fetchall():
        return_string = {"username_exists": "no", "email_exists": "yes", "authkey":"unknown"}
        return json.dumps(return_string)
    authentication = str(random.getrandbits(128))
    db.execute("INSERT INTO admins (name, email, password, authkey) VALUES (?, ?, ?, ?)", (item['name'], item['email'], item['password'], str(authentication)))
    return_string = {"username_exists": "no", "email_exists": "no", "authkey": str(authentication)}
    return json.dumps(return_string)


@post('/check_authkeyadmin')
def check_authkeyadmin(db):
    item = request.json;
    if not item:
        return "empty json"
    authentication = item['authkey']
    db.execute("SELECT * FROM admins WHERE authkey=?", (str(authentication),))
    user = db.fetchall()
    if user:
        data = {}
        data['valid'] = "yes"
        data['user'] = user
        return json.dumps(data)
    else:
        return_string = {"valid": "no"}
        return json.dumps(return_string)


@post('/check_loginadmin')
def check_loginadmin(db):
    item = request.json;
    db.execute("SELECT * FROM admins WHERE email=? AND password=?", (str(item['email']), str(item['password']),))
    user = db.fetchall()
    if not user:
        return_string = {"valid": "no"}
        return json.dumps(return_string)
    else:
        return_string = {"valid": "yes", "authkey": user[0]['authkey']}
        return json.dumps(return_string)




## OLLDDDDDDD


@get('/phones')
def get_phones(db):
    db.execute("SELECT * FROM phones")
    all_phones = db.fetchall()
    response.content_type = 'application/json; charset=UTF-8'
    return json.dumps(all_phones)

@get('/phones/brand=<brand>')
def get_phones_brand(db, brand):
    db.execute("SELECT * FROM phones WHERE brand=?", (brand,))
    brand_phones = db.fetchall()
    response.content_type = 'application/json; charset=UTF-8'
    return json.dumps(brand_phones)

@get('/phones/screensize=<size>')
def db_retrieve(db, size):
    db.execute("SELECT * FROM phones WHERE screensize=?", (size,))
    screensize_phones = db.fetchone()
    response.content_type = 'application/json; charset=UTF-8'
    return json.dumps(screensize_phones)

@get('/phones/os=<os>')
def get_phones_brand(db, os):
    db.execute("SELECT * FROM phones WHERE os=?", (os,))
    os_phones = db.fetchall()
    response.content_type = 'application/json; charset=UTF-8'
    return json.dumps(os_phones)

@get('/phones/id=<phone_id>')
def get_phones_id(db, phone_id):
    db.execute("SELECT FROM phones WHERE id=?", (phone_id,))
    id_phone = db.fetchone()
    response.content_type = 'application/json; charset=UTF-8'
    return json.dumps(id_phone)


#DELETE

@delete('/phones/id=<phone_id>')
def delete_phone(db, phone_id):
    db.execute("DELETE FROM phones WHERE id=?", (phone_id,))
    response.status = 204

@delete('/phones')
def delete_phone_json(db):
    item = request.json
    db.execute("DELETE FROM phones WHERE id=?", str(item['id']))
    response.status = 204

@delete('/delete-all-phones')
def delete_all_phones(db):
    db.execute("DELETE FROM phones")
    response.status = 204


#POST

@post('/phones')
def add_new_phone(db):
    if request.json is not None:
        item = request.json
        db.execute(""" INSERT INTO phones (brand, model, os, image, screensize)
                VALUES (?, ?, ?, ?, ?)""",
                (item['brand'], item['model'], item['os'], item['image'],  item['screensize']))
    else:
        brand = request.forms.get('brand')
        model = request.forms.get('model')
        os = request.forms.get('os')
        screensize = request.forms.get('screensize')
        image = request.forms.get('image')
        db.execute("INSERT INTO phones (brand, model, os, screensize, image) VALUES (?, ?, ?, ?, ?)", (brand, model, os, screensize, image))

# PUT
@put('/phones')
def update_phone(db):
    item = request.json
    db.execute("""UPDATE phones SET brand=?, model=?, os=?, image=?, screensize=? WHERE id=?""",
            (item['brand'], item['model'], item['os'], item['image'],  item['screensize']))
    response.status = 204

@put('/phones/id=<id>&newbrand=<newbrand>')
def change_brand(db, id, newbrand):
    db.execute("UPDATE phones SET brand=? WHERE id=?", (newbrand, id,))
    response.status = 204

@put('/phones/id=<id>&newmodel=<newmodel>')
def change_brand(db, id, newmodel):
    db.execute("UPDATE phones SET model=? WHERE id=?", (newmodel, id,))
    response.status = 204

@put('/phones/id=<id>&newos=<newos>')
def change_brand(db, id, newos):
    db.execute("UPDATE phones SET os=? WHERE id=?", (newos, id,))
    response.status = 204

@put('/phones/id=<id>&newscreensize=<newscreensize:int>')
def change_brand(db, id, newscreensize):
    db.execute("UPDATE phones SET screensize=? WHERE id=?", (newscreensize, id,))
    response.status = 204

@put('/phones/id=<id>&newimage=<newimage>')
def change_brand(db, id, newimage):
    db.execute("UPDATE phones SET image=? WHERE id=?", (newimage, id,))
    response.status = 204

# ERRORS

# @error(404)
# def error404(error):
#     return "This page doesn't exist, check the API for the documentation :( \n Error code: 404"
#
# @error(405)
# def error405(error):
#     return "This method is not allowed. You are probaply using the wrong GET/PUT/DELETE/POST method, check the API documentation to check if your using it correctly :( \n Error code: 405"
#
# @error(500)
# def error500(error):
#     return "Something went wrong on our server, our apologies for your discomfort :( \n Error code: 500"


# MAIN LOOP

if __name__ == "__main__":
    from bottle import install, run
    from wtplugin import WtDbPlugin, WtCorsPlugin

    install(WtDbPlugin())
    install(WtCorsPlugin())
    run(host='0.0.0.0', port=8081, reloader=True, debug=True, autojson=False)