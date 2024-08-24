import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, add_days, getdate, get_time, time_diff_in_hours
import datetime
from datetime import  timedelta, date, time, datetime

def validate(self, method):
    calulate_total_hours(self, method)
    calculate_due_date(self, method)
    set_closed_by(self, method)
	
def set_closed_by(self, method):
    if self.status == "Resolved":
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