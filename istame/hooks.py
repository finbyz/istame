app_name = "istame"
app_title = "istame"
app_publisher = "finbyz"
app_description = "istame"
app_email = "info@finbyz.tech"
app_license = "MIT"


doctype_js = {
	"Issue": "public/js/doctype_js/issue.js",
}
doc_events = {
    "Issue": {
        "validate": "istame.api.issue_validate"
    },
    "Ista Middle East": {
        "validate": "istame.istame.doc_events.ista_middle_east.validate"
    }
}

scheduler_events = {
	"cron": {
		"0/1 * * * *": [
			"istame.api.escalation_email",
		]
	},
	"all":[
		# "jciw.api.make_status_overdue",
		"istame.api.istame_overdue_email",
		"istame.api.istame_warning_email",
	]
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/istame/css/istame.css"
# app_include_js = "/assets/istame/js/istame.js"

# include js, css files in header of web template
# web_include_css = "/assets/istame/css/istame.css"
# web_include_js = "/assets/istame/js/istame.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "istame/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "istame.utils.jinja_methods",
# 	"filters": "istame.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "istame.install.before_install"
# after_install = "istame.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "istame.uninstall.before_uninstall"
# after_uninstall = "istame.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "istame.utils.before_app_install"
# after_app_install = "istame.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "istame.utils.before_app_uninstall"
# after_app_uninstall = "istame.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "istame.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"istame.tasks.all"
# 	],
# 	"daily": [
# 		"istame.tasks.daily"
# 	],
# 	"hourly": [
# 		"istame.tasks.hourly"
# 	],
# 	"weekly": [
# 		"istame.tasks.weekly"
# 	],
# 	"monthly": [
# 		"istame.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "istame.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "istame.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "istame.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["istame.utils.before_request"]
# after_request = ["istame.utils.after_request"]

# Job Events
# ----------
# before_job = ["istame.utils.before_job"]
# after_job = ["istame.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"istame.auth.validate"
# ]
