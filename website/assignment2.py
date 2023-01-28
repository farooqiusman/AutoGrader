import os
import uuid
import shutil
class assignment:
    def __init__(self, subprocess, code):
        self.subprocess = subprocess
        self.code = code
    
    def remove_submission(self, unique_dir, rootdir): 
        os.chdir('../')
        os.system(f'rm -rf {unique_dir}')
        os.chdir(rootdir)


    def run_a21(self):
        # store the root directory and change to assignment directory
        rootdir = os.getcwd()
        os.chdir("website/static/java/Assignment2/A21")
        unique_id = uuid.uuid1()
        unique_dir = f'Simulator_{unique_id}'
        # make a unique directory
        os.mkdir(unique_dir)
        os.system(f'cp DFA.java {unique_dir}')
        os.system(f'cp Simulator_template.java {unique_dir}')

        with open(f'Simulator_template.java', 'r') as f:
            A2template = f.read()
        
        os.chdir(unique_dir)

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
            self.remove_submission(unique_dir, rootdir)
            return "DFA.java failed to compile contact server owner to check for logs"

        # run the program
        dfa_map = {}
        expected_dfa = {}
        error = ""
        for i in range(4):
            try:
                command = "java DFA ../dfa{0}.txt ../dfa{0}.input.txt output.txt".format(i)
                proc = self.subprocess.Popen(command, shell=True, stdout=self.subprocess.PIPE, stderr=self.subprocess.PIPE)
                stdout, stderr = proc.communicate()
                error = stderr.decode('utf-8')
                if error != "":
                    raise Exception()
            except:
                self.remove_submission(unique_dir, rootdir)
                return f"Your java program compiled, but either had a runtime error or ran for too long. 1 mark received.<br> The following is the error:<br><br>{error}"

            with open(f'output.txt', 'r') as f:
                outputs = f.read().split('\n')[:-1]

            dfa_map['dfa {}'.format(i)] = outputs

            with open('../answer_dfa{}.txt'.format(i), 'r') as f:
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
        self.remove_submission(unique_dir, rootdir)
        return out

