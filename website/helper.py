from mysql.connector import connect, Error
class static_methods:
    
    @staticmethod
    def remove_submission(subprocess, unique_dir): 
        command = f"rm -rf {unique_dir}/"
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    @staticmethod
    def connect_to_sql(user, host, password, database):
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

    @staticmethod
    def run_process(subprocess, command, directory):
        print(command)
        proc = subprocess.Popen(command, shell=True, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        error = ""
        out = ""
        try:
            stdout, stderr = proc.communicate(timeout=15)
            error = stderr.decode('utf-8')
            print(error)
            if error != "":
                raise Exception()
        except subprocess.TimeoutExpired:
            proc.kill()
            out += f"Error running: <code>{command}</code> took too long to run. <br>"
            return False, out
        except:
            formatted_error = error.replace("\n", "<br>")
            out += f"Error running command: <code>{command}</code><br>{formatted_error}"
            return False, out
        out += stdout.decode('utf-8').replace("\n", "<br>")
        return True, out
    
    @staticmethod
    def run_cup(subprocess, command, directory):
        print(command)
        proc = subprocess.Popen(command, shell=True, cwd=directory, stdout=subprocess.PIPE)
        out = ""
        std = ""
        try:
            stdout = proc.communicate(timeout=15)[0]
            std = stdout.decode('utf-8')
            print(std)
            if "0 errors" not in std:
                raise Exception()
        except subprocess.TimeoutExpired:
            proc.kill()
            out += f"Error running: <code>{command}</code> took too long to run. <br>"
            return False, out
        except:
            out += f"Error running command: <code>{command}</code><br><code>{std}</code>"
            return False, out.replace('\n', '<br>')
        out += std
        return True, out.replace('\n', '<br>')

    @staticmethod
    def run_code(subprocess, command, directory):
        print(command)
        proc = subprocess.Popen(command, shell=True, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = ""
        error = ""
        try:
            stdout, stderr = proc.communicate(timeout=15)
            error = stderr.decode('utf-8')
            print(error)
            if "Syntax error" in error:
                raise Exception()
        except subprocess.TimeoutExpired:
            proc.kill()
            out += f"Error running: <code>{command}</code> took too long to run. <br>"
            return False, out
        except:
            out += f"<code>{error}</code><br>"
            return True, out.replace('\n', '<br>')
        out += stdout.decode('utf-8')
        return True, out.replace('\n', '<br>')
    
    @staticmethod
    def debug_code(subprocess, command, directory):
        print(command)
        proc = subprocess.Popen(command, shell=True, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = ""
        error = ""
        try:
            stdout, stderr = proc.communicate(timeout=15)
            error = stderr.decode('utf-8')
            if "Syntax error" in error:
                raise Exception()
        except subprocess.TimeoutExpired:
            proc.kill()
            out += f"Error running: <code>{command}</code> took too long to run. <br>"
            return False, out
        except:
            count = 0
            out += "Error in parsing printing last 20 tokens<br>"
            splitted = error.split('\n')
            for line in splitted:
                if "Current token" in line:
                    out += f'<code>{line}</code><br>'
                    count += 1
                if count == 20:
                    break
            index = splitted.index('Syntax error')
            for i in range(index, len(splitted)):
                out += f'<code>{splitted[i]}</code><br>'
            return True, out.replace('\n', '<br>')
        out += stdout.decode('utf-8')
        return True, out.replace('\n', '<br>')

    @staticmethod
    def find_and_replace(text_to_find, text_to_replace, file_name):
        out = ""
        try:
            with open(file_name, 'r') as f:
                A3template = f.read()
            
            with open(file_name, 'w') as f:
                f.write(A3template.replace(text_to_find, text_to_replace))
        except Exception as e:
            out += f'File error {e}<br>'
            return False, out
        
        return True, out

    @staticmethod
    def nested_dict_maker(unique_dir):
        nested_dct = {}
        try:
            with open(f"{unique_dir}/A3.output", 'r') as f:
                for line in f:
                    key, val = line.strip().split(":")

                    nested_dct[key.strip()] = val.strip()
        except IOError as e:
            return False, e
        
        return True, nested_dct

    @staticmethod 
    def check_runs(output_dict, data, test_case):
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
