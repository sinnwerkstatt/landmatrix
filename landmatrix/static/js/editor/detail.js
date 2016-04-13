

$(document).ready(function () {
        console.log('Deal Detail js loaded.');

        // TODO: Get Investor ID from Select and replace edit url


        $(".investorfield").each(function (index) {
            console.log("Initializing investorfield with select and sankey.")
            var investorId = $(this).val();
            $(this).select2({
                placeholder: 'Select Investor'
            });
            /*
             var investorId = $(this).val();
             $(this).select2({
             placeholder: 'Select Investor',
             ajax: {
             url: '/api/investors.json',
             cache: true
             }
             });
             */
            console.log('Investor:', investorId);

            generateButtons($(this), index);

            $(this).on('change', function () {
                generateButtons($(this), index);
                loadSankey(index, $(this).val());
            });

            loadSankey(index, investorId);

        });
    });
