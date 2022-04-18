from configuration import sql
from application import application
from flask import request, jsonify


# initialize application
@application.route("/")
def homepage():
    return "welcome to the home"


# creating new quiz
@application.route("/create-quiz", methods=["POST"])
def createQuiz():
    try:
        question = request.json["question"]
        choices = request.json["choices"]
    except Exception as e:
        print(e)
        response = jsonify({"message": "Invalid data"})
        response.status_code = 400
        return response
    if len(question) > 0 and len(choices) > 0 and request.method == "POST":
        sqlobj = sql.connect()
        cursor = sqlobj.cursor()
        try:
            query = f"insert into quiztable(question, choices) values(\"{question}\", \"{choices}\")"
            rowsAffected = cursor.execute(query)
            insertedId = cursor.lastrowid
            sqlobj.commit()
            if rowsAffected == 1:
                response = jsonify({"id": insertedId, "question": question, "choices": choices})
                response.status_code = 201
                return response
        except:
            print("error")
            return jsonify({"message": "some error occured while inserting data "})
        finally:
            cursor.close()
            sqlobj.close()
    else:
        response = jsonify({"message": "Invalid request"})
        response.status_code = 401
        return response


# getting all data
@application.route("/get-all-data", methods = ["GET"])
def retrieveDatas():
    sqlobj = sql.connect()
    cursor = sqlobj.cursor()
    try:
        rowCount = cursor.execute("select * from quiztable")
        datas = cursor.fetchall()
        data = []
        if len(datas) > 0:
            for d in datas:
                v = { "id":d[0], "question": d[1], "choices": d[2] }
                data.append(v)
        print(data)
        response = jsonify( data )
        response.status_code = 201
        return response
    except Exception as e:
        print(e)
        response = jsonify({ "message":"got some error" })
        response.status_code = 400
        return response
    finally:
        cursor.close()
        sqlobj.close()

# run the application
if __name__ == "__main__":
    application.run()
