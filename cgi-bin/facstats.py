#!/usr/bin/env python

import cgitb; cgitb.enable()

import cgi
import sys

from wikitools import wiki
from wikitools import api

CONTRIBS_LIMIT = 10
CHECK_LIMIT = 500

site = wiki.Wiki("https://en.wikipedia.org/w/api.php")

def main():
    header()
    form = cgi.FieldStorage()
    username = form.getvalue("username")
    if not username:
        error_and_exit("Error! No username specified.")
    print("""
    <h1>FAC Stats for <a href="https://en.wikipedia.org/wiki/User:{0}">{0}</a></h1>
<p style="font-size: 80%"><a href="https://tools.wmflabs.org/apersonbot/">Tools</a> &gt; <b>FAC Stats</b></p>
    """.format(username))
    contribs = format_user_fac_contribs(username)
    print(contribs)
    footer()

def wikilink(page_name):
    return "<a href='https://en.wikipedia.org/wiki/{0}' title='{0} on English Wikipedia'>{0}</a>".format(page_name)

def yield_user_fac_contribs(username):
    params = {"action": "query", "list": "usercontribs", "ucuser": username,
              "ucnamespace": "4", "ucprop": "title|timestamp", "uclimit": CHECK_LIMIT}
    request = api.APIRequest(site, params)

    edit_count = 0
    for each_result in request.queryGen():
        for each_edit in each_result["query"]["usercontribs"]:
            title, timestamp = each_edit["title"], each_edit["timestamp"]
            edit_count += 1
            if edit_count > CHECK_LIMIT:
                raise StopIteration
            if "Featured article candidates/" in title:
                yield title, timestamp

def format_user_fac_contribs(username):
    html_result = "<ul>"
    all_contribs = {} # {title: timestamp}
    for title, timestamp in yield_user_fac_contribs(username):
        if title not in all_contribs:
            all_contribs[title] = timestamp
        if len(all_contribs) > CONTRIBS_LIMIT:
            break

    all_contribs = sorted(all_contribs.iteritems(),
                          key=lambda x:x[1],
                          reverse=True)

    if len(all_contribs):
        return "<ul>" + "\n".join("<li><a href='https://en.wikipedia.org/wiki/{0}' title='{0} on English Wikipedia'>{1}</a> (last edited {2})</li>".format(a, a.replace("Wikipedia:Featured article candidates/", ""), b.replace("T", " at ").replace("Z", "")) for a, b in all_contribs) + "</ul>"
    else:
        return "<i>No FAC contributions found.</i>"

def error_and_exit(error):
    print("<p class='error'>" + error + "</p>")
    footer()
    sys.exit(0)

def header():
    print("""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>FAC Stats - Results</title>
    <link href="../static/base.css" rel="stylesheet" />
  </head>
<body>
  <p><a href="../index.html">&larr; New search</a></p>
    """)

def footer():
    print("""
    <footer>
      <a href="https://en.wikipedia.org/wiki/User:Enterprisey" title="Enterprisey's user page on the English Wikipedia">Enterprisey</a> (<a href="https://en.wikipedia.org/wiki/User_talk:Enterprisey" title="Enterprisey's talk page on the English Wikipedia">talk!</a>) &middot; <a href="https://github.com/APerson241/facstats" title="Source code on GitHub">Source code</a> &middot; <a href="https://github.com/APerson241/facstats/issues" title="Issues on GitHub">Issues</a>
    </footer>
  </body>
</html>
    """)

main()
