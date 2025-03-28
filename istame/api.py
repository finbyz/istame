import frappe
from email.utils import formataddr
from frappe.utils import now , time_diff_in_hours, split_emails
from frappe.utils import nowdate, add_days, getdate, get_time, add_months
import datetime
from datetime import  timedelta, date, time , datetime

@frappe.whitelist()
def get_building_detail(building_name,service_type):
	if building_name and service_type:
		data = frappe.db.sql("""
			SELECT name
			FROM `tabBuilding` as b
			where b.building_name = '%s' and b.service_type = '%s'
        	limit 1
		""" % (building_name,service_type),as_dict=1)
		if data:
			return data

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def service_type_query(doctype, txt, searchfield, start, page_len, filters):
	conditions = []
	
	if txt:
		conditions="and building.service_type like '%{}%'".format(txt)
	else:
		conditions=''
	return frappe.db.sql("""select building.service_type 
	from `tabBuilding` as building 
	where building.building_name ='{building_name}' {conditions}
	 """.format(
		building_name=filters.get("building_name"),
		conditions=conditions
	))

def issue_validate(self,method):
	calculate_due_date(self)
	#escalation_email(self)

def calculate_due_date(self):
	default_holiday = frappe.db.get_value("Company","Ista Middle East",'default_holiday_list')
	holiday = frappe.get_doc("Holiday List",default_holiday)
	holiday_list =[row.holiday_date for row in holiday.holidays]

	due_date = getdate(self.opening_date)
	opening_time = get_time(self.opening_time)

	if due_date not in holiday_list:
		due_date = (datetime.datetime.combine(due_date, opening_time) + timedelta(hours=12))
	else:
		due_date = (datetime.datetime.combine(add_days(due_date,1), opening_time) + timedelta(hours=12))
	
	self.due_date = due_date

def escalation_email():
	data = frappe.get_list("Issue",filters = {'job_status_by_sp':['=','']},fields = 'name')
	for row in data:
		doc = frappe.get_doc("Issue",row.name)
		recipients = []
		if doc.due_date:
			if str(doc.due_date) <= now() and not doc.escalation_sent:
				if doc.sp_email_addresses:
					recipients = split_emails(doc.sp_email_addresses.replace("\n", ""))
				header = "<p>Dear {}</p>".format(doc.service_provider_name or 'Sir/Mam')
				subject = "Escalation. Case Number {} Request due at : {}".format(doc.name,doc.due_date)
				doc.db_set('escalation_sent',1)
				body = """
				<p> This is to notify that the Ticket {} has been open for 12 hours. Please take action.</p>	
					<table style="height: 82px;" border="1" width="100%">
						<tbody>
							<tr>
								<td width="50%"><p>Zone:</p></td>
								<td width="50%"><p>{}</p></td>
							</tr>
							<tr>
								<td width="50%"><p>Area:</p></td>
								<td width="50%"><p>{}</p></td>
							</tr>
							<tr>
								<td width="50%"><p>Building Name:</p></td>
								<td width="50%"><p>{}</p></td>
							</tr>
							<tr>
								<td width="50%"><p>Unit / Villa Number:</p></td>
								<td width="50%"><p>{}</p></td>
							</tr>
							<tr>
								<td width="50%"><p>Service Type:</p></td>
								<td width="50%"><p>{}</p></td>
							</tr>
							<tr>
								<td width="50%"><p>Client Name:</p></td>
								<td width="50%"><p>{}</p></td>
							</tr>
							<tr>
								<td width="50%"><p>Client Contact Number:</p></td>
								<td width="50%"><p>{}</p></td>
							</tr>
							 <tr>
								<td width="50%"><p>Description:</p></td>
								<td width="50%"><p>{}</p></td>
							</tr>
						</tbody>  
					</table>
					<p>Please <a href="/desk#Form/Issue/{}">Click here</a> to view more details on the ticket. Make sure you update the status after you have completed the work.</p>
					<p><b>Note: </b>Do not respond to this email as this is system generated. If you have any questions then call +971 60 055 5667. </p>
				""".format(
					doc.name,
					doc.zone or '',
					doc.area or '',
					doc.building_name or '',
					doc.unit_villa_number_ or '',
					doc.service_type or '',
					doc.client_name or '',
					doc.contact_mobile or '',
					doc.issue_description or '',
					doc.name
				)
				message = header + body
				if recipients:
					try:
						frappe.sendmail(
							recipients=recipients,
							cc = '',
							subject = subject ,
							#sender = sender,
							message = message,
							now = 1
						)
					except:
						frappe.log_error(f"Email is not sent : {recipients}")


	
def istame_overdue_email():
	data = frappe.get_list("Ista Middle East",filters = {'status':['!=','Closed']},fields = ['name', 'building_name','service_type'])
	for row in data:
		doc = frappe.get_doc("Ista Middle East",row.name)
		recipients = []
		if doc.due_date_2 is not None and doc.due_date_2 <= datetime.now() and doc.escalation_sent == "0":
				doc.db_set('escalation_sent', 1)
				if doc.sp_details_email:
					recipients = split_emails(doc.sp_details_email.replace("\n", ""))
				level_2_supervisor_email = frappe.get_value("Service",filters={'name': doc.service_type},fieldname='level_2_supervisor_email')					
				recipients.extend(split_emails(level_2_supervisor_email.replace("\n", "")))
				header = "<p>This is a warning notification for a second response time getting overdue at {}</p>".format(doc.due_date_2.strftime('%B %d %Y, %I:%M %p'))
				# subject = "SLA Escalation. Ticket Number {} Request due at : {}".format(doc.name,doc.due_date_2.strftime('%B %d %Y, %I:%M %p'))
				subject = "<p>Case Overdue - Case Number {0} - Building Name {1}</p>".format(doc.name, doc.building_name)

				
				body = """
				<p> This is to notify that the Ticket {0} has been open for 24 hours. Please take action.</p>	
					<ul>
					<li>Caller Name</li> : {1}
					<li>Contact Source</li> : {2}
					<li>Caller Contact No</li> : {3}
					<li>Caller Email</li> : {4}
					<li>Building Name</li> : {5}
					<li>Unit Number</li> : {6}
					<li>Service Type</li> : {7}
					<li>Priority</li> : {8}
					<li>Building Number</li>:{9}
					</ul>
            """.format(
		    			doc.name or '',
					doc.caller_name or '', 
					doc.contact_source or '', 
					doc.caller_contact_number or '', 
					doc.caller_email or '', 
					doc.building_name or '', 
					doc.unit_number or '', 
					doc.service_type or '', 
					doc.priority or '',
					doc.custom_building_number or ''
				)

				message = header + body
				if recipients:
					try:
						frappe.sendmail(
							recipients=recipients,
							cc = '',
							subject = subject ,
							#sender = sender,
							message = message,
							now = 1
						)
					except:
						frappe.log_error(f"Email is not sent : {recipients}  {doc.name}")

def istame_warning_email():
	data = frappe.get_list("Ista Middle East",filters = {'status':['!=','Closed']},fields = ['name', 'building_name','service_type'])
	for row in data:
		doc = frappe.get_doc("Ista Middle East",row.name)
		recipients = []
		if doc.due_date_1 is not None and doc.due_date_1 <= datetime.now() and doc.warning_sent == "0":
				doc.db_set('warning_sent', 1)
				if doc.sp_details_email:
					recipients = split_emails(doc.sp_details_email.replace("\n", ""))
				level_2_supervisor_email = frappe.get_value("Service",filters={'name': doc.service_type},fieldname='level_2_supervisor_email')					
				recipients.extend(split_emails(level_2_supervisor_email.replace("\n", ""))
				header = "<p>This is a warning notification for a first response time getting overdue at {}</p>".format(doc.due_date_1.strftime('%B %d %Y, %I:%M %p'))
				# subject = "SLA Escalation. Ticket Number {} Request due at : {}".format(doc.name,doc.due_date_1.strftime('%B %d %Y, %I:%M %p'))
				subject = "<p>Case Overdue - Case Number {0} - Building Name {1}</p>".format(doc.name, doc.building_name)
				body = """
					<p> This is to notify that the Ticket {0} has been open for 20 hours. Please take action.</p>
					<ul>
					<li>Caller Name</li> : {1}
					<li>Contact Source</li> : {2}
					<li>Caller Contact No</li> : {3}
					<li>Caller Email</li> : {4}
					<li>Building Name</li> : {5}
					<li>Unit Number</li> : {6}
					<li>Service Type</li> : {7}
					<li>Priority</li> : {8}
     				<li>Building Number</li>:{9}
					</ul>
			""".format(
					doc.name or '',
					doc.caller_name or '', 
					doc.contact_source or '', 
					doc.caller_contact_number or '', 
					doc.caller_email or '', 
					doc.building_name or '', 
					doc.unit_number or '', 
					doc.service_type or '', 
					doc.priority or '',
					doc.custom_building_number or ""
				)
				message = header + body
				if recipients:
					try:
						frappe.sendmail(
							recipients=recipients,
							cc = '',
							subject = subject ,
							#sender = sender,
							message = message,
							now = 1
						)
					except:
						frappe.log_error(f"Email is not sent : {recipients} {doc.name}")
