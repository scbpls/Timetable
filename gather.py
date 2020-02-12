#!/usr/bin/python3

import re
import requests
import bs4
import sys

def insert(dict, *args): #don't add if nil, tbi
	for key in args:
		if key == "":
			return

	for key in args[:-2]:
		if not dict.get(key, False):
			dict[key] = {}
		dict = dict[key]
	dict[args[-2]] = args[-1]

def gettext(results):
	text = ""
	for r in results:
		for s in r.stripped_strings:
			text += s
	return text

def gather(data, num):
	raw = requests.get("https://www.zsk.poznan.pl/plany2020/technikum/plany/o"+str(num)+".html").text

	doc = bs4.BeautifulSoup(raw, "html.parser")

	table = doc.select(".tabela")[0]
	for hour in table.select("tr"):
		hr = gettext(hour.select(".g")).replace(" ", "")
		for i, day in zip(range(5), hour.select("td.l")):
			for j in range(len(day.select(".n"))):
				teacher = gettext(day.select(".n")[j:j+1])
				subject = gettext(day.select(".p")[j:j+1])
				room    = gettext(day.select(".s")[j:j+1])
				insert(data, teacher, hr, i, subject+", s. "+room)

def tohtml(data):
	for teacher in data:
		print("<p>", teacher, "</p>", "<table>")
		teacher = data[teacher]

		print("<tr><td>")
		print(*["godzina", "poniedziałek", "wtorek", "środa", "czwartek", "piątek"], sep="</td><td>")
		print("</td></tr>")

		for hr in sorted(teacher.keys(), key = lambda x: int(x.split("-")[0].replace(":", ""))):
			print("<tr>", "<td>", hr, "</td>")
			hr = teacher[hr]
			for i in range(5):
				subject = hr.get(i, "")
				print("<td>", subject, "</td>")
			print("</tr>")
		print("</table>")

data = {}
for i in range(33):
	gather(data, i+1)
tohtml(data)
