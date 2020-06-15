from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from aes import decrypt

import sys
import os
import ntpath
import subprocess
import platform


def resource_path(relative_path):
    base_path = '.'
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class App(object):
    def __init__(self, argv):
        app = QApplication(argv)
        Form, Window = uic.loadUiType(
            resource_path("dataviewer/resources/app.ui"))
        self.window = Window()
        self.form = Form()
        self.form.setupUi(self.window)

        # 绑定事件
        self.form.btn_decrypt.clicked.connect(self.btn_decrypt_clicked)
        self.form.btn_src_file.clicked.connect(self.btn_src_file_clicked)
        self.form.btn_dest_file.clicked.connect(self.btn_dest_file_clicked)
        self.form.lbl_opendir.mouseReleaseEvent = self.lbl_opendir_clicked

        # ajuest size
        self.form.label_3.adjustSize()
        self.form.lbl_opendir.adjustSize()

        self.window.setFixedSize(600, 400)
        self.window.show()
        exit_code = app.exec_()
        sys.exit(exit_code)

    def startfile(self, target_path):
        os_name = platform.system().lower()
        if "darwin" == os_name:
            subprocess.call(["open", target_path])
        elif "windows" == os_name:
            os.startfile(target_path)
        else:
            pass

    def lbl_opendir_clicked(self, event):
        dest_file_path = self.form.edit_line_dest_file.text()

        if len(dest_file_path) == 0:
            return

        if os.path.exists(dest_file_path) == False:
            self.warning_box("目录不存在")
            return

        self.startfile(dest_file_path)


    def btn_src_file_clicked(self):
        src_file_path = self.form.edit_line_src_file.text()

        src_dirname = ntpath.dirname(src_file_path)
        if len(src_dirname) == 0 or os.path.exists(src_dirname) == False:
            src_dirname = "./"

        file_name, _ = QFileDialog.getOpenFileName(self.window,
                                                   "选取文件",
                                                   src_dirname,
                                                   "All Files (*);;Text Files (*.txt);;Csv Files (*.csv);;JSON Files (*.json)")

        if len(file_name) != 0:
            self.form.edit_line_src_file.setText(file_name)

    def btn_dest_file_clicked(self):
        dest_file_path = self.form.edit_line_dest_file.text()

        if len(dest_file_path) == 0:
            dest_file_path = "./"

        dirname_selected = QFileDialog.getExistingDirectory(
            self.window, "选取目录", dest_file_path)

        if len(dirname_selected) != 0:
            self.form.edit_line_dest_file.setText(dirname_selected)

    def btn_decrypt_clicked(self):
        src_file_path = self.form.edit_line_src_file.text()
        dest_file_path = self.form.edit_line_dest_file.text()
        key = self.form.edit_line_key.text()

        if len(src_file_path) == 0:
            self.warning_box('请选择源文件')
            return

        if len(dest_file_path) == 0:
            self.warning_box('请选择解密后文件存放目录')
            return

        if len(key) == 0:
            self.warning_box('请输入密钥')
            return

        if not os.path.exists(src_file_path):
            self.warning_box('源文件不存在')
            return

        if not os.path.exists(dest_file_path):
            self.warning_box('解密后文件存放目录不存在')
            return

        with open(src_file_path, 'r') as f:
            try:
                enc = f.read()

                if len(enc) == 0:
                    self.warning_box('源文件为空')
                    return

                raw_back = decrypt(enc, key)

                if len(raw_back) == 0:
                    self.warning_box('密钥错误')
                    return

                self.write_dest_file(
                    "%s/%s" % (dest_file_path, ntpath.basename(src_file_path)), raw_back)
            except ValueError:
                self.warning_box('源文件格式错误')
                return

        self.information_box('解密完成，请前往解密后文件存放目录查看')

    def write_dest_file(self, dest_file, raw):
        with open(dest_file, 'w') as f:
            f.write(raw)

    def warning_box(self, content):
        QMessageBox.warning(self.window, '提示', content, QMessageBox.Ok)

    def information_box(self, content):
        QMessageBox.information(self.window, '提示', content, QMessageBox.Ok)


if __name__ == '__main__':
    App(sys.argv)
