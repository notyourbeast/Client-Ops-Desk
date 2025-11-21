from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify

from app.services.invoice_service import create_invoice_for_project, get_user_invoices, mark_user_invoice_paid
from app.services.project_service import get_user_projects
from app.utils.auth_decorators import login_required

invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')


@invoices_bp.route('', methods=['GET'])
@login_required
def list_invoices():
    user_id = str(g.current_user['_id'])
    invoices = get_user_invoices(user_id)
    projects = get_user_projects(user_id)

    project_map = {str(project['_id']): project for project in projects}

    for invoice in invoices:
        if invoice.get('project_id'):
            project = project_map.get(str(invoice['project_id']), {})
            invoice['project_name'] = project.get('title', 'Unknown Project')
        else:
            invoice['project_name'] = None

    filter_status = request.args.get('status', 'all')
    if filter_status == 'paid':
        invoices = [inv for inv in invoices if inv.get('status') == 'paid']
    elif filter_status == 'unpaid':
        invoices = [inv for inv in invoices if inv.get('status') == 'unpaid']

    return render_template('invoices/list.html', invoices=invoices, projects=projects, current_filter=filter_status)


@invoices_bp.route('', methods=['POST'])
@login_required
def create_invoice():
    user_id = str(g.current_user['_id'])
    project_id = request.form.get('project_id', '').strip()
    due_date = request.form.get('due_date', '').strip() or None

    if not project_id:
        flash('Project is required', 'error')
        return redirect(url_for('invoices.list_invoices'))

    invoice, error = create_invoice_for_project(user_id, project_id, due_date)
    if error:
        flash(error, 'error')
        return redirect(url_for('invoices.list_invoices'))

    flash('Invoice created successfully', 'success')
    return redirect(url_for('invoices.list_invoices'))


@invoices_bp.route('/<invoice_id>/mark-paid', methods=['POST'])
@login_required
def mark_paid(invoice_id):
    user_id = str(g.current_user['_id'])
    invoice, error = mark_user_invoice_paid(user_id, invoice_id)
    if error:
        return jsonify({'error': error}), 404

    return jsonify({'success': True, 'status': invoice['status']})

