from datetime import datetime
from bson import ObjectId

from app.repositories.db import get_db


def create_invoice(user_id, project_id, total_hours, amount_due, due_date):
    db = get_db()
    invoices = db.invoices

    invoice_doc = {
        'user_id': ObjectId(user_id),
        'project_id': ObjectId(project_id),
        'total_hours': total_hours,
        'amount_due': amount_due,
        'status': 'unpaid',
        'due_date': datetime.fromisoformat(due_date) if due_date else None,
        'created_at': datetime.utcnow()
    }

    result = invoices.insert_one(invoice_doc)
    invoice_doc['_id'] = result.inserted_id
    return invoice_doc


def get_invoices_for_user(user_id):
    db = get_db()
    invoices = db.invoices

    return list(invoices.find({'user_id': ObjectId(user_id)}).sort('created_at', -1))


def get_invoice_by_id(user_id, invoice_id):
    db = get_db()
    invoices = db.invoices

    return invoices.find_one({
        '_id': ObjectId(invoice_id),
        'user_id': ObjectId(user_id)
    })


def mark_invoice_paid(user_id, invoice_id):
    db = get_db()
    invoices = db.invoices

    result = invoices.update_one(
        {'_id': ObjectId(invoice_id), 'user_id': ObjectId(user_id)},
        {'$set': {'status': 'paid'}}
    )

    if result.matched_count == 0:
        return None

    return get_invoice_by_id(user_id, invoice_id)

