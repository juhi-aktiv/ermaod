odoo.define('sit_portal_dashboard.portal', function (require) {
'use strict';
var core = require('web.core');

    /*---- toogle password visibility--*/
    $(".toggle-password").click(function() {
      $(this).toggleClass("fa-eye fa-eye-slash");
      var input = $("#password")
      if (input.attr("type") == "password") {
        input.attr("type", "text");
      } else {
        input.attr("type", "password");
      }
    });
    /*--------check if the input login is filled-----------*/
    function check_login(){
    var login = $(".oe_login_form").find("input[name='login']")
        var password = $(".oe_login_form").find("input[name='password']")
        if($(login).val() == '' || $(password).val() == '')
        {
            $("button").attr("disabled",'disabled')
        }
        else{
            $("button").removeAttr("disabled")
        }
    }
    $("input").keyup(function(){
	    check_login()
    })
    $("input").blur(function(){
	    check_login();
    })
    $("input").focus(function(){
	    check_login()
    })
	check_login();
	/*-----Check inout value and given animation effect---*/
	function check_val(self){
        var input_val = $(self).val()
        if(input_val){
            $(self).parent().find(".cap_tran_label").css({"z-index":"99","top": "calc(90% - 46px)","opacity":"1","padding":"0px","padding-left":"4px","padding-right":"5px","background-color":"#fff","height":"21px","left":"23px","color":"#8b8b8b","font-size":"10px"})
        }
        else{
        $(self).parent().find(".cap_tran_label").css({"opacity":"0","z-index":"-1",})
        }
	}
	/*----------Display Save Button-------*/
	function display_button(self)
	{
	    var input_val = $(self).val()
	    var o_val = $(self).attr('data');
	    if($(self).val())
	    {
	        if(input_val.split(" ").join("").toLowerCase() != o_val.split(" ").join("").toLowerCase()){
	            $("#save_data").css("display","block")
	    }
	    }
	    else{
	        $("#save_data").css("display","none")
	    }
	}
    $( ".cap_hidden_input" ).each(function() {
        var self= this;
        check_val(self)

    })
    // Check on Keypress
    $(".cap_hidden_input").keypress(function(){
        var self=this
        check_val(self);
        display_button(self)
    })
    //Check on Keyup
    $(".cap_hidden_input").keyup(function(){
        var self = this
        check_val(self);
        display_button(self)
    })
    $("#save_data").click(function(ev){

        $("input").each(function(){
            var self = this
            if(!$(this).val())
            {
                $(self).addClass('s-error')
                return false;
            }
        })
        $("form").submit();
    })
    /*-----Loader----*/
    $(".s-li-style").click(function() {
        $(".s-fade-loader").addClass('se-pre-con')
        // Animate loader off screen
        $(".se-pre-con").fadeOut("slow");
    });

 })
