import logging
import erpnext
import json
import requests
import frappe
import salesforce
import frappe.defaults
from frappe.exceptions import ValidationError
from frappe import _, throw
from frappe import _
from frappe.cache_manager import clear_defaults_cache
from frappe.contacts.address_and_contact import load_address_and_contact
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.utils import cint, formatdate, get_timestamp, today
from frappe.utils.nestedset import NestedSet
from salesforce.test_sf_connection_api import test_sf_connection



@frappe.whitelist()
def import_item():
	username = frappe.db.get_single_value('Salesforce Settings', 'username')
	sf_client_id = frappe.db.get_single_value('Salesforce Settings', 'sf_client_id')
	sf_client_secret_key = frappe.db.get_single_value('Salesforce Settings', 'sf_client_secret_key')
	access_token = frappe.db.get_single_value('Salesforce Settings', 'access_token')
	password = frappe.db.get_single_value('Salesforce Settings', 'password')
	request_url = frappe.db.get_single_value('Salesforce Settings', 'request_url')
	"""Method to import contacts."""
	connection_dict, status = test_sf_connection(username,sf_client_id,sf_client_secret_key,access_token,password,request_url)
	if status != 200:
		raise ValidationError(_(
			"Configure the sales force account"
			" properly in salesforce connector auth tab."
		))
	if connection_dict:
		from_date = str(frappe.db.get_single_value('Salesforce Settings','from_date'))+''+'T00:00:00Z'
		to_date = str(frappe.db.get_single_value('Salesforce Settings','to_date'))+''+'T00:00:00Z'
		items_fetch_url = connection_dict.get('instance_url') + ("/services/data/v54.0/query/?q=SELECT CreatedDate,Id,ProductCode,Name,Description FROM Product2 WHERE CreatedDate > {0} AND CreatedDate < {1}").format(from_date,to_date)
		headers = {
			"Content-type": "application/json",
			"Authorization": connection_dict.get('token_type') +" "+connection_dict.get('access_token')
		}
		items_data = requests.get(items_fetch_url, headers=headers)
		items_data_dict = json.loads(items_data.text)

		for item_rec in items_data_dict.get('records'):
			item_sql = frappe.db.get_list('Item',filters={'sf_id': str(item_rec.get('Id'))},fields=['sf_id'],as_list=True)
			if not item_sql:
				new_item = frappe.get_doc(dict(
					doctype = 'Item',
					sf_id = str(item_rec.get('Id')),
					item_code = str(item_rec.get('ProductCode')),
					item_name = str(item_rec.get('Name')),
					description = str(item_rec.get('Description')),
					item_group = "Products",
					stock_uom = "Nos"
				))
				print('\033[92m' + 'New Item Added! \n')
				new_item.save()

			else:
				upd_item = frappe.db.get_value("Item",{'sf_id':str(item_rec.get('Id'))},'name')
				if upd_item:
					item_doc = frappe.get_doc("Item",upd_item)
					item_doc.item_name = str(item_rec.get('Name')),
					item_doc.description = str(item_rec.get('Description'))
					print('\033[93m' + 'Exiting Item Updated! \n')
					item_doc.save()