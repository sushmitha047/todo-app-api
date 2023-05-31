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
    group_name=data['group_name']
    if group_name == '':
        return make_response(jsonify({'message': 'Task group name cannot be empty'}))
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `task_groups` (`group_name`) VALUES (%s);"
            cursor.execute(sql, (group_name))
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
            cursor.execute(sql)
            result = cursor.fetchall()
            print("result: ", result)
            return make_response(jsonify(result), 200)
  except Exception as e:
    error_message = 'Error getting task groups: ' + str(e)
    print("Exception:", error_message)
    return make_response(jsonify({'message': error_message}), 500)
  
# get a task-group by id
@app.route('/task-groups/<int:id>', methods=['GET'])
def get_task_group(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `task_groups` WHERE `id` = %s;"
            cursor.execute(sql, (id))
            result = cursor.fetchall()
            print("result: ", result)
            return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = 'Error getting task group: ' + str(e)
        print("Exception:", error_message)
        return make_response(jsonify({'message': error_message}), 500)
    
# update a task-group
@app.route('/task-groups/<int:id>', methods=['PUT'])
def update_task_group(id):
    try:
        with connection.cursor() as cursor:
            data = request.get_json()
            group_name = data['group_name']
            sql = "UPDATE `task_groups` SET `group_name`=%s WHERE `id`=%s;"
            cursor.execute(sql, (group_name, id))
            connection.commit()
            return make_response(jsonify({'message': 'task group updated successfully'}), 200)
    except Exception as e:
        error_message = 'Error updating task group: ' + str(e)
        print("Exception: ", error_message)
        return make_response(jsonify({'message': error_message}), 500)


# delete a task-group
@app.route('/task-groups/<string:group_name>', methods=['DELETE'])
def delete_task_group(group_name):
    try:
        with connection.cursor() as cursor:
            # data =request.get_json()
            # group_name = data['group_name']
            sql = "DELETE from `task_groups` WHERE `group_name`=%s"
            cursor.execute(sql, (group_name))
            connection.commit()
            return make_response(jsonify({'message': 'task group deleted successfully'}), 200)
    except Exception as e:
        error_message = 'Error deleting task group: ' + str(e)
        print("Exception: ", error_message)
        return make_response(jsonify({'message': error_message}), 500)


if __name__ == '__main__':
    app.run(debug=True)