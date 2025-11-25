from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify

from app.services.invoice_service import create_invoice_for_project, get_user_invoices, mark_user_invoice_paid, get_user_invoice
from app.services.project_service import get_user_projects
from app.services.client_service import get_user_clients
from app.utils.auth_decorators import login_required

invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')


@invoices_bp.route('', methods=['GET'])
@login_required
def list_invoices():
    user_id = str(g.current_user['_id'])
    invoices = get_user_invoices(user_id)
    projects = get_user_projects(user_id)
    clients = get_user_clients(user_id)

    project_map = {str(project['_id']): project for project in projects}
    client_map = {str(client['_id']): client for client in clients}

    for invoice in invoices:
        if invoice.get('project_id'):
            project = project_map.get(str(invoice['project_id']), {})
            invoice['project_name'] = project.get('title', 'Unknown Project')
            if project.get('client_id'):
                invoice['client_name'] = client_map.get(str(project['client_id']), {}).get('name', 'Unknown')
            else:
                invoice['client_name'] = None
        else:
            invoice['project_name'] = None
            invoice['client_name'] = None

    search_query = request.args.get('search', '').strip()
    client_filter = request.args.get('client', '').strip()
    filter_status = request.args.get('status', 'all')

    if search_query:
        query_lower = search_query.lower()
        invoices = [inv for inv in invoices if 
                   query_lower in str(inv.get('_id', '')).lower() or
                   query_lower in (inv.get('project_name') or '').lower() or
                   query_lower in str(inv.get('amount_due', 0)).lower() or
                   query_lower in (inv.get('status') or '').lower()]

    if client_filter:
        filtered_invoices = []
        for inv in invoices:
            if inv.get('project_id'):
                project = project_map.get(str(inv['project_id']), {})
                if project.get('client_id') and str(project['client_id']) == client_filter:
                    filtered_invoices.append(inv)
        invoices = filtered_invoices

    if filter_status == 'paid':
        invoices = [inv for inv in invoices if inv.get('status') == 'paid']
    elif filter_status == 'unpaid':
        invoices = [inv for inv in invoices if inv.get('status') == 'unpaid']

    return render_template('invoices/list.html', 
                         invoices=invoices, 
                         projects=projects, 
                         clients=clients,
                         current_filter=filter_status,
                         search_query=search_query,
                         client_filter=client_filter)


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


@invoices_bp.route('/<invoice_id>', methods=['GET'])
@login_required
def view_invoice(invoice_id):
    user_id = str(g.current_user['_id'])
    invoice, error = get_user_invoice(user_id, invoice_id)
    
    if error:
        flash(error, 'error')
        return redirect(url_for('invoices.list_invoices'))
    
    projects = get_user_projects(user_id)
    project = None
    if invoice.get('project_id'):
        project = next((p for p in projects if str(p['_id']) == str(invoice['project_id'])), None)
    
    return render_template('invoices/detail.html', invoice=invoice, project=project)

