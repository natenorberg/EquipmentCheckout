$(function() {
    $("#id_out_time_0").datepicker();
    $("#id_in_time_0").datepicker();
    $("#id_out_time_1").timepicker({ 'timeFormat': 'H:i'});
    $("#id_in_time_1").timepicker({ 'timeFormat': 'H:i'});
    $("#dialog").dialog({
        autoOpen: false,
        modal: true,
        show: {
            effect: "fade",
            duration: 200
        },
        hide: {
            effect: "fade",
            duration: 200
        }
    });
});

$("#open_dialog").click(function() {
    selected_equipment = $(".equipment_list");
    $("#dialog").dialog("open");
});

//$("#reservation_form").submit(function(event) {
//    event.preventDefault();
//
////    var $form = $(this),
////      selected_equipment = $form.find("input[name='equipment']:checked").val(),
////      csrf_token = $form.find("input[name='csrfmiddlewaretoken']").val(),
////      url = "/checkout/reservations/add/check/";
//
//    var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
//
//    var labels = $('#id_equipment').find('input:checked').map(
//        function() {
//            return $(this).parent().text();
//        });
//
//    //var equipment_string = 'equipment';
//
//    $.ajax({
//        type: 'POST',
//        url: "/checkout/reservations/add/check/",
//        data: {'csrfmiddlewaretoken': csrf_token, 'equipment[]': labels},
//        dataType: 'html',
//        success: function(data) {
//            $("#dialog").empty().append(data);
//        },
//        error: function(data) {
//            alert("Error");
//        }
//    })
//
////    var posting = $.post(url, {'equipment': selected_equipment, 'csrfmiddlewaretoken': csrf_token});
////
////    posting.done(function(data) {
////        $("#dialog").empty().append(data);
////    });
//
//    $("#dialog").dialog("open");
//
//});
