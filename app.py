from flask import Flask, request, make_response, jsonify
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='12345#47',
                             db='app_test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


app = Flask(__name__)


# test route
@app.route('/test')
def test():
    return make_response(jsonify({'message': 'test'}), 200)


# create task groups
@app.route('/task-groups', methods=['POST'])
def task_groups():
    data = request.get_json()
    id=data['id']
    group_name=data['group_name']
    if group_name == '':
        return make_response(jsonify({'message': 'Task group name cannot be empty'}))
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `task_groups` (`id`,`group_name`) VALUES (%s, %s);"
            print(sql)
            cursor.execute(sql, (id, group_name))
            connection.commit()
            return make_response(jsonify({'message': 'task group created'}), 200)
    except Exception as e:
        error_message = 'Error creating task group: ' + str(e)
        print("Exception:", error_message)
        return make_response(jsonify({'message': error_message}), 500)


# get all task-groups
@app.route('/task-groups', methods=['GET'])
def get_task_groups():
  try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `task_groups`;"
            cols = ['id', 'group_name']
            cursor.execute(sql)
            result = cursor.fetchall()
            print("result: ", result)
            return make_response(jsonify(result), 200)
  except Exception as e:
    error_message = 'Error getting task groups: ' + str(e)
    print("Exception:", error_message)
    return make_response(jsonify({'message': error_message}), 500)
  


if __name__ == '__main__':
    app.run(debug=True)