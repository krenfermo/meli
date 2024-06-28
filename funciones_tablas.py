from init_db import get_db_connection
import ast

def llena_orders(user_id):
    try:
        conn=get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT json_data FROM public.orders where user_id='{}'".format(user_id))
        
        orders=cur.fetchall()
 
        #for ord in orders:
        #    print(ord)
        #cur.execute('INSERT INTO tokens (user_id, json_data)'
        #            'VALUES (%s, %s)',
        #            (token["user_id"],
        #                '{}'.format(token))
        #            )

        conn.commit()

        cur.close()
        conn.close()

        return orders
    
    except KeyError:
        pass
        
        
        
        
orders=[]

 

for i in range (0,len(llena_orders("40137874"))):
 

    json_data=  ast.literal_eval(str(llena_orders("40137874")[i][0]))  

    
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
                    "paid_amount":json_data["paid_amount"],"shipping_id":json_data["shipping"]["id"]})
    


print(orders)