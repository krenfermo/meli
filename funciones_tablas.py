from init_db import get_db_connection
import ast

import json
from psycopg2 import sql


def insert_orders_items(data, table_name):
    if not data:
        return
 
    conn=get_db_connection()
    cur = conn.cursor()
    
    #for item in data:
   
        

    # Extraer columnas de los diccionarios
    try:
        columns = data[0].keys()
        columns_str = ', '.join(columns)
        values_str = ', '.join(['%s'] * len(columns))

        insert_query = sql.SQL(
            f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"
        )
        
        
        # Preparar los valores
        values = [[record[col] for col in columns] for record in data]
    
        # Ejecutar la consulta de inserción
        cur.executemany(insert_query.as_string(conn), values)
        
    
        
               
        cur.execute("""  DELETE
                FROM orders_items s1
                USING orders_items s2
                WHERE s1.order_id = s2.order_id AND s1.id < s2.id;""")
        conn.commit() 
                
        #cur.close()
        #conn.close()
        
    except IndexError:
        #cur.close()
        #conn.close()
        return {}
    print("termina")
    
     


def insert_orders_datos(data, table_name):
    if not data:
        return
 
    conn=get_db_connection()
    cur = conn.cursor()
    #for item in data:

    

    # Extraer columnas de los diccionarios
    try:
        columns = data[0].keys()
        columns_str = ', '.join(columns)
        values_str = ', '.join(['%s'] * len(columns))

        insert_query = sql.SQL(
            f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"
        )
    
        
        # Preparar los valores
        values = [[record[col] for col in columns] for record in data]
        
        # Ejecutar la consulta de inserción
        cur.executemany(insert_query.as_string(conn), values)
        
    
        
        
        cur.execute("""  DELETE
            FROM orders_datos s1
            USING orders_datos s2
            WHERE s1.order_id = s2.order_id AND s1.id < s2.id;""")
        conn.commit() 
                
        #cur.close()
        #conn.close()
        
    except IndexError:
        #cur.close()
        #conn.close()
        return {}
    print("termina")
        
        


def llena_orders(user_id):
    try:
        conn=get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT json_data,user_id FROM public.orders where user_id='{}' ORDER BY id DESC".format(user_id))
        
        orders=cur.fetchall()
 
        
        orders_dat=[]
            
        for i in range (0,len(orders)):

            json_data=  ast.literal_eval(str(orders[i][0]))  

            payments=[]
            for item in json_data["payments"]:
                
                payments.append( {"total_paid_amount":item["total_paid_amount"], "date_approved": item["date_approved"],
                                    "order_id":item["order_id"]  } )
                
            order_items=[]

            for item in json_data["order_items"]:
                if item["item"]["seller_sku"] ==None:
                    seller_sku="N/A"
                else:
                    seller_sku=item["item"]["seller_sku"]
                    
                
                order_items.append( {"quantity":item["quantity"], "full_unit_price": item["unit_price"],"unit_price": item["unit_price"],
                                        "sale_fee":item["sale_fee"],"id":item["item"]["id"],"title":item["item"]["title"],
                                        "category_id":item["item"]["category_id"],"seller_sku":seller_sku  } )
                

                
                orders_dat.append({"payments": payments, "order_items":order_items, "date_created":json_data["date_created"],
                                "buyer_id": json_data["buyer"]["id"], "buyer_nickname": json_data["buyer"]["nickname"],
                                "paid_amount":json_data["paid_amount"],"shipping_id":json_data["shipping"]["id"]})

        
        datos_orders=[]
        orders_items=[]
        for item in orders_dat:
            
            datos_orders.append({"order_id":item["payments"][0]["order_id"],
                                "payments_total_paid_amount":item["payments"][0]["total_paid_amount"],
                                "payments_date_approved":item["payments"][0]["date_approved"],
                                "date_created":item["date_created"],
                                "buyer_id":item["buyer_id"],
                                "buyer_nickname":item["buyer_nickname"],
                                "paid_amount":item["paid_amount"],
                                "shipping_id":item["shipping_id"],
                            "user_id":user_id
                                })
        
            
            for orders in (item["order_items"]):
                
                orders_items.append({"order_id":item["payments"][0]["order_id"],
                            "quantity":orders["quantity"],
                            "full_unit_price" :orders["full_unit_price"],
                            "unit_price" :orders["unit_price"],
                            "sale_fee": orders["sale_fee"],
                            "item_id":orders["id"],
                            "title": orders["title"],
                            "category_id": orders["category_id"],
                            "seller_sku": orders["seller_sku"],
                            "user_id":user_id
                                })
        print("va itrems")
      
        insert_orders_items(orders_items,"orders_items")

 
        print("va orders_datos")
        insert_orders_datos(datos_orders,"orders_datos")


        cur.close()
        conn.close()

        return True
    
    except KeyError:
        pass
        
llena=llena_orders("1118811075")


 
        


