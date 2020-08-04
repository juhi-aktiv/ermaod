import odoo

from odoo import http, _
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.web.controllers.main import Home
from odoo.addons.web.controllers.main import ensure_db


class Home(Home):
    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' \
                and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            try:
                uid = request.session.authenticate(request.session.db, request.params['login'],
                                                   request.params['password'])
                request.params['login_success'] = True
                if request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
                    return http.redirect_with_hash(self._login_redirect(uid, redirect='/events'))
                else:
                    return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
            except odoo.exceptions.AccessDenied as e:
                request.uid = old_uid
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employee can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response


class WebsiteDashboard(http.Controller):
    @http.route('/events', type='http', auth="user", website=True)
    def sit_events(self, **kw):
        return request.render('sit_portal_dashboard.event_page')

    @http.route([
        '''/inventory''',
        '''/inventory/page/<int:page>'''],
        type='http', auth="user", website=True)
    def sit_inventory(self, page=0, ppg=False, **post):
        product_record = request.env['product.product'].sudo()\
            .search([('sale_ok', '=', True)])
        url = '/inventory'
        domain = []
        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        keep = QueryURL('/inventory',)
        search_product = product_record.search(domain)
        product_count = len(search_product)
        pager = request.website.pager(url=url,
                                      total=product_count, page=page,
                                      step=ppg, scope=7, url_args=post)
        products = product_record.search(domain, limit=ppg,
                                         offset=pager['offset'],)

        values = {
            'products': products,
            'pager': pager,
            'ppg': ppg,
            'keep': keep,
        }
        return request.render('sit_portal_dashboard.inventory_page', values)

    @http.route('/checklist', type='http', auth="user", website=True)
    def sit_checklist(self, **kw):
        return request.render('sit_portal_dashboard.checklist_page')

    @http.route('/feedback', type='http', auth="user", website=True)
    def sit_feedback(self, **kw):
        return request.render('sit_portal_dashboard.feedback_page')

    # CUSTOMER DETAILS CONTROLLER/ROUTE
    @http.route('/customer-details', type='http',
                auth="user", methods=['GET', 'POST'],
                website=True)
    def customer_details(self, **post):
        if post:
            company_record = request.env['res.company']
            company_id = post.get('company_id')
            company_data = company_record.sudo().browse(int(company_id))
            company_data.sudo().update({
                'name': post.get('name') or False
            })
        return request.render('sit_portal_dashboard.sit_portal_details')
