frappe.listview_settings['Lead'] = {
	onload: function(listview) {
		listview.page.add_menu_item(__("Import Salesforce Lead"), function() {
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
						method:'salesforce.lead_api.import_lead',
						callback: function() {
							listview.refresh();
							frappe.msgprint('Please check your Lead');
						}
					});
			   }
			});
			});
		});
	}
};