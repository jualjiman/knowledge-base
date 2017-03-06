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
