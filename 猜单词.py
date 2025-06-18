import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk,Image
import random
import json
#定义word类，包含方法：选择单词，打乱单词，将单词加错词库，错词库练习、增加单词
class Word():
    
    def __init__(self):
        self._file = "word.txt"
        self.word = ""
        self.mix_word = ""
        self.error_state = True
        self.add_state = True
    def select(self):
        with open(self._file) as word_file:
            line_list = word_file.readlines()
        word_list = [item.rstrip() for item in line_list]
        word_select = random.choice(word_list)
        self.word = word_select   

    def mix(self):
        word_copy = self.word
        jumble = ""
        while word_copy:
            position = random.randrange(len(word_copy))
            jumble+=word_copy[position]
            word_copy = word_copy[:position]+word_copy[(position+1):]
        self.mix_word =jumble

    def insert(self,error_filename):#由于每个用户的错词库名称不同，因此在调用有关错词库的方法时需要提供错词库名称
        with open(error_filename,'a') as error_file:
            error_file.write(self.word+'\n')

    def ErrorExercise(self,error_filename):
        try:
            with open(str(error_filename)) as word_file:
                line_list = word_file.readlines()
        except FileNotFoundError:
            self.error_state = False
        else:
            with open(error_filename) as word_file:
                line_list = word_file.readlines()
            word_list = []
            for item in line_list:
                word_list.append(item.rstrip())
            word_select = random.choice(word_list)
            self.word = word_select



    def wordadd(self,input_word):#在调用方法是需要提供要添加的单词名
    
        with open(self._file) as f:
            line_list = f.readlines()

        word_list=[item.rstrip() for item in line_list]
        if (input_word in word_list) or input_word == "":
            self.add_state = False
        else:
            with open(self._file,"a") as f:
                f.write(input_word+'\n')
            self.add_state = True
        


#定义user类，包含方法：判断是否是新用户、更改用户信息中的积分
class User():
    def __init__(self):
        self.username = ""
        self.user = ""
        self.score = 0
        self.user_dic = {}
        self.state = True
    def greet(self):
        #将用户信息保存在JSON类型文件中
        try:
            with open("user_name.json") as f:
                self.user_dic = json.load(f)
        except FileNotFoundError:           
            self.state=True

        if self.user not in self.user_dic:
            self.user_dic = {self.user:self.score}
            self.user_dic[self.user] = self.score
            with open("user_name.json", 'w') as f:
                json.dump(self.user_dic,f)

        else:
            self.state = False
            
    def Score(self,score):
        self.score = int(score)+self.user_dic[self.user]
        self.user_dic[self.user] = self.score
        with open("user_name.json",'w') as f1:
            json.dump(self.user_dic,f1)
        



w=Word()
u=User()        
#欢迎界面
def function():
    global u
    global w
    #规则及功能选择界面
    root1=tk.Tk()
    root1.title("rules")
    root1.geometry("550x350+600+300")
    errorfilename = str(u.user)+".txt"
    #针对新老用户，显示不同的欢迎语
    if u.state == False:
        tk.Label(root1,text = "欢迎回来，请仔细阅读以下规则！",font = 15).place(x = 140,y = 15)
    else:
        tk.Label(root1,text = "欢迎新用户，请仔细阅读以下规则！",font = 10).place(x = 120,y = 15)
    tk.Label(root1,text = "请根据下方提示按钮选择不同功能！",font = 10).place(x = 110,y = 50)
    tk.Label(root1,text = "每局游戏您有三次机会，如果答错，请注意下方提示。",font = 10).place(x = 50,y = 85)
    tk.Label(root1,text = "一次答对计三分，两次答对计两分，三次答对计一分",font = 10).place(x = 45,y = 120)


    #单词库增加界面
    def add():
        global w
        root2=tk.Toplevel(root1)
        root2.title("add")
        root2.geometry("400x200+700+350")
        var1 = tk.StringVar()
        def sure(word = w):
            
            word_get = entry3.get()
            word.wordadd(word_get)
            if word.add_state == True:
                root2.destroy()
            elif word.add_state == False:
                var1.set("请换一个单词！")

        tk.Label(root2,text = "请输入一个新单词").place(x = 10,y = 50)
        tk.Label(root2,textvariable = var1).place(x = 20,y = 90)
        entry3=tk.Entry(root2,width = 30)
        entry3.place(x = 120,y = 50)
        tk.Button(root2,text = "确定",width = 10,command = sure).place(x = 180,y = 100)
        root2.mainloop()

    #游戏主界面
    def game():
        global w
        global u
        nonlocal errorfilename
        root3=tk.Toplevel(root1)
        root3.title("game")
        root3.geometry("550x350+600+300")
        var2 = tk.StringVar()
        var3 = tk.StringVar()
        atp = 3
        canvas2 = tk.Canvas(root3,height = 150,width = 550,bg = "grey")
        i = Image.open('guess.jpg')
        i = i.resize((550,150),Image.Resampling.LANCZOS)
        image_file = ImageTk.PhotoImage(i)
        image = canvas2.create_image(0,0,anchor = "nw",image = image_file)
        canvas2.pack(side = 'top')
        #退出游戏
        def exit_game():
            root3.destroy()
            root4 = tk.Toplevel(root1)
            root4.title("score")
            root4.geometry("400x200+700+350")
            tk.Label(root4,text = u.username + "的成绩为" + str(u.score),font = 15).place(x = 100,y = 80)
            root4.mainloop()
        #开始游戏
        def begin(word = w):
            word.select()
            word.mix()
            var2.set(word.mix_word)
            nonlocal atp
            atp=3
        #评判作答结果
        def judge(word = w,user = u):
            #atp记录参与次数
            nonlocal atp
            word_input = entry3.get()
            if word_input == word.word:
                var3.set("你猜对了！")
                if atp == 3:
                    user.Score("3")
                elif atp == 2:
                    user.Score("2")
                elif atp == 1:
                    user.Score("1")
            if word_input!=word.word:
                if atp>0:
                    atp-=1
                    alp=word.word[(2-atp)]
                    var3.set("你猜错了！该单词第"+str(3-atp)+"个字母是:"+alp+"，你还有"+str(atp)+"次机会")
                    user.Score("0")

                elif atp == 0:
                    var3.set("很抱歉。你没有机会了！请重新开始游戏！")
        #加入收藏夹
        def erroradd(word = w,error_file = str(errorfilename)):
            try:
                with open(error_file) as f:
                    line_list = f.readlines()
            #如果该用户之前没有专属的错词库，建立一个
            except FileNotFoundError:
                with open(error_file,"w") as f:
                    f.write(str(word.word)+"\n")
            else:
                with open(error_file,"a") as f:
                    f.write(str(word.word)+"\n")
        tk.Label(root3,text = "乱序单词为：",font = 10).place(x = 70,y = 160)
        tk.Label(root3,text = "答案为：",font = 10).place(x = 110,y = 200)
        tk.Button(root3,text = "开始游戏",font = 15,command = begin).place(x = 240,y = 300)
        tk.Button(root3,text = "提交答案",command = judge).place(x = 260,y = 260)
        tk.Label(root3,textvariable = var2,font = 10).place(x = 190,y = 160)
        tk.Label(root3,textvariable = var3,fg = "red").place(x = 170,y = 230)
        tk.Button(root3,text = "退出游戏",font = 15,command = exit_game).place(x = 50,y = 300)
        tk.Button(root3,text = "加入收藏夹",font = 15,command = erroradd).place(x = 430,y = 300)
        entry3=tk.Entry(root3,width = 30,show = None)
        entry3.place(x = 190,y = 210)
        root3.mainloop()

    #错词库练习界面
    #具体原理和游戏界面相同
    def errorexercise():
        global u
        global w
        nonlocal errorfilename
        root5=tk.Toplevel(root1)
        root5.title("game")
        root5.geometry("550x350+600+300")
        w.ErrorExercise(str(errorfilename))
        w.mix()
        var4 = tk.StringVar()
        var5 = tk.StringVar()
        canvas3 = tk.Canvas(root5,height = 150,width = 550,bg = "grey")
        i = Image.open('exercise.jpg')
        i = i.resize((550,150),Image.Resampling.LANCZOS)
        image_file = ImageTk.PhotoImage(i)
        image = canvas3.create_image(0,0,anchor = "nw",image = image_file)
        canvas3.pack(side = 'top')
        def exit_game():
            root5.destroy()
        def begin(word = w):
            word.ErrorExercise(str(errorfilename))
            word.mix()
            var4.set(word.mix_word)
        def judge(word = w,uesr = u):
            word_input = entry3.get()
            if word_input != word.word:
                var5.set("你猜错了！")
            else:
                var5.set("你猜对了！")
        tk.Label(root5,text = "乱序单词为：",font = 10).place(x = 70,y =160)
        tk.Label(root5,text = "答案为：",font = 10).place(x = 110,y = 200)
        tk.Button(root5,text = "开始游戏",font = 15,command = begin).place(x = 240,y = 300)
        tk.Button(root5,text = "提交答案",command = judge).place(x = 260,y = 260)
        tk.Label(root5,textvariable = var4,font = 10).place(x = 190,y = 160)
        tk.Label(root5,textvariable = var5,fg = "red").place(x = 170,y = 230)
        tk.Button(root5,text = "退出游戏",font = 15,command = exit_game).place(x = 50,y = 300)
        entry3=tk.Entry(root5,width = 30,show = None)
        entry3.place(x = 190,y = 210)
        root5.mainloop()


    #可选择功能按钮
    tk.Button(root1,text = "增加新单词",width = 10,command = add).place(x = 50,y = 250)
    tk.Button(root1,text = "进入游戏",width = 10,command = game).place(x = 450,y = 200)
    tk.Button(root1,text = "收藏夹练习",width = 10,command = errorexercise).place(x = 450,y = 250)
    root1.mainloop()     

#登录界面
root=tk.Tk()
root.title("Guess Word")
root.geometry("550x350+600+300")
var = tk.StringVar()
canvas1 = tk.Canvas(root,height = 150,width = 550,bg = "grey")
i = Image.open('welcome.jpg')
i = i.resize((550,150),Image.Resampling.LANCZOS)
image_file = ImageTk.PhotoImage(i)
image = canvas1.create_image(0,0,anchor = "nw",image = image_file)
canvas1.pack(side = 'top')
tk.Label(root,text = "用户名:",font = 15).place(x = 90,y = 180)
tk.Label(root,text = "密码:",font = 15).place(x = 100,y = 220)
tk.Label(root,textvariable = var).place(x = 150,y = 260)
entry1=tk.Entry(root,width = 30,show = None)
entry1.place(x = 210,y = 185)
entry2=tk.Entry(root,width = 30,show = "*")
entry2.place(x = 210,y = 225)
def Log_in():
    if entry1.get() and entry2.get():
        username = entry1.get()
        userkey = entry2.get()
        global u
        u.user = username+userkey
        u.username = username
        u.greet()        
        root.destroy()
        function()
    #当用户输入用户名和密码为空时，返回提示语
    else:
        var.set("请输入你的用户名和密码！")

tk.Button(root,text = "Log in",width = 10,command = Log_in).place(x = 420,y = 280)
root.mainloop()

    

