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
    /*$('#eventName').html("<dt>Name:</dt>" + "<dd>"+data.name+"</dd>");
    $('#eventDescription').html("<dt>Description:</dt>" + "<dd>"+data.description+"</dd>");
    $('#eventUpdate').html("<dt>Update:</dt>" + "<dd>"+data.update+"</dd>");*/
}

function parse_json_property(key, val) {
    /*
     * This function takes a key and value and does what is required with that pair
     */
    if( key == 'id_alert' ) { //  There was an urgent message to be shown ... show it.
        alert(val['type'] + " : " + val['msg'])
    } else {
        key_name = key.toLowerCase();
        key_name = key_name.charAt(0).toUpperCase() + key_name.slice(1); //gives the first letter as capital letter, rest small letters
        html_content = '<dl class="eventDetailsText dl-horizontal">' +
                       '<dt>' + key_name + ":" + '</dt>' +
                       '<dd>' + val + '</dd>' + '</dl>';
        $('#eventDetails').append(html_content);
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
