function display_tab_event(id_tab) {
     if( id_tab == "tab_new" ) { // Need to get the form for the new tab
        do_dajax(Dajaxice.events.new_tab, Dajax.process, {'event_pk' : id_tab.substr("event_".length)}, 'id_tab')
    } else if( id_tab.lastIndexOf("event_", 0) === 0 ) { // Need to get the event info form
        do_dajax(Dajaxice.events.edit_event_get, Dajax.process, {'event_pk' : id_tab.substr("event_".length)}, 'id_tab')
    } else if( id_tab.lastIndexOf("tab_", 0) === 0 ) { // Need to get the form for the particular tab (to edit)
        
    } 
}
