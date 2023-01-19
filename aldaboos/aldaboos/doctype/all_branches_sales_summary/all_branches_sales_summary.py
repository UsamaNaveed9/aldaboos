# Copyright (c) 2022, smb and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AllBranchesSalesSummary(Document):
	@frappe.whitelist()
	def get_branch_sales(self):
		#frappe.errprint(self.from_date)
		bws = []
		branches = ["Farwaniya Shop - KAD","Fahaheel Shop - KAD","Abbasiya Shop - KAD","Saffat shop - KAD"]
		mode_of_pay = ["Cash","Bank Draft"]
		total = 0
		for i in branches:
			if i == "Saffat shop - KAD":
				s = frappe.db.sql('''select sum(p.allocated_amount) as paid from `tabSales Invoice` as s inner join `tabPayment Entry Reference` as p on p.reference_name = s.name
                        	inner join `tabPayment Entry` as pe on p.parent = pe.name where pe.mode_of_payment = "Bank Draft" and s.cost_center = %s and s.docstatus = 1 group by s.cost_center''',i,as_dict=1)
				s = s[0]["paid"] if s else 0
				total += s 
				bws.append(s)
			s = frappe.db.sql('''select sum(p.allocated_amount) as paid from `tabSales Invoice` as s inner join `tabPayment Entry Reference` as p on p.reference_name = s.name
            		inner join `tabPayment Entry` as pe on p.parent = pe.name where pe.mode_of_payment = "Cash" and s.cost_center = %s and s.docstatus = 1 group by s.cost_center''',i,as_dict=1)
			s = s[0]["paid"] if s else 0
			total += s
			bws.append(s)
		#frappe.errprint(bws)
		self.branches_sale = []
		self.append("branches_sale",{
			"farwaniya_cash":bws[0],
			"fahaheel__cash":bws[1],
			"abbasiya_cash":bws[2],
			"saffat_bank":bws[3],
			"saffat_cash":bws[4],
			"total":total,
			"total1":total
		})
#		self.save()
#		self.reload()
