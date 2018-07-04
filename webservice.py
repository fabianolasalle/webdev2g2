from flask import Flask, jsonify, abort, request
import pymysql, random

from classes.Database import Database

app = Flask(__name__)

@app.route('/api/alunos', methods=['GET'])
def index():
    try:
        with Database.getConn().cursor() as cursor:
            sql = "SELECT nome, email, endereco, matricula FROM aluno"
            cursor.execute(sql)
            result = cursor.fetchall()
            return_data = []
            for aluno in result:
                from classes.Aluno import Aluno
                return_data.append(Aluno(aluno).__dict__)
            return jsonify(return_data)
    finally:
        Database.closeConn()

@app.route('/api/alunos/<int:matricula>', methods=['GET'])
def get_aluno(matricula):
    try:
        if matricula is None:
            abort(404)
        with Database.getConn().cursor() as cursor:
            sql = "SELECT nome, email, endereco, cpf, matricula, telefone FROM aluno WHERE matricula  = %s"
            cursor.execute(sql, (matricula))
            result = cursor.fetchone()
            from classes.Aluno import Aluno
            return jsonify(Aluno(result).__dict__)
    finally:
        Database.closeConn()


@app.route('/api/alunos', methods=['POST'])
def post_aluno():
    try:
        if not request.json:
            abort(400)
        request_data = (request.json['nome'], request.json['email'], request.json['endereco'])
        from classes.Aluno import Aluno
        aluno = Aluno(request_data)
        matricula = random.randint(100, 2000)
        return_data = {"success": False}
        with Database.getConn().cursor() as cursor:
            sql = "INSERT INTO aluno (nome, email, endereco, matricula) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (aluno.name, aluno.email, aluno.endereco, matricula))
            Database.getConn().commit()
            aluno.matricula = matricula
            return_data['success'] = True
            return_data['aluno'] = aluno.__dict__
        return jsonify(return_data)
    finally:
        Database.closeConn()

@app.route('/api/aluno/delete', methods=['POST'])
def delete_aluno():
    try:
        if request.form['matricula'] is None:
            abort(404)
        return_data = {"success": False}
        with Database.getConn().cursor() as cursor:
            sql = "DELETE FROM aluno WHERE matricula = %s"
            cursor.execute(sql, (request.form['matricula']))
            Database.getConn().commit()
            return_data['success'] = True
        return jsonify(return_data)
    finally:
        Database.closeConn()

if __name__ == '__main__':
    app.run(debug=True)
