from PySide2.QtWidgets import QApplication, QMessageBox,QMainWindow
from PySide2.QtUiTools import QUiLoader

import random

class Main:

    def __init__(self):
        # 加载ui文件
        self.ui = QUiLoader().load('exam.ui')

        # 题号 初始值为0 即最开始为第一题
        self.count = 0

        # 创建一个空字典用于存储处理后的题目
        self.space_list = []

        # 设置要做得题数
        self.maxCount = 5

        # 最开始的分数
        self.fraction = 0

        # 设置满分
        self.fullScore = 100

        # 创建一个空变量，用于存储用户输入的答案
        # 思路：根据要做得题数创建一个跟题数一样长度的字典，其中的所有元素都为空
        # 下面哪个按钮被点击了，就根据索引将字典中的空元素修改为被点击的按钮
        self.user_answer = []
        for i in range(self.maxCount):
            self.user_answer.append('')
        print(f"最开始的答案:{self.user_answer}")


        # 创建一个空字典，用于存储标准答案
        self.standard_answer = []
        # 获取标准答案
        with open("questions.txt") as f:
            answers_list = f.readlines()
        # 添加上转义字符，使得界面显示空格
        for i in answers_list:
            self.standard_answer.append(i.replace('/n/t', '\n\t').split("#")[1])  # 0是题目 1是答案
        print(f'标准答案：{self.standard_answer}')




        # 执行点击事件
        self.action()



    def action(self):
        # 读取txt文件数据
        with open("questions.txt") as f:
            questions_list = f.readlines()
        # 添加上转义字符，使得界面显示空格
        for i in questions_list:
            self.space_list.append(i.replace('/n/t','\n\t').split("#")[0]) #0是题目 1是答案

        # 此时 space_list 变量存储的才是我们真正想要的题库数据 (数据清洗)
        # print(self.space_list,len(self.space_list))

        # 随机产生索引 使用set集合是为了不随机产生相同的索引数字
        # 创建一个空集合，用于存储产生不重复的随机数 用作索引题库(space_list)
        number_set = set()
        while True:
            # 如果number_set的长度等于最大题数，说明产生了我们想要的随机数个数 那就跳出死循环
            # 否则就继续产生随机数，（如果产生的随机数重复则进不来set集合中，
            # 所以要继续产生随机数并存入set集合中，直到set的长度与最大题数一致）
            if len(number_set) == self.maxCount:
                break
            # 将产生的随机数添加到number_set
            number_set.add(random.randint(0, len(self.space_list)-1)) #总题数
        # 将产生的索引集合转换成列表 然后通过该列表中的数字索引出题目列表
        global number_list #定义全局变量
        number_list = list(number_set)
        print(f"产生的索引:{number_list}")

        # # 尝试打印出本次随机生成的题目 number_list是存储最终产生的五个随机数
        # for j in number_list:
        #     print(f"随机产生的题目:\n{f'{int(self.count)+1}.'+self.space_list[j]}")


        # 执行按钮点击事件
        self.button_action()



    # 最终产生的随机题目
    def newQuestions(self,number_list,space_list):
        # 创建一个空列表，用于存储随机生成的题目
        new_questions = []
        # 给题目添加题号，并将产生的新题目存入到paper_list
        global paper_list
        paper_list = []
        for i in number_list:
            new_questions.append(space_list[i])
            # print(f"随机产生的题目:\n{f'{int(self.count+1)}.'+self.space_list[i]}")
        print(f'new_questions:{new_questions}')
        # 给题目增加题号
        for i in range(len(new_questions)):
            paper_list.append(f'{i+1}.'+new_questions[i])
        return paper_list


    # 上一题显示
    def before_button(self):
        # 最终的随机题目
        new_questions = self.newQuestions(number_list, self.space_list)
        self.count -= 1  # 索引自减1
        print(f"此时count索引是:{self.count}")

        # 当回到第一题的时候就禁用上一题按钮
        if self.count <= 0:
            self.ui.pushButton_before.setEnabled(False)

        # 清除所有按钮的颜色
        self.clear_color()
        # 保持上一题的答案选项
        self.keep_Answer()

        # 下一题按钮解放
        self.ui.pushButton_next.setEnabled(True)
        # 上一题按钮被点击了，就清空原来的显示框内容
        self.ui.textEdit.clear()
        # 显示上一题
        self.ui.textEdit.setText(paper_list[self.count])
        # self.ui.textEdit.setText(f'{self.count}.'+self.space_list[number_list[self.count]-1])
    # 下一题显示
    def next_button(self):
        # 最终的随机题目
        new_questions = self.newQuestions(number_list, self.space_list)
        self.count += 1  # 索引自增1
        print(f"此时count索引是:{self.count}")

        self.clear_color()
        # 保持上一题的答案选项
        self.keep_Answer()

        self.ui.pushButton_before.setEnabled(True)  # 上一题按钮解放
        # 如果到最后一题了，那么就不能再下一题了 即禁用下一题按钮 当前索引>=最大索引
        if self.count >= self.maxCount-1:
            self.ui.pushButton_next.setEnabled(False)

        # 下一页按钮被点击了，就清空原来的显示框内容
        self.ui.textEdit.clear()
        # 显示下一题
        self.ui.textEdit.setText(paper_list[self.count])

    # button事件
    def button_action(self):
        # 最终的随机题目
        new_questions = self.newQuestions(number_list, self.space_list)
        # 将题目显示到文本框上
        self.ui.textEdit.setText(paper_list[self.count])
        print(f"此时count数：{self.count}")
        # 在第一题的时候就禁用上一题按钮
        if self.count <= 0:
            self.ui.pushButton_before.setEnabled(False)
        # 上一题按钮
        self.ui.pushButton_before.clicked.connect(self.before_button)
        # 下一题按钮
        self.ui.pushButton_next.clicked.connect(self.next_button)
        # A按钮
        self.ui.pushButton_A.clicked.connect(self.A_button)
        # B按钮
        self.ui.pushButton_B.clicked.connect(self.B_button)
        # C按钮
        self.ui.pushButton_C.clicked.connect(self.C_button)
        # A按钮
        self.ui.pushButton_D.clicked.connect(self.D_button)
        # 交卷按钮
        self.ui.pushButton_submit.clicked.connect(self.Right_Or_Not)
        # 重置按钮
        self.ui.pushButton_reset.clicked.connect(self.reset_button)



    # 获取随机产生的题目的答案
    def get_random_standard_answer(self):
        # number_list 产生的随机索引
        random_answer = []
        for i in number_list:
            random_answer.append(self.standard_answer[i])
        # 去掉列表中的换行 \n
        return [x.strip() for x in random_answer if x.strip()]


    # 判断用户给的答案与正确答案是否一致
    def Right_Or_Not(self):
        self.ui.pushButton_A.setEnabled(False)
        self.ui.pushButton_B.setEnabled(False)
        self.ui.pushButton_C.setEnabled(False)
        self.ui.pushButton_D.setEnabled(False)
        self.ui.pushButton_next.setEnabled(False)
        self.ui.pushButton_before.setEnabled(False)
        self.ui.pushButton_submit.setEnabled(False)

        # 获取随机产生题目的标准答案
        random_answer = self.get_random_standard_answer()


        # 与用户给的答案 进行 判断对错
        for i in range(len(random_answer)):
            if self.user_answer[i] == random_answer[i]:
                # 满分 除以 本次做的题目的总数 来确定每道题几分
                self.fraction += float(self.fullScore/self.maxCount)
        if self.fraction == 100:
            # 弹出对话框
            reply = QMessageBox.about(self.ui,
                                      "本次答题总分",
                                      f"恭喜你满分过关",
                                      )
        elif self.fraction == 0:
            # 弹出对话框
            reply = QMessageBox.about(self.ui,
                                      "温馨提示",
                                      f"请仔细答题哦",
                                      )
        else:
            # 弹出对话框
            # round(小数(float类型),要保留的小数位数(int类型)) 函数 格式化小数点后几位
            reply = QMessageBox.about(self.ui,
                                      "本次答题总分",
                                      f"分数是：{round(self.fraction,1)}",
                                      )
        print(reply)

        print(f"用户的答案：{self.user_answer}")
        print(f"标准的答案：{random_answer}")
        print(f"最终得分：{self.fraction}")

    # A按钮
    def A_button(self):
        # 获取按钮上的字母
        word = self.ui.pushButton_A.text()

        # 当按钮被点击就改变颜色
        self.ui.pushButton_A.setStyleSheet("background-color: yellow")
        self.ui.pushButton_B.setStyleSheet('')
        self.ui.pushButton_C.setStyleSheet('')
        self.ui.pushButton_D.setStyleSheet('')
        # 将用户输入的答案存入到user_answer中
        self.user_answer[self.count] = 'A'
        print(self.user_answer)
        print("你点击了",word)

    # B按钮
    def B_button(self):
        # 获取按钮上的字母
        word = self.ui.pushButton_B.text()
        # 当按钮被点击就改变颜色
        self.ui.pushButton_A.setStyleSheet("")
        self.ui.pushButton_B.setStyleSheet("background-color: yellow")
        self.ui.pushButton_C.setStyleSheet("")
        self.ui.pushButton_D.setStyleSheet("")
        # 将用户输入的答案存入到user_answer中
        self.user_answer[self.count] = 'B'
        print(self.user_answer)
        print("你点击了",word)

    # C按钮
    def C_button(self):
        # 获取按钮上的字母
        word = self.ui.pushButton_C.text()
        # 当按钮被点击就改变颜色
        self.ui.pushButton_A.setStyleSheet("")
        self.ui.pushButton_B.setStyleSheet("")
        self.ui.pushButton_C.setStyleSheet("background-color: yellow")
        self.ui.pushButton_D.setStyleSheet("")
        # 将用户输入的答案存入到user_answer中
        self.user_answer[self.count] = 'C'
        print(self.user_answer)
        print("你点击了", word)

    # D按钮
    def D_button(self):
        # 获取按钮上的字母
        word = self.ui.pushButton_D.text()
        # 当按钮被点击就改变颜色
        self.ui.pushButton_A.setStyleSheet("")
        self.ui.pushButton_B.setStyleSheet("")
        self.ui.pushButton_C.setStyleSheet("")
        self.ui.pushButton_D.setStyleSheet("background-color: yellow")
        # 将用户输入的答案存入到user_answer中
        self.user_answer[self.count] = 'D'
        print(self.user_answer)
        print("你点击了", word)

    # 重置按钮
    def reset_button(self):
        # 清除颜色按钮
        self.clear_color()
        # 将count设为0
        self.count = 0
        # 将原本答案清空
        for i in range(len(self.user_answer)):
            self.user_answer[i] = ""
        # 回归到第一题
        self.ui.textEdit.setText(paper_list[self.count])
        # 设计按钮 启用 和 禁用
        self.ui.pushButton_A.setEnabled(True)
        self.ui.pushButton_B.setEnabled(True)
        self.ui.pushButton_C.setEnabled(True)
        self.ui.pushButton_D.setEnabled(True)
        self.ui.pushButton_submit.setEnabled(True)
        self.ui.pushButton_next.setEnabled(True)
        self.ui.pushButton_before.setEnabled(False)
        print(f"你点击了重置按钮,此时count为:{self.count}")


    # 清除按钮的所有颜色
    def clear_color(self):
        self.ui.pushButton_A.setStyleSheet("")
        self.ui.pushButton_B.setStyleSheet("")
        self.ui.pushButton_C.setStyleSheet("")
        self.ui.pushButton_D.setStyleSheet("")

    # 保持用户上一题点击的答案
    def keep_Answer(self):
        answer = self.user_answer[self.count]
        print("=================\n",answer,"\n===============")
        # 判断用户的答案是否为空
        if answer == "":
            return
        if answer == "A":
            self.ui.pushButton_A.setStyleSheet("background-color: yellow")
        elif answer == "B":
            self.ui.pushButton_B.setStyleSheet("background-color: yellow")
        elif answer == "C":
            self.ui.pushButton_C.setStyleSheet("background-color: yellow")
        elif answer == "D":
            self.ui.pushButton_D.setStyleSheet("background-color: yellow")
        else:
            self.ui.pushButton_D.setStyleSheet("")


if __name__ == '__main__':
    # 加载ui文件
    app = QApplication([])
    m = Main()
    m.ui.show()
    app.exec_()


