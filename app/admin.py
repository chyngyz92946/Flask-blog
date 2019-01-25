from flask import redirect, url_for, request

from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView


class AdminView(ModelView):
	def is_accessible(self):
		return current_user.has_role('admin')

	def inaccessible_callback(self, **kwargs):
		return redirect(url_for('security.login', next=request.url))


class HomeAdminView(AdminIndexView):
	def is_accessible(self):
		return current_user.has_role('admin')

	def inaccessible_callback(self, **kwargs):
		return redirect(url_for('security.login', next=request.url))
