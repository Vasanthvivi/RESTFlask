from app import app
from flask import request, jsonify
from config import sql


# homepage
@app.route("/")
def home():
    return "welcome to home"


# getting the quiz question as post
@app.route("/create-quiz", methods=["POST"])
def createQuiz():
    question = request.json["question"]
    choices = request.json["choices"]
    if not len(question) > 0 and not len(choices) > 0 and request.method is not "POST":
        response = jsonify({"message": "invalid data"})
        response.status_code = 400
        return response
    sqlobj = sql.connect()
    cursor = sqlobj.cursor()
    # insert into the database
    query = "INSERT INTO quiztable(question, choices) values(\"{0}\", \"{1}\")".format(question, choices)
    cursor.execute(query)
    insertedId = cursor.lastrowid
    sqlobj.commit()
    cursor.close()
    sqlobj.close()
    responseData = {"Id": insertedId, "question": question, "choices": choices}
    res = jsonify(responseData)
    res.status_code = 201
    return res


# getting the specified id of the question
@app.route("/get-quiz/<int:id>", methods=["GET"])
def getQuiz(id):
    if id is None:
        return jsonify({"messsage": "invalid id"})
    print(f"getting the quiz of id {id}")
    sqlobj = sql.connect()
    cursor = sqlobj.cursor()
    cursor.execute(f"select * from quiztable where id = {id}")
    quiz = cursor.fetchone()
    if not quiz:
        return jsonify({"message": "No Quizzes in the id"})
    id = quiz[0]
    question = quiz[1]
    choices = quiz[2]
    response = [{"id": id, "question": question, "choices": choices}]
    responseData = jsonify(response)
    responseData.status_code = 200
    return responseData


# getting all the quizzes
@app.route("/get-quizzes", methods = ["GET"])
def getAllQuizzes():
    sqlobj = sql.connect()
    cursor = sqlobj.cursor()
    # getting all the quizzes
    cursor.execute("select * from quiztable")
    dbData = cursor.fetchall()
    quizzes = []
    if dbData is not None:
        for quiz in dbData:
            id, question, choices = quiz
            data = { "id":id, "question":question, "choices":choices }
            quizzes.append(data)
    print(quizzes)
    cursor.close()
    sqlobj.close()
    response = jsonify(quizzes)
    response.status_code = 200
    return response


# delete the quiz from the database
@app.route("/delete-quiz/<int:id>", methods = ["DELETE"])
def deleteQuiz(id):
    if id is None:
        return jsonify({ "message":"Invalid id" })
    sqlobj = sql.connect()
    cursor = sqlobj.cursor()
    query = "delete from quiztable where id = %s"
    deletedRowsCount = cursor.execute(query, id)
    sqlobj.commit()
    cursor.close()
    sqlobj.close()
    if deletedRowsCount == 1:
        response = jsonify({ "message":f"The Quiz of id {id} is removed!" })
        response.status_code = 201
        return response
    else:
        response = jsonify({ "message":"quiz is not present or not deleted" })
        response.status_code = 400
        return response


# updating quiz
@app.route("/update-quiz/<int:id>", methods = ["POST"])
def updateQuiz(id):
    try:
        question = request.json["question"]
        choices = request.json["choices"]
    except:
        response = jsonify({"message": "invalid data"})
        response.status_code = 400
        return response
    sqlobj = sql.connect()
    cursor = sqlobj.cursor()
    query = "update quiztable set question = \"{0}\", choices = \"{1}\" where id = {2}".format(question, choices, id)
    rowsAffectedCount = cursor.execute(query)
    sqlobj.commit()
    cursor.close()
    sqlobj.close()
    if rowsAffectedCount == 1:
        response = jsonify({ "message":f"updated id {id} successfully!" })
        response.status_code = 201
        return response
    else:
        response = jsonify({ "message":f"Id {id} not updated" })
        response.status_code = 404
        return response


# getting the total quizzes
@app.route("/total-quizzes", methods = ["GET"])
def getTotalQuizzes():
    sqlobj = sql.connect()
    cursor = sqlobj.cursor()
    try:
        query = "select count(id) from quiztable"
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        response = jsonify({ "data":data[0] })
        response.status_code = 200
        return response
    except:
        print("got some error")
        return jsonify({ "message":"got some error" })
    finally:
        cursor.close()
        sqlobj.close()


if __name__ == '__main__':
    app.run()

