import subprocess, sys, shutil, os, glob

def prin_lst(lst, curr):
    '''
    prints in console the tree that was formed by
    << build_dict_list >> includes pointing to the
    position
    '''
    print("__________________________listing:")
    lst_stp = []
    for uni in lst:
        stp_str = str(uni.number) + " comm: " + str(uni.command)

        try:
            stp_str += " prev: " + str(uni.prev_step.number)

        except:
            stp_str += " prev: None"

        stp_str += " nxt: "
        try:
            for nxt_uni in uni.next_step_list:
                stp_str += "  " + str(nxt_uni.number)

        except:
            stp_str += "empty"

        if curr == uni.number:
            stp_str += "                           <<< here I am <<<"

        lst_stp.append(stp_str)

    print(lst_stp)
    return lst_stp


def build_dict_list(lst, curr):
    '''
    builds the list that either is shown in console on the server side
    or is sent back to the client. Here we handle format conversion more
    that the logic of running commands and building the tree.

    This function normally gets called when running the HTTP server
    '''
    print(" - - - - - building list:")
    lst_stp = []
    for uni in lst:
        step_dict = {
            "lin_num":uni.number,
            "command":str(uni.command[0]),
            "success":uni.success
        }

        try:
            step_dict["prev_step"] = int(uni.prev_step.number)

        except:
            step_dict["prev_step"] = None

        nxt_lst = []
        try:
            for nxt_uni in uni.next_step_list:
                nxt_lst.append(int(nxt_uni.number))

        except:
            pass

        step_dict["nxt"] = nxt_lst

        if( curr == uni.number ):
            step_dict["here"] = True

        else:
            step_dict["here"] = False

        lst_stp.append(step_dict)

    print(lst_stp)
    return lst_stp


class show_tree(object):
    '''
    Navigates recursively the connections on each object instance
    of << uni_step >> contained on the << step_list >> inside the
    only instance of << runner >>.

    This way we can show a tree of commands no matter how many ramifications
    the user creates.

    '''
    def __init__(self, uni_controler):
        self.lst_nodes = []
        self.build_recursive_list(
            step = uni_controler.step_list[0],
            curr = uni_controler.current, indent = 1
        )

        for node in self.lst_nodes:
            col = node["indent"] * 5 + 7
            for row_num in range(node["parent_row"] + 2, node["my_row"]):
                str_2_cp_from = str(self.lst_nodes[row_num]["lin2print"])
                new_str = str_2_cp_from[:col] + "|" + str_2_cp_from[col + 1:]
                self.lst_nodes[row_num]["lin2print"] = new_str

        for node in self.lst_nodes:
            print(node["lin2print"])

    def build_recursive_list(
        self, step = None, curr = None, indent = 1, parent_row = 0
    ):
        if step.success == True:
            stp_prn = " ✓ "

        elif step.success == False:
            stp_prn = " ✘ "

        else:
            stp_prn = " ? "

        str_lin_num = "{:3}".format(step.number)

        stp_prn += str_lin_num + "     " * indent + " \__"
        try:
            stp_prn += "(" + str(step.command[0]) + ")"

        except:
            stp_prn += "None"

        if step.number == curr:
            stp_prn += "            <<< here "

        my_row = len(self.lst_nodes)

        step_node = {
            "indent":indent, "lin2print":stp_prn,
            "my_row":my_row, "parent_row":parent_row,
        }
        self.lst_nodes.append(step_node)

        try:
            for line in step.next_step_list:
                self.build_recursive_list(
                    step = line, curr = curr,
                    indent = indent + 1, parent_row = my_row
                )

        except:
            #print("last indent =", indent)
            pass


def run_cmd(cmd_lst, run_dir):
    '''
    runs in << run_dir >> the command stored in << cmd_lst >>
    returns in a list the console output and the status of the execution
    '''
    lst_output = []
    lst_w_witch = list(cmd_lst)
    print("__________________________________\n << running >>", lst_w_witch)
    try:
        lst_w_witch[0] = str(shutil.which(lst_w_witch[0]))
        my_proc = subprocess.Popen(
            lst_w_witch,
            shell = False,
            cwd = run_dir,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            universal_newlines = True
        )

    except FileNotFoundError:
        return ["File Not Found"],  False

    try:
        while my_proc.poll() is None or new_line != '':
            new_line = my_proc.stdout.readline()[:-1]
            if new_line != '':
                lst_output.append(new_line)

        my_proc.stdout.close()
        if my_proc.poll() == 0:
            print("cmd Run OK")

        else:
            return ["Error Number" + str(my_proc.poll())],  False

    except AttributeError:
        return ["Attribute Error with: " + cmd_str],  False

    return lst_output, True


class uni_step(object):
    '''
    Handles each node of the tree in connection with its previous/parent node.

    Stores connection with parent node and builds command line connected
    to the file generated by the previous/parent node.

    when talking about nodes here we are not talking about O.O.P. we are
    referring to the command control tree
    '''
    def __init__(self, prev_step):
        self.number = 0
        self.next_step_list = []
        self.prev_step = prev_step
        self.command = [None]
        self.success = True
        self._base_dir = os.getcwd()
        self._run_dir = ""
        self._lst_file_in = []
        try:
            lst_parent_files = glob.glob(prev_step._run_dir + os.sep + "*.*")
            for file_2_add in lst_parent_files:
                self._lst_file_in.append(file_2_add)

        except TypeError:
            print(
                "prev_step =" + str(prev_step) + " empty "
            )

    def __call__(self, cmd_lst):
        self.command = cmd_lst
        self.set_run_dir(self.number)
        if cmd_lst[0] == "fail":
            #testing virtual failed step
            print("\n FAILED \n")
            self.success = False

        else:
            for parent_file in self._lst_file_in:
                cmd_lst.append(parent_file)

            self.log_lst, self.success = run_cmd(cmd_lst, self._run_dir)
            for line_out in self.log_lst:
                print(line_out)

            lof_file = open(self._run_dir + os.sep + "out.log", "w")
            for log_line in self.log_lst:
                wrstring = log_line + "\n"
                lof_file.write(wrstring)

            lof_file.close()

    def set_run_dir(self, num = None):
        self._run_dir = self._base_dir + os.sep + "run" + str(num)
        try:
            os.mkdir(self._run_dir)

        except FileExistsError:
            print("assuming the command should run in same dir")
            self._run_dir = self._base_dir


class root_node(object):
    '''
    An empty node without previous/parent node should be created
    as a  starting point
    '''
    def __init__(self):
        self._run_dir = os.getcwd()
        lof_file = open(self._run_dir + os.sep + "root_out.log", "w")
        lof_file.write("root init file \n")
        lof_file.close()
        print("Root dir =", self._run_dir)
        self.number = 0
        self.command = [None]
        self.success = True
        self.next_step_list = []


class runner(object):
    '''
    Handles user request to run commands and how nodes are connected

    properties of each node, like command that runs and how it is related
    to other nodes are in the list of objects << step_list >> , this objects
    are instances of the class << uni_step >>
    '''
    def __init__(self):
        try:
            shutil.rmtree("cmd_tree")
            print("\n removed cmd_tree dir to run program \n")

        except FileNotFoundError:
            print("no need to remove cmd_tree")

        os.mkdir("cmd_tree")
        os.chdir("cmd_tree")
        root_ini = root_node()
        self.step_list = [root_ini]
        self.bigger_lin = 0
        self.current = self.bigger_lin

    def run(self, command):
        print("command =", command)
        cmd_lst = command.split()
        try:
            if cmd_lst[0] == "goto":
                self.goto(int(cmd_lst[1]))

            elif cmd_lst[0] == "slist":
                self.slist()

            elif cmd_lst[0].isdigit():
                print("Should go to line", int(cmd_lst[0]))
                self.goto(int(cmd_lst[0]))
                if len(cmd_lst) > 1:
                    self.exec_step(cmd_lst[1:])

            else:
                self.exec_step(cmd_lst)

        except IndexError:
            print("\n empty command \n")

    def exec_step(self, cmd_lst):
        print("self.current =", self.current)
        if self.step_list[self.current].success == True:
            self.create_step(self.step_list[self.current])
            self.step_list[self.current](cmd_lst)

        else:
            print("cannot run from failed step")

    def create_step(self, prev_step):
        new_step = uni_step(prev_step)
        self.bigger_lin += 1
        new_step.number = self.bigger_lin
        self.step_list[self.current].next_step_list.append(new_step)
        self.step_list.append(new_step)
        self.goto(new_step.number)

    def goto_prev(self):
        print("forking")
        try:
            self.goto(self.step_list[self.current].prev_step.number)

        except:
            print("can NOT fork <None> node ")

    def goto(self, new_lin):
        if new_lin <= self.bigger_lin:
            self.current = new_lin

    def slist(self):
        print("printing in steps list mode: \n")
        prin_lst(self.step_list, self.current)


if __name__ == "__main__":
    uni_controler = runner()
    command = ""
    while command.strip() != 'exit':
        #prin_lst(uni_controler.step_list, uni_controler.current)

        # showing tree
        print("________ showing steps tree:")
        show_tree(uni_controler)

        try:
            command = str(input(">>> "))

        except:
            print(" ...tweak key pressed ... quitting")
            sys.exit(0)

        uni_controler.run(command)

