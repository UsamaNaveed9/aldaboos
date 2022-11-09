# Copyright (c) 2022, smb and contributors
# For license information, please see license.txt

import frappe
import json
from frappe import _, msgprint
from frappe.model.document import Document

class UpdateAltUOM(Document):
	def submit(self):
		if len(self.uoms) > 10:
			msgprint(_("The task has been enqueued as a background job. In case there is any issue on processing in background, the system will add a comment about the error on this Update Alternate UOM and revert to the Draft stage"))
			self.queue_action('submit', timeout=3000)
		else:
			self._submit()
						 
			
@frappe.whitelist(allow_guest=True)
def update_alt_uom(uoms_list):
	us = json.loads(uoms_list)
	e_uoms = dict()
	for i in us:
		e_uoms = frappe.db.sql(f"""SELECT uom
		FROM `tabUOM Conversion Detail` WHERE parent='{i['item_code']}' AND parentfield='uoms' AND parenttype='Item'; """, 
		as_dict=True)

		list_of_all_values = [value for elem in e_uoms
									for value in elem.values()]

		u1 = i.get("alt_1",None)
		if u1:
			if i['alt_1'] in list_of_all_values and i['value_alt_1'] > 0:
				frappe.db.sql(f"""UPDATE `tabUOM Conversion Detail`
				SET conversion_factor='{i['value_alt_1']}'
				WHERE uom='{i['alt_1']}' AND parent='{i['item_code']}' AND parentfield='uoms' AND parenttype='Item'; """)

				frappe.db.commit()
			else:
				add_uom = frappe.get_doc({"doctype": "UOM Conversion Detail",
					"uom": i['alt_1'],
					"conversion_factor": i['value_alt_1'],
					"parent": i['item_code'],
					"parentfield": "uoms",
					"parenttype": "Item"
				})

				add_uom.insert()
				frappe.db.commit()

		u2 = i.get("alt_2",None)
		if u2:
			if i['alt_2'] in list_of_all_values and i['value_alt_2'] > 0:
				frappe.db.sql(f"""UPDATE `tabUOM Conversion Detail`
				SET conversion_factor='{i['value_alt_2']}'
				WHERE uom='{i['alt_2']}' AND parent='{i['item_code']}' AND parentfield='uoms' AND parenttype='Item'; """)

				frappe.db.commit()
			else:
				add_uom = frappe.get_doc({"doctype": "UOM Conversion Detail",
					"uom": i['alt_2'],
					"conversion_factor": i['value_alt_2'],
					"parent": i['item_code'],
					"parentfield": "uoms",
					"parenttype": "Item"
				})

				add_uom.insert()
				frappe.db.commit()

		u3 = i.get("alt_3",None)
		if u3:
			if i['alt_3'] in list_of_all_values and i['value_alt_3'] > 0:
				frappe.db.sql(f"""UPDATE `tabUOM Conversion Detail`
				SET conversion_factor='{i['value_alt_3']}'
				WHERE uom='{i['alt_3']}' AND parent='{i['item_code']}' AND parentfield='uoms' AND parenttype='Item'; """)

				frappe.db.commit()
			else:
				add_uom = frappe.get_doc({"doctype": "UOM Conversion Detail",
					"uom": i['alt_3'],
					"conversion_factor": i['value_alt_3'],
					"parent": i['item_code'],
					"parentfield": "uoms",
					"parenttype": "Item"
				})

				add_uom.insert()
				frappe.db.commit()

		u4 = i.get("alt_4",None)	
		if u4:
			if i['alt_4'] in list_of_all_values and i['value_alt_4'] > 0:
				frappe.db.sql(f"""UPDATE `tabUOM Conversion Detail`
				SET conversion_factor='{i['value_alt_4']}'
				WHERE uom='{i['alt_4']}' AND parent='{i['item_code']}' AND parentfield='uoms' AND parenttype='Item'; """)

				frappe.db.commit()
			else:
				add_uom = frappe.get_doc({"doctype": "UOM Conversion Detail",
					"uom": i['alt_4'],
					"conversion_factor": i['value_alt_4'],
					"parent": i['item_code'],
					"parentfield": "uoms",
					"parenttype": "Item"
				})

				add_uom.insert()
				frappe.db.commit()

		u5 = i.get("alt_5",None)
		if u5:
			if i['alt_5'] in list_of_all_values and i['value_alt_5'] > 0:
				frappe.db.sql(f"""UPDATE `tabUOM Conversion Detail`
				SET conversion_factor='{i['value_alt_5']}'
				WHERE uom='{i['alt_5']}' AND parent='{i['item_code']}' AND parentfield='uoms' AND parenttype='Item'; """)

				frappe.db.commit()
			else:
				add_uom = frappe.get_doc({"doctype": "UOM Conversion Detail",
					"uom": i['alt_5'],
					"conversion_factor": i['value_alt_5'],
					"parent": i['item_code'],
					"parentfield": "uoms",
					"parenttype": "Item"
				})

				add_uom.insert()
				frappe.db.commit()

														

	return e_uoms,list_of_all_values,u1,u2,u3,u4,u5