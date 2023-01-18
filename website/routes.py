from flask import render_template, url_for, flash, redirect, request
from website import app
import os
import subprocess

@app.route('/home', methods=['GET'])
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/a1', methods=['GET'])
def a1():
    return render_template('a1.html')

@app.route('/run/a11', methods=['POST'])
def a11():

    code = request.get_json()['code']

    # create the program
    with open('website/static/java/A11_template.java', 'r') as f:
        A11template = f.read()
    
    with open('website/static/java/A11.java', 'w') as f:
        f.write(A11template.replace('//IDENTIFIERCODEHERE', code).replace('A11_template', 'A11'))

    # compile the program
    try:
        os.system('rm website/static/java/A11.class')
        subprocess.run(['javac', 'website/static/java/A11.java'])
        if not os.path.exists('website/static/java/A11.class'):
            raise Exception()
    except:
        os.system('rm website/static/java/A11.java')
        return "Your java program would not compile. 0 marks received."

    # run the program
    try:
        output = subprocess.check_output(['java', 'A11'], cwd='website/static/java', timeout=2).decode()
    except:
        os.system('rm website/static/java/A11.class')
        os.system('rm website/static/java/A11.java')
        return "Your java program compiled, but had a runtime error. 1 mark received."

    os.system('rm website/static/java/A11.class')
    os.system('rm website/static/java/A11.java')

    # program ran without error
    counts = [5, 4, 6, 7, 8, 9]
    out = '<ul>'
    output = output.split('\n')
    for i in range(len(output)-1):
        out+=f'<li>case {i+1} | received: {int(output[i]):02} | expected: {counts[i]:02}</li>'
    out+='</ul>'
    return out

@app.route('/run/a12', methods=['POST'])
def a12():

    code = request.get_json()['code']

    # create the program
    with open('website/static/java/A12_template.java', 'r') as f:
        A12template = f.read()
    
    with open('website/static/java/A12.java', 'w') as f:
        f.write(A12template.replace('//IDENTIFIERCODEHERE', code).replace('A12_template', 'A12'))

    # compile the program
    try:
        os.system('rm website/static/java/A12.class')
        subprocess.run(['javac', 'website/static/java/A12.java'])
        if not os.path.exists('website/static/java/A12.class'):
            raise Exception()
    except:
        os.system('rm website/static/java/A12.java')
        return "Your java program would not compile. 0 marks received."

    # run the program
    try:
        output = subprocess.check_output(['java', 'A12'], cwd='website/static/java', timeout=2).decode()
    except:
        os.system('rm website/static/java/A12.class')
        os.system('rm website/static/java/A12.java')
        return "Your java program compiled, but had a runtime error. 1 mark received."

    os.system('rm website/static/java/A12.class')
    os.system('rm website/static/java/A12.java')

    # program ran without error
    counts = [5, 4, 6, 7, 8, 9]
    out = '<ul>'
    output = output.split('\n')
    for i in range(len(output)-1):
        out+=f'<li>case {i+1} | received: {int(output[i]):02} | expected: {counts[i]:02}</li>'
    out+='</ul>'
    return out
