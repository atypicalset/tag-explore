#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Import modules for CGI handling 
import cgi
import sqlite3
import json

# enable debugging
import cgitb
cgitb.enable()

db_file = "./taginfo.db"

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields, support keyword query and range query
# data format either "raw" or "percentile"
df = form.getvalue('dataformat')
qword = form.getvalue('q')
xfrom = float(form.getvalue('xfrom')) if form.getvalue('xfrom') else []
xto = float(form.getvalue('xto')) if form.getvalue('xto') else []
yfrom = float(form.getvalue('yfrom')) if form.getvalue('yfrom') else []
yto = float(form.getvalue('yto')) if form.getvalue('yto') else []
DEBUG_TEST = int(form.getvalue('debug')) if form.getvalue('debug') else []

print "Content-Type: text/plain;charset=utf-8"
print

#print "Hello World!"

if DEBUG_TEST and qword:
	print "query word= " + qword

if DEBUG_TEST and xfrom and xto:
	print "range: x [%0.3f, %0.3f] y[%0.3f, %0.3f]" % (xfrom, xto, yfrom, yto)


conn = sqlite3.connect(db_file)
cursor = conn.cursor()
failed = False
if not qword and not xfrom: # get all the data
	cursor.execute('SELECT tag, count, infm FROM tag_score')
elif qword:
	cursor.execute('SELECT tag, count, infm FROM tag_score WHERE tag=?', [qword] )
elif xfrom and xto and yfrom and yto:
	cursor.execute('SELECT tag, count, infm FROM tag_score WHERE count>=? AND count<=? AND infm>=? AND infm<=?', 
		(xfrom, xto, yfrom, yto))
else:
	failed = True

if not failed:
	result = map(lambda t: {'tag': t[0], 'count': t[1], 'infm': t[2]}, cursor)
	if DEBUG_TEST:
		print " %d data points found " % len(result)
	print json.dumps(result, sort_keys=True, indent=4)
else:
	print "DO NOT know how to get data, QUIT!"

conn.close()





