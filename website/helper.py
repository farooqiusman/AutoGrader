class static_methods:
        
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

