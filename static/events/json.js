function display_event(json_got){
    //json_got = JSON.parse(json_got);
    //alert(json2txt(json_got, "/"))
    for (var key in json_got) {
        if (json_got.hasOwnProperty(key)) {
            parse_json_property(key, json_got[key])
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
