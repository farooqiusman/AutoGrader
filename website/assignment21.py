import os
import uuid
import json
class assignment21:
    def __init__(self, subprocess, code):
        self.subprocess = subprocess
        self.code = code
    
    def remove_submission(self, unique_dir): 
        '''
            Will remove the entire unique submission directory if code crashes 
        '''
        command = f"rm -rf {unique_dir}/"
        self.subprocess.Popen(command, shell=True, stdout=self.subprocess.PIPE, stderr=self.subprocess.STDOUT)


    def nested_dict_maker(self, unique_dir):
        '''
            Will create a dictionary from the output file
        '''
        nested_dct = {} 
        with open(f"{unique_dir}/output.txt", 'r') as f:
            for line in f:
                key, val = line.strip().split(":")

                nested_dct[key.strip()] = val.strip()
        
        return nested_dct
    
    def check_runs(self, output_dict, data, test_case):
        '''
            Evaluate runs by checking values in both dictionaries and comparing them
        '''
        output = ""
        for key in data.keys():
            if key not in output_dict.keys():
                return False, f"Error: key: {key} not in {output_dict}, please rename.<br>"
            elif data[key] != output_dict[key]:
                output += ("Expected output was: <br>&nbsp &nbsp &nbsp" 
                "{1}<br> Actual output was: <br>" 
                "&nbsp &nbsp &nbsp {2} <br>".format(test_case, data, output_dict))
                return False, output
        return True, output

    def run_process(self, command, directory):
        '''
            will run a thread given the command and directory to run in
            handling all errors and exceptions correctly
        '''
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

    def run_a21(self):
        # store the root directory and change to assignment directory
        unique_id = uuid.uuid1()
        assignment_dir = f"website/static/java/Assignment2/A21"
        unique_dir = f'{assignment_dir}/assignment1_{unique_id}'
        out = ""

        #################### Setup Assignment Directory ####################
        os.mkdir(unique_dir)
        os.system(f'cp {assignment_dir}/DFA.java {unique_dir}')
        os.system(f'cp {assignment_dir}/Simulator_template.java {unique_dir}')

        with open(f'{unique_dir}/Simulator_template.java', 'r') as f:
            A2template = f.read()
        

        with open(f'{unique_dir}/Simulator.java', 'w') as f:
            f.write(A2template.replace('//INSERTCODEHERE', self.code))

        if os.path.getsize(f'{unique_dir}/Simulator.java') == 1:
            out += "You did not submit anything.<br>"
            self.remove_submission(unique_dir)
            return out

        #################### Compile DFA.java ####################
        command = "javac DFA.java"
        ret, perror = self.run_process(command, unique_dir)

        if not ret:
            out += perror
            self.remove_submission(unique_dir)
            return out.replace("\n", "<br>")
        else:
            out += "DFA.java compiled successfully.<br>"

        #################### Run DFA.java ####################
        count = 0
        for i in range(4):
            command = f"java DFA ../dfa{i}.txt ../dfa{i}.input.txt output.txt"
            ret, perror = self.run_process(command, unique_dir)

            if not ret:
                out += perror
                self.remove_submission(unique_dir)
                return out.replace("\n", "<br>")

            #check output 
            with open(f'{assignment_dir}/answers.json', 'r') as json_file:
                data = json.load(json_file) 
            
            out += f"<br> Running test Cases {i}.... <br>"
            ret, string_out = self.check_runs(self.nested_dict_maker(unique_dir), data[f"dfa_{i}"], f"A2_{i}.tiny")
            if ret and string_out == "":
                string_out += "Test passed...<br>"
                out += string_out
                count +=1
            else:
                string_out += "Test failed...<br>"
                out += string_out
        
        #################### Handle Test Passed ####################
        final_out = f"<br> {count}/4 Test cases ran successfully see below: <br>"
        if count == 4:
            final_out += out + "<br> All Tests passed!<br>"
        else:
            final_out += out 
        self.remove_submission(unique_dir)
        return final_out.replace("\n", "<br>")

