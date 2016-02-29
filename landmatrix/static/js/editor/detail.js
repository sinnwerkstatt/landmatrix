var openInvestorPopup = function(investorId) {
    if (typeof investorId === 'undefined') {
        investorId = 'add';
    }
    window.open("/en/stakeholder/" + investorId);
};

$(document).ready(function () {
    console.log('Deal Detail js loaded.');

    // TODO: Get Investor ID from Select and replace edit url


    var generateButtons = function(field) {
        var investorId = field.val();
        console.log("Heya:", field, investorId);

        var buttons = '<a onClick="openInvestorPopup()" href="javascript:void(0);" class="noul"><i class="lm lm-plus"></i></a>';
        buttons += '<a onClick="openInvestorPopup(' + investorId + ')" href="javascript:void(0);" class="noul"><i class="lm lm-pencil"></i></a>';
        var wrap = '<span class="investorops">' + buttons + '</span>';

        field.parent().find('.investorops').remove();
        field.parent().append(wrap);

    };

    $(".investorfield").each(function () {
        var investorId = $(this).val();
        $(this).select2({
            placeholder: 'Select Investor'
        });
        console.log('Investor:', investorId);
        generateButtons($(this));
        $(this).on('change', function () {
             generateButtons($(this));
        })
    });
});
