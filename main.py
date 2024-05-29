from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Configuração do banco de dados
db_connect = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'new_schema'
}

def get_db_connection():
    connect = mysql.connector.connect(**db_connect)
    return connect

@app.route('/livros', methods=['GET'])
def get_livros():
    search = request.args.get('q')
    print(search)
    connect = get_db_connection()
    cursor = connect.cursor(dictionary=True)

    if search == "all":
        cursor.execute("SELECT * FROM livros")
    elif search:
        query = "SELECT * FROM livros WHERE Nome LIKE %s OR autor LIKE %s"
        like_term = f"%{search}%"
        cursor.execute(query, (like_term, like_term))

    sql_return = cursor.fetchall()

    if sql_return:
        livros = jsonify(sql_return)
    else:
        livros = "API found no records"
    
    cursor.close()
    connect.close()
    return livros

if __name__ == '__main__':
    app.run()
