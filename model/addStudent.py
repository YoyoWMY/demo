# 用来实现新增读者功能
import sys
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QLabel, QLineEdit, QToolButton, QGroupBox, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

from model import database_try

KEY_LIST = ['SID', 'PASSWORD', 'SNAME',
            'DEPARTMENT', 'MAJOR']

class addStudent(QGroupBox):
    '''
        新增学生信息的界面
        返回 user_message{
        'SID': str,
        'PASSWORD': str,
        'SNAME': str,
        'DEPARTMENT': str,
        'MAJOR': str,
        'MAX': int
    }
    }
    '''
    after_close = pyqtSignal(dict)

    def __init__(self, stu_info: dict = None):
        super().__init__()
        if stu_info is not None:
            self.stu_info = stu_info
        else:
            self.stu_info = {
                'SID':'请输入学号',
                'PASSWORD': '请输入密码',
                'SNAME': '请输入姓名',
                'DEPARTMENT': '请输入所在学院',
                'MAJOR': '请输入所在专业',
                'MAX':10
            }

        self.title = QLabel()
        self.title.setText('新增学生')

        self.subTitle = QLabel()
        self.subTitle.setText('新增一个学生信息')

        # 学号输入框
        self.SIDInput = QLineEdit()
        self.SIDInput.setFixedSize(400, 40)
        self.SIDInput.setText(self.stu_info['SID'])
        self.SIDInput.initText = '请输入学号'
        self.SIDInput.mousePressEvent = lambda x: self.inputClick(self.SIDInput)

        # 姓名输入框
        self.nameInput = QLineEdit()
        self.nameInput.setFixedSize(400, 40)
        self.nameInput.setText(self.stu_info['SNAME'])
        self.nameInput.initText = '请输入姓名'
        self.nameInput.setTextMargins(5, 5, 5, 5)
        self.nameInput.mousePressEvent = lambda x: self.inputClick(self.nameInput)

        # 密码
        self.passwordInput = QLineEdit()
        self.passwordInput.setFixedSize(400, 40)
        self.passwordInput.setText('请输入密码')
        self.passwordInput.initText = '请输入密码'
        self.passwordInput.setTextMargins(5, 5, 5, 5)
        self.passwordInput.mousePressEvent = lambda x: self.inputClick(self.passwordInput)

        # 重复密码
        self.repPasswordInput = QLineEdit()
        self.repPasswordInput.setFixedSize(400, 40)
        self.repPasswordInput.setText('请重复输入密码')
        self.repPasswordInput.initText = '请重复输入密码'
        self.repPasswordInput.setTextMargins(5, 5, 5, 5)
        self.repPasswordInput.mousePressEvent = lambda x: self.inputClick(self.repPasswordInput)

        # 学院
        self.deptInput = QLineEdit()
        self.deptInput.setFixedSize(400, 40)
        self.deptInput.setText(self.stu_info['DEPARTMENT'])
        self.deptInput.initText = '请输入所在学院'
        self.deptInput.setTextMargins(5, 5, 5, 5)
        self.deptInput.mousePressEvent = lambda x: self.inputClick(self.deptInput)

        # 专业
        self.majorInput = QLineEdit()
        self.majorInput.setFixedSize(400, 40)
        self.majorInput.setText(self.stu_info['MAJOR'])
        self.majorInput.initText = '请输入所在专业'
        self.majorInput.setTextMargins(5, 5, 5, 5)
        self.majorInput.mousePressEvent = lambda x: self.inputClick(self.majorInput)

        # 提交
        self.submit = QToolButton()
        self.submit.setText('提交')
        self.submit.setFixedSize(400, 40)
        self.submit.clicked.connect(self.submitFunction)

        # 退出
        self.back = QToolButton()
        self.back.setText('退出')
        self.back.setFixedSize(400, 40)
        self.back.clicked.connect(self.close)

        self.btnList = [
            self.SIDInput,
            self.nameInput,
            self.passwordInput,
            self.repPasswordInput,
            self.deptInput,
            self.majorInput
        ]

        self.bodyLayout = QVBoxLayout()
        self.bodyLayout.addWidget(self.title)
        self.bodyLayout.addWidget(self.subTitle)
        for i in self.btnList:
            self.bodyLayout.addWidget(i)
        self.bodyLayout.addWidget(self.submit)
        self.bodyLayout.addWidget(self.back)

        self.setLayout(self.bodyLayout)
        self.initUI()

    def inputClick(self, e):
        # for i in range(2, 9):
        for i in range(1, 8):
            item = self.bodyLayout.itemAt(i).widget()
            if item.text() == '':
                item.setText(item.initText)
                if item is self.passwordInput or item is self.repPasswordInput:
                    item.setEchoMode(QLineEdit.Normal)

        if e.text() == e.initText:
            e.setText('')
        if e is self.passwordInput or e is self.repPasswordInput:
            e.setEchoMode(QLineEdit.Password)

    def submitFunction(self):
        for btn, key in zip(self.btnList, KEY_LIST):
            if btn.text() == btn.initText:
                self.stu_info[key] = ''
            else:
                self.stu_info[key] = btn.text()

        if self.passwordInput.text() != self.repPasswordInput.text():
            msgBox = QMessageBox(QMessageBox.Warning, "错误!", '两次输入密码不一致!', QMessageBox.NoButton, self)
            msgBox.addButton("确认", QMessageBox.AcceptRole)
            msgBox.exec_()
            return
        # self.stu_info['PASSWORD'] = database.encrypt(self.passwordInput.text())
        self.stu_info['PASSWORD'] = database_try.encrypt(self.passwordInput.text())
        self.stu_info['SNAME'] = self.nameInput.text()
        self.stu_info['DEPARTMENT'] = self.deptInput.text()
        self.stu_info['MAJOR'] = self.majorInput.text()
        self.close()
        self.after_close.emit(self.stu_info)


    def initUI(self):
        self.setFixedSize(422, 500)
        self.setWindowTitle('新增学生')
        self.setWindowIcon(QIcon('icon/person.png'))
        self.setMyStyle()

    def errorBox(self, mes: str):
        msgBox = QMessageBox(
            QMessageBox.Warning,
            "警告!",
            mes,
            QMessageBox.NoButton,
            self
        )
        msgBox.addButton("确认", QMessageBox.AcceptRole)
        msgBox.exec_()


    def setMyStyle(self):
        self.setStyleSheet('''
        QWidget{
            background-color: white;
        }
        QLineEdit{
            border:0px;
            border-bottom: 1px solid rgba(229, 229, 229, 1);
            color: grey;
        }
        QToolButton{
            border:0;
            background-color:rgba(50, 198, 212, 1);
            color: white;
            font-size: 20px;
            font-family: 微软雅黑;
        }
        QGroupBox{
            border: 1px solid rgba(229, 229, 229, 1);
            border-radius: 5px;
        }
        ''')
        self.title.setStyleSheet('''
        *{
            color: rgba(113, 118, 121, 1);
            font-size: 30px;
            font-family: 微软雅黑;
        }
        ''')
        self.subTitle.setStyleSheet('''
        *{
            color: rgba(184, 184, 184, 1);
        }
        ''')


if __name__ == '__main__':
    stu_msg = temp = {
        'SID': '3',
        'SNAME': '小王',
        'DEPARTMENT': '数学与信息科学学院',
        'MAJOR': 'SE'
    }
    app = QApplication(sys.argv)
    ex = addStudent(stu_msg)
    ex.show()
    sys.exit(app.exec_())
