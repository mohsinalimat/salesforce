import logging
import erpnext
import json
import requests
import frappe
import frappe.defaults
from frappe.exceptions import ValidationError
from frappe import _, throw
from frappe import _
from frappe.cache_manager import clear_defaults_cache
from frappe.contacts.address_and_contact import load_address_and_contact
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.utils import cint, formatdate, get_timestamp, today
from frappe.utils.nestedset import NestedSet



@frappe.whitelist()
def test_sf_connection(username,sf_client_id,sf_client_secret_key,access_token,password,request_url):
	username=username
	request_url = request_url
	sf_client_id = sf_client_id
	sf_client_secret_key = frappe.get_single("Salesforce Settings").get_password('sf_client_secret_key')
	access_token = access_token
	password = frappe.get_single("Salesforce Settings").get_password('password')

	if not(request_url and sf_client_id and sf_client_secret_key and access_token and username and password):
			raise ValidationError(_(
                "Missing 'Request URL' OR 'Client App-key ID' "
                "OR 'Client App-Secret Key' Information OR 'Username' "
                "OR 'Password' Please Configure it properly !!"
            ))
	url = request_url

	headers = {"Content-Type": "application/x-www-form-urlencoded"}
	data = {
			"grant_type": "password",
			"client_id": sf_client_id,
			"client_secret": sf_client_secret_key,
			"username": username,
			"password": password + access_token
		}
	sf_response = requests.post(url, headers=headers, data=data)
	sf_dict = {}
	if sf_response.status_code != 200:
		print('\n \033[91m' + 'Authentication failed! \n')
		sf_dict = {}

	if sf_response.status_code == 200:
		print('\n \033[92m' + 'Authentication Successfully Done! \n')
		sf_dict = json.loads(sf_response.text)

	return sf_dict, sf_response.status_code