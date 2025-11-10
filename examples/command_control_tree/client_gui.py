
import sys, requests, json, os

import gui_deps
from qt_libs import *

class Form(QObject):
    '''
    controls the behaviour of the main window, including its own
    events and the click/goto signal coming from the << tree_scene >>

    The user can do a left click on any node of the tree
    to launch a << goto >> http request. By clicking on the buttons
    in the main window can be launched other http requests or modify
    the next http request
    '''
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        ui_dir_path = os.path.dirname(os.path.abspath(__file__))
        ui_path = ui_dir_path + os.sep
        self.window = QtUiTools.QUiLoader().load(ui_path + "simple.ui")
        self.req_qr = ""
        self.tree_scene = gui_deps.TreeDirScene(self)
        self.window.TreeGraphicsView.setScene(self.tree_scene)

        self.window.Button4Post.clicked.connect(self.clicked_4_post)
        self.window.LsButton.clicked.connect(self.clicked_ls)
        self.window.CatButton.clicked.connect(self.clicked_cat)
        self.window.EditPostRequestLine.textChanged.connect(self.new_req_txt)
        self.tree_scene.node_clicked_w_left.connect(self.clicked_goto)

        self.window.show()

    def clicked_goto(self, nod_lin_num):
        self.window.EditPostRequestLine.setText(str(nod_lin_num))
        print("clicked nod: ", nod_lin_num)
        if self.clicked_4_post():
            self.tree_scene.draw_cursor_only(nod_lin_num)

    def clicked_ls(self):
        self.window.EditPostRequestLine.setText("ls")

    def clicked_cat(self):
        self.window.EditPostRequestLine.setText("cat")

    def do_get(self):
        #print("do_get")
        req_get = requests.get(
            "http://127.0.0.1:45678", params = {"message":"dummy"}
        )
        lst_out = req_get.content
        my_lst = json.loads(lst_out)['Answer']
        self.tree_scene.draw_4_me(my_lst)

    def clicked_4_post(self):
        full_cmd = {"message":self.req_qr}
        try:
            req_post = requests.post(
                "http://127.0.0.1:45678", data = json.dumps(full_cmd)
            )
            lst_out = req_post.content
            self.window.LogTextEdit.appendPlainText(
                str(json.loads(lst_out))
            )
            self.do_get()
            return True

        except requests.exceptions.RequestException:
            print("requests.exceptions.RequestException")
            self.window.LogTextEdit.appendPlainText(
                "Request Exception Error"
            )
            return False

        except NameError:
            print("NameError")
            self.window.LogTextEdit.appendPlainText(
                "Name Error"
            )
            return False

    def new_req_txt(self, new_txt):
        self.req_qr = str(new_txt)


def main():
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

