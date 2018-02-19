from flask import Flask, render_template, url_for, redirect, request, Response, jsonify
import sqlite3
import time
import urllib2
import os

app = Flask(__name__) 

@app.route('/')
def index(): return render_template("index.html")

@app.route('/about')
def about(): return render_template("about.html")

@app.route('/documentation')
def documentation(): return render_template("documentation.html")

@app.route('/privacy')
def privacy(): return render_template("privacy.html")

@app.route('/terms')
def terms(): return render_template("terms.html")

@app.route('/advertise')
def ads(): return render_template("ads.html")

@app.route('/sponsor')
def sponsor(): return render_template("sponsor.html")

@app.route('/contact')
def contact(): return render_template("contact.html")

@app.route('/idfk')
def error(): return render_template("no-link.html")

@app.route('/add', methods=['GET', 'POST'])
def add():
	long_url = request.form["original_url"]
	short_url = request.form["short_url"]
	custom_url = request.form["customGnome"]
	conn = sqlite3.connect('test1.db')
	cur = conn.cursor()

	if len(custom_url) >= 1:
		cur.execute("SELECT * FROM guest_links WHERE customurl=?", (custom_url,))
		custom_rows = cur.fetchall()

		if not custom_rows:
			cur.execute("INSERT INTO guest_links (longurl, shorturl, custom, customurl, clicks, date_created, firefox_clicks, chrome_clicks, msie_clicks, opera_clicks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (long_url, short_url, 1, custom_url, 0, time.strftime('%x %X'), 0, 0, 0, 0))
			conn.commit()

	cur.execute("SELECT * FROM guest_links WHERE longurl=?", (long_url,))
	rows = cur.fetchall()

	if not rows:
		cur.execute("INSERT INTO guest_links (longurl, shorturl, custom, customurl, clicks, date_created, firefox_clicks, chrome_clicks, msie_clicks, opera_clicks, safari_clicks, iphone_clicks, android_clicks, windows_clicks, macos_clicks, otherbrowser_clicks, otherplatform_clicks, fb_clicks, twitter_clicks, google_clicks, othermedia_clicks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (long_url, short_url, 0, None, 0, time.strftime('%x %X'), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
		conn.commit()

	detail = {"long_url": long_url, "short_url": short_url, "custom_url": custom_url}
	return jsonify(detail)

def portal(gnome, destination, clicks, title, date, ff_clicks, chrome_clicks, ie_clicks, opera_clicks, safari_clicks, iphone_clicks, android_clicks, windows_clicks, macos_clicks, otherbrowser_clicks, otherplatform_clicks, fb_clicks, twitter_clicks, google_clicks, othermedia_clicks):
	return render_template('portal.html', gnome=gnome, destination=destination, clicks=clicks, title=title, date=date.split(' '), ff_clicks=ff_clicks, chrome_clicks=chrome_clicks, ie_clicks=ie_clicks, opera_clicks=opera_clicks, safari_clicks=safari_clicks, iphone_clicks=iphone_clicks, android_clicks=android_clicks, windows_clicks=windows_clicks, macos_clicks=macos_clicks, otherbrowser_clicks=otherbrowser_clicks, otherplatform_clicks=otherplatform_clicks)
	
@app.route('/<gnome>-', methods=['GET','POST'])
def analytics(gnome):
	conn = sqlite3.connect("test1.db")
	cur = conn.cursor()

	gnome = gnome

	cur.execute("SELECT * FROM guest_links WHERE customurl=?", (gnome,))
	custom_rows = cur.fetchall()

	cur.execute("SELECT * FROM guest_links WHERE shorturl=?", (gnome,))
	rows = cur.fetchall()
	print rows
	if rows:
		for row in rows:
			if row[2] == gnome:
				cur.execute("SELECT `clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				clicks = cur.fetchone()[0]

				cur.execute("SELECT `firefox_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				firefox_clicks = cur.fetchone()[0]

				cur.execute("SELECT `chrome_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				chrome_clicks = cur.fetchone()[0]

				cur.execute("SELECT `msie_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				msie_clicks = cur.fetchone()[0]

				cur.execute("SELECT `opera_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				opera_clicks = cur.fetchone()[0]

				cur.execute("SELECT `safari_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				safari_clicks = cur.fetchone()[0]

				cur.execute("SELECT `iphone_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				iphone_clicks = cur.fetchone()[0]

				cur.execute("SELECT `android_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				android_clicks = cur.fetchone()[0]

				cur.execute("SELECT `windows_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				windows_clicks = cur.fetchone()[0]

				cur.execute("SELECT `macos_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				macos_clicks = cur.fetchone()[0]

				cur.execute("SELECT `otherbrowser_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				otherbrowser_clicks = cur.fetchone()[0]

				cur.execute("SELECT `otherplatform_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				otherplatform_clicks = cur.fetchone()[0]

				cur.execute("SELECT `fb_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				fb_clicks = cur.fetchone()[0]

				cur.execute("SELECT `twitter_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				twitter_clicks = cur.fetchone()[0]

				cur.execute("SELECT `google_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				google_clicks = cur.fetchone()[0]

				cur.execute("SELECT `othermedia_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				othermedia_clicks = cur.fetchone()[0]

	return render_template('analytics.html', gnome=gnome, destination=row[1], clicks=clicks, ff_clicks=firefox_clicks, chrome_clicks=chrome_clicks, ie_clicks=msie_clicks, opera_clicks=opera_clicks, safari_clicks=safari_clicks, iphone_clicks=iphone_clicks, android_clicks=android_clicks, windows_clicks=windows_clicks, macos_clicks=macos_clicks, otherbrowser_clicks=otherbrowser_clicks, otherplatform_clicks=otherplatform_clicks, fb_clicks=fb_clicks, twitter_clicks=twitter_clicks, google_clicks=google_clicks, othermedia_clicks=othermedia_clicks)


@app.route("/<gnome>", methods=['GET', 'POST'])
def urlexchange(gnome):
	referer = request.headers.get("Referer")
	gnome = gnome
	
	userBrowser = request.user_agent.browser
	userPlatform = request.user_agent.platform

	conn = sqlite3.connect("test1.db")
	cur = conn.cursor()

	cur.execute("SELECT * FROM guest_links WHERE customurl=?", (gnome,))
	custom_rows = cur.fetchall()

	cur.execute("SELECT * FROM guest_links WHERE shorturl=?", (gnome,))
	rows = cur.fetchall()
	print rows
	if rows:
		for row in rows:
			if row[2] == gnome:
				cur.execute("SELECT `clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				clicks = cur.fetchone()
				clicks = clicks[0] + 1
				cur.execute("UPDATE guest_links SET clicks = ? WHERE shorturl is ?", (clicks, gnome))
				conn.commit()

				cur.execute("SELECT `firefox_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				firefox_clicks = cur.fetchone()[0]

				cur.execute("SELECT `chrome_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				chrome_clicks = cur.fetchone()[0]

				cur.execute("SELECT `msie_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				msie_clicks = cur.fetchone()[0]

				cur.execute("SELECT `opera_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				opera_clicks = cur.fetchone()[0]

				cur.execute("SELECT `safari_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				safari_clicks = cur.fetchone()[0]

				cur.execute("SELECT `iphone_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				iphone_clicks = cur.fetchone()[0]

				cur.execute("SELECT `android_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				android_clicks = cur.fetchone()[0]

				cur.execute("SELECT `windows_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				windows_clicks = cur.fetchone()[0]

				cur.execute("SELECT `macos_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				macos_clicks = cur.fetchone()[0]

				cur.execute("SELECT `otherbrowser_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				otherbrowser_clicks = cur.fetchone()[0]

				cur.execute("SELECT `otherplatform_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				otherplatform_clicks = cur.fetchone()[0]

				cur.execute("SELECT `fb_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				fb_clicks = cur.fetchone()[0]

				cur.execute("SELECT `twitter_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				twitter_clicks = cur.fetchone()[0]

				cur.execute("SELECT `google_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				google_clicks = cur.fetchone()[0]

				cur.execute("SELECT `othermedia_clicks` FROM guest_links WHERE shorturl is ?", (gnome,))
				othermedia_clicks = cur.fetchone()[0]

				if userBrowser == "firefox":
					firefox_clicks = firefox_clicks + 1
					cur.execute("UPDATE guest_links SET firefox_clicks = ? WHERE shorturl is ?", (firefox_clicks, gnome))
					conn.commit()
				elif userBrowser == "chrome":
					chrome_clicks = chrome_clicks + 1
					cur.execute("UPDATE guest_links SET chrome_clicks = ? WHERE shorturl is ?", (chrome_clicks, gnome))
					conn.commit()
				elif userBrowser == "msie":
					msie_clicks = msie_clicks + 1
					cur.execute("UPDATE guest_links SET msie_clicks = ? WHERE shorturl is ?", (msie_clicks, gnome))
					conn.commit()
				elif userBrowser == "opera":
					opera_clicks = opera_clicks + 1
					cur.execute("UPDATE guest_links SET opera_clicks = ? WHERE shorturl is ?", (opera_clicks, gnome))
					conn.commit()
				elif userBrowser == "safari":
					safari_clicks = safari_clicks + 1
					cur.execute("UPDATE guest_links SET safari_clicks = ? WHERE shorturl is ?", (safari_clicks, gnome))
					conn.commit()
				else:
					otherbrowser_clicks = otherbrowser_clicks + 1
					cur.execute("UPDATE guest_links SET otherbrowser_clicks = ? WHERE shorturl is ?", (otherbrowser_clicks, gnome))
					conn.commit()


				if userPlatform == "iphone":
					iphone_clicks = iphone_clicks + 1
					cur.execute("UPDATE guest_links SET iphone_clicks = ? WHERE shorturl is ?", (iphone_clicks, gnome))
					conn.commit()
				elif userPlatform == "android":
					android_clicks = android_clicks + 1
					cur.execute("UPDATE guest_links SET android_clicks = ? WHERE shorturl is ?", (android_clicks, gnome))
					conn.commit()
				elif userPlatform == "windows":
					windows_clicks = windows_clicks + 1
					cur.execute("UPDATE guest_links SET windows_clicks = ? WHERE shorturl is ?", (windows_clicks, gnome))
					conn.commit()
				elif userPlatform == "macos":
					macos_clicks = macos_clicks + 1
					cur.execute("UPDATE guest_links SET macos_clicks = ? WHERE shorturl is ?", (macos_clicks, gnome))
					conn.commit()
				else:
					otherplatform_clicks = otherplatform_clicks + 1
					cur.execute("UPDATE guest_links SET otherplatform_clicks = ? WHERE shorturl is ?", (otherplatform_clicks, gnome))
					conn.commit()

				print referer
				if referer == None: referer = "noooope"
				if 'facebook' in referer:
					fb_clicks = fb_clicks + 1
					cur.execute("UPDATE guest_links SET fb_clicks = ? WHERE shorturl is ?", (fb_clicks, gnome))
					conn.commit()
				elif 't.co' in referer:
					twitter_clicks = twitter_clicks + 1
					cur.execute("UPDATE guest_links SET twitter_clicks = ? WHERE shorturl is ?", (twitter_clicks, gnome))
					conn.commit()
				elif 'plus.url' in referer:
					google_clicks = google_clicks + 1
					cur.execute("UPDATE guest_links SET google_clicks = ? WHERE shorturl is ?", (google_clicks, gnome))
					conn.commit()
				else:
					othermedia_clicks = othermedia_clicks + 1
					cur.execute("UPDATE guest_links SET othermedia_clicks = ? WHERE shorturl is ?", (othermedia_clicks, gnome))
					conn.commit()

				try:
					soup = BeautifulSoup(urllib2.urlopen("http://" + row[1]))
				except:
					soup = "Their title is missing..."
				try:
					title = soup.title.string
				except AttributeError:
					title = "Their title is missing...."
				cur.execute("SELECT `date_created` FROM guest_links WHERE shorturl is ?", (gnome,))
				date = cur.fetchone()[0]
				return redirect("http://" + row[1]) #portal(gnome, row[1], clicks, title, date, firefox_clicks, chrome_clicks, msie_clicks, opera_clicks, safari_clicks, iphone_clicks, android_clicks, windows_clicks, macos_clicks, otherbrowser_clicks, otherplatform_clicks, fb_clicks, twitter_clicks, google_clicks, othermedia_clicks)
	elif custom_rows:
		for row in custom_rows:
			if row[4] == gnome:
				return redirect("http://gnfy.co/" + row[2])
	else:
		return redirect("http://gnomify.net/idfk")


if __name__ == '__main__':
	conn = sqlite3.connect("test1.db")
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS guest_links (
			`id` INTEGER PRIMARY KEY,
			`longurl` TEXT, 
			`shorturl` TEXT,
			`custom` INT,
			`customurl` TEXT,
			`clicks` INTEGER,
			`date_created` TEXT,
			`firefox_clicks` INTEGER,
			`chrome_clicks` INTEGER,
			`msie_clicks` INTEGER,
			`opera_clicks` INTEGER,
			`safari_clicks` INTEGER,
			`iphone_clicks` INTEGER,
			`android_clicks` INTEGER,
			`windows_clicks` INTEGER,
			`macos_clicks` INTEGER,
			`otherbrowser_clicks` INTEGER,
			`otherplatform_clicks` INTEGER,
			`fb_clicks` INTEGER,
			`twitter_clicks` INTEGER,
			`google_clicks` INTEGER,
			`othermedia_clicks` INTEGER
		);
	""")
	app.run(port=8080, debug=True)
