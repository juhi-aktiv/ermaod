odoo.define('sit_custom_recruitment.custom-form', function(require) {
	'use strict';

	var sAnimations = require('website.content.snippets.animation');
	var core = require('web.core');
	var _t = core._t;
	var ajax = require('web.ajax');
	var rpc = require('web.rpc')

    $(document).ready(function(){
    /*------------Form Sumission--------------------*/
        $("#custom_form_submit").click(function(){
        /*-----------Check required Fields-----------------*/
        $(".required_fields").each(function(){
            var self = this
            if($(this).val() == '')
            {
                $(self).addClass('sit_error')
            }
        })
        if($('sit_error').length){
            return false
        }
        var email_id = $("#hr_recruitment_form input[name='email_from']").val()
        var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        if(!regex.test(email_id)) {
          alert(_t("Please Enter Valid Email Address"))
          $("input[name='email_from']").val('')
          return false;
          }
        /*----------------Variables---------------*/
        var education_details = []
        var certification_details = []
        var professional_details = []

        /* ---------------Education Data------------------*/
        $("#hr_recruitment_form .mainedu_details").each(function(){
            var institute_id = false
            var institute_name = false
            if ($(this).find("select[name='institute_id']").length)
            {
                institute_id = $(this).find("select[name='institute_id']").val()
                if (institute_id == -1 || institute_id == 0){
                    if (institute_id == -1){
                        institute_name = $(this).find("input[name='institute_id']").val()
                    }
                    institute_id = false
                }
            }
            else
            {
                institute_name = $(this).find("input[name='institute_id']").val()
            }
            var type_id = $(this).find("select[name='type_id']").val()
            if (type_id == 0)
            {
                type_id = false;
            }
            var qualified_year = $(this).find("input[name='qualified_year']").val()

            var edu_dict = {
                'institute_id': institute_id,
                'institute_name': institute_name,
                'type_id': type_id,
                'qualified_year': qualified_year || false
            }

            education_details.push(edu_dict)
        });
        /*-------------------- Certification Data----------------*/
        $("#hr_recruitment_form .main_certificate_details").each(function(){
            var date = $(this).find("input[name='year']").val()
            var levels = $(this).find("input[name='levels']").val()
            var course_id = false
            var course_name = false
            if ($(this).find("select[name='course_id']").length)
            {
                course_id = $(this).find("select[name='course_id']").val()
                if (course_id == 0){
                    course_id = false
                }
            }
            else
            {
                course_name = $(this).find("input[name='course_id']").val()
            }
            var certificate_dict = {
                'course_id': course_id,
                'course_name': course_name,
                'levels': levels || false,
                'date': date || false
            }
            certification_details.push(certificate_dict)
        });
        /*--------------- Professional Experience---------------*/
        $("#hr_recruitment_form .prof_exp_details").each(function(){
            var location = $(this).find("input[name='location']").val()
            var from_date = $(this).find("input[name='from_date']").val()
            var to_date = $(this).find("input[name='to_date']").val()
            console.log("Date", $(this).find(".sit_s_date").val())
            if($(this).find(".sit_s_date").val() > $(this).find(".sit_e_date").val()){
               alert(_t("Start Date should less than end date"))
               return false
            }else{
               //end is less than start
            }
            var prof_dict = {
                'location': location || false,
                'to_date': to_date || false,
                 'from_date': from_date || false,
            }

            professional_details.push(prof_dict)
        });
    /*-------------Ajax Request for form Submission-----------------*/
    ajax.jsonRpc("/website_form_recruitment", 'call', {
                'partner_name' : $("#hr_recruitment_form input[name='partner_name']").val(),
                'email_from' : $("#hr_recruitment_form input[name='email_from']").val(),
                'partner_phone' : $("#hr_recruitment_form input[name='partner_phone']").val(),
                'job_id': $("#hr_recruitment_form input[name='job_id']").val(),
                'department_id': $("#hr_recruitment_form input[name='department_id']").val(),
                'salary_expected': $("#hr_recruitment_form input[name='salary_expected']").val(),
                'description': $("#hr_recruitment_form textarea[name='description']").val(),
                'education_ids': education_details,
                'certification_ids': certification_details,
                'profession_ids': professional_details,
        }).then(function (data) {
            window.location.replace('/job-thank-you');
        })
    })

        // On "other" add the char field
        function onchangesel(self){
            $(self).change(function(){
                if($(self).val() == -1){
                    if (!$(self).next("input.custom_added_class").length || $(self).next("input.custom_added_class").length == 0)
                    {
                        $('<input style="margin-top:10px;" type="text" name="'+ $(self).attr("for") +'" class="effect-2 custom_added_class form-control o_website_form_input" placeholder="'+ $(self).attr("data") +'" />').insertAfter($(self))
                        var input_val = $(self).next("input.custom_added_class").val()
                    }
                }
                else{
                    $(self).next("input.custom_added_class").remove()
                }
            })
        }
        $('select').each(function(){
            var self = this
            onchangesel(self)
        })

    // File Input Style
    var inputs = document.querySelectorAll('.file-input')
    for (var i = 0, len = inputs.length; i < len; i++) {
      customInput(inputs[i])
    }

    function customInput (el) {
      const fileInput = el.querySelector('[type="file"]')
      const label = el.querySelector('[data-js-label]')

      fileInput.onchange =
      fileInput.onmouseout = function () {
        if (!fileInput.value) return

        var value = fileInput.value.replace(/^.*[\\\/]/, '')
        el.className += ' -chosen'
        label.innerText = value
      }
    }
    // Ajax request for adding new Fields
    $(".add_details").click(function(){
        var detail_type = $(this).find("#details").val()
        ajax.jsonRpc("/add_details", 'call', {
                    'detail_type' : detail_type,
            }).then(function (data) {
            if (detail_type == 'edu'){
                $("#edu_details").append(data)
                $(document).on("click", '#remove_detail', function(event) {
                    $(this).parents('.mainedu_details').remove()
                });
                var inputs = document.querySelectorAll('.file-input')
                for (var i = 0, len = inputs.length; i < len; i++) {
                    customInput(inputs[i])
                }
                $('select').each(function(){
                    var self = this
                    onchangesel(self)
                })
            }
            if (detail_type == 'cert'){
                $("#cert_details").append(data)
                $(document).on("click", '#remove_detail', function(event) {
                    $(this).parents('.main_certificate_details').remove()
                });
                var inputs = document.querySelectorAll('.file-input')
                for (var i = 0, len = inputs.length; i < len; i++) {
                    customInput(inputs[i])
                }
                $('select').each(function(){
                    var self = this
                    onchangesel(self)
                })
            }
            if (detail_type == 'prof'){
                $("#prof_details").append(data)
                $(document).on("click", '#remove_detail', function(event) {
                    $(this).parents('.prof_exp_details').remove()
                });
                var inputs = document.querySelectorAll('.file-input')
                for (var i = 0, len = inputs.length; i < len; i++) {
                    customInput(inputs[i])
                }
            }
       })
    })
})
});