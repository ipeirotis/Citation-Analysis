(function () {
    "use strict";

    if(typeof jQuery === 'undefined')
        throw new Error("jQuery is required...");

    $("#retrieve").click(function (e) {
        // on submit, make a GET request to fetch "local" author data
        e.preventDefault();
        var form = $("#author-form");
        var retrieve_form = $("#retrieve-form");
        var author = $("#authorId").val().trim();
        retrieve_form.prop('action', retrieve_form.prop('action') + "/" + author);
        retrieve_form.submit();
    });
})();
