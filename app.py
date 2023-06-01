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
    priority = data['priority']
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
            sql = "INSERT INTO `tasks` (`task_name`, `description`, `due_date`, `priority`, `status`, `task_groupid`) VALUES (%s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (task_name, description, due_date, priority, status, task_groupid))
            connection.commit()
            return make_response(jsonify({'message': f'task {task_name} created successfully'}), 200)
    except Exception as e:
        error_message = f'Error creating task {task_name}: ' + str(e)
        print("Exception:", error_message)
        return make_response(jsonify({'message': error_message}), 500)
    
# get all tasks
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `tasks`;"
            cursor.execute(sql)
            result = cursor.fetchall()
            print("result: ", result)
            return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = 'Error getting all tasks: ' + str(e)
        print("Exception:", error_message)
        return make_response(jsonify({'message': error_message}), 500)

# get tasks by task group id
@app.route('/task-groups/<int:task_groupid>/tasks', methods=['GET'])
def get_all_task(task_groupid):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `tasks` WHERE `task_groupid`=%s;"
            cursor.execute(sql, (task_groupid))
            result = cursor.fetchall()
            return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = 'Error getting all tasks from this task group: ' + str(e)
        print("Exception:", error_message)
        return make_response(jsonify({'message': error_message}), 500)
    
# get task by task id
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `tasks` WHERE `id`=%s;"
            cursor.execute(sql, (id))
            result = cursor.fetchall()
            return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = 'Error getting the task: ' + str(e)
        print("Exception:", error_message)
        return make_response(jsonify(error_message), 500)
    
# # update task name
# @app.route('/task/<string:task_name>', methods=['PUT'])
# def update_task_name(task_name):
#     # print("What do you wish to update?")
#     # print("1. Task name")
#     # print("2. Task description")
#     # print("3. Task due date")
#     # print("4. Priority")
#     # print("5. Task status")
#     # print("6. Update all fields")

#     # choice = input("Enter your choice")

#     try:
#         with connection.cursor() as cursor:
#             data = request.get_json()
#             new_task_name = data['task_name']
#             sql = "UPDATE `tasks` SET `task_name`=%s WHERE `task_name`=%s;"
#             cursor.execute(sql, (new_task_name, task_name))
#             connection.commit()
#             return make_response(jsonify({'message': 'task name updated successfully'}), 200)
#     except Exception as e:
#         error_message = 'Error updating task name: ' + str(e)
#         print("Exception: ", error_message)
#         return make_response(jsonify(error_message), 500)
    
# # update task description
# @app.route('/task/<int:id>', methods=['PUT'])
# def update_task_desc(id):
#     try:
#         with connection.cursor() as cursor:
#             data = request.get_json()
#             description = data['description']
#             sql = "UPDATE `tasks` SET `description`=%s WHERE `id`=%s;"
#             cursor.execute(sql, (description, id))
#             connection.commit()
#             return make_response(jsonify({'message': 'task description updated successfulyy'}), 200)
#     except Exception as e:
#         error_message = 'Error updating task description: ' + str(e)
#         print("Exception: ", error_message)
#         return make_response(jsonify(error_message), 500)
    
# # update task due_date
# @app.route('/task/<int:id>', methods=["PUT"])
# def update_task_duedate(id):
#     try:
#         with connection.cursor() as cursor:
#             data = request.get_json()
#             due_date = data['due_date']
#             sql = "UPDATE `tasks` SET `due_date`=%s WHERE `id`=%s;"
#             cursor.execute(sql, (due_date, id))
#             connection.commit()
#             return make_response(jsonify({'message': 'task due_date updated successfully'}), 200)
#     except Exception as e:
#         error_message = 'Error updating task due_date: ' + str(e)
#         print("Exception: ", error_message)
#         return make_response(jsonify(error_message), 500)
    
# # update task priority
# @app.route('/task/<int:id>', methods=["PUT"])
# def update_task_priority(id):
#     try:
#         with connection.cursor() as cursor:
#             data = request.get_json()
#             priority = data['priority']
#             sql = "UPDATE `tasks` SET `priority`=%s WHERE `id`=%s;"
#             cursor.execute(sql, (priority, id))
#             connection.commit()
#             return make_response(jsonify({'message': 'task priority updated successfully'}), 200)
#     except Exception as e:
#         error_message = 'Error updating task priority: ' + str(e)
#         print("Exception: ", error_message)
#         return make_response(jsonify(error_message), 500)

# # update task status
# @app.route('/task/<int:id>', methods=["PUT"])
# def update_task_status(id):
#     try:
#         with connection.cursor() as cursor:
#             data = request.get_json()
#             status = data['status']
#             sql = "UPDATE `tasks` SET `status`=%s WHERE `id`=%s;"
#             cursor.execute(sql, (status, id))
#             connection.commit()
#             return make_response(jsonify({'message': 'task status updated successfully'}), 200)
#     except Exception as e:
#         error_message = 'Error updating task status: ' + str(e)
#         print("Exception: ", error_message)
#         return make_response(jsonify(error_message), 500)

# update task information
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `tasks` WHERE `id`=%s;"
            cursor.execute(sql, (id))
            result = cursor.fetchall()

            if len(result) == 0:
                return make_response(jsonify({'message': 'Task not found'}), 404)

            task = result[0]
            print(task)

            data = request.get_json()
            new_task_name = data['task_name']
            new_description = data['description']
            new_due_date = data['due_date']
            new_priority = data['priority']
            new_status = data['status']

            name = new_task_name if new_task_name else task['task_name']
            desc = new_description if new_description else task['description']
            due = new_due_date if new_due_date else task['due_date']
            pri = new_priority if new_priority else task['priority']
            state = new_status if new_status else task['status']

            sqlup = "UPDATE `tasks` SET `task_name`=%s, `description`=%s, `due_date`=%s, `priority`=%s, `status`=%s WHERE `id`=%s;"
            cursor.execute(sqlup, (name, desc, due, pri, state, id))
            connection.commit()
            return make_response(jsonify({'message': 'Task information updated successfully'}), 200)
    except Exception as e:
        error_message = 'Error updating task status: ' + str(e)
        print("Exception: ", error_message)
        return make_response(jsonify({'message': error_message}), 500)


                
            






if __name__ == '__main__':
    app.run(debug=True)