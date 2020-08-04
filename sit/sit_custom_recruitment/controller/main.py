from odoo import http
from odoo.http import request
import json
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.exceptions import ValidationError
from psycopg2 import IntegrityError
import base64


class WebsiteFormRecruitment(WebsiteForm):
    @http.route('/website_form_recruitment', type='json', auth="public", methods=['POST'], website=True)
    def website_form(self, **kwargs):

        '''Variabls'''

        institute_record = request.env['hr.institute'].sudo()
        applicant_record = request.env['hr.applicant'].sudo()
        education_record = request.env['employee.education'].sudo()
        institute_record = request.env['hr.institute'].sudo()
        course_record = request.env['cert.cert'].sudo()
        education_ids = kwargs.get('education_ids') or False
        certification_ids = kwargs.get('certification_ids') or False
        profession_ids = kwargs.get('profession_ids') or False
        certification_obj = request.env['employee.certification'].sudo()
        employee_profession_obj = request.env['employee.profession'].sudo()

        '''Dictionary for the Applicant Record'''
        vals = {
            'partner_name': kwargs.get('partner_name') or False,
            'name': kwargs.get('partner_name') or False,
            'email_from': kwargs.get('email_from') or False,
            'partner_phone': kwargs.get('partner_phone') or False,
            'stage_id': request.env.ref('hr_recruitment.stage_job1').sudo().id,
            'job_id': kwargs.get('job_id') and int(kwargs.get('job_id')) or False,
            'department_id': kwargs.get('department_id') and int(kwargs.get('department_id')) or False,
            'description': kwargs.get('description') or False,
            'salary_expected': kwargs.get('salary_expected') or False,
        }

        applicant = applicant_record.create(vals)

        '''Education Details'''

        for education_data in education_ids:
            if not all(values == False for values in education_data.values()):
                edu_vals = {
                    'applicant_id': applicant.id,
                    'type_id': education_data['type_id'] and int(education_data['type_id']) or False,
                    'qualified_year': education_data['qualified_year'] and education_data['qualified_year'] or False
                }

                if education_data['institute_id'] or not education_data['institute_name']:
                    edu_vals['institute_id'] = education_data['institute_id'] and int(
                        education_data['institute_id']) or False
                else:
                    institute = institute_record.create(
                        {'name': education_data['institute_name']})
                    edu_vals['institute_id'] = institute.id
                education = education_record.create(edu_vals)

        '''Certification Details'''
        if certification_ids:
            for certification_data in certification_ids:
                if not all(values == False for values in certification_data.values()):
                    cert_vals = {
                        'applicant_id': applicant.id,
                        'year': certification_data['date'] and certification_data['date'] or False,
                        'levels': certification_data['levels'] and certification_data['levels'] or False
                    }
                    if certification_data['course_id'] or not certification_data['course_name']:
                        cert_vals['course_id'] = certification_data['course_id'] and int(
                            certification_data['course_id']) or False
                    else:
                        course = course_record.create(
                            {'name': certification_data['course_name']})
                        cert_vals['course_id'] = course.id
                    certification = certification_obj.create(cert_vals)

        '''Professional Experience'''

        for profession_data in profession_ids:
            if not all(values == False for values in profession_data.values()):
                prof_vals = {
                    'applicant_id': applicant.id,
                    'from_date': profession_data['from_date'] and profession_data['from_date'] or False,
                    'to_date': profession_data['to_date'] and profession_data['to_date'] or False,
                    'location': profession_data['location'] and profession_data['location'] or False
                }
                employee_profession_obj.sudo().create(prof_vals)
        return True


class Details(http.Controller):
    @http.route('/add_details', type='json', auth='public', website=True)
    def add_details(self, detail_type=None):
        View = request.env['ir.ui.view'].sudo()
        if detail_type == 'edu':
            return View.render_template('sit_custom_recruitment.education_details')
        if detail_type == 'cert':
            return View.render_template('sit_custom_recruitment.certification_details')
        if detail_type == 'prof':
            return View.render_template('sit_custom_recruitment.profession_details')