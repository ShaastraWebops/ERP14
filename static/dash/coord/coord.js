var oTable = null // table variable

function give_dajax(el) {
    /*
     * An elegant solution to the sidebar, but it never worked properly ... 
     * This reutnr the Window ?
     */
    alert(el)
    var page_name = el.parentElement.id.substring("list_".length)
    Dajaxice.tasks.add_task(show_page, {'page' : page_name})
}
