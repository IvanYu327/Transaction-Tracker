def create_user_table(username):
    create_table_query = f"""
        CREATE TABLE {username} (
        id INT PRIMARY KEY,
        date DATE NOT NULL,
        category VARCHAR(25),
        amount DOUBLE(10, 2) NOT NULL,
        payment_method VARCHAR(50) NOT NULL
        );
    """

    return create_table_query

def full_user_table(username):
    full_table_query = f"""
        SELECT *
        FROM {username};
    """

    return full_table_query

def insert(username,id,date,category,amount,payment_method):
    insert_query = f"""
        INSERT INTO {username}
        VALUES ({id}, {date}, {category},{amount}, {payment_method});
    """
    return insert_query

def get_max_ID(username):
    get_max_ID_query=f"""
        SELECT MAX(id)
        FROM {username}
    """
    return get_max_ID_query