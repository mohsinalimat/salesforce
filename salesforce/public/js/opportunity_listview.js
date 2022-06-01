frappe.listview_settings['Opportunity'] = {
	add_fields: ["customer_name", "opportunity_type", "opportunity_from", "status"],
	get_indicator: function(doc) {
		var indicator = [__(doc.status), frappe.utils.guess_colour(doc.status), "status,=," + doc.status];
		if(doc.status=="Quotation") {
			indicator[1] = "green";
		}
		return indicator;
	},
	onload: function(listview) {
		var method = "erpnext.crm.doctype.opportunity.opportunity.set_multiple_status";

			listview.page.add_menu_item(__("Import Salesforce Opportunity"), function() {
			let from_date = frappe.db.get_single_value('Salesforce Settings','from_date')
			let to_date = frappe.db.get_single_value('Salesforce Settings','to_date')
			from_date.then(function(f_date) {
			   to_date.then(function(t_date) {
			   if(f_date == '0001-01-01'){
			   	frappe.msgprint("Please set"+'<b>'+ " From Date "+'</b>' + "to" +'<b>'+ " To Date "+'</b>' + "in " +'<b>'+ '<a onclick="window.open(this.href);return false;" href="/app/salesforce-setting/Salesforce Setting">Salesforce Setting</a>'+'</b>');
			   }
			   else if(t_date == '0001-01-01'){
			   	frappe.msgprint("Please set"+'<b>'+ " From Date "+'</b>' + "to" +'<b>'+ " To Date "+'</b>' + "in " +'<b>'+ '<a onclick="window.open(this.href);return false;" href="/app/salesforce-setting/Salesforce Setting">Salesforce Setting</a>'+'</b>');
			   }
			   else{
			   		frappe.msgprint('Please Wait ... ');
					frappe.call({
						method:'salesforce.opportunity_api.import_opportunity',
						callback: function() {
							listview.refresh();
							frappe.msgprint('Please check your Opportunity');
						}
					});
			   }
			});
			});
		});

		listview.page.add_menu_item(__("Set as Open"), function() {
			listview.call_for_selected_items(method, {"status": "Open"});
		});

		listview.page.add_menu_item(__("Set as Closed"), function() {
			listview.call_for_selected_items(method, {"status": "Closed"});
		});

		if(listview.page.fields_dict.opportunity_from) {
			listview.page.fields_dict.opportunity_from.get_query = function() {
				return {
					"filters": {
						"name": ["in", ["Customer", "Lead"]],
					}
				};
			};
		}
	}
};