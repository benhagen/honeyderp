#!/usr/bin/env python

from flask import Flask, abort, request, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import settings
import boto.sqs
from boto.sqs.message import RawMessage
import json
from base64 import b64encode

app = Flask(__name__)
app.config.from_object(settings.Config)

sqs_conn = boto.sqs.connect_to_region("us-east-1", aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'], aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])
q = sqs_conn.get_queue(app.config['QUEUE'])


def encode(s):
	# For now, base64 encode everything; Ideally, I'd like to preserve ASCII if there are no non-ASCII chars
	return b64encode(s)


def log_request(request):
	log = {}
	log['method'] = request.method[:256]
	log['url'] = request.url[:256]
	log['ip'] = request.remote_addr
	ua = request.headers.get('User-Agent')
	if ua:
		ua = encode(ua[:256])
	log['ua'] = ua
	m = RawMessage()
	m.set_body(json.dumps(log, sort_keys=True))
	q.write(m)
	return


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
	try:
		log_request(request)
	except:
		pass
	abort(404)


if __name__ == '__main__':
	app.run(host="127.0.0.1", debug=True)
