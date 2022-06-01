from . import __version__ as app_version

app_name = "salesforce"
app_title = "Salesforce"
app_publisher = "Nihantra Patel"
app_description = "Salesforce to ERPNext integration"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "n.patel.serpentcs@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

fixtures = [{
	"doctype": "Property Setter",
	"filters": {
		"module": ["=", "Salesforce"]
		}
	}]


# include js, css files in header of desk.html
# app_include_css = "/assets/salesforce/css/salesforce.css"
# app_include_js = "/assets/salesforce/js/salesforce.js"

# include js, css files in header of web template
# web_include_css = "/assets/salesforce/css/salesforce.css"
# web_include_js = "/assets/salesforce/js/salesforce.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "salesforce/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}

doctype_list_js = {
					"Contact" : "public/js/contact_listview.js",
					"Lead" : "public/js/lead_listview.js",
					"Opportunity" : "public/js/opportunity_listview.js",
					"Item" : "public/js/item_listview.js"
					}

# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "salesforce.utils.jinja_methods",
# 	"filters": "salesforce.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "salesforce.install.before_install"
# after_install = "salesforce.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "salesforce.uninstall.before_uninstall"
# after_uninstall = "salesforce.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "salesforce.notifications.get_notification_config"

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
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"salesforce.tasks.all"
# 	],
# 	"daily": [
# 		"salesforce.tasks.daily"
# 	],
# 	"hourly": [
# 		"salesforce.tasks.hourly"
# 	],
# 	"weekly": [
# 		"salesforce.tasks.weekly"
# 	],
# 	"monthly": [
# 		"salesforce.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "salesforce.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "salesforce.event.get_events"
# }

# override_whitelisted_methods = {
# 	"erpnext.setup.doctype.company.company.onload": "salesforce.api.import_contact"
# }

#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "salesforce.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"salesforce.auth.validate"
# ]

