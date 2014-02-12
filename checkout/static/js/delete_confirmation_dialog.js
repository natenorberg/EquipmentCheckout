$(function() {
    $("#dialog").dialog({
        autoOpen: false,
        modal: true,
        show: {
            effect: 'fade',
            duration: 300
        },
        hide: {
            effect: 'hide',
            duration: 200
        },
        buttons: {
            Cancel: function() {
                $(this).dialog("close");
            },
            "Delete": function() {
                $("#delete").submit();
            }
        }
    });
});

$("#delete_button").click(function(event) {
    event.preventDefault();
    $("#dialog").dialog('open');
});