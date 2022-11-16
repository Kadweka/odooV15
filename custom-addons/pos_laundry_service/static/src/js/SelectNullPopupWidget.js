odoo.define('pos_laundry_service.SelectNullPopupWidget', function(require) {
    "use strict";

    const Popup = require('point_of_sale.ConfirmPopup');
    const Registries = require('point_of_sale.Registries');
    const PosComponent = require('point_of_sale.PosComponent');

    class SelectNullPopupWidget extends Popup {

        constructor() {
            super(...arguments);
        }

        go_back_screen() {
            this.trigger('close-popup');
        }

    };
    SelectNullPopupWidget.template = 'SelectNullPopupWidget';

    Registries.Component.add(SelectNullPopupWidget);

    return SelectNullPopupWidget;
});
