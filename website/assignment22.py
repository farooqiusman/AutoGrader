import os
import uuid
import shutil
import time
import json

class assignment22:
    def __init__(self, subprocess, code):
        self.subprocess = subprocess
        self.code = code
    
    def remove_submission(self, unique_dir, rootdir): 
        os.chdir('../')
        os.system(f'rm -rf {unique_dir}')
        os.chdir(rootdir)

    def rename_input(self, file, inputfile):
        with open(file, 'r') as f:
            fileinput = f.read()
        
        if "\"A2.input.tiny\"" in fileinput:
            with open(file, 'w') as f:
                f.write(fileinput.replace("\"A2.input.tiny\"", inputfile))
            return True

        return False

    def nested_dict_maker(self):
        nested_dct = {} 
        with open("A2.output", 'r') as f:
            for line in f:
                key, val = line.strip().split(":")

                nested_dct[key.strip()] = val.strip()
        
        return nested_dct
    
    def check_runs(self, output_dict, data, test_case):
        output = ""
        for key in data.keys():
            if key not in output_dict.keys():
                return False, f"Error: key: {key} not in {output_dict}, please rename.<br>"
            elif int(data[key]) != int(output_dict[key]):
                output += ("Test Case: {0} Failed! <br>" 
                "Expected output was: <br>&nbsp &nbsp &nbsp" 
                "{1}<br> Actual output was: <br>" 
                "&nbsp &nbsp &nbsp {2}".format(test_case, data, output_dict))
                return False, output
        return True, output
                                  
    def run_a22(self):
        # store the root directory and change to assignment directory
        rootdir = os.getcwd()
        assignment_dir = "website/static/java/Assignment2/A22"
        if os.getcwd() != assignment_dir:
            os.chdir(os.path.abspath(assignment_dir))

        unique_id = uuid.uuid1()
        unique_dir = f'assignment2_{unique_id}'
        out = ""
        # make a unique directory
        os.mkdir(unique_dir)
        os.mkdir(f'{unique_dir}/JLex')

        os.system(f'cp a2_template.lex {unique_dir}')
        os.system(f'cp Main.java {unique_dir}/JLex/')

        with open('a2_template.lex', 'r') as f:
            A2template = f.read()
        
        os.chdir(unique_dir)
        
        with open('A2.lex', 'w') as f:
            f.write(A2template.replace('//INSERTCODEHERE', self.code))

        # setup JLex environment
        try:
            os.chdir('JLex')
            command = "ls | wc -l"
            proc = self.subprocess.Popen("javac Main.java", shell=True)
            while proc.poll() is None: 
                time.sleep(1)
            size = self.subprocess.Popen(command, shell=True, stdout=self.subprocess.PIPE, stderr=self.subprocess.PIPE)
            stdout, stderr = size.communicate()
            error = stdout.decode('utf-8')
            if int(error) != 27:
                raise Exception()
        except:
            print(error)
            self.remove_submission(unique_dir, rootdir)
            return f"JLex setup failed contact server owner to check for logs {error}"
        
        print("JLex Setup was a success")
        os.chdir("../")

        #Run JLex
        out = "Creating DFA from Lex file...<br>"

        command = "java JLex.Main A2.lex"
        proc = self.subprocess.Popen(command, shell=True, stdout=self.subprocess.PIPE, stderr=self.subprocess.PIPE)
        try:
            stdout, stderr = proc.communicate(timeout=15)
            jLex_error = stderr.decode('utf-8')
            if jLex_error != "":
                raise Exception()
        except self.subprocess.TimeoutExpired:
            proc.kill()
            out += "Error: java JLex.Main A2.lex took too long to run. <br>"
            self.remove_submission(unique_dir, rootdir)
            return out
        except:
            self.remove_submission(unique_dir, rootdir)
            out += f"Error running command: <code>java JLex.Main A2.lex</code> <br><br>{jLex_error}"
            return out

        output = stdout.decode('utf-8')
        out += f'<code>{output}</code>'
        
        output_dict = {}

        #Compiling A2.lex.java
        out += f"<br>Compiling A2.lex.java, command: <code>javac A2.lex.java </code><br>"

        #Pre compile check and replace input file 
        if not self.rename_input("A2.lex.java", f"argv[0]"):
            self.remove_submission(unique_dir, rootdir)
            out += "Error renaming file did you forget to name input file to \"A2.input.tiny\"?"
            return out
            
        command = "javac A2.lex.java" 
        proc = self.subprocess.Popen(command, shell=True, stdout=self.subprocess.PIPE, stderr=self.subprocess.PIPE)
        try:
            stdout, stderr = proc.communicate(timeout=15)
            compile_error = stderr.decode('utf-8')
            if compile_error != "":
                raise Exception()
        except self.subprocess.TimeoutExpired:
            proc.kill()
            out += "Error: javac A2.lex.java took too long to compile. <br>"
            self.remove_submission(unique_dir, rootdir)
            return out
        except:
            self.remove_submission(unique_dir, rootdir)
            out += f"Error compiling A2.lex.java, command: <code>javac A2.lex.java</code> <br><br>{compile_error}"
            return out

        out += "A2.lex.java compiled successfully <br>"

        #Running A2
        count = 0 
        for i in range(6):
            command = f"java A2 ../A2_{i}.tiny"
            proc = self.subprocess.Popen(command, shell=True, stdout=self.subprocess.PIPE, stderr=self.subprocess.PIPE)
            try:
                stdout, stderr = proc.communicate(timeout=15)
                run_error = stderr.decode('utf-8')
                if run_error != "":
                    raise Exception()
            except self.subprocess.TimeoutExpired:
                proc.kill()
                out += "Error: Your code timed out. <br>"
                self.remove_submission(unique_dir, rootdir)
                return out
            except:
                self.remove_submission(unique_dir, rootdir)
                out += f"Run time error, command: <code>java A2 ../A2_{i}.tiny</code> <br><br>{run_error}"
                return out

            
            #check output 
            with open('../answers.json', 'r') as json_file:
                data = json.load(json_file) 
            out += f"<br> Running test Cases {i}.... <br>"
            ret, string_out = self.check_runs(self.nested_dict_maker(), data[f"A2_{i}"], f"A2_{i}.tiny")
            if ret and string_out == "":
                string_out += "Test passed...<br>"
                out += string_out
                count +=1
            else:
                string_out += "Test failed...<br>"
                out += string_out

        final_out = f"<br> {count}/6 Test cases ran successfully see below: <br>"
        if count == 6:
            final_out += out + "<br> All Tests passed!<br>"
        else:
            final_out += out 
        self.remove_submission(unique_dir, rootdir)
        return final_out.replace("\n", "<br>")

