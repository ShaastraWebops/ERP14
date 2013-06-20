
jQuery(function() {
    jQuery("#id_deadline").datepicker({ dateFormat: 'dd/mm/yy' });
});
Dajaxice.tasks.display_task_get(Dajax.process, { 'primkey':'{{task.pk}}' })
