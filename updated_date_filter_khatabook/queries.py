from connection import DB_Connection

class Queries:
    
    # To fetch the name from customer table
    def get_all_customers(shopkeeper_id):
        query = """
            SELECT CONCAT(first_name, ' ', last_name) AS full_name
            FROM customer
            WHERE shopkeeper_id = {}
        """
        query=query.format(shopkeeper_id)
        db = DB_Connection()
        return db.execute_query(query)

    # To fetch transaction details from transaction table
    def get_all_transactions(shopkeeper_id):
        query = """
            SELECT 
                customer_id, date, you_give, you_got
            FROM transactions
            WHERE shopkeeper_id = {}
        """
        query=query.format(shopkeeper_id)
        db = DB_Connection()
        return db.execute_query(query)

    
    def get_customer_name(customer_id):
        query = """
            SELECT CONCAT(first_name, ' ', last_name)
            FROM customer
            WHERE customer_id = {}
        """
        query=query.format(customer_id)
        db = DB_Connection()
        result = db.execute_query(query)
        return result[0][0] if result else None

    # Filter transactions
    def filter_transactions(shopkeeper_id, from_date, till_date, customer_name):
        query = f"""
            SELECT 
                customer_id, date, you_give, you_got
            FROM transactions
            WHERE shopkeeper_id = {shopkeeper_id}
        """

        if from_date:
            query += f" AND date >= '{from_date}'"
        if till_date:
            query += f" AND date <= '{till_date}'"
        if customer_name:
            query += f" AND customer_id IN (SELECT customer_id FROM customer WHERE CONCAT(first_name, ' ', last_name) LIKE '%{customer_name}%')"
        db = DB_Connection()
        return db.execute_query(query)
