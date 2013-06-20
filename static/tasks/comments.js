
function comment(object_id){
    var comments_field_id = '#comments_field_task_' + object_id
    var comments_alert ='#comments_alert_task_'+ object_id
    var elementid = '#comments_table_task_' + object_id
        
    var comment = $(comments_field_id).val()
    if (comment=='') {
        $(comments_alert).show()
    }
    else {
        $(comments_field_id).val('')
        Dajaxice.tasks.comment(Dajax.process, {
                    'object_id' : object_id,
                    'comment' : comment,
                    'is_task' : is_task,
                    'elementid': elementid
        });
    }
}
 
    
