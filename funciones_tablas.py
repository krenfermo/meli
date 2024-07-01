from init_db import get_db_connection
import ast



def mete_order_items(order_items):
    
    conn=get_db_connection()
    cur = conn.cursor()

    # Iterar sobre los elementos del pedido y guardar cada uno en la base de datos
    for item in order_items['order_items']:
        item_data = item['item']
        quantity = item['quantity']
        unit_price = item['unit_price']
        full_unit_price = item['full_unit_price']
        currency_id = item['currency_id']
        sale_fee = item['sale_fee']
        listing_type_id = item['listing_type_id']
        element_id = item['element_id']

        # Ejemplo de consulta SQL para insertar los datos en una tabla llamada 'order_items'
        sql = """
        INSERT INTO order_items (item_id, title, category_id, quantity, unit_price, full_unit_price, currency_id, sale_fee, listing_type_id, element_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Ejecutar la consulta con los parámetros correspondientes
        cur.execute(sql, (
            item_data['id'],
            item_data['title'],
            item_data['category_id'],
            quantity,
            unit_price,
            full_unit_price,
            currency_id,
            sale_fee,
            listing_type_id,
            element_id
        ))

    # Confirmar la transacción y cerrar la conexión
    conn.commit()
    cur.close()
    conn.close()


def llena_orders(user_id):
    try:
        conn=get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT json_data FROM public.orders where user_id='{}' ORDER BY id DESC limit 2".format(user_id))
        
        orders=cur.fetchall()
 
 
        conn.commit()

        cur.close()
        conn.close()

        return orders
    
    except KeyError:
        pass
        
        
        
        
orders=[]

 
llena=llena_orders("1411430232")

for i in range (0,len(llena)):

    json_data=  ast.literal_eval(str(llena[i][0]))  

    payments=[]
    for item in json_data["payments"]:
        
        payments.append( {"total_paid_amount":item["total_paid_amount"], "date_approved": item["date_approved"],
                            "order_id":item["order_id"]  } )
        
    order_items=[]
    for item in json_data["order_items"]:
        
        order_items.append( {"quantity":item["quantity"], "full_unit_price": item["full_unit_price"],
                                "sale_fee":item["sale_fee"],"id":item["item"]["id"],"title":item["item"]["title"],
                                "category_id":item["item"]["category_id"],"seller_sku":item["item"]["seller_sku"]   } )
    
    orders.append({"payments": payments, "order_items":order_items, "date_created":json_data["date_created"],
                    "buyer_id": json_data["buyer"]["id"], "buyer_nickname": json_data["buyer"]["nickname"],
                    "paid_amount":json_data["paid_amount"],"shipping_id":json_data["shipping"]["id"]})
    
print(orders)



