#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
os.environ['PYTHON_EGG_CACHE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "python-eggs")

from flask import Flask, send_from_directory, jsonify, render_template, request
import MySQLdb
import sys
import time

app = Flask(__name__)
MySQLConn = None

# Serve static files like js, img, css etc.
@app.route('/<folder>/<fileName>')
def serveStatic(folder, fileName):
    if folder in ('js', 'img', 'css', 'lib', 'fonts', 'views'):
        return send_from_directory(folder, fileName)
    
    return "404"

@app.route("/api/mosaic/")
def mosaic():
    l = []
    l.append({"event_id": 1, "event_category": "ART_EVENT", "event_name": "אומנות בכיכר1111", "event_description":"אומנות בכיכר הוא אירוע מיוחד במינו שקורה פעם בשנה בו עושים מלא מלא מלא אומנות בכיכר"})
    l.append({"event_id": 1, "event_category": "FOOD_TASTING", "event_name": "פסטיבל האוכל", "event_description":
              "מלא מלא אוכל בלה בלה בלה אוכל בלה אוכל."})    
    l.append({"event_id": 1, "event_category": "ART_EVENT", "event_name": "אומנות בכיכר", "event_description":"אומנות בכיכר הוא אירוע מיוחד במינו שקורה פעם בשנה בו עושים מלא מלא מלא אומנות בכיכר"})
    l.append({"event_id": 1, "event_category": "MOVIES_EVENT", "event_name": "ספרים רבותיי", "event_description":
              "מה עוד נאמר על עם הספר..."})
    l.append({"event_id": 1, "event_category": "FOOD_TASTING", "event_name": "פסטיבל האוכל", "event_description":
              "מלא מלא אוכל בלה בלה בלה אוכל בלה אוכל."})    
    l.append({"event_id": 1, "event_category": "NIGHTLIFE", "event_name": "אומנות בכיכר", "event_description":"אומנות בכיכר הוא אירוע מיוחד במינו שקורה פעם בשנה בו עושים מלא מלא מלא אומנות בכיכר"})
    l.append({"event_id": 1, "event_category": "BOOK_EVENT", "event_name": "ספרים רבותיי", "event_description":
              "מה עוד נאמר על עם הספר..."})
    l.append({"event_id": 1, "event_category": "SPORTS_EVENT", "event_name": "11פסטיבל האוכל", "event_description":
              "מלא מלא אוכל בלה בלה בלה אוכל בלה אוכל."})    
    
    return jsonify(l)

@app.route("/api/query/<query_name>/")
def query(query_name):
    if query_name in ("highest_attending", "hottest_city", "mosaic"):
        sql = open("queries/" + query_name + ".sql").read()
        cur = MySQLConn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(sql)
        return jsonify(cur.fetchall())
    
    return "404"

@app.route("/api/event/<id>/update/")
def eventUpdate(id):
    return "DONE"

@app.route("/api/event/<event_id>/")
def event(event_id):
    cur = MySQLConn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM Event WHERE id = %s", (event_id,))
    event = cur.fetchone()
    return jsonify(event) 

@app.route("/api/event/<event_id>/comments/")
def comments(event_id):
#    cur = MySQLConn.cursor(MySQLdb.cursors.DictCursor)
#    cur.execute("SELECT * FROM Comment WHERE event_id = %s ORDER BY updated_time DESC", (event_id,))
#    event = cur.fetchall()
#    return jsonify(event) 
    return ""

@app.route("/api/event/<event_id>/comments/add/", methods=['POST'])
def addComment(event_id):
    json_data = request.get_json(force=True) 
    newComment = json_data['newComment']
    
    cur = MySQLConn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO Comment (message, event_id) VALUES (%s, %s)", (newComment, event_id,))
    return "DONE"

@app.route("/api/city/")
def city():
    events = []
    events.append({"city_name": "Tel-Aviv", "event_id": 1, "event_category": "ART_EVENT", "event_name": "אומנות בכיכר1111", "event_description":"אומנות בכיכר הוא אירוע מיוחד במינו שקורה פעם בשנה בו עושים מלא מלא מלא אומנות בכיכר"})
    
    d = {"city_name": "Tel-Aviv", "events": events}
    
    return jsonify(d)

@app.route("/api/search/", methods=['POST'])
def search():
    json_data = request.get_json(force=True) 
    searchString = json_data['searchString']

    events = []
    events.append({"city_name": "Tel-Aviv", "event_id": 1, "event_category": "ART_EVENT", "event_name": "אומנות בכיכר1111", "event_description":"אומנות בכיכר הוא אירוע מיוחד במינו שקורה פעם בשנה בו עושים מלא מלא מלא אומנות בכיכר"})
    
    return jsonify(events)

@app.route("/<path>")
@app.route("/<path>/")
def index(path):
	return send_from_directory("", "index.html")

@app.route("/")
def index2():
	return send_from_directory("", "index.html")

if __name__ == "__main__":
    port = 40666
    
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
        if port > 65535 or port < 0:
            print("Error: port range is 0 to 65535.")
            exit()
    elif len(sys.argv) > 2:
        print("Usage: Server.py [port]")
        exit()
        
    while True:
        try:
            MySQLConn = MySQLdb.connect('mysqlsrv.cs.tau.ac.il', 'DbMysql08', 'DbMysql08', 'DbMysql08')
            MySQLConn.autocommit(True)

            app.run(host='0.0.0.0', port=port, threaded=True, debug=True)
        except MySQLdb.Error, e:
            print "MySQL Error %d: %s" % (e.args[0],e.args[1])
        except:
            print "Unexpected error:", sys.exc_info()[0]
            
        time.sleep(1)