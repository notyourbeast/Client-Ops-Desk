from flask import Blueprint, render_template, request, g

from app.services.search_service import search_all
from app.utils.auth_decorators import login_required

search_bp = Blueprint('search', __name__, url_prefix='/search')


@search_bp.route('', methods=['GET'])
@login_required
def search_results():
    user_id = str(g.current_user['_id'])
    query = request.args.get('q', '').strip()
    
    if not query:
        return render_template('search/results.html', 
                             query='', 
                             results={'clients': [], 'projects': [], 'invoices': []},
                             total_results=0)
    
    results = search_all(user_id, query)
    total_results = len(results['clients']) + len(results['projects']) + len(results['invoices'])
    
    return render_template('search/results.html', 
                         query=query, 
                         results=results,
                         total_results=total_results)

