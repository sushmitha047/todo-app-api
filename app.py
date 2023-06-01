from flask import Flask, request, make_response, jsonify
import pymysql.cursors
import datetime



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
def create_task_groups():
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

# create tasks
@app.route('/task-groups/<int:task_groupid>/tasks', methods=['POST'])
def create_tasks(task_groupid):
    data = request.get_json()
    task_name = data['task_name']
    description = data['description']
    due_date = data['due_date']
    status = 'added'

    if task_name == '' and due_date == '':
        return make_response(jsonify({'message': 'Task name and due date cannot be empty'}))

    due_date_datetime = datetime.datetime.strptime(due_date, '%Y/%m/%d').date()
    current_date = datetime.datetime.now().date()

    # print(current_date)

    if due_date_datetime < current_date:
        return make_response(jsonify({'message': 'Due date must be in the future'}), 400)
    
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `tasks` (`task_name`, `description`, `due_date`, `status`, `task_groupid`) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(sql, (task_name, description, due_date, status, task_groupid))
            connection.commit()
            return make_response(jsonify({'message': f'task {task_name} created successfully'}), 200)
    except Exception as e:
        error_message = f'Error creating task {task_name}: ' + str(e)
        print("Exception:", error_message)
        return make_response(jsonify({'message': error_message}), 500)




if __name__ == '__main__':
    app.run(debug=True)