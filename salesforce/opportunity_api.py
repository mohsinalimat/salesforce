import logging
from datetime import datetime
from frappe.utils import add_to_date
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
def import_opportunity():
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
		oppo_fetch_url = connection_dict.get('instance_url') + ("/services/data/v54.0/query/?q=SELECT CreatedDate,Id,ContactId,Name,Amount,CloseDate,Probability FROM Opportunity WHERE CreatedDate > {0} AND CreatedDate < {1}").format(from_date,to_date)
		headers = {
			"Content-type": "application/json",
			"Authorization": connection_dict.get('token_type') +" "+connection_dict.get('access_token')
		}
		oppo_data = requests.get(oppo_fetch_url, headers=headers)
		oppo_data_dict = json.loads(oppo_data.text)
		for oppo_rec in oppo_data_dict.get('records'):

			oppo_sql = frappe.db.get_list('Opportunity',filters={'sf_id': str(oppo_rec.get('Id'))},fields=['sf_id'],as_list=True)
			if not oppo_sql:
				new_oppo = frappe.get_doc(dict(
					doctype = "Opportunity",
					sf_id = str(oppo_rec.get('Id')),
					contact_sf_id = str(oppo_rec.get('ContactId')),
					customer_name = str(oppo_rec.get('Name')),
					opportunity_amount = str(oppo_rec.get('Amount')),
					transaction_date = frappe.utils.get_datetime(formatdate(oppo_rec.get('CreatedDate'))).strftime('%Y-%m-%d'),
					expected_closing = str(oppo_rec.get('CloseDate')),
					probability = str(oppo_rec.get('Probability'))
				))
				print('\033[92m' + 'New Opportunity Added! \n')
				new_oppo.save()
				
			
			oppo = frappe.db.get_value("Opportunity",{'sf_id':str(oppo_rec.get('Id'))},'name')
			oppo_contsfid = frappe.db.get_value("Opportunity",{'contact_sf_id':str(oppo_rec.get('ContactId'))},'contact_sf_id')
			oppo_name = frappe.db.get_value("Opportunity",{'contact_sf_id':str(oppo_rec.get('ContactId'))},'name')
			cont_sfid = frappe.db.get_value("Contact",{'sf_id':str(oppo_rec.get('ContactId'))},'sf_id')
			cont_name = frappe.db.get_value("Contact",{'sf_id':str(oppo_rec.get('ContactId'))},'name')

			if oppo_contsfid == cont_sfid:
				test_doc_oppo = frappe.get_doc("Contact",cont_name)
				test_doc_oppo.append('links', {
					'link_doctype': "Opportunity",
					'link_name': oppo_name
					})
				test_doc_oppo.save()

			if oppo:
				upd_oppo = frappe.get_doc("Opportunity",oppo)
				upd_oppo.contact_person = cont_name
				upd_oppo.customer_name = str(oppo_rec.get('Name')),
				upd_oppo.opportunity_amount = str(oppo_rec.get('Amount'))
				upd_oppo.transaction_date = frappe.utils.get_datetime(formatdate(oppo_rec.get('CreatedDate'))).strftime('%Y-%m-%d')
				upd_oppo.expected_closing = str(oppo_rec.get('CloseDate'))
				upd_oppo.probability = str(oppo_rec.get('Probability'))
				print('\033[93m' + 'Exiting Opportunity Updated! \n')
				upd_oppo.save()