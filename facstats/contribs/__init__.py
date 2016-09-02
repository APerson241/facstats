from collections import defaultdict
from flask import Blueprint, render_template, request, Markup
from wikitools import wiki
from wikitools import api

site = wiki.Wiki("https://en.wikipedia.org/w/api.php")

contribs = Blueprint('contribs', __name__, template_folder='templates')

@contribs.route('/')
def show():
    username = request.args.get('username', '')
    if username:
        result = get_user_fac_contribs(username)
        return render_template('results.html', username=username, content=Markup(result))
    else:
        return render_template('error.html')

def wikilink(page_name):
    return "<a href='https://en.wikipedia.org/wiki/{0}' title='{0} on English Wikipedia'>{0}</a>".format(page_name)

def get_user_fac_contribs(username):
    html_result = "<ul>"
    params = {"action": "query", "list": "usercontribs", "ucuser": username,
              "ucnamespace": "4", "ucprop": "title|timestamp", "uclimit": 50}
    request = api.APIRequest(site, params)

    all_contribs = {} # {title: timestamp}
    for each_result in request.queryGen():
        for each_edit in each_result["query"]["usercontribs"]:
            title, timestamp = each_edit["title"], each_edit["timestamp"]
            if "Featured article candidates/" in title and title not in all_contribs:
                all_contribs[title] = timestamp

    all_contribs = sorted(all_contribs.iteritems(),
                          key=lambda x:x[1],
                          reverse=True)

    if len(all_contribs):
        return "<ul>" + "\n".join("<li>{} (last edited {})</li>".format(wikilink(a), b.replace("T", " at ").replace("Z", "")) for a, b in all_contribs) + "</ul>"
    else:
        return "<i>No FAC contributions found.</i>"
