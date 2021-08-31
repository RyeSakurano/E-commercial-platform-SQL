from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.font as tkFont
from tkinter import ttk
import pymssql
import datetime

# 连接数据库
def get_connection():
    con = pymssql.connect(host='127.0.0.1', user = 'visitor', password = '123456', 
                          database='midterm')
    return con

# 初始主页
class MainPage(object):
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1000x600")
        self.root.title('购物商城主页')
        ft1 = tkFont.Font(size=24)
        ft2 = tkFont.Font(size=16)
        lb = Label(self.root, text="请选择您的身份", font = ft1)
        lb.place(x = 390, y = 50)
        bn1 = Button(self.root, text="顾客", font = ft1, command=self.jump_customer_init)
        bn1.place(x = 400, y = 150, width = 200, height = 100)
        bn2 = Button(self.root, text="商户", font = ft1, command=self.jump_shop_init)
        bn2.place(x = 400, y = 300, width = 200, height = 100)
        
        self.root.mainloop()
    
    # 跳转到顾客初始页
    def jump_customer_init(self):
        self.root.destroy()
        CustomerInitPage()

    # 跳转到商铺初始页
    def jump_shop_init(self):
        self.root.destroy()
        ShopInitPage()

# 顾客初始页
class CustomerInitPage(object):
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1000x600")
        self.root.title('用户')
        ft1 = tkFont.Font(size=24)
        ft2 = tkFont.Font(size=16)
        bn1 = Button(self.root, text="注册", font = ft1, command=self.jump_customer_register)
        bn1.place(x = 400, y = 150, width = 200, height = 100)
        bn2 = Button(self.root, text="登录", font = ft1, command=self.jump_customer_login)
        bn2.place(x = 400, y = 300, width = 200, height = 100)
        bn3 = Button(self.root, text="返回主页", font = ft2, command=self.jump_main)
        bn3.place(x = 700, y = 450, width = 100, height = 50)

        self.root.mainloop()

    # 跳转到初始主页
    def jump_main(self):
        self.root.destroy()
        MainPage()

    # 顾客注册弹窗
    def jump_customer_register(self):
        inputDialog = CustomerRegisterPage()
        self.root.wait_window(inputDialog)
        if not inputDialog.userinfo == None:
            self.root.destroy()
            MainPage()
    
    # 顾客登录弹窗
    def jump_customer_login(self):
        inputDialog = CustomerLoginPage()
        self.root.wait_window(inputDialog)
        if not inputDialog.userinfo == None: # 登录成功
            self.root.destroy()
            CustomerPage(inputDialog.userinfo)

# 顾客注册弹窗
class CustomerRegisterPage(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('用户注册')
        self.userinfo = None

        row1 = Frame(self)
        row1.pack(fill='x')
        Label(row1, text='用户名（不超过15字）：',width=20).pack(side=LEFT)
        self.username = StringVar()
        Entry(row1, textvariable=self.username, width=20).pack(side=LEFT)
        
        row2 = Frame(self)
        row2.pack(fill='x')
        Label(row2, text='密码（不超过30字）：',width=20).pack(side=LEFT)
        self.password = StringVar()
        Entry(row2, textvariable=self.password, width=20).pack(side=LEFT)

        row3 = Frame(self)
        row3.pack(fill='x')
        Label(row3, text='电话号码：',width=20).pack(side=LEFT)
        self.phone = StringVar()
        Entry(row3, textvariable=self.phone, width=20).pack(side=LEFT)

        row4 = Frame(self)
        row4.pack(fill='x')
        Label(row4, text='所在地（不超过10字）：',width=20).pack(side=LEFT)
        self.location = StringVar()
        Entry(row4, textvariable=self.location, width=20).pack(side=LEFT)

        row5 = Frame(self)
        row5.pack(fill='x')
        Label(row5, text='地址（不超过50字）：',width=20).pack(side=LEFT)
        self.address = StringVar()
        Entry(row5, textvariable=self.address, width=20).pack(side=LEFT)

        row6 = Frame(self)
        row6.pack(fill='x')
        Button(row6, text='取消',command=self.cancel).pack(side=RIGHT)
        Button(row6, text='确定',command=self.ok).pack(side=RIGHT)

    # 点击“取消”时
    def cancel(self):
        self.destroy()
    
    # 点击“确认”时
    def ok(self):
        self.username = self.username.get()
        self.password = self.password.get()
        self.phone = self.phone.get()
        self.location = self.location.get()
        self.address = self.address.get()
        # 检查输入是否满足长度要求；一定程度预防SQL注入攻击
        if self.username.find("--")>=0 or len(self.username)>15:
            print(len(self.username))
            messagebox.showerror('错误','用户名不符合要求，请重新输入！')
        elif self.password.find("--")>=0 or len(self.password)>30:
            messagebox.showerror('错误','密码不符合要求，请重新输入！')
        elif self.phone.find("--")>=0 or len(self.phone)>15:
            messagebox.showerror('错误','电话号码不符合要求，请重新输入！')
        elif self.location.find("--")>=0 or len(self.location)>10:
            messagebox.showerror('错误','所在地不符合要求，请重新输入！')
        elif self.address.find("--")>=0 or len(self.address)>50:
            messagebox.showerror('错误','地址不符合要求，请重新输入！')
        else:
            self.customer_register()
            self.destroy()

    # 访问数据库查找是否存在用户名；若不存在，插入信息及用户的两个视图
    def customer_register(self):
        username = self.username
        password = self.password
        phone = self.phone
        location = self.location
        address = self.address
    
        sql = """select * from CUSTOMER where USERNAME = '{}'""".format(username)
        sql_insert = """insert into CUSTOMER values('{}', '{}', '{}', '{}', '{}')""".format(username, password, phone, location, address)
        sql_purchaseview = """create view PURCHASEVIEW_{}
                    as (select LIST.NUM, CONTAIN.SHOPNAME, CONTAIN.PRONAME, CONTAIN.PRICE
                    from LIST join CONTAIN on LIST.NUM = CONTAIN.NUM
                    where LIST.USERNAME = '{}')""".format(username, username)
        sql_trolleyview = """create view TROLLEYVIEW_{}
                    as (select TROLLEY.SHOPNAME, TROLLEY.PRONAME, PRODUCT.PRICE
                    from TROLLEY join PRODUCT on PRODUCT.SHOPNAME = TROLLEY.SHOPNAME and PRODUCT.PRONAME = TROLLEY.PRONAME
                    where TROLLEY.USERNAME = '{}')""".format(username, username)

        try:
            con = get_connection()
            cur = con.cursor()
            print(sql)
            cur.execute(sql)
            res = cur.fetchall()
            if len(res) > 0:
                messagebox.showerror('错误','用户名已存在！')
                cur.close()
                con.close()
                return False
            con.commit()
            print(sql_insert)
            cur.execute(sql_insert)
            print(sql_purchaseview)
            cur.execute(sql_purchaseview)
            print(sql_trolleyview)
            cur.execute(sql_trolleyview)
            con.commit()
            cur.close()
            con.close()
            self.userinfo = username
            messagebox.showinfo('提示','注册成功，返回主页……')
            return True
        except Exception as e:
            cur.rollback()
            print(e)
            messagebox.showerror('错误','注册发生错误，请重试！')
            return False

# 顾客登录弹窗
class CustomerLoginPage(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('用户登录')
        self.userinfo = None

        row1 = Frame(self)
        row1.pack(fill='x')
        Label(row1, text='用户名：',width=20).pack(side=LEFT)
        self.username = StringVar()
        Entry(row1, textvariable=self.username, width=20).pack(side=LEFT)
        
        row2 = Frame(self)
        row2.pack(fill='x')
        Label(row2, text='密码：',width=20).pack(side=LEFT)
        self.password = StringVar()
        Entry(row2, textvariable=self.password, width=20).pack(side=LEFT)

        row6 = Frame(self)
        row6.pack(fill='x')
        Button(row6, text='取消',command=self.cancel).pack(side=RIGHT)
        Button(row6, text='确定',command=self.ok).pack(side=RIGHT)

    # 点击“取消”
    def cancel(self):
        self.destroy()

    # 点击“确认”
    def ok(self):
        self.username = self.username.get()
        self.password = self.password.get()
        # 检查输入长度是否符合要求；避免SQL注入攻击
        if self.username.find("--")>=0 or len(self.username)>15:
            messagebox.showerror('错误','用户名不符合要求，请重新输入！')
        elif self.password.find("--")>=0 or len(self.password)>30:
            messagebox.showerror('错误','密码不符合要求，请重新输入！')
        else:
            if self.customer_login():
                self.userinfo = self.username
            self.destroy()

    # 操作数据库检查用户名是否存在；查找密码比较是否正确
    def customer_login(self):
        username = self.username
        password = self.password
        sql_query = """select PWD from CUSTOMER
                    where USERNAME = '{}'""".format(username)
        pwd = ""

        try:
            con = get_connection()
            cur = con.cursor()
            print(sql_query)
            cur.execute(sql_query)
            result = cur.fetchall()
            cur.close()
            con.close()
            if len(result) > 0:
                pwd = result[0][0]
                if pwd == password:
                    messagebox.showinfo('提示','登录成功！')
                    return True
                else:
                    messagebox.showerror('错误', '密码错误，请重新输入！')
                    return False
            else:
                messagebox.showerror('错误',"不存在此用户名，请重新输入！")
                return False
        except Exception as e:
            messagebox.showerror('错误','登录发生错误，请重试！')
            return False

# 用户主页
class CustomerPage(object):
    def __init__(self, username):
        self.root = Tk()
        self.root.geometry("1000x600")
        self.root.title('用户')
        self.username = username
        ft1 = tkFont.Font(size=24)
        ft2 = tkFont.Font(size=16)
        lb = Label(self.root, text="欢迎用户 {}".format(username), font= ft2)
        lb.place(x = 200, y = 50)
        bn1 = Button(self.root, text="按商铺名查找商品", font = ft1, command=self.jump_searchshop)
        bn1.place(x = 300, y = 100, width = 400, height = 100)
        bn1 = Button(self.root, text="按商品名查找商品", font = ft1, command=self.jump_searchitem)
        bn1.place(x = 300, y = 200, width = 400, height = 100)
        bn2 = Button(self.root, text="查看购物车", font = ft1, command=self.jump_trolley)
        bn2.place(x = 300, y = 300, width = 400, height = 100)
        bn3 = Button(self.root, text="查看已购订单", font = ft1, command=self.jump_list)
        bn3.place(x = 300, y = 400, width = 400, height = 100)
        bn4 = Button(self.root, text="退出登录", font = ft2, command=self.jump_main)
        bn4.place(x = 750, y = 450, width = 100, height = 50)

        self.root.mainloop() 
    
    def jump_searchshop(self):
        SearchShopPage(self.username)

    def jump_searchitem(self):
        SearchItemPage(self.username)

    def jump_trolley(self):
        result = check_trolley(self.username)
        TrolleyPage(self.username, result)

    def jump_list(self):
        inputDialog = CheckList()
        self.root.wait_window(inputDialog)
        orders, result = check_purchase(self.username, inputDialog.userinfo)
        ListPage(orders, result)

    def jump_main(self):
        self.root.destroy()
        MainPage()

# 查找指定商铺的所有商品的输入页面
class SearchShopPage(Toplevel):
    def __init__(self, username):
        super().__init__()
        self.title('查找商品')
        self.username = username

        row1 = Frame(self)
        row1.pack(fill='x')
        Label(row1, text='商铺名：',width=20).pack(side=LEFT)
        self.shopname = StringVar()
        Entry(row1, textvariable=self.shopname, width=20).pack(side=LEFT)

        row6 = Frame(self)
        row6.pack(fill='x')
        Button(row6, text='取消',command=self.cancel).pack(side=RIGHT)
        Button(row6, text='确定',command=self.ok).pack(side=RIGHT)

    def cancel(self):
        self.destroy()

    def ok(self):
        shopname = self.shopname.get()
        if shopname.find("--") >= 0 or len(shopname) > 15:
            messagebox.showerror("错误","商铺名不符合要求，请重新输入！")
        else:
            # 查询结果并跳转到结果显示页
            result = item_in_shop(shopname)
            self.destroy()
            SearchResultPage(self.username, result)

# 查找包含指定关键字的商品及所在商铺
class SearchItemPage(Toplevel):
    def __init__(self, username):
        super().__init__()
        self.title('查找商品')
        self.username = username

        row1 = Frame(self)
        row1.pack(fill='x')
        Label(row1, text='商品名关键字：',width=20).pack(side=LEFT)
        self.proname = StringVar()
        Entry(row1, textvariable=self.proname, width=20).pack(side=LEFT)

        row6 = Frame(self)
        row6.pack(fill='x')
        Button(row6, text='取消',command=self.cancel).pack(side=RIGHT)
        Button(row6, text='确定',command=self.ok).pack(side=RIGHT)

    def cancel(self):
        self.destroy()

    def ok(self):
        proname = self.proname.get()
        if proname.find("--") >= 0 or len(proname) > 15:
            messagebox.showerror("错误","商品名不符合要求，请重新输入！")
        else: # 查找结果并跳转到结果显示页
            result = search_product(proname)
            self.destroy()
            SearchResultPage(self.username, result)

# 查找结果显示页
class SearchResultPage(object):
    def __init__(self, username, result):
        self.root = Tk()
        self.result = result
        self.username = username
        Label(self.root, text = "请选择您要加入购物车的商品").pack()
        lb = Listbox(master = self.root, width = 100, selectmode = MULTIPLE)
        lb.pack()
        bt = Button(self.root, text="确定加入购物车", command=lambda: self.add_trolley(lb.curselection()))
        bt.pack()

        if len(result) == 0:
            messagebox.showinfo('提示','没有找到结果')
            self.root.destroy()
        else:
            for item in result:
                lb.insert("end", "商铺：{} | 商品：{} | 价格：{}".format(item[0], item[1], item[2]))
        
        self.root.mainloop()
    
    # 将选中的商品插入购物车表
    def add_trolley(self, indices):
        sql_insert = """execute AddTrolley @username = '{}', @shopname = '{}', @proname = '{}'"""
        try:
            con = get_connection()
            cur = con.cursor()
            for idx in indices:
                idx = int(idx)
                print(sql_insert)
                cur.execute(sql_insert.format(self.username, self.result[idx][0], self.result[idx][1]))
            con.commit()
            cur.close()
            con.close()
            messagebox.showinfo('提示','加入购物车成功！')
            self.root.destroy()
        except Exception as e:
            messagebox.showinfo('错误','加入购物车发生错误，请重试！')

# 返回所有在名字为shopname的商铺的商品信息（商铺名、商品名、价格）
def item_in_shop(shopname):
    sql_query = """exec FindItemInShop @shopname = '{}'""".format(shopname)
    result = []

    try:
        con = get_connection()
        cur = con.cursor()
        print(sql_query)
        cur.execute(sql_query)
        result = cur.fetchall()
        print(result)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showeeror("错误","查询发生错误，请重试！")

    return result

# 返回所有包含proname关键字的商品信息（商铺名、商品名、价格）
def search_product(proname):
    sql_query = """exec FindShopWithItem @proname = '%{}%'""".format(proname)
    result = []

    try:
        con = get_connection()
        cur = con.cursor()
        print(sql_query)
        cur.execute(sql_query)
        result = cur.fetchall()
        print(result)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showeeror("错误","查询发生错误，请重试！")

    return result

# 购物车页
class TrolleyPage(object):
    def __init__(self, username, result):
        self.root = Tk()
        self.root.title('购物车')
        self.result = result
        self.username = username
        lb = Listbox(master = self.root, width = 100, selectmode = MULTIPLE)
        lb.pack()
        bt = Button(self.root, text="确定购买", command=lambda: self.make_purchase(lb.curselection()))
        bt.pack()

        if len(result) == 0:
            messagebox.showinfo('提示','购物车为空，赶紧去看看吧！')
            self.root.destroy()
        else:
            for item in result:
                lb.insert("end", "商铺：{} | 商品：{} | 价格：{}".format(item[0], item[1], item[2]))
        
        self.root.mainloop()

    # 下单——事务
    def make_purchase(self, indices):
        dt = datetime.datetime.now()
        purchase_num = dt.strftime('%Y%m%d%H%M%S')
        lst = []
        for idx in indices:
            idx = int(idx)
            item = self.result[idx]
            lst.append((purchase_num, item[0], item[1], item[2]))

        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute("""insert into LIST values('{}', '{}')""".format(purchase_num, self.username))
            cur.executemany("""insert into CONTAIN values(%s,%s,%s,%s)""", lst)
            con.commit()
            cur.close()
            con.close()
            messagebox.showinfo('提示','购买成功！')
            self.root.destroy()
        except Exception as e:
            cur.rollback()
            print(e)
            messagebox.showerror('错误','购买发生错误，请重试！')

# 已购清单查看方式弹窗
class CheckList(Toplevel):
    def __init__(self):
        super().__init__()
        row6 = Frame(self)
        row6.pack(fill='x')
        Button(row6, text='按订单号升序查看',command=self.asc).pack()
        Button(row6, text='按总价格降序查看',command=self.desc).pack()

    def asc(self):
        self.userinfo = '0'
        self.destroy()

    def desc(self):
        self.userinfo = '1'
        self.destroy()

# 已购清单页
class ListPage(object):
    def __init__(self, orders, result):
        self.root = Tk()
        self.root.geometry("1000x600")
        self.root.title('已购订单')
        tree = ttk.Treeview(self.root)

        x = 0
        for order in orders:
            print(order)
            node = tree.insert("", x, order[0], 
                       text = "订单号：{} | 总价格：{}".format(order[0], order[1]))
            y = 0
            for item in result[x]:
                print(item)
                tree.insert(node, y, order[0]+item[0]+item[1], 
                       text = "商铺名：{} | 商品名：{} | 价格：{}".format(item[0], item[1], item[2]))
                y += 1
            x += 1
        tree.pack(expand = True, fill = 'both')
        self.root.mainloop()

# 查看用户的购物车视图
def check_trolley(username):
    sql_query = """select * from TROLLEYVIEW_{}""".format(username)

    try:
        con = get_connection()
        cur = con.cursor()
        print(sql_query)
        cur.execute(sql_query)
        result = cur.fetchall()
        print(result)
        cur.close()
        con.close()
    except Exception as e:
        print(e)

    return result

# 查询购物清单结果：先查找订单号+总价；再查找每个订单的具体商品信息
def check_purchase(username, action):
    sql_query = ''
    if action == '0':
        sql_query = """select NUM, sum(PRICE)
                       from PURCHASEVIEW_{}
                       group by NUM
                       order by NUM asc""".format(username)
    else:
        sql_query = """select NUM, sum(PRICE) as TOTALPRICE
                       from PURCHASEVIEW_{}
                       group by NUM
                       order by TOTALPRICE desc""".format(username)

    try:
        con = get_connection()
        cur = con.cursor()
        print(sql_query)
        cur.execute(sql_query)
        orders = cur.fetchall()
        result = []
        for lst in orders:
            cur.execute("""select SHOPNAME, PRONAME, PRICE
                           from PURCHASEVIEW_{}
                           where NUM = '{}'""".format(username, lst[0]))
            items = cur.fetchall()
            result.append(items)
        cur.close()
        con.close()
        return orders, result
    except Exception as e:
        messagebox.showerror('错误','查询错误，请重试！')
        print(e)

# 商铺初始页面
class ShopInitPage(object):
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1000x600")
        self.root.title('商铺')
        ft1 = tkFont.Font(size=24)
        ft2 = tkFont.Font(size=16)
        bn1 = Button(self.root, text="注册", font = ft1, command=self.jump_shop_register)
        bn1.place(x = 400, y = 150, width = 200, height = 100)
        bn2 = Button(self.root, text="登录", font = ft1, command=self.jump_shop_login)
        bn2.place(x = 400, y = 300, width = 200, height = 100)
        bn3 = Button(self.root, text="返回主页", font = ft2, command=self.jump_main)
        bn3.place(x = 700, y = 450, width = 100, height = 50)

        self.root.mainloop()

    def jump_main(self):
        self.root.destroy()
        MainPage()

    def jump_shop_register(self):
        inputDialog = ShopRegisterPage()
        self.root.wait_window(inputDialog)
        if not inputDialog.userinfo == None:
            self.root.destroy()
            MainPage()

    def jump_shop_login(self):
        inputDialog = ShopLoginPage()
        self.root.wait_window(inputDialog)
        if not inputDialog.userinfo == None:
            self.root.destroy()
            ShopPage(inputDialog.userinfo)

# 商铺注册弹窗
class ShopRegisterPage(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('商铺注册')
        self.userinfo = None

        row1 = Frame(self)
        row1.pack(fill='x')
        Label(row1, text='商铺名（不超过15字）：',width=20).pack(side=LEFT)
        self.shopname = StringVar()
        Entry(row1, textvariable=self.shopname, width=20).pack(side=LEFT)
        
        row2 = Frame(self)
        row2.pack(fill='x')
        Label(row2, text='密码（不超过15字）：',width=20).pack(side=LEFT)
        self.password = StringVar()
        Entry(row2, textvariable=self.password, width=20).pack(side=LEFT)

        row6 = Frame(self)
        row6.pack(fill='x')
        Button(row6, text='取消',command=self.cancel).pack(side=RIGHT)
        Button(row6, text='确定',command=self.ok).pack(side=RIGHT)

    def cancel(self):
        self.destroy()

    def ok(self):
        self.shopname = self.shopname.get()
        self.password = self.password.get()
        if self.shopname.find("--")>=0 or len(self.shopname)>15:
            print(len(self.shopname))
            messagebox.showerror('错误','商铺名不符合要求，请重新输入！')
        elif self.password.find("--")>=0 or len(self.password)>30:
            messagebox.showerror('错误','密码不符合要求，请重新输入！')
        else:
            self.shop_register()
            self.destroy()
    
    # 从数据库中查询商铺名是否存在；若不存在，将商铺信息插入商铺表
    def shop_register(self):
        sql = """select * from SHOP where SHOPNAME = '{}'""".format(self.shopname)
        sql_insert = """insert into SHOP values('{}','{}')""".format(self.shopname, self.password)
    
        try:
            con = get_connection()
            cur = con.cursor()
            print(sql)
            cur.execute(sql)
            res = cur.fetchall()
            if len(res) > 0:
                messagebox.showerror('错误','商铺名已存在！')
                cur.close()
                con.close()
                return False
            print(sql_insert)
            cur.execute(sql_insert)
            con.commit()
            cur.close()
            con.close()
            self.userinfo = self.shopname
            return True
        except Exception as e:
            print(e)
            messagebox.showerror('错误','注册发生错误！')
            return False

# 商铺登录弹窗
class ShopLoginPage(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('商铺登录')
        self.userinfo = None

        row1 = Frame(self)
        row1.pack(fill='x')
        Label(row1, text='商铺名：',width=20).pack(side=LEFT)
        self.shopname = StringVar()
        Entry(row1, textvariable=self.shopname, width=20).pack(side=LEFT)
        
        row2 = Frame(self)
        row2.pack(fill='x')
        Label(row2, text='密码：',width=20).pack(side=LEFT)
        self.password = StringVar()
        Entry(row2, textvariable=self.password, width=20).pack(side=LEFT)

        row6 = Frame(self)
        row6.pack(fill='x')
        Button(row6, text='取消',command=self.cancel).pack(side=RIGHT)
        Button(row6, text='确定',command=self.ok).pack(side=RIGHT)

    def cancel(self):
        self.destroy()

    def ok(self):
        self.shopname = self.shopname.get()
        self.password = self.password.get()
        if self.shopname.find("--")>=0 or len(self.shopname)>15:
            messagebox.showerror('错误','商铺名不符合要求，请重新输入！')
        elif self.password.find("--")>=0 or len(self.password)>30:
            messagebox.showerror('错误','密码不符合要求，请重新输入！')
        else:
            if self.shop_login():
                self.userinfo = self.shopname
            self.destroy()
    
    # 从数据库查询是否存在商铺名；从商铺表选择对应密码，比较是否正确
    def shop_login(self):
        sql_query = """select PWD from SHOP
                    where SHOPNAME = '{}'""".format(self.shopname)
        pwd = ""

        try:
            con = get_connection()
            cur = con.cursor()
            print(sql_query)
            cur.execute(sql_query)
            result = cur.fetchall()
            cur.close()
            con.close()
            if len(result) > 0:
                pwd = result[0][0]
                if pwd == self.password:
                    messagebox.showinfo('提示','登录成功！')
                    return True
                else:
                    messagebox.showerror('错误','密码错误，请重新输入！')
                    return False
            else:
                messagebox.showerror('错误',"不存在此商铺名，请重新输入！")
                return False
        except Exception as e:
            messagebox.showerror('错误','登录发生错误，请重试！')
            return False

# 商铺主页
class ShopPage(object):
    def __init__(self, shopname):
        self.root = Tk()
        self.root.geometry("1000x600")
        self.root.title('商铺')
        self.shopname = shopname
        ft1 = tkFont.Font(size=24)
        ft2 = tkFont.Font(size=16)
        lb = Label(self.root, text="欢迎商家 {}".format(shopname), font= ft2)
        lb.place(x = 200, y = 50)
        bn1 = Button(self.root, text="添加新品", font = ft1, command=self.jump_addproduct)
        bn1.place(x = 300, y = 100, width = 400, height = 100)
        bn1 = Button(self.root, text="调整价格", font = ft1, command=self.jump_alterprice)
        bn1.place(x = 300, y = 200, width = 400, height = 100)
        bn2 = Button(self.root, text="下架商品", font = ft1, command=self.jump_deleteproduct)
        bn2.place(x = 300, y = 300, width = 400, height = 100)
        bn3 = Button(self.root, text="查看出售统计", font = ft1, command=self.jump_sale)
        bn3.place(x = 300, y = 400, width = 400, height = 100)
        bn4 = Button(self.root, text="退出登录", font = ft2, command=self.jump_main)
        bn4.place(x = 750, y = 450, width = 100, height = 50)

        self.root.mainloop() 
    
    def jump_addproduct(self):
        AddProductPage(self.shopname)

    def jump_alterprice(self):
        AlterPricePage(self.shopname)

    def jump_deleteproduct(self):
        DeleteProductPage(self.shopname)

    def jump_sale(self):
        SalePage(self.shopname)

    def jump_main(self):
        self.root.destroy()
        MainPage()

# 插入新商品弹窗
class AddProductPage(Toplevel):
    def __init__(self, shopname):
        super().__init__()
        self.title('添加新品')
        self.shopname = shopname

        row1 = Frame(self)
        row1.pack(fill='x')
        Label(row1, text='商品名：',width=20).pack(side=LEFT)
        self.proname = StringVar()
        Entry(row1, textvariable=self.proname, width=20).pack(side=LEFT)

        row2 = Frame(self)
        row2.pack(fill='x')
        Label(row2, text='价格：',width=20).pack(side=LEFT)
        self.price = StringVar()
        Entry(row2, textvariable=self.price, width=20).pack(side=LEFT)

        row6 = Frame(self)
        row6.pack(fill='x')
        Button(row6, text='取消',command=self.cancel).pack(side=RIGHT)
        Button(row6, text='确定',command=self.ok).pack(side=RIGHT)

    def cancel(self):
        self.destroy()

    def ok(self):
        proname = self.proname.get()
        price = self.price.get()
        try:
            price = float(price)
        except:
            messagebox.showerror("错误","输入的价格不是数字！")
        if proname.find("--") >= 0 or len(proname) > 15:
            messagebox.showerror("错误","商品名不符合要求，请重新输入！")
        else:
            add_product(self.shopname, proname, float(price))
            self.destroy()

# 往商品表中插入新商品（若已存在则更新信息）
def add_product(shopname, proname, price):
    sql = """execute AddProduct @shopname = '{}', @proname = '{}', @price = {}""".format(shopname, proname, price)

    try:
        con = get_connection()
        cur = con.cursor()
        print(sql)
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()
        messagebox.showinfo('提示','添加成功！')
    except Exception as e:
        messagebox.showerror('错误','添加错误，请重试！')
        print(e)

# 显示商铺现存所有商品，两种调整价格方式
class AlterPricePage(object):
    def __init__(self, shopname):
        self.root = Tk()
        self.shopname = shopname
        self.root.geometry("1000x600")
        self.root.title('商品列表')
        columns = ("proname","price")
        tree = ttk.Treeview(self.root, show = "headings", columns = columns, selectmode = BROWSE)
        tree.column("proname",anchor = "center")
        tree.column("price",anchor = "center")
        tree.heading("proname", text = "商品名")
        tree.heading("price", text = "价格")

        self.result = item_in_shop(shopname)
        if len(self.result) == 0:
            messagebox.showinfo('提示','店铺中还没有商品，请先添加！')
            self.root.destroy()
            return

        i = 0
        for item in self.result:
            tree.insert('', i, values=(item[1], item[2]))
            i += 1

        tree.pack(expand = True, fill = BOTH)

        row6 = Frame(self.root)
        row6.pack(fill='x')
        Button(row6, text='调整单个商品',command=self.single).pack()
        Button(row6, text='按比例调整所有商品',command=self.all).pack()

        self.root.mainloop()

    def single(self):
        self.root.destroy()
        AlterSinglePricePage(self.shopname, self.result)

    def all(self):
        self.root.destroy()
        AlterAllPricePage(self.shopname)

# 选择单个商品调整价格
class AlterSinglePricePage(Toplevel):
    def __init__(self, shopname, result):
        super().__init__()
        self.shopname = shopname
        self.result = result
        self.title('调整单个价格')
        
        label = Label(self, text = '请选择要调整的商品').pack()
        lb = Listbox(master = self, width = 100, selectmode = SINGLE)
        lb.pack()
        for item in result:
            lb.insert("end","商品名：{} | 当前价格：{}".format(item[1], item[2]))

        Label(self, text='新价格：',width=20).pack()
        self.price = StringVar()
        Entry(self, textvariable=self.price, width=20).pack()

        row6 = Frame(self)
        row6.pack(fill='x')
        Button(row6, text='确定',command= lambda: self.alter_single_price(lb.curselection())).pack()

    # 在商品表中修改选中商品的价格
    def alter_single_price(self, indices):
        if len(indices) == 0:
            self.destroy()
            return
        item = self.result[int(indices[0])]
        try:
            price = float(self.price.get())
        except:
            messagebox.showerror('错误','输入的价格不是数字！')
            return
        proname = item[1]
        sql = """execute AlterSinglePrice @shopname = '{}', @proname = '{}', @price = {}""".format(self.shopname, proname, price)
        try:
            con = get_connection()
            cur = con.cursor()
            print(sql)
            cur.execute(sql)
            con.commit()
            cur.close()
            con.close()
            messagebox.showinfo('提示','修改成功！')
            self.destroy()
        except Exception as e:
            print(e)
            messagebox.showerror('错误','修改发生错误，请重试！')

# 按同一比例调整所有商品的价格
class AlterAllPricePage(Toplevel):
    def __init__(self, shopname):
        super().__init__()
        self.title('调整所有价格')

        self.shopname = shopname
        row1 = Frame(self)
        row1.pack(fill='x')
        Label(row1, text='调整后价格是现有价格的：',width=20).pack()
        self.percentage = StringVar()
        Entry(row1, textvariable=self.percentage, width=20).pack()
        Label(row1, text='%',width=20).pack()

        row6 = Frame(self)
        row6.pack(fill='x')
        Button(row6, text='确定',command=self.ok).pack(side=RIGHT)

    def ok(self):
        try:
            percentage = float(self.percentage.get())/100
        except:
            messagebox.showerror('错误', '输入的比例不是数字！')
        sql = """execute AlterAllPrice @shopname = '{}', @percentage = {}""".format(self.shopname, percentage)
        
        try:
            con = get_connection()
            cur = con.cursor()
            print(sql)
            cur.execute(sql)
            con.commit()
            cur.close()
            con.close()
            messagebox.showinfo('提示','修改成功！')
            self.destroy()
        except Exception as e:
            print(e)
            messagebox.showerror('错误','修改发生错误，请重试！')

# 显示商铺现存商品，选择某些商品删除
class DeleteProductPage(object):
    def __init__(self, shopname):
        self.root = Tk()
        self.shopname = shopname
        self.root.geometry("1000x600")
        self.root.title('删除商品')
        self.result = result = item_in_shop(shopname)

        lb = Listbox(master = self.root, width = 100, selectmode = MULTIPLE)
        lb.pack()
        for item in result:
            lb.insert("end","商品名：{}".format(item[1]))

        row6 = Frame(self.root)
        row6.pack(fill='x')
        Button(row6, text='确定',command= lambda: self.delete_product(lb.curselection())).pack()

        self.root.mainloop()

    def delete_product(self, indices):
        sql = """execute DeleteProduct @shopname = '{}', @proname = '{}'"""
        if len(indices) == 0:
            self.root.destroy()
            return
        try:
            con = get_connection()
            cur = con.cursor()
            for idx in indices:
                idx = int(idx)
                print(sql)
                cur.execute(sql.format(self.shopname, self.result[idx][1]))
                con.commit()
            cur.close()
            con.close()
            messagebox.showinfo('提示','删除成功！')
            self.root.destroy()
        except Exception as e:
            messagebox.showerror('错误','删除发生错误！')
            print(e)

# 查看商铺总收入、按商品统计的总收入、每个商品按地区统计的总收入
class SalePage(object):
    def __init__(self, shopname):
        self.root = Tk()
        self.root.geometry("1000x600")
        self.root.title('店铺收入合计')
        tree = ttk.Treeview(self.root)
        total, prototal, pros = check_sale(shopname)

        rt = tree.insert("", 0, "total", text = "总收入：{}".format(total))
        x = 0
        for pro in prototal:
            print(pro)
            node = tree.insert("", x, pro, 
                       text = "商品：{} | 总收入：{}".format(pro[0], pro[1]))
            y = 0
            for item in pros[x]:
                print(item)
                tree.insert(node, y, item[0]+item[1], 
                       text = "地区：{} | 总收入：{}".format(item[1], item[2]))
                y += 1
            x += 1
        tree.pack(expand = True, fill = 'both')
        self.root.mainloop()

# 使用rollup实现商铺交易统计
def check_sale(shopname):
    sql = """execute CheckSale @shopname = '{}'""".format(shopname)
    try:
        con = get_connection()
        cur = con.cursor()
        print(sql)
        cur.execute(sql)
        result = cur.fetchall()
        print(result)
        con.commit()
        cur.close()
        con.close()

        total = 0
        prototal = []
        pros = []
        curpro = []
        for item in result:
            if item[0] == None:
                total = item[2]
            elif item[1] == None:
                prototal.append((item[0], item[2]))
                pros.append(curpro)
                curpro = []
            else:
                curpro.append(item)
        return total, prototal, pros
    except Exception as e:
        print(e)
        return None, None, None

if __name__ == '__main__':
    MainPage()

        