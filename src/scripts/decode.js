import * as Templates from './templates.js';

Handlebars.registerHelper('decodeUploadContent', decodeUploadContent);
export function decodeUploadContent(id, content) {
    return Templates.UPLOAD_CONTENT_TEMPLATE({
        'id': id,
        'content': content,
    });
}

Handlebars.registerHelper('decodeUploadButton', decodeUploadButton);
export function decodeUploadButton() {
    return Templates.UPLOAD_BUTTON_TEMPLATE();
}

Handlebars.registerHelper('decodeTransactions', decodeTransactions);
export function decodeTransactions(transactions) {
    return Templates.TRANSACTIONS_TEMPLATE(transactions);
}

Handlebars.registerHelper('sign', sign);
export function sign(amount) {
    return (parseFloat(amount) > 0) ? 'positive' : 'negative';
}

Handlebars.registerHelper('concat', concat);
export function concat(text) {
    return text.replaceAll(/\W/g, '');
}
