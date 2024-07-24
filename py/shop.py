import tkinter as tk
from tkinter import messagebox, simpledialog
import pymysql


db = pymysql.connect(host='127.0.0.1', user='root', password='1234', database='finalExam')
cursor = db.cursor()

def customer_signup():
    signup_window = tk.Toplevel(root)
    signup_window.title("고객 회원가입")

    user_login_id_label = tk.Label(signup_window, text="아이디:")
    user_login_id_entry = tk.Entry(signup_window)
    pass_w_label = tk.Label(signup_window, text="비밀번호:")
    pass_w_entry = tk.Entry(signup_window, show="*")
    name_label = tk.Label(signup_window, text="이름:")
    name_entry = tk.Entry(signup_window)
    email_label = tk.Label(signup_window, text="이메일:")
    email_entry = tk.Entry(signup_window)
    phone_label = tk.Label(signup_window, text="전화번호:")
    phone_entry = tk.Entry(signup_window)
    address_label = tk.Label(signup_window, text="주소:")
    address_entry = tk.Entry(signup_window)

    signup_button = tk.Button(signup_window, text="회원가입", command=lambda: insert_customer(db, cursor, user_login_id_entry.get(), pass_w_entry.get(), name_entry.get(), email_entry.get(), phone_entry.get(), address_entry.get(), signup_window))

    user_login_id_label.pack()
    user_login_id_entry.pack()
    pass_w_label.pack()
    pass_w_entry.pack()
    name_label.pack()
    name_entry.pack()
    email_label.pack()
    email_entry.pack()
    phone_label.pack()
    phone_entry.pack()
    address_label.pack()
    address_entry.pack()
    signup_button.pack()

def insert_customer(db, cursor, user_login_id, pass_w, name, email, phone, address, window):
    cursor.execute("""
        INSERT INTO customers (user_Login_id, pass_W, name, email, phone, address, total_purchase_amount, total_mileage, entryD)
        VALUES (%s, %s, %s, %s, %s, %s, 0, 0, NOW())
    """, (user_login_id, pass_w, name, email, phone, address))

    db.commit()
    messagebox.showinfo("회원가입 성공", "회원가입이 성공적으로 완료되었습니다.")
    window.destroy()
    
def store_owner_signup():
    signup_window = tk.Toplevel(root)
    signup_window.title("점주 회원가입")

    name_label = tk.Label(signup_window, text="상점 이름:")
    name_entry = tk.Entry(signup_window)
    contact_number_label = tk.Label(signup_window, text="연락처:")
    contact_number_entry = tk.Entry(signup_window)

    signup_button = tk.Button(signup_window, text="회원가입", command=lambda: insert_shopping_mall(db, cursor, name_entry.get(), contact_number_entry.get(), signup_window))

    name_label.pack()
    name_entry.pack()
    contact_number_label.pack()
    contact_number_entry.pack()
    signup_button.pack()

def insert_shopping_mall(db, cursor, name, contact_number, window):
    cursor.execute("""
        INSERT INTO shopping_malls (name, entry_date, contact_number, accumulated_platform_fee)
        VALUES (%s, NOW(), %s, 0)
    """, (name, contact_number))

    db.commit()
    messagebox.showinfo("회원가입 성공", "회원가입이 성공적으로 완료되었습니다.")
    window.destroy()


def check_login(db, cursor, username, password, window):
    cursor.execute("""
        SELECT * FROM shopping_malls WHERE name = %s AND RIGHT(contact_number, 4) = %s
    """, (username, password))

    result = cursor.fetchone()

    if result:
        messagebox.showinfo("로그인 성공", "로그인이 성공적으로 완료되었습니다.")
        window.destroy()
    else:
        messagebox.showerror("로그인 실패", "상점 이름 혹은 비밀번호가 잘못되었습니다.")
def login():
    entered_username = username_entry.get()
    entered_password = password_entry.get()
    
    if entered_username.lower() == 'root' and entered_password == 'admin':
        admin_window = tk.Toplevel(root)
        admin_window.title("플랫폼 전체 관리 화면")
        admin_window.geometry("800x600")
        show_admin_page(admin_window)
    else:
        cursor.execute("SELECT * FROM customers WHERE user_login_id=%s AND pass_w=%s", (entered_username, entered_password))
        customer = cursor.fetchone()

        if customer:
            customer_window = tk.Toplevel(root)
            customer_window.title("고객 화면")
            customer_window.geometry("800x600")
            show_customer_page(db, cursor, customer_window, customer)
        elif cursor.execute("SELECT * FROM shopping_malls WHERE name=%s AND RIGHT(contact_number, 4)=%s", (entered_username, entered_password)):
            store_owner = cursor.fetchone()
            
            if store_owner:
                    store_owner_dashboard(db, cursor, root, store_owner)
            else:
                    messagebox.showerror("로그인 실패", "아이디 또는 비밀번호가 올바르지 않습니다.")
        else:
            messagebox.showerror("로그인 실패", "아이디 또는 비밀번호가 올바르지 않습니다.")

def update_total_price(cart_listbox, total_price_label):
    total_price = 0
    for item in cart_listbox.get(0, tk.END):
        price = float(item[2])
        total_price += price
    total_price_label.config(text=f"총 금액: {total_price}")



def remove_from_cart(cart_listbox, total_price_label):
    selected_product_index = cart_listbox.curselection()

    if not selected_product_index:
        messagebox.showwarning("물품 제거", "장바구니에서 제거할 물품을 선택하세요.")
        return

    cart_listbox.delete(selected_product_index)
    update_total_price(cart_listbox, total_price_label)



def show_customer_page(db, cursor, customer_window, customer):
    
    cursor.execute("SELECT * FROM shopping_malls")
    malls = cursor.fetchall()

    customer_window.geometry("800x400")
    
    mall_listbox = tk.Listbox(customer_window)
    mall_listbox.pack(side=tk.LEFT, pady=10)
    for mall in malls:
        mall_listbox.insert(tk.END, mall[1])

    product_listbox = tk.Listbox(customer_window)
    product_listbox.pack(side=tk.LEFT, pady=10)

    cart_listbox = tk.Listbox(customer_window, width=50)
    cart_listbox.pack(side=tk.LEFT, pady=10)

    button_frame = tk.Frame(customer_window)
    button_frame.pack(side=tk.RIGHT, fill=tk.X, padx=10)

    select_mall_button = tk.Button(button_frame, text="가게 선택", command=lambda: show_products(cursor, malls, mall_listbox, product_listbox,customer_window))
    select_mall_button.pack(fill=tk.Y, expand=True, pady=10)

    select_product_button = tk.Button(button_frame, text="물품 선택", command=lambda: add_to_cart(mall_listbox, product_listbox, cart_listbox, total_price_label,customer_window))
    select_product_button.pack(fill=tk.Y, expand=True, pady=10)

    remove_product_button = tk.Button(button_frame, text="물품 제거", command=lambda: remove_from_cart(cart_listbox, total_price_label))
    remove_product_button.pack(fill=tk.Y, expand=True, pady=10)

    purchase_button = tk.Button(button_frame, text="구매", command=lambda: purchase(db, cursor, customer, cart_listbox,customer_window,total_price_label))
    purchase_button.pack(fill=tk.Y, expand=True, pady=10)

    myInfo_button = tk.Button(button_frame, text="내 정보", command=lambda: my_info(db, customer, customer_window))
    myInfo_button.pack(fill=tk.Y, expand=True, pady=10)

    logout_button = tk.Button(button_frame, text="로그아웃", command=customer_window.destroy)
    logout_button.pack(fill=tk.Y, expand=True, pady=10)

    total_price_label = tk.Label(customer_window, text="총 금액: 0")
    total_price_label.pack(side=tk.BOTTOM)

selected_product = None
selected_mall = None

def my_info(db, customer, customer_window):
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("CALL GetMonthlyInfo(%s)", [customer[1]])
        monthly_purchase_info = cursor.fetchall()
        cursor.nextset()
        order_history_info = cursor.fetchall()
        cursor.nextset()
        mileage_info = cursor.fetchall()

    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM customers WHERE id = %s", [customer[0]])
        customer_info = cursor.fetchone()

    info_window = tk.Toplevel(customer_window)
    info_window.title("내 정보")

    name_label = tk.Label(info_window, text=f"이름: {customer_info['name']}")
    name_label.pack()

    address_label = tk.Label(info_window, text=f"주소: {customer_info['address']}")
    address_label.pack()

    phone_label = tk.Label(info_window, text=f"휴대폰번호: {customer_info['phone']}")
    phone_label.pack()

    email_label = tk.Label(info_window, text=f"이메일: {customer_info['email']}")
    email_label.pack()

    join_date_label = tk.Label(info_window, text=f"가입일: {customer_info['entryD']}")
    join_date_label.pack()

    remaining_mileage = mileage_info[0]['remaining_mileage'] if mileage_info else 0

    mileage_label = tk.Label(info_window, text=f"마일리지: {remaining_mileage}")
    mileage_label.pack()

    order_history_label = tk.Label(info_window, text="주문 기록:")
    order_history_label.pack()

    order_history_text = tk.Text(info_window,width=100)
    order_history_text.pack()

    for order in order_history_info:
        order_history_text.insert(tk.END, f"주문 ID: {order['order_id']}, 제품 이름: {order['product_name']}, 쇼핑몰 이름: {order['mall_name']}, 주문 날짜: {order['order_date']}, 주문 금액: {order['order_amount']}\n\n")



def show_products(cursor, malls, mall_listbox, product_listbox,customer_window):
    global selected_mall
    selected_mall_index = mall_listbox.curselection()

    if not selected_mall_index:
        messagebox.showwarning("가게 선택", "가게를 먼저 선택하세요.")
        customer_window.lift()
        return
    
    selected_mall = malls[selected_mall_index[0]]
    cursor.execute("SELECT * FROM products WHERE mall_id=%s", (selected_mall[0],))

    products = cursor.fetchall()
    product_listbox.delete(0, tk.END)
    
    for product in products:
        product_listbox.insert(tk.END, (product[0], product[1], product[2]))  

def add_to_cart(mall_listbox, product_listbox, cart_listbox, total_price_label, customer_window):
    global selected_product, selected_mall
    selected_product_index = product_listbox.curselection()

    if not selected_mall or not selected_product_index:
        messagebox.showwarning("물품 선택", "가게와 물품을 먼저 선택하세요.")
        customer_window.lift()
        return

    selected_product = product_listbox.get(selected_product_index[0])
    cart_listbox.insert(tk.END, (selected_product[0], f"{selected_mall[1]} - {selected_product[1]}", selected_product[2])) 
    update_total_price(cart_listbox, total_price_label)

def purchase(db, cursor, customer, cart_listbox, customer_window,total_price_label):
    items_in_cart = cart_listbox.get(0, tk.END)

    if not items_in_cart:
        messagebox.showwarning("장바구니", "장바구니에 아무것도 없습니다.")
        customer_window.lift()
        return

    for item in items_in_cart:
        product_id = item[0]
        cursor.execute("SELECT price FROM products WHERE id = %s", (product_id,))
        price = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO orders (product_id, customer_id, order_date, order_amount)
            VALUES (%s, %s, NOW(), %s)
        """, (product_id, customer[0], price))

    messagebox.showinfo("구매 성공", "구매가 성공적으로 처리되었습니다.")
    customer_window.lift()
    db.commit()
    cart_listbox.delete(0, tk.END)
    update_total_price(cart_listbox, total_price_label)  


def show_admin_page(admin_window):
    db = pymysql.connect(host='127.0.0.1', user='root', password='kjh1549', database='finalExam')
    cursor = db.cursor()

    cursor.execute("SELECT * FROM shopping_malls")
    malls = cursor.fetchall()

    mall_listbox = tk.Listbox(admin_window)
    mall_listbox.pack(pady=10)
    for mall in malls:
        mall_listbox.insert(tk.END, mall[1])

    selected_mall_info_label = tk.Label(admin_window, text="")
    selected_mall_info_label.pack(pady=10)

    select_mall_button = tk.Button(admin_window, text="가게 선택", command=lambda: show_selected_mall_info(cursor, malls, mall_listbox, selected_mall_info_label))
    select_mall_button.pack(pady=10)

    delete_mall_button = tk.Button(admin_window, text="가게 삭제", command=lambda: delete_mall(db, cursor, malls, mall_listbox))
    delete_mall_button.pack(pady=10)

    logout_button = tk.Button(admin_window, text="로그아웃", command=admin_window.destroy)
    logout_button.pack(pady=10)
    
def delete_mall(db, cursor, malls, mall_listbox):
    selected_mall_index = mall_listbox.curselection()

    if not selected_mall_index:
        messagebox.showwarning("가게 선택", "가게를 먼저 선택하세요.")
        return

    selected_mall = malls[selected_mall_index[0]]

    cursor.execute(f"SELECT id FROM products WHERE mall_id = {selected_mall[0]}")
    product_ids = [item[0] for item in cursor.fetchall()]

    for product_id in product_ids:
        cursor.execute(f"SELECT id FROM orders WHERE product_id = {product_id}")
        order_ids = [item[0] for item in cursor.fetchall()]

        for order_id in order_ids:
            cursor.execute(f"DELETE FROM order_history WHERE order_id = {order_id}")

        cursor.execute(f"DELETE FROM orders WHERE product_id = {product_id}")
    cursor.execute(f"DELETE FROM products WHERE mall_id = {selected_mall[0]}")
    cursor.execute(f"DELETE FROM shopping_malls WHERE id = {selected_mall[0]}")
    db.commit()
    mall_listbox.delete(selected_mall_index)


    
   
def show_selected_mall_info(cursor, malls, mall_listbox, selected_mall_info_label):
    selected_mall_index = mall_listbox.curselection()

    if not selected_mall_index:
        messagebox.showwarning("가게 선택", "가게를 먼저 선택하세요.")
        return

    selected_mall = malls[selected_mall_index[0]]
    cursor.execute("CALL CalculatePlatformFee(NULL)") 
    results = cursor.fetchall()

    total_sales = 0.0
    platform_fee = 0.0
    for result in results:
        if result[0] == selected_mall[0]:
            total_sales = float(result[6])
            platform_fee = float(result[7])
            break

    cursor.execute("CALL CalculateSalesAndProfitsByMall('%s')" % selected_mall[1])

    while True:
        sales_results = cursor.fetchall()
        
        for result in sales_results:
            if result[0] == selected_mall[0] and result[1] == 2023:
                yearly_sales_2023 = float(result[2])
                break
        
        if cursor.nextset() is None:
            break

    yearly_sales_2023 += platform_fee

    selected_mall_info = f"""
    가게명: {selected_mall[1]}
    입점날: {selected_mall[2]}
    전화번호: {selected_mall[3]}
    누적 플랫폼 사용료: {selected_mall[4]}
    총 매출 액 : {total_sales}
    올해 매출 액 : {yearly_sales_2023}
    2023년 플랫폼 사용료: {platform_fee}
    """
    selected_mall_info_label.config(text=selected_mall_info)

def add_product(db, cursor, store_owner,dashboard_window,products_list):
    product_name = simpledialog.askstring("상품 추가", "상품 이름을 입력해주세요:")
    product_price = simpledialog.askstring("상품 추가", "상품 가격을 입력해주세요:")
    mall_id = store_owner[0]
    cursor.execute("INSERT INTO products (name, price, mall_id) VALUES (%s, %s, %s)", (product_name, product_price, mall_id))
    db.commit()

    messagebox.showinfo("상품 추가", "상품이 성공적으로 추가되었습니다.")
    products_list.delete(0, tk.END)
    cursor.execute("SELECT id, name, price FROM products WHERE mall_id=%s", (store_owner[0],))
    for product in cursor.fetchall():
        products_list.insert(tk.END, f"ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]}")
    dashboard_window.lift()
    
def remove_product(db, cursor, store_owner, products_list):
    product_id = simpledialog.askstring("상품 삭제", "삭제할 상품의 ID를 입력해주세요:")
    cursor.execute("SELECT id FROM orders WHERE product_id=%s", (product_id,))
    order_ids = cursor.fetchall()
    for order_id in order_ids:
        cursor.execute("DELETE FROM order_history WHERE order_id=%s", (order_id[0],))
    cursor.execute("DELETE FROM orders WHERE product_id=%s", (product_id,))
    cursor.execute("DELETE FROM products WHERE id=%s AND mall_id=%s", (product_id, store_owner[0]))
    db.commit()
    products_list.delete(0, tk.END)
    cursor.execute("SELECT id, name, price FROM products WHERE mall_id=%s", (store_owner[0],))
    for product in cursor.fetchall():
        products_list.insert(tk.END, f"ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]}")

    messagebox.showinfo("상품 삭제", "상품이 성공적으로 삭제되었습니다.")


def store_owner_dashboard(db, cursor, window, store_owner):
    dashboard_window = tk.Toplevel(window)
    dashboard_window.title("점주 대시보드")
    products_label = tk.Label(dashboard_window, text="상품 목록:",width=50)
    products_list = tk.Listbox(dashboard_window,width=40)

    sales_label = tk.Label(dashboard_window, text="현재 매출:")
    cursor.execute("SELECT SUM(order_amount) FROM orders WHERE product_id IN (SELECT id FROM products WHERE mall_id=%s)", (store_owner[0],))  
    sales = cursor.fetchone()[0]
    sales_value_label = tk.Label(dashboard_window, text=str(sales))

    cursor.execute("CALL CalculatePlatformFee(NULL)")
    results = cursor.fetchall()

    platform_fee = 0.0
    for result in results:
        if result[0] == store_owner[0]:
            platform_fee = float(result[7])
            break

    if platform_fee != 0.0:
        fee_label = tk.Label(dashboard_window, text=f"2023년 플랫폼 사용료: {platform_fee}")
    else:
        fee_label = tk.Label(dashboard_window, text="2023년 플랫폼 사용료 데이터가 없습니다.")
    fee_label.pack()

    cursor.execute("SELECT accumulated_platform_fee FROM shopping_malls WHERE id=%s", (store_owner[0],)) 
    fee = cursor.fetchone()[0]
    fee_value_label = tk.Label(dashboard_window, text=f"누적 플랫폼 사용료: {fee}")

    add_product_button = tk.Button(dashboard_window, text="상품 추가", command=lambda: add_product(db, cursor, store_owner, dashboard_window, products_list))
    products_list.delete(0, tk.END)
    cursor.execute("SELECT id, name, price FROM products WHERE mall_id=%s", (store_owner[0],))
    for product in cursor.fetchall():
        products_list.insert(tk.END, f"ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]}")
    remove_product_button = tk.Button(dashboard_window, text="상품 제거", command=lambda: [remove_product(db, cursor, store_owner, products_list), dashboard_window.lift()])
    logout_button = tk.Button(dashboard_window, text="로그아웃", command=dashboard_window.destroy)
    logout_button.pack(pady=10)

    products_label.pack()
    products_list.pack()
    sales_label.pack()
    sales_value_label.pack()
    fee_label.pack()
    fee_value_label.pack()
    add_product_button.pack()
    remove_product_button.pack()
    
root = tk.Tk()
root.title("로그인 화면")
root.geometry("400x500")

username_label = tk.Label(root, text="아이디:")
username_label.pack(pady=10)
username_entry = tk.Entry(root)
username_entry.pack(pady=10)

password_label = tk.Label(root, text="비밀번호:")
password_label.pack(pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=10)

login_button = tk.Button(root, text="로그인", command=login)
login_button.pack(pady=20)
customer_signup_button = tk.Button(root, text="고객 회원가입", command=customer_signup)
store_owner_signup_button = tk.Button(root, text="점주 회원가입", command=store_owner_signup)

customer_signup_button.pack(pady=10)
store_owner_signup_button.pack(pady=10)

root.bind('<Return>', lambda event: login())
root.mainloop()
