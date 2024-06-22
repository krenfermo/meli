from init_db import get_db_connection
import ast
import hashlib

def pass_md5(password):
           
    return hashlib.md5(password.encode()).hexdigest()


def getUser(email):
    try:               
 
        conn=get_db_connection()
        cur = conn.cursor()   
        
        cur.execute("SELECT * from users where email='{}' and login_type='Google' ".format(email))
        usuario=cur.fetchone()        

        cur.close()
        conn.close()
    except Exception as error:
        print("ERROR:", error)
        return False
    return usuario

    
    
def creaUser(json_data,login_type,email,display_name):
    try:                
 
        json_data=ast.literal_eval(str(json_data))
        print(type(json_data))
        conn=get_db_connection()
        cur = conn.cursor()
        
        
        
        cur.execute('INSERT INTO users (json_data,login_type,email,display_name)'
                'VALUES (%s, %s, %s, %s)',
                (str(json_data),login_type,email,display_name)
                )
    
        conn.commit()

        cur.close()
        conn.close()
    except Exception as error:
        print("ERROR:", error)
        return False
    return True
    
    

def get_orders(user_idML):
    try:                
 
        print("SELECT * from orders where user_id='{}'".format(user_idML))
              
        conn=get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * from orders where user_id='{}'".format(user_idML))
    
        #conn.commit()
        result=cur.fetchall()
        cur.close()
        conn.close()
        orders=[]

        for i in range (0,len(result)):
   
            json_data=  ast.literal_eval(str(result[i][2]))  
     
            
            payments=[]
            for item in json_data["payments"]:
                
                #print(item["total_paid_amount"] )
                #print(item["date_approved"] )
                #print(item["order_id"] )
                payments.append( {"total_paid_amount":item["total_paid_amount"], "date_approved": item["date_approved"],
                                  "order_id":item["order_id"]  } )
             
            order_items=[]
            for item in json_data["order_items"]:
                
                #print(item["quantity"])
                #print(item["full_unit_price"] )
                #print(item["sale_fee"] )
                #print(item["item"]["id"])
                #print(item["item"]["title"] )
                #print(item["item"]["category_id"] )
                #print(item["item"]["seller_sku"] )
                order_items.append( {"quantity":item["quantity"], "full_unit_price": item["full_unit_price"],
                                     "sale_fee":item["sale_fee"],"id":item["item"]["id"],"title":item["item"]["title"],
                                     "category_id":item["item"]["category_id"],"seller_sku":item["item"]["seller_sku"]   } )
             
            #print(json_data["date_created"])
            #print(json_data["buyer"]["id"])
            #print(json_data["buyer"]["nickname"])
            #print(json_data["paid_amount"])
            
            orders.append({"payments": payments, "order_items":order_items, "date_created":json_data["date_created"],
                           "buyer_id": json_data["buyer"]["id"], "buyer_nickname": json_data["buyer"]["nickname"],
                           "paid_amount":json_data["paid_amount"]})
        return orders
        #return result
    #2000005831648568
    #payments[] . reason.  total_paid_amount.  date_approved.  order_id.  
    #date_closed {}
    #order_items.[] item {}. id . title. category_id. seller_sku. 
    #order_items.{} quantity. full_unit_price. sale_fee . 
    #date_created
    #buyer{} id. nickname
    #paid_amount
    

    except Exception as error:
        print("ERROR:", error)
        return False
    return True
    


def post_user(kwargs):
    try:  

        query = "select * from users where email='{}' ".format(
            kwargs['username'])
        conn=get_db_connection()
        cur = conn.cursor()
        
        cur.execute(query )
        res=cur.fetchone()
        cur.close()
        conn.close()
        
        return res
    except Exception as err:
        print("error login",err)
       
        return err
        
       
def post_login(kwargs):
    try:  
    
        if kwargs['password']:
                    
            query = "select * from users where email='{}' and password='{}' and login_type='retool'".format(
                kwargs['username'],kwargs['password'])

            print(query)
            conn=get_db_connection()
            cur = conn.cursor()
            
            cur.execute(query )
            res=cur.fetchone()
            cur.close()
            conn.close()
        
            return res
        else:
            return False
        
    except Exception as err:
        print("error login",err)
     
        return err 
        