import * as Decode from './decode.js';

function initViewTransactionsButton() {

    function viewTransactions(
        readRegEx = true,
        tagUpdate = null,
    ) {

        var pattern = $('#textbox-pattern').val();
        var alias = $('#textbox-alias').val();
        var regex = (!readRegEx || pattern === '') ? null : {
            'pattern': pattern,
            'alias': alias || null,
        }

        $.ajax({
            data: JSON.stringify({
                'regex': regex,
                'tag_update': tagUpdate,
            }),
            contentType: 'application/json',
            dataType: 'json',
            method: 'POST',
            url: '/transactions',
            success: function(transactions) {

                if (transactions.transactions.length === 0) {
                    return;
                }

                $('#transactions').addClass('active');
                $('#transactions-body')[0].innerHTML = (
                    Decode.decodeTransactions(transactions)
                );

                $('#transactions .copy-button').each(function(i, button) {
                    $(button).click(function(event) {
                        i = button.id.replace(/^copy-button/, '');
                        navigator.clipboard.writeText(
                            transactions.transactions[i].clean_description
                        );
                        event.stopPropagation();
                    });
                });

                $('#transactions .tag').each(function(i, tag) {
                    $(tag).click(function(event) {

                        var tags = transactions.tags;
                        var currTag = $(tag).text();
                        var nextTag = tags[(tags.indexOf(currTag) + 1) % tags.length];
                        i = tag.id.replace(/^tag-/, '');

                        viewTransactions(
                            readRegEx=false,
                            tagUpdate={
                                'datum': transactions.transactions[i],
                                'new_tag': nextTag,
                            },
                        );
                        event.stopPropagation();

                    });
                });

                $('#button-regex').removeClass('disabled');
                $('#textbox-pattern').val('');
                $('#textbox-alias').val('');

            },
        });

    }

    $('#button-transactions').click(viewTransactions);
    $(document).on('keypress', function(event) {
        var isBudgeting = $('#index-nav-option-budgeting').hasClass('active');
        if (isBudgeting && event.which === 13) {
            viewTransactions();
        }
    });

}

function initInvestingTable() {

    var targetVTI = $('#textbox-target-VTI');
    var targetVXUS = $('#textbox-target-VXUS');

    var actualVTI = $('#actual-VTI');
    var actualVXUS = $('#actual-VXUS');

    var balanceVTI = $('#current-balance-VTI');
    var balanceVXUS = $('#textbox-current-balance-VXUS');
    var balanceTotal = $('#textbox-current-balance-total');

    var toInvestVTI = $('#to-invest-VTI');
    var toInvestVXUS = $('#to-invest-VXUS');
    var toInvestTotal = $('#textbox-to-invest-total');

    var toFullyRebalanceVTI = $('#to-fully-rebalance-VTI');
    var toFullyRebalanceVXUS = $('#to-fully-rebalance-VXUS');
    var toFullyRebalanceTotal = $('#to-fully-rebalance-total');

    var fullyRebalancedVTI = $('#fully-rebalanced-VTI');
    var fullyRebalancedVXUS = $('#fully-rebalanced-VXUS');
    var fullyRebalancedTotal = $('#fully-rebalanced-total');

    function isNumber(text, maxAfterDecimal = null) {

        var pattern;

        switch (maxAfterDecimal) {
            case null:
                pattern = /^[\d,]*$/;
                break;
            case Infinity:
                pattern = /^[\d,]*\.?\d*$/;
                break;
            default:
                pattern = new RegExp(String.raw`^[\d,]*\.?\d{0,${maxAfterDecimal}}$`);
        }

        return text !== '' && pattern.test(text);

    }

    function validateInput(textbox, condition) {

        textbox.prop('prevValue', textbox.val());

        textbox.on('input', function() {

            if (textbox.val() === '' || condition(textbox.val())) {
                textbox.prop('prevValue', textbox.val());
            } else {
                textbox.val(textbox.prop('prevValue'));
            }

        });

    }

    function get(textbox) {

        var isInput = textbox.is('input');
        var value = ((isInput) ? textbox.val() : textbox.text()).replaceAll(',', '');

        if (isNumber(value, Infinity)) {
            return Math.round(parseFloat(value));
        } else {
            return undefined;
        }

    }

    function set(textbox, value) {

        var isInput = textbox.is('input');

        if (typeof value === 'number') {
            value = Math.round(value);
            value = Number(value).toLocaleString();
        }

        return (isInput) ? textbox.val(value) : textbox.text(value);

    }

    function updateTable() {

        var targetVTIValue = get(targetVTI);
        var targetVXUSValue = get(targetVXUS);

        var actualVTIValue;
        var actualVXUSValue;

        var balanceVTIValue;
        var balanceVXUSValue = get(balanceVXUS);
        var balanceTotalValue = get(balanceTotal);

        var toInvestVTIValue;
        var toInvestVXUSValue;
        var toInvestTotalValue = get(toInvestTotal);

        var toFullyRebalanceVTIValue;
        var toFullyRebalanceVXUSValue;
        var toFullyRebalanceTotalValue;

        var fullyRebalancedVTIValue;
        var fullyRebalancedVXUSValue;
        var fullyRebalancedTotalValue;

        function hasFields(requiredFields) {

            var hasRequiredFields = true;

            $(requiredFields).each(function(i, textbox) {
                if (get(textbox) === undefined) {
                    hasRequiredFields = false;
                }
            });

            return hasRequiredFields;

        }

        $([
            actualVTI,
            actualVXUS,
            toInvestVTI,
            toInvestVXUS,
            toFullyRebalanceVTI,
            toFullyRebalanceVXUS,
            toFullyRebalanceTotal,
            fullyRebalancedVTI,
            fullyRebalancedVXUS,
            fullyRebalancedTotal,
        ]).each(function(i, textbox) {
            set(textbox, '-');
        });

        if (hasFields([
            balanceVXUS,
            balanceTotal,
        ])) {

            balanceVTIValue = balanceTotalValue - balanceVXUSValue;

            if (balanceVTIValue < 0) {
                return;
            }

            actualVTIValue = 100 * balanceVTIValue / balanceTotalValue;
            actualVXUSValue = 100 * balanceVXUSValue / balanceTotalValue;

            set(actualVTI, actualVTIValue);
            set(actualVXUS, actualVXUSValue);

            set(balanceVTI, balanceVTIValue);

        }

        if (hasFields([
            targetVTI,
            targetVXUS,
            balanceVTI,
            balanceVXUS,
            balanceTotal,
            toInvestTotal,
        ])) {

            fullyRebalancedTotalValue = Math.max(
                balanceTotalValue + toInvestTotalValue,
                balanceVTIValue * 100 / targetVTIValue,
                balanceVXUSValue * 100 / targetVXUSValue,
            );
            fullyRebalancedVTIValue = fullyRebalancedTotalValue * targetVTIValue / 100;
            fullyRebalancedVXUSValue = fullyRebalancedTotalValue * targetVXUSValue / 100;

            toFullyRebalanceVTIValue = fullyRebalancedVTIValue - balanceVTIValue;
            toFullyRebalanceVXUSValue = fullyRebalancedVXUSValue - balanceVXUSValue;
            toFullyRebalanceTotalValue = fullyRebalancedTotalValue - balanceTotalValue;

            toInvestVTIValue = toInvestTotalValue * toFullyRebalanceVTIValue / toFullyRebalanceTotalValue;
            toInvestVXUSValue = toInvestTotalValue * toFullyRebalanceVXUSValue / toFullyRebalanceTotalValue;

            set(toInvestVTI, toInvestVTIValue);
            set(toInvestVXUS, toInvestVXUSValue);

            set(toFullyRebalanceVTI, toFullyRebalanceVTIValue);
            set(toFullyRebalanceVXUS, toFullyRebalanceVXUSValue);
            set(toFullyRebalanceTotal, toFullyRebalanceTotalValue);

            set(fullyRebalancedVTI, fullyRebalancedVTIValue);
            set(fullyRebalancedVXUS, fullyRebalancedVXUSValue);
            set(fullyRebalancedTotal, fullyRebalancedTotalValue);

        }

    }

    $([
        targetVTI,
        targetVXUS,
        balanceVXUS,
        balanceTotal,
        toInvestTotal,
    ]).each(function(i, textbox) {

        textbox.on('input', function() {
            var value = get(textbox);
            if (value !== undefined) {
                textbox.val(value);
                set(textbox, value);
            }
        });
        validateInput(textbox, isNumber);

    });

    $([
        targetVTI,
        targetVXUS,
    ]).each(function(i, textbox) {

        // validateInput(textbox, isNumber);
        textbox.on('input', function() {

            var targetVTIValue = get(targetVTI);
            var targetVXUSValue = get(targetVXUS);

            if (textbox.is(targetVTI)) {
                if (targetVTIValue === 0) {
                    set(targetVTI, '');
                }
                set(targetVXUS, targetVTIValue ? 100 - targetVTIValue : '');
            }
            if (textbox.is(targetVXUS)) {
                if (targetVXUSValue === 0) {
                    set(targetVXUS, '');
                }
                set(targetVTI, targetVXUSValue ? 100 - targetVXUSValue : '');
            }

            updateTable();

        });

    });

    $([
        balanceVXUS,
        balanceTotal,
        toInvestTotal,
    ]).each(function(i, textbox) {

        textbox.on('input', updateTable);

    });

}

$(window).on('load', function() {

    initViewTransactionsButton();
    initInvestingTable();

});
