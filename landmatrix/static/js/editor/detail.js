var collapseState = 'hide';

$(document).ready(function () {


    $('.expandcollapse').click(function () {

        if (collapseState == 'hide') {
            collapseState = 'show';
        } else {
            collapseState = 'hide';
        }

        console.log("Expanding/collapsing: ", collapseState);
        $('.collapse').each(function(index) {
            $(this).collapse(collapseState);
        });


        if ($(this).html() == "<i class=\"icon-white icon-plus-sign\"></i> Expand All") {
            $(this).html("<i class=\"icon-white icon-minus-sign\"></i> Collapse All");
        }
        else {
            $(this).html("<i class=\"icon-white icon-plus-sign\"></i> Expand All");
        };
    });

    console.log("Detail.js loaded");

});
