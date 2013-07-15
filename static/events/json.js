function display_event(json_got){
    //json_got = JSON.parse(json_got);
    //alert(json2txt(json_got, "/"))
    
    //if there is any key-value pair to display, then remove loading.gif and display basic layout for event details
    if(Object.getOwnPropertyNames(json_got)){
        event_details_html = '<div id="eventDetailsContainer">' +
                                '<center>' +
                                    '<h3 style="color:#758FB2; text-decoration: underline">Event Details</h3>' +
                                    '<div id="eventDetails">' + 
                                         '<br />'+
                                    '</div>' +
                                    '<a class="btn btn-primary" href="#" onclick="do_dajax(Dajaxice.events.edit_event_get, Dajax.process, {\'event_name\' : \'test\'}, \'id_content\');"> Edit Event Details </a>' + 
                                 '</center>';
        $('#id_content').html(event_details_html);
    }
    else{
        event_details_html = 'No event detail to display. Check again later.'
        $('#id_content').html(event_details_html);
    }
    
    for (var key in json_got) {
        if (json_got.hasOwnProperty(key)) {
            parse_json_property(key, json_got[key]);
        }
    }
}

function display_event_erp(json_got){
    /* show_page - the universal js function to handle all sidebar dajaxice 
     * handles the populating of the div with the necessary html
     * This function will just create the fields for the event
     */
    json_got = JSON.parse(json_got);
    for (var key in json_got) {
        if (json_got.hasOwnProperty(key) && key.match("^event_")) {
            parse_json_property(key.slice(6), json_got[key], 'eventDetails');
        }
    }
}

function display_tab_erp(json_got, tab_pk){
    /*
     * This function gets the tab details from json_got and 
     * populates the corresponding tab div
     */
     //json_got = JSON.parse(json_got);
     //tab_dest_id = 'tab' + tab_pk.toString() + 'Details';
     tab_dest_id = 'tab_' + tab_pk.toString();
     $('#'+tab_dest_id).html('')
     for (var key in json_got) {
        if (json_got.hasOwnProperty(key) && key.match("^tab"+ tab_pk.toString() +"_")) {
            parse_json_property(key.slice(5), json_got[key], tab_dest_id);
        }
    }
}

function display_tab_event_erp(json_got, destId){
    /*
     * This function populates the destId with the appropriate content.
     * json_got gives all necessary content about events and tabs.
     *
     * destId must be of the form 'event_<pk>' or 'tab_<pk>'
     *
     * html has been added such that the event/tab display is consistent with edit_form.html
     */
     var pattern; // holds the pattern to match in json_got to retrieve appropriate data
     var name;
     
     if( destId.match('^event_') ){
        pattern = "event_";
        name = "Event";
     }
     else if( destId.match('^tab_') ){
        pattern = "tab" + destId.slice(4) + "_"; // destId.slice(4) gives the tab's pk
        name = "Tab"
     }
     
     $('#'+destId).html('<table class="table table-hover table-bordered">' +
                            '<caption><h3 style="color:#758FB2;">'+name+' Details</h3></caption>' +
                            '<tbody>');
     
     for (var key in json_got) {
        if (json_got.hasOwnProperty(key) && key.match("^"+pattern)) {
            parse_json_property(key.slice(pattern.length), json_got[key], destId);
        }
     }
    
    // adding 'Edit' button to edit data
    $('#'+destId).append("<button class='btn btn-info' onclick=javascript:display_tab_event('"+destId+"');> Edit </button>");
}

function parse_json_property(key, val, destId) {
    /*
     * This function takes a key and value and does what is required with that pair
     * destId holds the destination id where the content has to be displayed
     */
    if( key == 'id_alert' ) { //  There was an urgent message to be shown ... show it.
        alert(val['type'] + " : " + val['msg'])
    } else {
        key_name = key.toLowerCase();
        key_name = key_name.charAt(0).toUpperCase() + key_name.slice(1); // gives the first letter as capital letter, rest small letters
        /*html_content = '<dl class="contentDetailsText dl-horizontal">' +
                       '<dt>' + key_name + ":" + '</dt>' +
                       '<dd>' + val + '</dd>' + '</dl>';*/
        html_content = '<tr style="height:57px;">' +
                       '<th style="width:241px;"> <label>' + key_name + ":" + '</label> </th>' +
                       '<td>' + val + '</td>' +
                       '</tr>';
        $('#'+destId).find("table").append(html_content);
    }
}

function json2txt(obj, path) {
    var txt = '';
    for (var key in obj) {
        if (obj.hasOwnProperty(key)) {
            if ('object' == typeof(obj[key])) {
                txt += json2txt(obj[key], path + (path ? '.' : '') + key);
            } else {
                txt += path + '.' + key + '\t' + obj[key] + '\n';
            }
        }
    }
    return txt;
}
