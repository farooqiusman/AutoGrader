import os
class a3lex:
    def __init__(self, subprocess, lex_file):
        self.subprocess = subprocess
        self.lex_file = lex_file
    

    def generate_lex(self, assignment_dir, unique_dir):
        # store the root directory and change to assignment directory
        out = ""

        #################### Setup Assignment Directory ####################
        os.mkdir(unique_dir)

        os.system(f'cp {assignment_dir}/a3_template.lex {unique_dir}')

        with open(f'{unique_dir}/a3_template.lex', 'r') as f:
            A3template = f.read()
        

        with open(f'{unique_dir}/A3.lex', 'w') as f:
            f.write(A3template.replace('//INSERTCODEHERE', self.lex_file))

        #################### Run JLex ####################
        out = "Creating DFA from Lex file...<br>"
        command = f'java JLex.Main {unique_dir}/A3.lex'
        ret, perror = self.run_process(command, assignment_dir)
        if not ret:
            out += perror
            return False, out.replace("\n", "<br>")
        elif "Error" in perror:
            out += f"You have an error in your lex file please check the output below.<br><code>{perror}</code><br>"
            return False, out
        else:
            out += f'<code>{perror}</code>'
    
        print("JLex Ran fine")

        #################### Handle Test Passed ####################
        return True, out.replace('\n', '<br>')
