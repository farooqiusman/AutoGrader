import os
import uuid
import json
from .assign3Files.assign3cup import a3cup
from .assign3Files.assign3lex import a3lex
from mysql.connector import connect, Error
from dotenv import load_dotenv

class assignment3:
    def __init__(self, subprocess, lex_code, cup_code, stduID):
        self.subprocess = subprocess
        self.lex_code = lex_code
        self.cup_code = cup_code
        self.stduID = stduID
        self.sql_connection = None
    
    def remove_submission(self, unique_dir): 
        command = f"rm -rf {unique_dir}/"
        self.subprocess.Popen(command, shell=True, stdout=self.subprocess.PIPE, stderr=self.subprocess.STDOUT)

    def connect_to_sql(self, user, host, password, database):
        cnx = None
        try:
            cnx = connect(
                host = host,
                user = user,
                password = password,
                database=database,
            )
            print("Database connection success")
        except Error as e:
            print(e)
        return cnx

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
            # self.remove_submission(directory)
            return out
        except:
            # self.remove_submission(directory)
            formatted_error = error.replace("\n", "<br>")
            out += f"Error running command: <code>{command}</code> <br><br>{formatted_error}"
            return out
        out += stdout.decode('utf-8').replace("\n", "<br>")
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

        self.sql_connection = self.connect_to_sql(user, host, password, database)
        if self.sql_connection == None:
            out += "Error connecting to sql database please contact server owner"
            return out
        
        name, uwinid = self.check_student_id()
        
        if name == "" or uwinid == "":
            out += "Error grabbing name and student number, either does not exist or query failed.\n"
            out += "Contact server owner.\n"
            return out.replace("\n", "<br>")
        
        out += f'{name}, {uwinid}\n'

        if self.lex_code == "": 
            out += "Please submit your lex file"

        ###########################  Prepare Lex file ###########################
        assignment_dir = f"website/static/java/Assignment3"
        unique_dir = f'{assignment_dir}/assignment3_{self.stduID}'

        os.mkdir(unique_dir)

        os.system(f'cp {assignment_dir}/a3_template.lex {unique_dir}')

        with open(f'{unique_dir}/a3_template.lex', 'r') as f:
            A3template = f.read()
        
        with open(f'{unique_dir}/A3.lex', 'w') as f:
            f.write(A3template.replace('//INSERTCODEHERE', self.lex_code))

        print("Created A3.lex")
        ###########################  Run Lex file ###########################
        out = "Creating DFA from Lex file...<br>"
        command = f'java JLex.Main assignment3_{self.stduID}/A3.lex'
        ret, perror = self.run_process(command, assignment_dir)
        if not ret:
            out += perror
            # self.remove_submission(unique_dir)
            return out.replace("\n", "<br>")
        elif "Error" in perror:
            out += f"You have an error in your lex file please check the output below.<br><code>{perror}</code><br>"
            # self.remove_submission(unique_dir)
            return out
        else:
            out += f'<code>{perror}</code>'
    
        print("JLex Ran fine")
        return out.replace('\n', '<br>')

