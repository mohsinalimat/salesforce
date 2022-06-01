import logging
import erpnext
import json
import requests
import frappe
import frappe.defaults
import salesforce
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
def import_contact():
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
		contacts_fetch_url = connection_dict.get('instance_url') + ("/services/data/v54.0/query/?q=SELECT CreatedDate,Id,FirstName,LastName,Department,Email,MobilePhone FROM Contact WHERE CreatedDate > {0} AND CreatedDate < {1}").format(from_date,to_date)
		headers = {
			"Content-type": "application/json",
			"Authorization": connection_dict.get('token_type') +" "+connection_dict.get('access_token')
		}
		contacts_data = requests.get(contacts_fetch_url, headers=headers)

		# For ERPNext to salesforce integration 
		# contacts_post_url = connection_dict.get('instance_url') + "/services/data/v54.0/sobjects/Contact/"
		# data={
		#     "FirstName":"Test",
		#     "LastName":"Contact"
		# }
		# data = json.dumps(data)
		# contacts_post_data = requests.post(contacts_post_url,headers=headers,data=data)
		# print("==============",data)

		contacts_data_dict = json.loads(contacts_data.text)
		for contact_rec in contacts_data_dict.get('records'):
			lead_con = frappe.db.get_value("Contact",{'name':str(contact_rec.get('Name'))},'name')
			if lead_con:
				doc = frappe.get_doc("Contact",lead_con)
				doc.sf_id = contact_rec.get('Id')
				print('\033[93m' + 'Linked Contact Updated! \n')
				doc.save()

			sql1= frappe.db.get_list('Contact',filters={'sf_id': str(contact_rec.get('Id'))},fields=['sf_id'],as_list=True)
			if not sql1:
				rrr = frappe.get_doc(dict(
					doctype = 'Contact',
					sf_id = str(contact_rec.get('Id')),
					first_name = str(contact_rec.get('FirstName')),
					last_name = str(contact_rec.get('LastName')),
					department = str(contact_rec.get('Department')),
				))
				mob_mail=rrr.save()
				if contact_rec.get('Email'):
					mob_mail.append('email_ids', {
						'email_id': str(contact_rec.get('Email'))
						})
				if contact_rec.get('MobilePhone'):
					mob_mail.append('phone_nos', {
						'phone': str(contact_rec.get('MobilePhone')),
						'is_primary_mobile_no': 1
						})
				print('\033[92m' + 'New Contact Added! \n')
				mob_mail.save()
			else:
				upd = frappe.db.get_value("Contact",{'sf_id':str(contact_rec.get('Id'))},'name')
				if upd:
					test_doc = frappe.get_doc("Contact",upd)
					test_doc.first_name = str(contact_rec.get('FirstName')),
					test_doc.last_name = str(contact_rec.get('LastName')),
					test_doc.department = str(contact_rec.get('Department'))

					mob_mail_upd = test_doc.save()

					if contact_rec.get('Email'):
						if not test_doc.email_ids:
							mob_mail_upd.append('email_ids', {
								'email_id': str(contact_rec.get('Email'))
								})
						for em in test_doc.get('email_ids'):
							em.email_id = str(contact_rec.get('Email'))

					if contact_rec.get('MobilePhone'):
						if not test_doc.phone_nos:
							mob_mail_upd.append('phone_nos', {
								'phone': str(contact_rec.get('MobilePhone')),
								'is_primary_mobile_no': 1
								})
						for mp in test_doc.get('phone_nos'):
							mp.phone = str(contact_rec.get('MobilePhone'))

					print('\033[93m' + 'Exiting Contact Updated! \n')
					mob_mail_upd.save()