#!/bin/bash

import os
from os import path, walk
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response
import openai
import bleach

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()
openai.api_key = dbkey


extra_dirs = ['templates/', ] #reload html templates when saved, while app is running
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/', methods=['POST', 'GET'])

def home():
    error = None
    return render_template("Question.html", error=error)


@app.route('/submit', methods=('GET', 'POST'))
def submission():
    error = None
    response=None

    def answer(myquestion):
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=myquestion,
        temperature=0.5,
        max_tokens=100,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )
        return (response["choices"][0]['text'])

    if request.method == 'POST':
        userquestion = bleach.clean(request.form.get('question'))
        response = answer(userquestion)
        return render_template("Question.html", error=error, response=response)

    return render_template("Question.html", error=error)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True #reload html templates when saved, while app is running
    app.run(host='0.0.0.0', debug=True)

    