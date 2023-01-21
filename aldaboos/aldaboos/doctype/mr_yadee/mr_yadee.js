// Copyright (c) 2023, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mr Yadee', {
	setup: function (frm) {
		frm.set_query("uom", "items", function (doc, cdt, cdn) {
		  let row = locals[cdt][cdn];
		  return {
			query:
			  "erpnext.accounts.doctype.pricing_rule.pricing_rule.get_item_uoms",
			filters: {
			  value: row.item_code,
			  apply_on: "Item Code",
			},
		  };
		});
	}
})

frappe.ui.form.on('Mr Yadee Item', {
	item_code:function(frm, cdt, cdn){
		let row = locals[cdt][cdn];
		if(row.item_code){
			frappe.db.get_value("Item",{"item_code": row.item_code},"sales_uom").then(r=>{
				row.uom = r.message.sales_uom
				row.qty = 1;
				var sals_uom = r.message.sales_uom;

				if(frappe.db.get_value("Item Price", {"item_code":row.item_code, "selling":1, "uom":sals_uom}, "price_list_rate")){
					frappe.db.get_value("Item Price", {"item_code":row.item_code, "selling":1, "uom":sals_uom}, "price_list_rate").then(r=>{
						if(r.message.price_list_rate){
							//console.log(r.message.price_list_rate,sals_uom)
							let price = 0;
							price = r.message.price_list_rate
							row.rate = price;
							row.amount = row.qty * price
							frappe.call({
								method: "frappe.client.get",
								args: {
									doctype: "Item",
									name: row.item_code,
								},
								callback(r) {
									if(r.message) {
										var d = r.message;
										var uoms = d.uoms;
										for(var i=0;i<d.uoms.length;i++){
											if(uoms[i].uom == row.uom){
												row.conversion_factor = uoms[i].conversion_factor;
											}
										}
									}
								}
							});
							frm.refresh_fields("items");
							let total = 0
							let total_qty = 0
							for(let i in frm.doc.items){
								total += frm.doc.items[i].amount
								total_qty += frm.doc.items[i].qty
							} 
							frm.set_value("total", total);
							frm.set_value("total_qty", total_qty);
							frm.refresh();
						}
					});
				}
				frm.refresh_fields("items");
			});
			
		}
	},
	qty:function(frm, cdt, cdn){
		let row = locals[cdt][cdn];
		row.amount = row.qty * row.rate;
		frm.refresh_fields("items");
		let total = 0
		let total_qty = 0
		for(let i in frm.doc.items){
			total += frm.doc.items[i].amount
			total_qty += frm.doc.items[i].qty
		}
		frm.set_value("total", total)
		frm.set_value("total_qty", total_qty)
		frm.refresh();
	},
	rate:function(frm, cdt, cdn){
		let row = locals[cdt][cdn];
		row.amount = row.qty * row.rate;
		frm.refresh_fields("items");
		let total = 0
		let total_qty = 0
		for(let i in frm.doc.items){
			total += frm.doc.items[i].amount
			total_qty += frm.doc.items[i].qty
		}
		frm.set_value("total", total)
		frm.set_value("total_qty", total_qty)
		frm.refresh();
	},
	items_remove(frm,cdt,cdn){
		let total = 0
		let total_qty = 0
		for(let i in frm.doc.items){
				total += frm.doc.items[i].amount
				total_qty += frm.doc.items[i].qty
		}
		frm.set_value("total", total)
		frm.set_value("total_qty", total_qty)
		frm.refresh();
	},
	uom(frm, cdt, cdn){
	    let row = locals[cdt][cdn];
		row.rate = 0
		row.amount = 0
		row.conversion_factor = 1
		if(frappe.db.get_value("Item Price", {"item_code":row.item_code, "selling":1, "uom":row.uom}, "price_list_rate")){
			frappe.db.get_value("Item Price", {"item_code":row.item_code, "selling":1, "uom":row.uom}, "price_list_rate").then(r=>{
				if(r.message.price_list_rate){
					//console.log(r.message.price_list_rate,sals_uom)
					let price = 0;
					price = r.message.price_list_rate
					row.rate = price;
					row.amount = row.qty * price
					
					frappe.call({
						method: "frappe.client.get",
						args: {
							doctype: "Item",
							name: row.item_code,
						},
						callback(r) {
							if(r.message) {
								var d = r.message;
								var uoms = d.uoms;
								for(var i=0;i<d.uoms.length;i++){
									if(uoms[i].uom == row.uom){
										row.conversion_factor = uoms[i].conversion_factor;
									}
								}
							}
						}
					});
					frm.refresh_fields("items");
					let total = 0
					let total_qty = 0
					for(let i in frm.doc.items){
						total += frm.doc.items[i].amount
						total_qty += frm.doc.items[i].qty
					}
					frm.set_value("total", total)
					frm.set_value("total_qty", total_qty)
					frm.refresh();
				}
			});
		}
		frm.refresh_fields("items");
		
	}
});
