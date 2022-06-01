frappe.ui.form.on('Salesforce Settings', {
	refresh(frm) {
		$("Button[data-fieldname=test_sf_connection]").addClass("btn-info").removeClass("btn-default");
		$("Button[data-fieldname=import_contact]").addClass("btn-info").removeClass("btn-default");
		$("Button[data-fieldname=import_lead]").addClass("btn-info").removeClass("btn-default");
		$("Button[data-fieldname=import_opportunity]").addClass("btn-info").removeClass("btn-default");
		$("Button[data-fieldname=import_item]").addClass("btn-info").removeClass("btn-default");
	}
});



frappe.ui.form.on("Salesforce Settings", "test_sf_connection", function(frm) {
                frappe.call({
                        method: "salesforce.test_sf_connection_api.test_sf_connection",
                           args: {
					username: frm.doc.username,
					sf_client_id: frm.doc.sf_client_id,
					sf_client_secret_key: frm.doc.sf_client_secret_key,
					access_token: frm.doc.access_token,
					password: frm.doc.password,
					request_url: frm.doc.request_url
			    		},
                        callback(r) {
                		if (r.message[1] == 200) {
                			frappe.msgprint({
				            title: __('Success'),
				            indicator: 'green',
				            message: __('Authentication Successfully Done!')
    					    });
			                }
			                else{
			                	frappe.msgprint({
					            title: __('Error'),
					            indicator: 'red',
					            message: __('Authentication failed!')
						});
			                }
			         }
                    });
    });

frappe.ui.form.on("Salesforce Settings", "import_contact", function(frm) {
	if(!frm.doc.from_date){
		frappe.msgprint({
		            title: __('Error'),
		            indicator: 'red',
		            message: __("Please set"+'<b>'+ " From Date "+'</b>' + "to" +'<b>'+ " To Date "+'</b>')
			});
	}
	else if(!frm.doc.to_date){
		frappe.msgprint({
		            title: __('Error'),
		            indicator: 'red',
		            message: __("Please set"+'<b>'+ " From Date "+'</b>' + "to" +'<b>'+ " To Date "+'</b>')
			});
	}
	else{
	frappe.msgprint({
	            title: __('Please Wait ... '),
	            indicator: 'yellow',
	            message: __('Please wait for Import and Update Contact')
		});
                frappe.call({
                        method: "salesforce.contact_api.import_contact",
                       
                        callback(r) {
                        frappe.msgprint({
			            title: __('Success'),
			            indicator: 'green',
			            message: __('Please check your ' + '<a onclick="window.open(this.href);return false;" href="/app/contact"> Contact </a>')
				});
                		if (r.message) {
                			
			                }
			         }
                    });
            }
    });


frappe.ui.form.on("Salesforce Settings", "import_lead", function(frm) {
	if(!frm.doc.from_date){
		frappe.msgprint({
		            title: __('Error'),
		            indicator: 'red',
		            message: __("Please set"+'<b>'+ " From Date "+'</b>' + "to" +'<b>'+ " To Date "+'</b>')
			});
	}
	else if(!frm.doc.to_date){
		frappe.msgprint({
		            title: __('Error'),
		            indicator: 'red',
		            message: __("Please set"+'<b>'+ " From Date "+'</b>' + "to" +'<b>'+ " To Date "+'</b>')
			});
	}
	else{
	frappe.msgprint({
	            title: __('Please Wait ... '),
	            indicator: 'yellow',
	            message: __('Please wait for Import and Update Lead')
		});
                frappe.call({
                        method: "salesforce.lead_api.import_lead",
                    
                        callback(r) {
                	frappe.msgprint({
			            title: __('Success'),
			            indicator: 'green',
			            message: __('Please check your ' + '<a onclick="window.open(this.href);return false;" href="/app/lead"> Lead </a>')
				});	
                		if (r.message) {
			                }
			         }
                    });
        }
    });

frappe.ui.form.on("Salesforce Settings", "import_opportunity", function(frm) {
	if(!frm.doc.from_date){
		frappe.msgprint({
		            title: __('Error'),
		            indicator: 'red',
		            message: __("Please set"+'<b>'+ " From Date "+'</b>' + "to" +'<b>'+ " To Date "+'</b>')
			});
	}
	else if(!frm.doc.to_date){
		frappe.msgprint({
		            title: __('Error'),
		            indicator: 'red',
		            message: __("Please set"+'<b>'+ " From Date "+'</b>' + "to" +'<b>'+ " To Date "+'</b>')
			});
	}
	else{
	frappe.msgprint({
	            title: __('Please Wait ... '),
	            indicator: 'yellow',
	            message: __('Please wait for Import and Update Opportunity')
		});
                frappe.call({
                        method: "salesforce.opportunity_api.import_opportunity",
                    
                        callback(r) {
                	frappe.msgprint({
			            title: __('Success'),
			            indicator: 'green',
			            message: __('Please check your ' + '<a onclick="window.open(this.href);return false;" href="/app/opportunity"> Opportunity </a>')
				});	
                		if (r.message) {
			                }
			         }
                    });
        }
    });


frappe.ui.form.on("Salesforce Settings", "import_item", function(frm) {
	if(!frm.doc.from_date){
		frappe.msgprint({
		            title: __('Error'),
		            indicator: 'red',
		            message: __("Please set"+'<b>'+ " From Date "+'</b>' + "to" +'<b>'+ " To Date "+'</b>')
			});
	}
	else if(!frm.doc.to_date){
		frappe.msgprint({
		            title: __('Error'),
		            indicator: 'red',
		            message: __("Please set"+'<b>'+ " From Date "+'</b>' + "to" +'<b>'+ " To Date "+'</b>')
			});
	}
	else{
	frappe.msgprint({
	            title: __('Please Wait ... '),
	            indicator: 'yellow',
	            message: __('Please wait for Import and Update Item')
		});
                frappe.call({
                        method: "salesforce.item_api.import_item",
                    
                        callback(r) {
                	frappe.msgprint({
			            title: __('Success'),
			            indicator: 'green',
			            message: __('Please check your ' + '<a onclick="window.open(this.href);return false;" href="/app/item"> Item </a>')
				});	
                		if (r.message) {
			                }
			         }
                    });
        }
    });