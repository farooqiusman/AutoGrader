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

    # create the program
    rootdir = os.getcwd()
    os.chdir("website/static/java/Assignment2/A21")
    with open(f'Simulator_template.java', 'r') as f:
        A2template = f.read()
    
    with open('Simulator.java', 'w') as f:
        f.write(A2template.replace('//INSERTCODEHERE', code).replace(f'Simulator{id}_template', 'A1'))
    os.system('cat Simulator.java')
    # compile the program
    try:
        os.system('rm DFA.class')
        subprocess.run(['javac', 'DFA.java'])
        if not os.path.exists('DFA.class'):
            raise Exception()
    except:
        os.system('rm Simulator.java')
        return "Your java program would not compile. 0 marks received."

    # run the program
    dfa_map = {}
    expected_dfa = {}
    for i in range(4):
        try:
            output = subprocess.check_output(['java', 'DFA', 'dfa{}.txt'.format(i), 'dfa{}.input.txt'.format(i), 'output.txt'], cwd='.', timeout=2).decode()
        except:
            os.system('rm DFA.class')
            os.system('rm Simulator.java')
            os.system('rm output.txt')
            return "Your java program compiled, but either had a runtime error or ran for too long. 1 mark received."

        with open(f'output.txt', 'r') as f:
            outputs = f.read().split('\n')[:-1]

        dfa_map['dfa {}'.format(i)] = outputs

        with open('answer_dfa{}.txt'.format(i), 'r') as f:
            answers = f.read().split('\n')[:-1]
            
        expected_dfa['dfa {}'.format(i)] = answers
    
    os.system("rm Simulator.java")
    os.system("rm *.class")
   # program ran without error
    os.chdir("../")
    out = '<ul>'
    output = output.split('\n')
    if len(dfa_map) == len(expected_dfa):
        for dfa in dfa_map.keys():
            out+= f'<li>Output of {dfa}:<br>'
            for i in range(len(dfa_map[dfa])):
                out+=f'&nbsp case {i}: <br> &nbsp &nbsp &nbsp received: {dfa_map[dfa][i]}, <br> &nbsp &nbsp &nbsp expected: {expected_dfa[dfa][i]}<br>'
            out+= f'<br>'
        out+='</ul>'
    else:
        out+= f'<li> Error in parsing received outputs and expected outputs'
    os.chdir(rootdir)
    return out
