SELECT * FROM public.orders
ORDER BY id desc 


SELECT user_id, COUNT(*) AS num_orders
FROM public.orders
GROUP BY user_id;

