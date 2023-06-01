import app

# sql queries for task groups
CREATE_TASK_GROUP = "INSERT INTO `task_groups` (`group_name`) VALUES (%s);"
GET_ALL_TASK_GROUPS = "SELECT * FROM `task_groups`;"
GET_TASK_GROUP_BY_ID = "SELECT * FROM `task_groups` WHERE `id` = %s;"
UPDATE_TASK_GROUP_BY_ID = "UPDATE `task_groups` SET `group_name`=%s WHERE `id`=%s;"
DELETE_TASK_GROUP_BY_ID = "DELETE from `task_groups` WHERE `id`=%s"

#sql queries for tasks
CREATE_TASKS = "INSERT INTO `tasks` (`task_name`, `description`, `due_date`, `priority`, `status`, `task_groupid`) VALUES (%s, %s, %s, %s, %s, %s);"
GET_ALL_TASKS = "SELECT * FROM `tasks`;"
GET_TASKS_BY_TASK_GROUP_ID = "SELECT * FROM `tasks` WHERE `task_groupid`=%s;"
GET_TASK_BY_TASK_ID = "SELECT * FROM `tasks` WHERE `id`=%s;"
UPDATE_TASK_BY_TASK_ID = "UPDATE `tasks` SET `task_name`=%s, `description`=%s, `due_date`=%s, `priority`=%s, `status`=%s WHERE `id`=%s;"
GET_TASK_BY_STATUS = "SELECT * FROM `tasks` WHERE `status`='completed';"
DELETE_TASK_BY_STATUS = "DELETE from `tasks` WHERE `status`=%s"
DELETE_TASK_BY_ID = "DELETE from `tasks` WHERE `id`=%s;"
