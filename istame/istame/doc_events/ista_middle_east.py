import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, add_days, getdate, get_time, time_diff_in_hours
import datetime
from datetime import  timedelta, date, time, datetime

def validate(self, method):
    calulate_total_hours(self, method)
    calculate_due_date(self, method)
    set_closed_by(self, method)
    send_new_ticket_email(self, method)
    # send_closed_ticket_email(self, method)
	
def set_closed_by(self, method):
    if self.status == "Closed":
        self.closed_by = frappe.session.user
        self.closure_date_time = frappe.utils.now()
    else:
        self.closed_by = ''
        self.closure_date_time = ''

def calculate_due_date(self, method):
        self.due_date_1 = (datetime.strptime(self.creation, "%Y-%m-%d %H:%M:%S.%f") + timedelta(hours=20))
        self.due_date_2 = (datetime.strptime(self.creation, "%Y-%m-%d %H:%M:%S.%f") + timedelta(hours=24))


def calulate_total_hours(self, method):
	if self.creation:
		self.total_hour =  format_duration(time_diff_in_hours(frappe.utils.now(), str(self.creation)))
            
def format_duration(duration):
    hours = int(duration)
    minutes = int((duration - hours) * 60)
    seconds = round((duration - hours - minutes / 60) * 3600)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def send_new_ticket_email(self, method):
    if self.status == "Open":
            recipients = []
            if self.sp_details_email:
                if self.priority == "Critical" and self.service_type ==  "Regulatory Adherence Queries":
                    cri_email = frappe.get_value("Service", self.service_type, "customer_service_agent")
                    recipients.append(cri_email),
                else:
                    recipients = self.sp_details_email.split(",\n")
                    recipients.append(self.building_email),
                    if self.priority == "Medium":
                        level2email = frappe.get_value("Service", self.service_type, "level_2_supervisor_email")
                        recipients.append(level2email),
                    if self.priority == "High":
                        level3email = frappe.get_value("Service", self.service_type, "level_3_supervisor_email")
                        level2email = frappe.get_value("Service", self.service_type, "level_2_supervisor_email")
                        recipients.append(level2email),
                        recipients.append(level3email),
                frappe.throw(f"recipients : {recipients}")
            header = "<p>Dear 'Sir/Mam'</p>"
            subject = "{0} - {1} - {2}".format(self.building_name , self.unit_number, self.service_type)
            body = """
                <table style="height: 82px;" border="1" width="100%">
                    <tbody>
                        <tr>
                            <td width="50%"><p>Call Time:</p></td>
                            <td width="50%"><p>{}</p></td>
                        </tr>
                        <tr>
                            <td width="50%"><p>Call Date:</p></td>
                            <td width="50%"><p>{}</p></td>
                        </tr>
                        <tr>
                            <td width="50%"><p>Agent Name:</p></td>
                            <td width="50%"><p>{}</p></td>
                        </tr>
                        <tr>
                            <td width="50%"><p>Contact Source:</p></td>
                            <td width="50%"><p>{}</p></td>
                        </tr>
                        <tr>
                            <td width="50%"><p>Caller Name</p></td>
                            <td width="50%"><p>{}</p></td>
                        </tr>
                        <tr>
                            <td width="50%"><p>Caller Contact Number</p></td>
                            <td width="50%"><p>{}</p></td>
                        </tr>
                        <tr>
                            <td width="50%"><p>Caller Email:</p></td>
                            <td width="50%"><p>{}</p></td>
                        </tr>
                            <tr>
                            <td width="50%"><p>Building Name:</p></td>
                            <td width="50%"><p>{}</p></td>
                        </tr>
                        </tr>
                            <tr>
                            <td width="50%"><p>Unit Number:</p></td>
                            <td width="50%"><p>{}</p></td>
                        </tr>
                        </tr>
                            <tr>
                            <td width="50%"><p>Service Type:</p></td>
                            <td width="50%"><p>{}</p></td>
                        </tr>
                        </tr>
                            <tr>
                            <td width="50%"><p>Priority:</p></td>
                            <td width="50%"><p>{}</p></td>
                        </tr>
                        </tr>
                            <tr>
                            <td width="50%"><p>Issue Description:</p></td>
                            <td width="50%"><p>{}</p></td>
                        </tr>
                    </tbody>  
                </table>
            """.format(self.call_time, self.call_date, self.agent_name, self.contact_source, self.caller_name, self.caller_contact_number, self.caller_email, self.building_name, self.unit_number, self.service_type, self.priority, self.issue_description)
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

def send_closed_ticket_email(self, method):
       if self.status == "Closed":
            recipients = []
            if self.caller_email:
                recipients.append(self.caller_email),
            
            header = "<p>Dear 'Sir/Mam'</p>"
            subject = "Escalation. Case Number {} Request due at : {}".format(self.name ,datetime.now().__format__('%Y-%m-%d %H:%M:%S'))
            body = """
            <p> This is to notify that the Ticket  has been open for 12 hours. Please take action.</p>	
                <table style="height: 82px;" border="1" width="100%">
                    <tbody>
                        <tr>
                            <td width="50%"><p>Zone:</p></td>
                            <td width="50%"><p></p></td>
                        </tr>
                        <tr>
                            <td width="50%"><p>Area:</p></td>
                            <td width="50%"><p></p></td>
                        </tr>
                        <tr>
                            <td width="50%"><p>Building Name:</p></td>
                            <td width="50%"><p></p></td>
                        </tr>
                        <tr>
                            <td width="50%"><p>Unit / Villa Number:</p></td>
                            <td width="50%"><p></p></td>
                        </tr>
                        <tr>
                            <td width="50%"><p>Service Type:</p></td>
                            <td width="50%"><p></p></td>
                        </tr>
                        <tr>
                            <td width="50%"><p>Client Name:</p></td>
                            <td width="50%"><p></p></td>
                        </tr>
                        <tr>
                            <td width="50%"><p>Client Contact Number:</p></td>
                            <td width="50%"><p></p></td>
                        </tr>
                            <tr>
                            <td width="50%"><p>Description:</p></td>
                            <td width="50%"><p></p></td>
                        </tr>
                    </tbody>  
                </table>
                <p>Please <a href="/desk#Form/Issue/">Click here</a> to view more details on the ticket. Make sure you update the status after you have completed the work.</p>
                <p><b>Note: </b>Do not respond to this email as this is system generated. If you have any questions then call +971 60 055 5667. </p>
            """
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