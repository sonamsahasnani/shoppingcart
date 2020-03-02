import pandas as pd
import psycopg2
conn = psycopg2.connect(database = "testdb", user = "postgres", host = "127.0.0.1", port = "5432")
print ("Opened database successfully")

class Shopping():  # shopping
    def __init__(self,id,role):
        self.user = id
        self.user_type = role
        
    def __call__(self):
        argument=int(input("Enter valid argument: "))
        if self.user_type=='admin':
           self.admin_functions(argument)
        else:
            self.customer_functions(argument)
    
   def admin_functions(self,argument):
     try:
        if argument==1:
            self.list_product()
        if argument==2:
            self.add_product()
        if argument==3:
            self.delete_product()
        if argument==4:
            self.view_orders()
     except:
        print("input value did not matched..Please enter valid input")
    
    def customer_functions(self,argument):
      try:
        if argument==1:
            self.list_product()
        if argument==2:
            self.add_items_to_cart()
        if argument==3:
            self.view_order_history()
        except:
            print("input value did not matched..Please enter valid input")

   
    def view_orders(self):
        cursor = conn.cursor()
        sql = "select * from order_history"
        cursor.execute(sql)
        results=cursor.fetchall()
        df = pd.DataFrame(results)
        print(df)
     
    
    def list_product(self):
        cursor = conn.cursor()
        sql = "select * from product"
        cursor.execute(sql)
        results=cursor.fetchall()
        df = pd.DataFrame(results)
        print(df)
       

    def add_product(self):
        print("enter product details:")
        id=int(input("enter product id: "))
        name=input("enter product name: ")
        price=float(input("enter product price: "))
        cursor = conn.cursor()
        sql="insert into product values(%s,'%s',%s)"%(id,name,price)
        cursor.execute(sql)
        conn.commit()
        print("product with product id {} inserted in the product table".format(id))

    def delete_product(self):
        cursor = conn.cursor()
        id=int(input("enter product id: "))
        sql="Delete from product where id=%s" %id
        cursor.execute(sql)
        print("item is deleted")

    def add_items_to_cart(self):
        cursor = conn.cursor()
        input_string = input("Enter the product ids you want to add in the cart : ")
        cartitems = input_string.split(',')
        print("cart list is ", cartitems)
        sql="Select sum(list_price) from product where id in (%s)" % ",".join(map(str,cartitems))
        cursor.execute(sql)
        result=cursor.fetchone()[0]
        print("total value of the cart Items are: {}".format(result))
        a=input("if you want delete any product from your cart  enter y and if not enter n and check them out: ")
        if a=='y':
            id=int(input("Enter product id: "))
            cartitems.remove('id')
            print(cartitems)
        else:
            sql="Select sum(list_price) from product where id in (%s)" % ",".join(map(str,cartitems))
            cursor.execute(sql)
            result=cursor.fetchone()[0]
            print("total value of the cart Items are: {}".format(result))
            for i in cartitems:
                sql="Select list_price from product where id=%s" %i
                cursor.execute(sql)
                price=cursor.fetchone()[0]
                self.add_order(i,price)


    def view_order_history(self):    
        cursor = conn.cursor()
        sql="Select * from order_history where c_id=%s"%self.user
        results=cursor.fetchall()
        df = pd.DataFrame(results)
        print(df)

    def add_order(self,product_id,price):
        cursor = conn.cursor()
        sql="Insert into order_history (p_id,c_id,price) values(%s,%s,%s) RETURNING id;"
        cursor.execute(sql,(product_id,self.user,price,))
        results=cursor.fetchall()
        conn.commit()

if __name__ == '__main__':
    try:
        print("Enter username and password")
        user=input("Enter username: ")
        password=input("Enter password: ")
        cursor = conn.cursor()
        sql = "select id,role from user_account where username='%s' and password='%s'" % (user,password)
        cursor.execute(sql)
        result=cursor.fetchone()
        id=result[0]
        role = result[1]
        if role=='admin':
            print("\n1.Enter 1 for view all products\n2.Enter 2 for adding products\n3.Enter 3 for deleting any product\n4.Enter 4 for view order reports")
        elif role=='customer':
            print("\n1.Enter 1 to browse all the products \n2.Enter 2 to add products into the cart\n3.Enter 3 to see the order history")
        Shopping(id=id,role=role).__call__()
    except:
        print("Please enter correct username and password")

conn.commit() 
conn.close()
