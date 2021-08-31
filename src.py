from tkinter import *
import pymssql
import datetime

def get_connection():
    con = pymssql.connect(host='127.0.0.1', user = 'visitor', password = '123456', 
                          database='midterm')
    return con

def main():
    lb = Label(root, text="请选择您的身份", font=("Arial",24))
    lb.place(x = 380, y = 50)
    bn1 = Button(root, text="顾客", font=("Arial",24), command=jump_to_customer)
    bn1.place(x = 400, y = 150, width = 200, height = 100)
    bn2 = Button(root, text="商户", font=("Arial",24), command=jump_to_shop)
    bn2.place(x = 400, y = 300, width = 200, height = 100)
    root.mainloop()

def jump_to_customer():
    frame.destroy()
    customer()

def jump_to_shop():
    frame.destroy()
    shop()

def customer():
    bn1 = Button(root, text="注册", font=("Arial",24), command=customer_register)
    bn1.place(x = 400, y = 150, width = 200, height = 100)
    bn2 = Button(root, text="登录", font=("Arial",24), command=customer_login)
    bn2.place(x = 400, y = 300, width = 200, height = 100)

def customer():

        res = False
        username = ''
        while True:
            res, username = customer_login()
            if res == True:
                break
        print("登录成功！")
        while True:
            print("查询商铺：0；查询商品：1；查看购物车：2；查看购买记录：3；退出登录：4")
            action = input()
            if action == '0':
                shopname = input("请输入商铺名：")
                search_shop(username, shopname)
            elif action == '1':
                proname = input("请输入商品名：")
                search_product(username, proname)
            elif action == '2':
                check_trolley(username)
            elif action == '3':
                check_purchase(username)
            else:
                break
           
def customer_register():
    username = input('用户名：')
    password = input('密码：')
    phone = input('电话号码：')
    location = input('所在地：')
    address = input('地址：')
    
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
        print(sql_insert)
        cur.execute(sql_insert)
        print(sql_purchaseview)
        cur.execute(sql_purchaseview)
        print(sql_trolleyview)
        cur.execute(sql_trolleyview)
        con.commit()
        cur.close()
        con.close()
    except Exception as e:
        print(e)

def customer_login():
    username = input('用户名：')
    password = input('密码：')
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
                return True, username
            else:
                print('密码错误，请重新输入！')
                return False, ''
        else:
            print("不存在此用户名，请重新输入！")
            return False, ''
    except Exception as e:
        print(e)

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
        print(e)

    return result

def search_shop(username, shopname):
    result = item_in_shop(shopname)
    
    want = []
    print("请输入你想加入购物车的商品的序号，#号结束选择")
    while True:
        idx = input()
        if idx == '#':
            break
        elif int(idx) >= 0:
            want.append(result[int(idx)])
    if len(want) > 0:
        add_trolley(username, want)

def search_product(username, proname):
    sql_query = """exec FindShopWithItem @proname = '{}'""".format(proname)
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
        print(e)
    
    want = []
    print("请输入你想加入购物车的商品的序号，#号结束选择")
    while True:
        idx = input()
        if idx == '#':
            break
        elif int(idx) >= 0:
            want.append(result[int(idx)])
    if len(want) > 0:
        add_trolley(username, want)

def add_trolley(username, result):
    sql_insert = """insert into TROLLEY values (%s, %s, %s)"""
    trolleyList = []
    for item in result:
        trolleyList.append((username, item[0], item[1]))
    print(trolleyList)
    input()
    
    try:
        con = get_connection()
        cur = con.cursor()
        print(sql_insert)
        cur.executemany(sql_insert, trolleyList)
        con.commit()
        cur.close()
        con.close()
    except Exception as e:
        print(e)

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

    want = []
    print("请输入你本次想购买的商品的序号，#号结束选择")
    while True:
        idx = input()
        if idx == '#':
            break
        elif int(idx) >= 0:
            want.append(result[int(idx)])
    if len(want) > 0:
        make_purchase(username, want)

def make_purchase(username, result):
    dt = datetime.datetime.now()
    purchase_num = dt.strftime('%Y%m%d%H%M%S')
    for i in range(len(result)):
        item = result[i]
        result[i] = (purchase_num, item[0], item[1], item[2])

    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute("""insert into LIST values('{}', '{}')""".format(purchase_num, username))
        con.commit()
        cur.executemany("""insert into CONTAIN values(%s,%s,%s,%s)""", result)
        con.commit()
        cur.close()
        con.close()
    except Exception as e:
        print(e)

def check_purchase(username):
    print("按订单号升序查看：0；按订单总价降序查看：1")
    action = input()
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
        print(orders)
        for lst in orders:
            cur.execute("""select SHOPNAME, PRONAME, PRICE
                           from PURCHASEVIEW_{}
                           where NUM = '{}'""".format(username, lst[0]))
            items = cur.fetchall()
            print(lst)
            print(items)
        cur.close()
        con.close()
    except Exception as e:
        print(e)

def shop():
    print("注册：0；登录：1")
    action = input()
    if action == '0':
        shop_register()
    else:
        res = False
        shopname = ''
        while True:
            res, shopname = shop_login()
            if res == True:
                break
        print("登录成功！")
        while True:
            print("加入新品：0；调整商品价格：1；下架商品：2；查看出售情况：3；退出登录：4")
            action = input()
            if action == '0':
                add_product(shopname)
            elif action == '1':
                alter_price(shopname)
            elif action == '2':
                delete_product(shopname)
            elif action == '3':
                check_sale(shopname)
            else:
                break

def shop_register():
    shopname = input('商铺名：')
    password = input('密码：')
    
    sql_insert = """insert into SHOP values('{}','{}')""".format(shopname, password)
    
    try:
        con = get_connection()
        cur = con.cursor()
        print(sql_insert)
        cur.execute(sql_insert)
        con.commit()
        cur.close()
        con.close()
    except Exception as e:
        print(e)

def shop_login():
    shopname = input('商铺名：')
    password = input('密码：')
    sql_query = """select PWD from SHOP
                where SHOPNAME = '{}'""".format(shopname)
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
                return True, shopname
            else:
                print('密码错误，请重新输入！')
                return False, ''
        else:
            print("不存在此商铺名，请重新输入！")
            return False, ''
    except Exception as e:
        print(e)

def add_product(shopname):
    proname = input('请输入要上架的商品：')
    price = float(input('请输入价格:'))
    sql = """execute AddProduct @shopname = '{}', @proname = '{}', @price = {}""".format(shopname, proname, price)

    try:
        con = get_connection()
        cur = con.cursor()
        print(sql)
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()
    except Exception as e:
        print(e)

def alter_price(shopname):
    items = item_in_shop(shopname)
    print(items)
    print('调整单个商品：0；按比例调整所有商品：1')
    action = input()
    sql = ''
    if action == '0':
        proname = input('请输入要调整的商品名')
        price = float(input('请输入新定价'))
        sql = """execute AlterSinglePrice @shopname = '{}', @proname = '{}', @price = {}""".format(shopname, proname, price)
    else:
        price = float(input('请输入调整百分数'))/100
        sql = """execute AlterAllPrice @shopname = '{}', @percentage = {}""".format(shopname, price)
    
    try:
        con = get_connection()
        cur = con.cursor()
        print(sql)
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()
    except Exception as e:
        print(e)

def delete_product(shopname):
    items = item_in_shop(shopname)
    print(items)
    proname = input('请输入要下架的商品名')
    sql = """execute DeleteProduct @shopname = '{}', @proname = '{}'""".format(shopname, proname)
    try:
        con = get_connection()
        cur = con.cursor()
        print(sql)
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()
    except Exception as e:
        print(e)

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
    except Exception as e:
        print(e)

root = Tk()
root.title("购物平台")
root.geometry("1000x600")
frame = Frame(root)

main()
        