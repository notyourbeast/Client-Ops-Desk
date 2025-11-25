from app.repositories.client_repository import get_clients_for_user
from app.repositories.project_repository import get_projects_for_user
from app.repositories.invoice_repository import get_invoices_for_user
from app.services.project_service import get_user_projects
from app.services.client_service import get_user_clients


def search_clients(user_id, query):
    if not query or not query.strip():
        return []
    
    clients = get_user_clients(user_id)
    query_lower = query.lower().strip()
    
    results = []
    for client in clients:
        name_match = query_lower in (client.get('name') or '').lower()
        company_match = query_lower in (client.get('company') or '').lower()
        email_match = query_lower in (client.get('email') or '').lower()
        notes_match = query_lower in (client.get('notes') or '').lower()
        
        if name_match or company_match or email_match or notes_match:
            results.append(client)
    
    return results


def search_projects(user_id, query):
    if not query or not query.strip():
        return []
    
    projects = get_user_projects(user_id)
    query_lower = query.lower().strip()
    
    results = []
    for project in projects:
        title_match = query_lower in (project.get('title') or '').lower()
        description_match = query_lower in (project.get('description') or '').lower()
        
        if title_match or description_match:
            results.append(project)
    
    return results


def search_invoices(user_id, query):
    if not query or not query.strip():
        return []
    
    invoices = get_invoices_for_user(user_id)
    projects = get_user_projects(user_id)
    projects_map = {str(p['_id']): p for p in projects}
    
    query_lower = query.lower().strip()
    
    results = []
    for invoice in invoices:
        invoice_id_str = str(invoice.get('_id', ''))
        invoice_id_match = query_lower in invoice_id_str.lower()
        
        if invoice_id_match:
            results.append(invoice)
            continue
        
        amount_str = str(invoice.get('amount_due', 0))
        if query_lower in amount_str:
            results.append(invoice)
            continue
        
        status_match = query_lower in (invoice.get('status') or '').lower()
        if status_match:
            results.append(invoice)
            continue
        
        if invoice.get('project_id'):
            project = projects_map.get(str(invoice['project_id']))
            if project:
                project_title = (project.get('title') or '').lower()
                if query_lower in project_title:
                    results.append(invoice)
    
    return results


def search_all(user_id, query):
    if not query or not query.strip():
        return {
            'clients': [],
            'projects': [],
            'invoices': []
        }
    
    clients = search_clients(user_id, query)
    projects = search_projects(user_id, query)
    invoices = search_invoices(user_id, query)
    
    projects_with_client_names = []
    clients_map = {str(c['_id']): c for c in get_user_clients(user_id)}
    
    for project in projects:
        project_dict = dict(project)
        if project.get('client_id'):
            client = clients_map.get(str(project['client_id']))
            if client:
                project_dict['client_name'] = client.get('name', 'Unknown')
        projects_with_client_names.append(project_dict)
    
    invoices_with_project_names = []
    projects_map = {str(p['_id']): p for p in get_user_projects(user_id)}
    
    for invoice in invoices:
        invoice_dict = dict(invoice)
        if invoice.get('project_id'):
            project = projects_map.get(str(invoice['project_id']))
            if project:
                invoice_dict['project_name'] = project.get('title', 'Unknown Project')
        invoices_with_project_names.append(invoice_dict)
    
    return {
        'clients': clients,
        'projects': projects_with_client_names,
        'invoices': invoices_with_project_names
    }

