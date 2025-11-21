from app.repositories.invoice_repository import (
    create_invoice,
    get_invoices_for_user,
    get_invoice_by_id,
    mark_invoice_paid
)
from app.repositories.time_log_repository import get_time_logs_for_project
from app.repositories.project_repository import get_project_by_id


def create_invoice_for_project(user_id, project_id, due_date):
    project = get_project_by_id(user_id, project_id)
    if not project:
        return None, 'Project not found'

    if not project.get('hourly_rate'):
        return None, 'Project has no hourly rate set'

    time_logs = get_time_logs_for_project(user_id, project_id)
    total_minutes = sum(log.get('duration_minutes', 0) for log in time_logs if log.get('duration_minutes'))
    total_hours = round(total_minutes / 60, 2)
    amount_due = round(total_hours * project['hourly_rate'], 2)

    invoice = create_invoice(user_id, project_id, total_hours, amount_due, due_date)
    return invoice, None


def get_user_invoices(user_id):
    return get_invoices_for_user(user_id)


def get_user_invoice(user_id, invoice_id):
    invoice = get_invoice_by_id(user_id, invoice_id)
    if not invoice:
        return None, 'Invoice not found'
    return invoice, None


def mark_user_invoice_paid(user_id, invoice_id):
    invoice = mark_invoice_paid(user_id, invoice_id)
    if not invoice:
        return None, 'Invoice not found'
    return invoice, None

