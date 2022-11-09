// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Update Alt UOM', {
	// refresh: function(frm) {

	// }
	on_submit:function(frm){
		frappe.call({
			method: "aldaboos.aldaboos.doctype.update_alt_uom.update_alt_uom.update_alt_uom",
			args: {
				"uoms_list": frm.doc.uoms,
			},
			callback: function(r) {
				console.log(r.message);
			}
		})
	}
});
