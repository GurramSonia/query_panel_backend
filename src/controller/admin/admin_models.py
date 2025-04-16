from flask_restx import fields
from src.controller.admin.admin_ns import admin_ns_get,admin_ns_add,admin_ns_remove

audit_logs_model = admin_ns_get.model('AuditLogs', {
            'id': fields.Integer(description='Log ID'),
            'username': fields.String(description='User ID who performed the action'),
            'action': fields.String(description='Action performed'),
            'timestamp': fields.DateTime(description='Timestamp of the action')
})

group_permission_model = admin_ns_add.model('Permission', {
            'group':fields.String(required=True, description="Name of the group"),
            'source': fields.String(required=True, description="Database source (e.g., MySQL, MongoDB)"),
            'tableName': fields.String(required=True, description="Name of the table"),
            'operations': fields.List(fields.String, required=True, description="List of allowed operations"),
})

user_permission_model = admin_ns_add.model('UserPermission', {
            'username':fields.String(required=True, description="Name of the group"),
            'source': fields.String(required=True, description="Database source (e.g., MySQL, MongoDB)"),
            'db_name': fields.String(required=True, description="Database source (e.g., MySQL, MongoDB)"),
            'tableName': fields.String(required=True, description="Name of the table"),
            'operations': fields.List(fields.String, required=True, description="List of allowed operations"),
})

group_model = admin_ns_add.model('Group',{
            'groupName': fields.String(required=True, description="group name to add users into group"),
            'users': fields.List(fields.String, required=True, description="list of users")
})

remove_user=admin_ns_remove.model('Remove_user',{
            'group_name':fields.String(required=True, description="group name  to remove users"),
            'username':fields.String(required=True, description=" username to remove from group"),
})

remove_group=admin_ns_remove.model('Remove_Group',{
            'group_name':fields.String(required=True, description="group name  to remove from groups-list"),
})

remove_user_usermangement=admin_ns_remove.model('Remove_user_usermanagement',{
            'username':fields.String(required=True, description=" username to remove from users-list"),
})

add_user=admin_ns_add.model('Add_user',{
            'group_name':fields.String(required=True,  description="group name  to add user"), 'username':fields.String(required=True, description=" username to add into group"),
 })

remove_group_operation=admin_ns_remove.model('Remove_Group_Operation',{
            'group_name':fields.String(required=True, description="group name to remove opeartion"),
            'source':fields.String(required=True, description=" source to remove opeartion"),
            'database':fields.String(required=True, description=" database to remove opeartion"),
            'table':fields.String(required=True, description=" table_name to remove remove opeartion"),
            'operation':fields.String(required=True, description="  operation to remove from group"),
})   

remove_user_operation=admin_ns_remove.model('Remove_User_Operation',{
            'user_name':fields.String(required=True, description="username to remove opeartion"),
            'source':fields.String(required=True, description=" source to remove opeartion"),
            'database':fields.String(required=True, description=" database to remove opeartion"),
            'table':fields.String(required=True, description=" table_name to remove opeartion"),
            'operation':fields.String(required=True, description="  operation to remove from user"),
})

add_group_operation=admin_ns_add.model('Add_Group_Operation',{
            'group_name':fields.String(required=True, description="group name to add opeartion"),
            'source':fields.String(required=True, description=" source to add opeartion"),
            'database':fields.String(required=True, description=" database to add opeartion"),
            'table':fields.String(required=True, description=" table_name to add opeartion"),
            'operation':fields.String(required=True, description="  operation to into  group"),
})

add_user_operation=admin_ns_add.model('Add_User_Operation',{
            'user_name':fields.String(required=True, description="username to add opeartion"),
            'source':fields.String(required=True, description=" source to add opeartion"),
            'database':fields.String(required=True, description=" database to add opeartion"),
            'table':fields.String(required=True, description=" table_name to add opeartion"),
            'operation':fields.String(required=True, description="  operation to add into  group"),
 })

available_databases=admin_ns_get.model('AvailableDatabases',{})
users=admin_ns_get.model('Users',{})
groups=admin_ns_get.model('Groups',{})
operations=admin_ns_get.model('operations',{})
update_email_pass=admin_ns_add.model('UpdateEmailPass',{
            'group_name':fields.String(required=True, description="group name to add opeartion"),
            'source':fields.String(required=True, description=" source to add opeartion"),
            'database':fields.String(required=True, description=" database to add opeartion"),
            'table':fields.String(required=True, description=" table_name to add opeartion"),
            'view_email':fields.Integer(required=True, description=" table_name to add opeartion"),
            'view_pass':fields.Integer(required=True, description=" table_name to add opeartion"),
            
})