function prepareErrorMessagesWithTitles(response){
    var errors = "";
    $.map(response.data, function(value, index) {
        errors = errors + "\n" + index + ": " + value;
    });
    return errors;
}

function prepareErrorMessages(response){
    var errors = "";
    $.map(response.data, function(value, index) {
        errors = errors + "\n" + value[0];
    });
    return errors;
}

function textareaAllowTabs(e) {
    var keyCode = e.keyCode || e.which;
    var tabValue = "    ";

    if (keyCode == 9) {
        e.preventDefault();
        var start = $(this).get(0).selectionStart;
        var end = $(this).get(0).selectionEnd;

        // set textarea value to: text before caret + tab + text after caret
        $(this).val($(this).val().substring(0, start)
            + tabValue
            + $(this).val().substring(end));

        // put caret at right position again
        $(this).get(0).selectionStart =
        $(this).get(0).selectionEnd = start + tabValue.length;
    }
}
