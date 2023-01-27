import os
import secrets
class assignment:
    def __init__(self, subprocess, code):
        self.subprocess = subprocess
        self.code = code

    def run_a21(self):
        # store the root directory and change to assignment directory
        rootdir = os.getcwd()
        os.chdir("website/static/java/Assignment2/A21")
        unique_id = secrets.token_hex()
        with open(f'Simulator_template.java', 'r') as f:
            A2template = f.read()
        
        with open('Simulator.java', 'w') as f:
            f.write(A2template.replace('//INSERTCODEHERE', self.code))

        # compile the program
        try:
            proc = self.subprocess.Popen("javac DFA.java", shell=True, stdout=self.subprocess.PIPE, stderr=self.subprocess.PIPE)
            stdout, stderr = proc.communicate()
            error = stderr.decode('utf-8')
            if not os.path.exists('DFA.class') or error != "":
                raise Exception()
        except:
            print(error)
            os.system('rm Simulator.java')
            return "DFA.java failed to compile contact server owner to check for logs"

        # run the program
        dfa_map = {}
        expected_dfa = {}
        for i in range(4):
            try:
                output = self.subprocess.check_output(['java', 'DFA', 'dfa{}.txt'.format(i), 'dfa{}.input.txt'.format(i), 'output.txt'], cwd='.', timeout=2).decode()
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
        
        out = "" 
        if len(dfa_map) == len(expected_dfa):
            for dfa in dfa_map.keys():
                out+= f'<li>Output of {dfa}:<br>'
                for i in range(len(dfa_map[dfa])):
                    out+=f'&nbsp case {i}: <br> &nbsp &nbsp &nbsp received: {dfa_map[dfa][i]}, <br> &nbsp &nbsp &nbsp expected: {expected_dfa[dfa][i]}<br>'
                out+= f'<br>'
        else:
            out+= f'<li> Error in parsing received outputs and expected outputs'

        os.system('rm *.class')
        os.system('rm Simulator.java')
        os.chdir(rootdir)
        return out

