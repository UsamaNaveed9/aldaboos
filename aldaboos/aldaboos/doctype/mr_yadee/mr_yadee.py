# Copyright (c) 2023, smb and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint
from frappe.model.document import Document

class MrYadee(Document):
	def before_save(self):
		t_qty = 0
		t_amount = 0
		for row in self.items:
			t_qty = t_qty + row.qty
			t_amount = t_amount + row.amount

		self.total_qty = t_qty
		self.total = t_amount	

	def before_submit(self):
		se = frappe.new_doc("Stock Entry")
		se.mr_yadee = self.name
		se.stock_entry_type = "Material Transfer"
		se.set_posting_time = 1
		se.posting_date = self.transaction_date
		se.from_warehouse = self.from_warehouse
		se.to_warehouse = self.to_warehouse

		for i in self.items:
			se_item = frappe.new_doc("Stock Entry Detail")
			se_item.s_warehouse = self.from_warehouse
			se_item.t_warehouse = self.to_warehouse
			se_item.item_code = i.item_code
			se_item.qty = i.qty
			se_item.uom = i.uom
			se_item.unit_price = i.rate
			se_item.s_amount = i.qty * i.rate
			if i.rate == 0:
				se_item.allow_zero_valuation_rate = 1
			se.append("items", se_item)	

		se.save()

	def submit(self):
		if len(self.items) > 5:
			msgprint(_("The task has been enqueued as a background job. In case there is any issue on processing in background, the system will add a comment about the error on this MR YADEE and revert to the Draft stage"))
			self.queue_action('submit', timeout=5000)
		else:
			self._submit()	
