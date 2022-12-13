#!/bin/bash

import os
from os import path, walk
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response
import openai
import bleach
import math

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
        max_tokens=1000,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )
        return (response["choices"][0]['text'])

    if request.method == 'POST':
        userquestion = bleach.clean(request.form.get('question'))
        response = answer(userquestion)
        padding = (response.count('\n') )
        print(padding)
        if padding <= 20:
            padding=100
        elif padding <=25: 
            padding = (((math.ceil(padding / 2) * 2) / 2 )+98 ) # round up to nearest even number, then divide by two and add 100.  total = 100-115% padding
        elif padding <=30:
            padding = (((math.ceil(padding / 2) * 2) / 2 )+105 ) # round up to nearest even number, then divide by two and add 100.  total = 100-115% padding
        response = response.split('\n')
        return render_template("Question.html", error=error, response=response, padding=padding)

    return render_template("Question.html", error=error)

@app.route('/test', methods=['POST', 'GET'])

def testing():
    error = None
    return render_template("Test.html", error=error)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True #reload html templates when saved, while app is running
    app.run(host='127.0.0.1', debug=True)

    