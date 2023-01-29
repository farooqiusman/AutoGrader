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
        
        if "A2.input.tiny" in fileinput:
            with open(file, 'w') as f:
                f.write(fileinput.replace("A2.input.tiny", inputfile))
            return True

        return False

    def restore_input(self, file, inputfile):
        with open(file, 'r') as f:
            fileinput = f.read()

        if inputfile in fileinput:
            with open(file, 'w') as f:
                f.write(fileinput.replace(inputfile, "A2.input.tiny"))

    def nested_dict_maker(self):
        nested_dct = {} 
        with open("A2.output", 'r') as f:
            for line in f:
                key, val = line.strip().split(":")

                nested_dct[key.strip()] = val.strip()
        
        return nested_dct
    
    def check_runs(self, output_dict):
        count = 0
        output = ""
        with open('../answers.json', 'r') as json_file:
            data = json.load(json_file) 
            for test_case in data.keys():
                if test_case not in output_dict.keys():
                    return count, "Not all test cases ran, please contact server owner<br>"
                else:
                    for key in data[test_case].keys():
                        if key not in output_dict[test_case].keys():
                            return count, f"Key: {key} not in {output_dict[test_case].keys()}"
                        else:
                            if int(data[test_case][key]) != int(output_dict[test_case][key]):
                                output += ("Test Case: {0} Failed! <br>" 
                                "Expected output was: <br>&nbsp &nbsp &nbsp" 
                                "{1}<br> Actual output was: <br>" 
                                "&nbsp &nbsp &nbsp {2}".format(test_case, data[test_case], output_dict[test_case]))
                                return count, output
                count += 1
        return count, output
                                  
    def run_a22(self):
        # store the root directory and change to assignment directory
        rootdir = os.getcwd()
        os.chdir("website/static/java/Assignment2/A22")
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

        try:
            command = "java JLex.Main A2.lex"
            proc = self.subprocess.Popen(command, shell=True, stdout=self.subprocess.PIPE, stderr=self.subprocess.PIPE)
            stdout, stderr = proc.communicate()
            jLex_error = stderr.decode('utf-8')
            if jLex_error != "":
                raise Exception()
        except:
            self.remove_submission(unique_dir, rootdir)
            out += f"Error running command: <code>java JLex.Main A2.lex</code> <br><br>{jLex_error}"
            return out

        output = stdout.decode('utf-8')
        out += f'<code>{output}</code>'
        
        output_dict = {}
        for i in range(6):
            #Compiling A2.lex.java
            out += f"<br>Compiling A2.lex.java with input A2_{i}.tiny, command: <code>javac A2.lex.java </code><br>"

            #Pre compile check for inputfile:
            if not self.rename_input("A2.lex.java", f"../A2_{i}.tiny"):
                self.remove_submission(unique_dir, rootdir)
                out += "Error renaming file did you forget to name input file to \"A2.input.tiny\"?"
                return out
                
            try:
                command = "javac A2.lex.java" 
                proc = self.subprocess.Popen(command, shell=True, stdout=self.subprocess.PIPE, stderr=self.subprocess.PIPE)
                stdout, stderr = proc.communicate()
                compile_error = stderr.decode('utf-8')
                if compile_error != "":
                    raise Exception()
            except:
                self.remove_submission(unique_dir, rootdir)
                out += f"Error compiling A2.lex.java, command: <code>javac A2.lex.java</code> <br><br>{jLex_error}"
                return out

            out += "A2.lex.java compiled successfully <br>"
            self.restore_input("A2.lex.java", f"../A2_{i}.tiny")

            #Running A2
            try:
                command = "java A2"
                proc = self.subprocess.Popen(command, shell=True, stdout=self.subprocess.PIPE, stderr=self.subprocess.PIPE)
                stdout, stderr = proc.communicate()
                run_error = stderr.decode('utf-8')
                if run_error != "":
                    raise Exception()
            except:
                self.remove_submission(unique_dir, rootdir)
                out += f"Run time error, command: <code>java A2 </code> <br><br>{run_error}"
                return out
            
            #check output 
            output_dict[f"A2_{i}"] = self.nested_dict_maker()
            
        out += "<br> Running test Cases.... <br>"
        count, string_out = self.check_runs(output_dict)
        final_out = f"<br> {count}/6 Test cases ran successfully see below: <br>"
        if string_out != "":
            final_out += out + string_out
        else:
            final_out += out + "<br> All Tests passed!<br>"
        self.remove_submission(unique_dir, rootdir)
        return final_out.replace("\n", "<br>")

