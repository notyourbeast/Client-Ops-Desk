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
        results = {'clients': [], 'projects': [], 'invoices': []}
        total_results = 0
    else:
        results = search_all(user_id, query)
        total_results = len(results['clients']) + len(results['projects']) + len(results['invoices'])
    
    # Check if this is an AJAX request for partial HTML
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return header and content for AJAX
        header_html = render_template('search/_results_header.html', query=query, total_results=total_results)
        content_html = render_template('search/_results_content.html', query=query, results=results, total_results=total_results)
        return header_html + content_html
    
    return render_template('search/results.html', 
                         query=query, 
                         results=results,
                         total_results=total_results)

