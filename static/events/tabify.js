function display_tab_event(id_tab, event_id) {
    var nodeList = document.getElementsByTagName("textarea");
    for (var index = 0; index < nodeList.length; index++) {
        found_tab_id = nodeList.item(index).parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.id;
        if(found_tab_id != id_tab){
            $("#"+found_tab_id).empty();
        }
    }
     if( id_tab == "tab_new" ) { // Need to get the form for the new tab
        do_dajax(Dajaxice.events.edit_tab_get, Dajax.process, {'event_pk' : event_id.substr("event_".length)}, id_tab)
    } else if( id_tab.lastIndexOf("event_", 0) === 0 ) { // Need to get the event info form
        do_dajax(Dajaxice.events.edit_event_get, Dajax.process, {'event_pk' : id_tab.substr("event_".length)}, id_tab)
    } else if( id_tab.lastIndexOf("tab_", 0) === 0 ) { // Need to get the form for the particular tab (to edit)
        do_dajax(Dajaxice.events.edit_tab_get, Dajax.process, {'tab_pk' : id_tab.substr("tab_".length), 'event_pk' : event_id.substr("event_".length)}, id_tab)
    } 
}

function display_editor(textarea_id){
    path_to_editor_icons = $('#nicEditor_icons_path').val();
    $("#"+textarea_id).css({'width':'90%'});
	new nicEditor({iconsPath : '/static/img/nicEditorIcons.gif', maxHeight: 300, buttonList:
	                ['bold','italic','underline', 'indent', 'outdent']}).panelInstance(textarea_id);
	$(".nicEdit-panel").parent().parent().css({'width':'89.6%'});
	$('.nicEdit-main').bind('DOMSubtreeModified', function(){
	    editor_content = $(this).html();
	    $("#"+textarea_id).html(editor_content);
	});
}
