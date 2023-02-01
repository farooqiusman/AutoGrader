import os
import uuid
import shutil
import time
import json

class assignment22:
    def __init__(self, subprocess, code):
        self.subprocess = subprocess
        self.code = code
    
    def remove_submission(self, unique_dir): 
        command = f"rm -rf {unique_dir}/"
        self.subprocess.Popen(command, shell=True, stdout=self.subprocess.PIPE, stderr=self.subprocess.STDOUT)

         

    def rename_input(self, file, inputfile, directory):
        with open(f'{directory}/{file}', 'r') as f:
            fileinput = f.read()
        
        if "\"A2.input.tiny\"" in fileinput:
            with open(f'{directory}/{file}', 'w') as f:
                f.write(fileinput.replace("\"A2.input.tiny\"", inputfile))
            return True

        return False

    def nested_dict_maker(self, unique_dir):
        nested_dct = {} 
        with open(f"{unique_dir}/A2.output", 'r') as f:
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
                output += ("Expected output was: <br>&nbsp &nbsp &nbsp" 
                "{1}<br> Actual output was: <br>" 
                "&nbsp &nbsp &nbsp {2}.<br>".format(test_case, data, output_dict))
                return False, output
        return True, output

    def run_process(self, command, directory):
        print(command)
        proc = self.subprocess.Popen(command, shell=True, cwd=directory, stdout=self.subprocess.PIPE, stderr=self.subprocess.PIPE)
        error = ""
        out = ""
        try:
            stdout, stderr = proc.communicate(timeout=15)
            error = stderr.decode('utf-8')
            print(error)
            if error != "":
                raise Exception()
        except self.subprocess.TimeoutExpired:
            proc.kill()
            out += f"Error running: <code>{command}</code> took too long to run. <br>"
            self.remove_submission(directory)
            return False, out
        except:
            self.remove_submission(directory)
            formatted_error = error.replace("\n", "<br>")
            out += f"Error running command: <code>{command}</code> <br><br>{formatted_error}"
            return False, out
        out += stdout.decode('utf-8').replace("\n", "<br>")
        return True, out
    
    def run_a22(self):
        # store the root directory and change to assignment directory
        unique_id = uuid.uuid1()
        assignment_dir = f"website/static/java/Assignment2/A22"
        unique_dir = f'{assignment_dir}/assignment2_{unique_id}'
        out = ""

        #################### Setup Assignment Directory ####################
        os.mkdir(unique_dir)
        os.mkdir(f'{unique_dir}/JLex')

        os.system(f'cp {assignment_dir}/a2_template.lex {unique_dir}')
        os.system(f'cp {assignment_dir}/Main.java {unique_dir}/JLex/')

        with open(f'{unique_dir}/a2_template.lex', 'r') as f:
            A2template = f.read()
        

        with open(f'{unique_dir}/A2.lex', 'w') as f:
            f.write(A2template.replace('//INSERTCODEHERE', self.code))

        if os.path.getsize(f'{unique_dir}/A2.lex') == 1:
            out += "You did not submit anything.<br>"
            self.remove_submission(unique_dir)
            return out

        #################### Setup JLex Directory ####################
        error = ""
        try:
            command = "ls | wc -l"
            proc = self.subprocess.Popen("cd JLex && javac Main.java", shell=True, cwd=unique_dir)
            while proc.poll() is None: 
                time.sleep(1)
            size = self.subprocess.Popen(command, shell=True, cwd=f'{unique_dir}/JLex', stdout=self.subprocess.PIPE, stderr=self.subprocess.PIPE)
            stdout, stderr = size.communicate()
            error = stdout.decode('utf-8')
            if int(error) != 27:
                raise Exception()
        except:
            self.remove_submission(unique_dir)
            return f"JLex setup failed contact server owner to check for logs {error}"
        
        print("JLex Setup was a success")

        #################### Run JLex ####################
        out = "Creating DFA from Lex file...<br>"
        command = "java JLex.Main A2.lex"
        ret, perror = self.run_process(command, unique_dir)
        if not ret:
            out += perror
            self.remove_submission(unique_dir)
            return out.replace("\n", "<br>")
        elif "Error" in perror:
            out += f"You have an error in your lex file please check the output below.<br><code>{perror}</code><br>"
            self.remove_submission(unique_dir)
            return out
        else:
            out += f'<code>{perror}</code>'
    
        print("JLex Ran fine")

        #################### Compiling A2.lex.java ####################
        out += f"<br>Compiling A2.lex.java, command: <code>javac A2.lex.java </code><br>"

        #Pre compile check and replace input file 
        if not self.rename_input("A2.lex.java", f"argv[0]", unique_dir):
            self.remove_submission(unique_dir)
            out += "Error renaming file did you forget to name input file to \"A2.input.tiny\"?"
            return out
        
        print("renaming worked")
        command = "mv A2.lex.java A2.java && javac A2.java" 
        ret, perror = self.run_process(command, unique_dir)
        if not ret:
            out += perror
            self.remove_submission(unique_dir)
            return out.replace("\n", "<br>")
        else:
            out += "A2.lex.java compiled successfully <br>"

        #################### Run A2 ####################
        count = 0 
        for i in range(6):
            command = f"java A2 ../A2_{i}.tiny"
            ret, perror = self.run_process(command, unique_dir)
            
            if not ret:
                out += perror
                self.remove_submission(unique_dir)
                return out.replace("\n", "<br>")
            #check output 
            with open(f'{assignment_dir}/answers.json', 'r') as json_file:
                data = json.load(json_file) 
            out += f"<br> Running test Cases {i}.... <br>"
            ret, string_out = self.check_runs(self.nested_dict_maker(unique_dir), data[f"A2_{i}"], f"A2_{i}.tiny")
            if ret and string_out == "":
                string_out += "Test passed...<br>"
                out += string_out
                count +=1
            else:
                string_out += "Test failed...<br>"
                out += string_out

        #################### Handle Test Passed ####################
        final_out = f"<br> {count}/6 Test cases ran successfully see below: <br>"
        if count == 6:
            final_out += out + "<br> All Tests passed!<br>"
        else:
            final_out += out 
        self.remove_submission(unique_dir)
        return final_out.replace("\n", "<br>")

