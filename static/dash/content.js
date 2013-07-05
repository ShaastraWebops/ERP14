// default value of all buttons on the data-table button bar
var default_href_datatable = "javascript:alert(\"You need to choose a task first ! Do this by clicking on a row.\");" 

function fnGetSelected( oTableLocal ) { 
    // Function to get selected row from the table oTabelLocal
    // oTableLocal is an instance of the data-table class.
    // It searches for the row with 'row_selected' class
    var aReturn = new Array();
    var aTrs = oTableLocal.fnGetNodes();
            
    for ( var i=0 ; i<aTrs.length ; i++ ) {
        if ( $(aTrs[i]).hasClass('row_selected') ) {
            aReturn.push( aTrs[i] );
        }
    }
    return aReturn;
}


function show_table(oTable_element) { // show and initialize datatable
    /*
     * It initializes the data-table
     * Currently : 
     *      1. Makes each row selectable
     *      2. Datatable atrrs : JQueryUI_theme, Searchbar w/o text, button toolbar, auto width, sort
     *      3. Creates and Handles the button bar
     */
    
    if( oTable != null )    oTable.fnDestroy() // delete last instance of table
    // oTable_element is the table element which needs to be made data-table
    
    $("#" + oTable_element.id + " tbody").click(function(event) { 
        // Link the onclick event to the table to handle the click and selecting part
        $(oTable.fnSettings().aoData).each(function (){
            $(this.nTr).removeClass('row_selected');
        });
        if( event.target.nodeName == "TD" ) { // if links are present, gives an error
            $(event.target.parentNode).addClass('row_selected');
            // Change the Links to what is currently selected in You
            var sel_tr = fnGetSelected(oTable)[0]
            
            /* The new revamped code basically checks if the button exists first. 
             * This makes the function universal for cores, supercoords and coords.
             * And much more cleaner
             */
            
            if( sel_tr.getElementsByClassName('button_in_table_edit')[0] ) { // Edit button
                $("#button_" + oTable_element.id + " a.button_edit")[0].href = sel_tr.getElementsByClassName('button_in_table_edit')[0].href 
                $("#button_" + oTable_element.id + " a.button_edit")[0].onclick = sel_tr.getElementsByClassName('button_in_table_edit')[0].onclick
            }
            if( sel_tr.getElementsByClassName('button_in_table_status')[0] ) { // Status Upgrade button
                $("#button_" + oTable_element.id + " a.button_status")[0].href = sel_tr.getElementsByClassName('button_in_table_status')[0].href
                $("#button_" + oTable_element.id + " a.button_status")[0].onclick = sel_tr.getElementsByClassName('button_in_table_status')[0].onclick
            }    
            if( sel_tr.getElementsByClassName('button_in_table_del')[0] ) { // Status Upgrade button
                $("#button_" + oTable_element.id + " a.button_del")[0].href = sel_tr.getElementsByClassName('button_in_table_del')[0].href 
                $("#button_" + oTable_element.id + " a.button_del")[0].onclick = sel_tr.getElementsByClassName('button_in_table_del')[0].onclick
            }
            if( sel_tr.getElementsByClassName('button_in_table_subtaskDept')[0] ) { // Add dept Subtask Button
                $("#button_" + oTable_element.id + " a.button_subtaskDept")[0].href = sel_tr.getElementsByClassName('button_in_table_subtaskDept')[0].href 
                $("#button_" + oTable_element.id + " a.button_subtaskDept")[0].onclick = sel_tr.getElementsByClassName('button_in_table_subtaskDept')[0].onclick
            }
            if( sel_tr.getElementsByClassName('button_in_table_subtaskCross')[0] ) { // Add cross Subtask button
                $("#button_" + oTable_element.id + " a.button_subtaskCross")[0].href = sel_tr.getElementsByClassName('button_in_table_subtaskCross')[0].href 
                $("#button_" + oTable_element.id + " a.button_subtaskCross")[0].onclick = sel_tr.getElementsByClassName('button_in_table_subtaskCross')[0].onclick 
            }
            /* As pending has approve and disapprove buttons, and this makes it more universal,
             * The button's innerHTML is also taken care of by the table column for buttons.
             * 
             * As every row having a new innerHTML is unfeasible (as alignment issues come up)
             * It assumes all rows have the same buttons and innerHTMLs
             * Only the innerHTML of buttons of first row is taken and
             * put into the topbar's button's innerHTML : done at the end of function
             * 
            $("#button_" + oTable_element.id + " a.button_edit")[0].innerHTML = fnGetSelected(oTable)[0].getElementsByClassName('button_in_table_edit')[0].innerHTML
            $("#button_" + oTable_element.id + " a.button_del")[0].innerHTML = fnGetSelected(oTable)[0].getElementsByClassName('button_in_table_del')[0].innerHTML
            $("#button_" + oTable_element.id + " a.button_subtaskDept")[0].innerHTML = fnGetSelected(oTable)[0].getElementsByClassName('button_in_table_subtaskDept')[0].innerHTML
            $("#button_" + oTable_element.id + " a.button_subtaskCross")[0].innerHTML = fnGetSelected(oTable)[0].getElementsByClassName('button_in_table_subtaskCross')[0].innerHTML
            */
        }
    });
    
    // Get all columns with buttons and handle them in Searches and printing
    var cols = Array(), cols_table_tools = Array()
        th_cols = oTable_element.getElementsByTagName("thead")[0].getElementsByTagName("th")
        cols_len = th_cols.length
    for ( var col_i = 0; col_i < cols_len; col_i++ ) {
        // For universality between tables, get length from the table elements itself.
        if( ! $(th_cols[col_i]).hasClass('button_in_table') ) {
            cols.push(null);
            cols_table_tools.push(col_i)
        } else {
            cols.push({ "bSearchable": false }); // for Edit/Del & Subtask adding buttons
        }
    }
    
    
    oTable = $(oTable_element).dataTable( { // Initializes the table with necessary params
        "bJQueryUI" : true, // let jqueryUI handle rendering
        "bLengthChange" : false, // Don't show dropdown for number of entries to show on one page
        "bFilter" : true, // On the fly Search text-field on top right
        "bSort" : true, // Sorting by clicking on table header
        "bAutoWidth": true, // Auto fit the table columns
        "oLanguage": { "sSearch": "" } , // Remove the Search Label (for the text-field)
        "aoColumns": cols, // Choose which columns are used in Filter(Search) [[ needed to ignore button columns ]]
        "sDom": 'R<C>H<"clear"><"ui-toolbar ui-widget-header ui-corner-tl ui-corner-tr ui-helper-clearfix"<"#button_' + oTable_element.id + '">lfr>tT<"ui-toolbar ui-widget-header ui-corner-bl ui-corner-br ui-helper-clearfix"ip>',
        "oTableTools": {
            "sSwfPath": "/static/dash/datatables/swf/copy_csv_xls_pdf.swf",
            "aButtons": [ {
                    "sExtends": "copy",
                    "mColumns": cols_table_tools
                },
                {
                    "sExtends": "csv",
                    "mColumns": cols_table_tools
                },
                {
                    "sExtends": "pdf",
                    "mColumns": cols_table_tools
                },"xls" 
            ]
        }
        /*
         * The sDom is a complicated line. It holds what all is there on 
         * the table based on some coded html :P
         * basics : <"#aaa"> means add a div tag with id 'aaa' in that location
         *          <"aaa"> means add a div tag with class 'aaa' in that location
         *          R, <C>, H etc are inbuilt things for header, and stuff ... 
         *          t - table, f - filter-text-input, 
         *          ui-widget-header, etc are classes which jquery uses for the top-bar
         * 
         * For a better reference, look in the data-tables website for sDom
         */
    } );
    
    var first_tr = oTable_element.getElementsByTagName('tr')[1]
    if( first_tr.getElementsByTagName("td").length != 1 ) { 
        // add button bar only if there are some rows (i.e. it doesn't just have 1 row and 1 col with "no rows" msg)
        
        /*
         * As the btn top bar is created by data-tables (using sDom), we cannot put it's html in html. 
         * It needs to be done after the data-table is created. So, it is done here :
         * It goes through th first row and based on which all buttons it finds there, it sets the href 
         * as "default_href_datatable" and the innerHTML as what ever is given in thhe datatables
         */
        
        var btn_html =  "<div class='btn-group'>"; // Adds what to do with the buttons in the table
        if( first_tr.getElementsByClassName('button_in_table_edit')[0] ) { // Edit button
            btn_html +=         "<a class='btn btn-primary button_edit' href='" + default_href_datatable + "'>"
            btn_html +=             first_tr.getElementsByClassName('button_in_table_edit')[0].innerHTML
            btn_html +=         "</a>"
        }
        if( first_tr.getElementsByClassName('button_in_table_status')[0] ) { // Status Update button
            btn_html +=         "<a class='btn btn-success button_status' href='" + default_href_datatable + "'>"
            btn_html +=             first_tr.getElementsByClassName('button_in_table_status')[0].innerHTML
            btn_html +=         "</a>"
        }
        if( first_tr.getElementsByClassName('button_in_table_del')[0] ) { // Delete button
            btn_html +=         "<a class='btn btn-danger button_del' href='" + default_href_datatable + "'>"
            btn_html +=             first_tr.getElementsByClassName('button_in_table_del')[0].innerHTML
            btn_html +=         "</a>"
        }
        btn_html +=     "</div>"
        btn_html +=     "<div class='btn-group'>"
        if( first_tr.getElementsByClassName('button_in_table_subtaskDept')[0] ) { // Add dept subtask
            btn_html +=         "<a class='btn btn-info button_subtaskDept' href='" + default_href_datatable + "'>"
            btn_html +=             first_tr.getElementsByClassName('button_in_table_subtaskDept')[0].innerHTML
            btn_html +=         "</a>"
        }
        if( first_tr.getElementsByClassName('button_in_table_subtaskCross')[0] ) { // Add cross Subtask
            btn_html +=         "<a class='btn btn-inverse button_subtaskCross' href='" + default_href_datatable + "'>"
            btn_html +=             first_tr.getElementsByClassName('button_in_table_subtaskCross')[0].innerHTML
            btn_html +=         "</a>"
        }
        btn_html +=     "</div>"
        $("#button_" + oTable_element.id).html(btn_html);
    }
    
    /* Bootstrap is handling the resizing
    $(window).bind('resize', function () { // to resize table when window changed
          if( oTable != null )    oTable.dataTable.fnAdjustColumnSizing();
     } ); 
    */
}

function show_page(json_got) {
    /*
     * Used to render the right_content with dajax.
     * It handles the left_content based on ids
     * 
     * It expects that all elements from sidebar have "list_" in it's name
     * And that what ever is fetched from js has the id of the list without "list_"
     * 
     * If the data is table, it expects the id of the fetched div to be "table_*"
     * If the data is a random page, it expects the id of the fetched div to be "page_*"
     * 
     * e.g. of datatable : #sidebar li.id = "list_table_my_name" , #id_content_right div.id = "table_my_name"
     */
    
    Dajax.process(json_got) // Process the json
    
    var oDiv_element = document.getElementById('id_content_right').getElementsByTagName('div')[0]
    $("#id_content_left ul.nav li").removeClass("active") // de-activate all other elements
    $("#id_content_left ul.nav li").removeClass("active_head") // de-activate all other elements's head also ...
    $("#list_" + oDiv_element.id).addClass("active") // activate
    elem_body_classes = $("#list_" + oDiv_element.id).attr('class').split(" ")
    elem_str = ""
    elem_head_id = ""
    for ( var i = 0; i < elem_body_classes.length; i++ )
        if ( elem_body_classes[i].match("^list_") ) {
            elem_str = elem_body_classes[i].replace(/_body$/, ""); // The iden string
            elem_head_id = elem_body_classes[i].replace(/_body$/, "_head"); // the actual head id
        }
    if (elem_head_id) {
        $("#" + elem_head_id).addClass("active_head") // activate the head for the collapsible also ...
        if( ! $("#list_" + oDiv_element.id).hasClass("in") ) { // if accordion for active element is not open, open it.
            do_accordion(elem_str, "show")
        }
    } else { // this is a lone sidenav link
        //alert( "Not head found in collapsiblle ...")
    }
    
    // Check if div or table info -- extra processing ...
    if( oDiv_element.id.match("^form_") ) {
        if( oDiv_element.id.match("^form_new_task") || oDiv_element.id.match("^form_new_cross_task")) {
            $( '#id_deadline' ).datepicker({ 
                showAnim: 'slide', 
                dateFormat: 'd M yy', 
                /*showOn: "button",
                buttonImage: "images/calendar.gif",
                buttonImageOnly: true,*/
            });
        }
    } else if( oDiv_element.id.match("^table_") ) {
        // initiates datatable for task tables
        var oTable_element = oDiv_element.getElementsByTagName('table')[0]
        show_table(oTable_element)
    }
}

function do_accordion(elem_str, type) {
/*    e = e || window.event;
    e = e.target || e.srcElement;
    var ep = $(e).closest('li'), epid = ep.attr('id')
    alert(epid);
    if (ep.hasClass("active-head")) {
        // Close all children
        $(".list_"+epid.substring("list_head_".length)).collapse("hide");
        //$(".list_"+epid.substring("list_head_".length)).addClass("collapse");
        //$(".list_"+epid.substring("list_head_".length)).removeClass("on");
        // Show up arrow
        $(epid + " a i").removeClass("icon-chevron-down")
        $(epid + " a i").addClass("icon-chevron-up")
        // Change its own class
        $("list_head").removeClass("active-head")
    } else {
        // Close all children
        $(".list_"+epid.substring("list_head_".length)).collapse("show");
        //$(".list_"+epid.substring("list_head_".length)).addClass("on");
        //$(".list_"+epid.substring("list_head_".length)).removeClass("collapse");
        // Show up arrow
        $(epid + " a i").addClass("icon-chevron-down")
        $(epid + " a i").removeClass("icon-chevron-up")
        // Change its own class
        $("list_head").removeClass("active-head")
        ep.addClass("active-head")
        
    }
*/
    elem_id = "#" + elem_str + "_head"
    elem_class_body = "." + elem_str + "_body"
    elem_head = $(elem_str)
    if ( type == "hide" || type == "show" )
        $(elem_class_body).collapse(type)
    else
        $(elem_class_body).collapse('toggle')
    elem_head.addClass("active_head")
    
    elem_head_i = $(elem_id + " a i")
    if( elem_head_i.hasClass("icon-chevron-down") ) {
        elem_head_i.removeClass("icon-chevron-down")
        elem_head_i.addClass("icon-chevron-up")
    } else {
        elem_head_i.removeClass("icon-chevron-up")
        elem_head_i.addClass("icon-chevron-down")
        
    }
    
}
