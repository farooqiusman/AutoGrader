from .assignment2 import assignment
from flask import render_template, url_for, flash, redirect, request
from website import app
import os
import subprocess
import secrets

@app.route('/home', methods=['GET'])
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/a1', methods=['GET'])
def a1():
    return render_template('a1.html')

@app.route('/a2', methods=['GET'])
def a2():
    return render_template('a2.html')

@app.route('/run/a1/<id>', methods=['POST'])
def runa1(id):

    code = request.get_json()['code']

    # create the program
    with open(f'website/static/java/A1{id}_template.java', 'r') as f:
        A1template = f.read()
    
    with open('website/static/java/A1.java', 'w') as f:
        f.write(A1template.replace('//IDENTIFIERCODEHERE', code).replace(f'A1{id}_template', 'A1'))

    # compile the program
    try:
        os.system('rm website/static/java/A1.class')
        subprocess.run(['javac', 'website/static/java/A1.java'])
        if not os.path.exists('website/static/java/A1.class'):
            raise Exception()
    except:
        os.system('rm website/static/java/A1.java')
        return "Your java program would not compile. 0 marks received."

    # run the program
    try:
        output = subprocess.check_output(['java', 'A1'], cwd='website/static/java', timeout=2).decode()
    except:
        os.system('rm website/static/java/A1.class')
        os.system('rm website/static/java/A1.java')
        return "Your java program compiled, but either had a runtime error or ran for too long. 1 mark received."

    os.system('rm website/static/java/A1.class')
    os.system('rm website/static/java/A1.java')

    # program ran without error
    counts = [5, 4, 6, 7, 8, 9]
    out = '<ul>'
    output = output.split('\n')
    for i in range(len(output)-1):
        out+=f'<li>case {i+1} | received: {int(output[i]):02} | expected: {counts[i]:02}</li>'
    out+='</ul>'
    return out


@app.route('/run/a2/<id>', methods=['POST'])
def runa21(id):
    code = request.get_json()['code']
    out = '<ul>'
    assignment2 = assignment(subprocess, code)
    out += assignment2.run_a21()
    out += '</ul>'
    return out
