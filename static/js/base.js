
// DAJAXICE HANDLER
function dajaxice_id_handler(json_got) {
    // This is a function that does what ever is specified to the id, prop(erty), val(ue)
    // *** Note : this function is redundant after finding out about Dajax.process
    
    for(var element_i = 0; element_i < json_got.length; element_i+=1) {
        try {
            // Sanity checks
            if(! document.getElementById(json_got[element_i].id) ) {
                js_alert_show("error", "Unable to find ID : " + json_got[element_i].id + ", Notify the Webops team.");
                return;
            } else if( json_got[element_i].id == 'id_alert' ) {
                if( 'hide' in document.getElementById('id_alert').className.split(' ') ) {
                    js_alert_show(json_got[element_i].prop, json_got[element_i].val)
                } else {
                    js_alert_hide()
                    js_alert_show(json_got[element_i].prop, json_got[element_i].val)
                }
            } else {
                // Set the value ... for various divs
                document.getElementById(json_got[element_i].id)[json_got[element_i].prop] = json_got[element_i].val;
            }
        } catch (err) {
                js_alert_show("error", "Error found :" + err + ", Notify the Webops team.");
                return;
        }
    }
    //Dajaxice.tasks.shout(Dajax.process, {
    //    'shout' : shout_text
    //});
}

// MAJOR DIV HANDLING
function js_alert_show(alert_type, alert_msg) { // Alert type = success, info, error, warning
    // To show an alert using javascript
    // Note : this is redundant after the show_alert in misc.utilities was made
    document.getElementById('id_alert').className = 'alert alert-' + alert_type.toLowerCase();
    document.getElementById('id_alert').innerHTML = '<button onclick="javascript:js_alert_hide();">&times;</button>' +
        '<strong>' + alert_type.toUpperCase() + '!</strong> ' + alert_msg;
}

function js_alert_hide() {
    // Hide the alert with javascript
    // Note : this is used for the cross close button in the alert div
    document.getElementById('id_alert').className = 'alert hide';
    document.getElementById('id_alert').innerHTML = '';
}

function modal_hide() {
    // Hides the modal which is used for temp views
    document.getElementById('id_modal').className = 'modal hide';
    document.getElementById('id_modal').innerHTML = '';
    
    /* On hiding modal, refresh the page's right content based on which 
        tab is active on the left_content
    */
    str_tab_active = $("#id_content_left ul.nav li.active")[0].id
    str_tab_active = str_tab_active.substring("list_".length)
    Dajaxice.tasks.task_table(show_page, {'page' : str_tab_active})
}

// FORM SENDING -- Needs to be cleaned up unnecessary to have different
//              functions for all of them
function save_profile_form(v) { // v is id of the form in question
    // takes the edit profile form and gives it to dajaxice
    form_model = $(v).serialize(true);
    Dajaxice.users.edit_profile_post(Dajax.process, {'edit_form' : form_model});
}

function new_task_form(v) { // v is id of the form in question
    // takes the new task form and gives it to dajaxice
    form_model = $(v).serialize(true);
    Dajaxice.tasks.add_task_post(Dajax.process, {'page' : 'new_task', 'edit_form' : form_model});
}

function new_cross_task_form(v) { // v is id of the form in question
    // takes a cross task form and gives it to dajaxice
    form_model = $(v).serialize(true);
    Dajaxice.tasks.add_task_post(Dajax.process, {'page' : 'new_cross_task', 'edit_form' : form_model});
}
