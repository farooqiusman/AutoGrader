import os
import json
import time
from .helper import static_methods
from dotenv import load_dotenv

class assignment3:
    def __init__(self, subprocess, lex_code, cup_code, stduID, debug_code):
        self.subprocess = subprocess
        self.lex_code = lex_code
        self.cup_code = cup_code
        self.stduID = stduID
        self.sql_connection = None
        self.debug_code = debug_code
    
    def check_student_id(self):
        try:
            query = f'SELECT name, uwinID from students where user like "%{self.stduID}%";'
            c = self.sql_connection.cursor()
            c.execute(query)
            for x in c:
                result = x

            return result[0], result[1]
        except:
            return "", ""

    def generate_file_from_template(self, template_file, generated_file, code):
        out = ""
        try:
            with open(template_file, 'r') as f:
                A3template = f.read()
            
            with open(generated_file, 'w') as f:
                f.write(A3template.replace('//INSERTCODEHERE', code))
        except Exception as e:
            out += f'File error {e}<br>'
            return False, out
        
        return True, out

    def run_a3(self):
        load_dotenv() 
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASS")
        host = os.getenv("MYSQL_HOST")
        database = os.getenv("MYSQL_DB")
        out = ""
        
        if self.stduID == "":
            out += "Please enter a valid student number.<br>"
            return out

        self.sql_connection = static_methods.connect_to_sql(user, host, password, database)
        if self.sql_connection == None:
            out += "Error connecting to sql database please contact server owner"
            return out
        
        name, uwinid = self.check_student_id()
        
        if name == "" or uwinid == "":
            out += "Error grabbing name and student number, either does not exist or query failed.\n"
            out += "Contact server owner.\n"
            return out.replace("\n", "<br>")
        
        out += f'{name}, {uwinid}<br>'

        if self.lex_code == "": 
            out += "Please submit your lex file"

        ###########################  Prepare Lex file ###########################
        assignment_dir = f"website/static/java/Assignment3"
        user_dir = f'assignment3_{self.stduID}'
        unique_dir = f'{assignment_dir}/{user_dir}'
        
        if os.path.exists(unique_dir):
            static_methods.remove_submission(self.subprocess, unique_dir)
            print("Cleaning up working DIR")
            time.sleep(1)
            os.mkdir(unique_dir)
        else:
            os.mkdir(unique_dir)

        os.system(f'cp {assignment_dir}/a3_template.lex {unique_dir}')
        
        ret, perror = self.generate_file_from_template(f'{unique_dir}/a3_template.lex', f'{unique_dir}/A3.lex', self.lex_code)
        if not ret:
            out += perror
            static_methods.remove_submission(self.subprocess, unique_dir)
            return out.replace('\n', '<br>')

        print("Created A3.lex")

        ###########################  Run Lex file ###########################
        out += "Creating DFA from Lex file...<br>"
        command = f'java JLex.Main {user_dir}/A3.lex'
        out += "Running: <code>java JLex.Main A3.lex</code> <br>"
        ret, perror = static_methods.run_process(self.subprocess, command, assignment_dir)
        if not ret:
            out += perror
            static_methods.remove_submission(self.subprocess, unique_dir)
            return out.replace("\n", "<br>")
        elif "Error" in perror:
            out += f"You have an error in your lex file please check the output below.<br><code>{perror}</code><br>"
            static_methods.remove_submission(self.subprocess, unique_dir)
            return out
        else:
            out += f'<code>{perror}</code>'
    
        print("JLex Ran fine")

        ###########################  Install JavaCup for User ###########################
        os.system(f'cp {assignment_dir}/javaCup.tar {unique_dir}')
        command = 'tar -xvf javaCup.tar'
        ret, perror = static_methods.run_process(self.subprocess, command, unique_dir)
        if not ret:
            out += f"Error installing javaCup please contact server owner.<br>{perror}"
            static_methods.remove_submission(self.subprocess, unique_dir)
            return out.replace('\n', '<br>')
        print("Java cup installed fine")

        ###########################  Generate files using Cup file ###########################
        os.system(f'cp {assignment_dir}/a3_template.cup {unique_dir}')
        ret, perror = self.generate_file_from_template(f'{unique_dir}/a3_template.cup', f'{unique_dir}/A3.cup', self.cup_code)
        if not ret:
            out += perror
            static_methods.remove_submission(self.subprocess, unique_dir)
            return out.replace('\n', '<br>')

        out += "Generated A3.lex.java<br>"
        if self.cup_code == "":
            static_methods.remove_submission(self.subprocess, unique_dir)
            out += "You did not submit a cup file.\n"
            return out.replace('\n', '<br>')

        command = f'java java_cup.Main -parser A3Parser -symbols A3Symbol < A3.cup 2>&1'
        out += "Running: <code>java java_cup.Main -parser A3Parser -symbols A3Symbol < A3.cup</code> <br>"
        ret, perror = static_methods.run_cup(self.subprocess, command, unique_dir)
        if not ret:
            out += perror
            static_methods.remove_submission(self.subprocess, unique_dir)
            return out.replace('\n', '<br>')
        out += f'<code>{perror}</code>'
        out += "A3Parser, A3Symbol generated. <br>"
        print("Command ran fine")

        ########################### Compile lex, parser, symbol and user file ###########################
        os.system(f'cp {assignment_dir}/A3User.java {unique_dir}')
        command = 'javac A3.lex.java A3Parser.java A3Symbol.java A3User.java'
        out += f'Running: <code>{command}</code><br>'
        ret, perror = static_methods.run_process(self.subprocess, command, unique_dir)
        if not ret:
            out += perror
            static_methods.remove_submission(self.subprocess, unique_dir)
            return out.replace('\n', '<br>')
        out += "All files compiled successfully.<br>"
        print("Compiling files ran fine")
        print(self.debug_code)
        ########################### Run Code using A3User.java ###########################
        for i in range(10):
            out += f'Running <code>java A3User A3_{i+1}.tiny</code> <br>'
            command = f'java A3User ../A3_{i+1}.tiny'
            ret, perror = static_methods.run_code(
                    self.subprocess, command, unique_dir) if not self.debug_code else static_methods.debug_code(
                            self.subprocess, command, unique_dir)
            if not ret:
                out += perror
                # static_methods.remove_submission(self.subprocess, unique_dir)
            command = f'cat A3.output'
            ret, perror = static_methods.run_process(self.subprocess, command, unique_dir)
            out += perror
            out += "<br>"

        # self.remove_submission(unique_dir)
        return out.replace('\n', '<br>')

