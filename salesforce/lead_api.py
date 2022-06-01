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
def import_lead():
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
		leads_fetch_url = connection_dict.get('instance_url') + ("/services/data/v54.0/query/?q=SELECT CreatedDate,Id,FirstName,LastName,Company,NumberOfEmployees,Description,City,State,PostalCode,Phone,MobilePhone,Email FROM Lead WHERE CreatedDate > {0} AND CreatedDate < {1}").format(from_date,to_date)
		# leads_fetch_url = connection_dict.get('instance_url') + "/services/data/v54.0/query/?q=SELECT FIELDS(All) FROM Lead LIMIT 200"
		headers = {
			"Content-type": "application/json",
			"Authorization": connection_dict.get('token_type') +" "+connection_dict.get('access_token')
		}
		leads_data = requests.get(leads_fetch_url, headers=headers)
		leads_data_dict = json.loads(leads_data.text)
		for lead_rec in leads_data_dict.get('records'):
			lead_sql = frappe.db.get_list('Lead',filters={'sf_id': str(lead_rec.get('Id'))},fields=['sf_id'],as_list=True)
			if not lead_sql:
				new_lead = frappe.get_doc(dict(
					doctype = 'Lead',
					sf_id = str(lead_rec.get('Id')),
					first_name = str(lead_rec.get('FirstName')),
					last_name = str(lead_rec.get('LastName')),
					company_name = str(lead_rec.get('Company')),
					no_of_employees = str(lead_rec.get('NumberOfEmployees')),
					notes = str(lead_rec.get('Description')),
					city = str(lead_rec.get('City')),
					state = str(lead_rec.get('State')),
					pincode = str(lead_rec.get('PostalCode'))
				))

				mob_mail = new_lead.save()

				if lead_rec.get('Phone'):
					mob_mail.phone = str(lead_rec.get('Phone'))
				if lead_rec.get('MobilePhone'):
					mob_mail.mobile_no = str(lead_rec.get('MobilePhone'))
				if lead_rec.get('Email'):
					mob_mail.email_id = str(lead_rec.get('Email'))

				print('\033[92m' + 'New Lead Added! \n')
				mob_mail.save()

			else:
				upd_lead = frappe.db.get_value("Lead",{'sf_id':str(lead_rec.get('Id'))},'name')
				
				if upd_lead:
					lead_doc = frappe.get_doc("Lead",upd_lead)
					lead_doc.company_name = str(lead_rec.get('Company')),
					lead_doc.no_of_employees = str(lead_rec.get('NumberOfEmployees')),
					lead_doc.notes = str(lead_rec.get('Description')),
					lead_doc.city = str(lead_rec.get('City')),
					lead_doc.state = str(lead_rec.get('State')),
					lead_doc.pincode = str(lead_rec.get('PostalCode')),
					myTuple = ''.join(lead_doc.no_of_employees)
					qqq = myTuple
					lead_doc.no_of_employees = qqq

					mob_mail_upd = lead_doc.save()

					if lead_rec.get('Phone'):
						mob_mail_upd.phone = str(lead_rec.get('Phone'))
					if lead_rec.get('MobilePhone'):
						mob_mail_upd.mobile_no = str(lead_rec.get('MobilePhone'))
					if lead_rec.get('Email'):
						mob_mail_upd.email_id = str(lead_rec.get('Email'))

					print('\033[93m' + 'Exiting Lead Updated! \n')


					mob_mail_upd.save()