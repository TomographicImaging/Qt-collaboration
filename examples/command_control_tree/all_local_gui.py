
import sys, requests, json, os

import gui_deps
from qt_libs import *
from tree_nav import runner, show_tree, build_dict_list

class Form(QObject):
    '''
    controls the behaviour of the main window, including its own
    events and the click/goto signal coming from the << tree_scene >>
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
        self.tree_scene.node_clicked_w_left.connect(self.clicked_goto)

        self.uni_controler = runner()

        self.window.show()

    def clicked_goto(self, nod_lin_num):
        self.window.EditPostRequestLine.setText(str(nod_lin_num))
        self.clicked_4_post()
        self.tree_scene.draw_cursor_only(nod_lin_num)

    def clicked_ls(self):
        self.window.EditPostRequestLine.setText("ls")

    def clicked_cat(self):
        self.window.EditPostRequestLine.setText("cat")

    def clicked_4_post(self):
        req_qr = str(self.window.EditPostRequestLine.text())
        self.uni_controler.run(req_qr)
        show_tree(self.uni_controler)
        lst_out = build_dict_list(
            self.uni_controler.step_list, self.uni_controler.current
        )
        self.tree_scene.draw_4_me(lst_out)


def main():
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

