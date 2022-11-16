odoo.define('pos_laundry_service.WashingErrorPopupWidget', function(require) {
    "use strict";

    const Popup = require('point_of_sale.ConfirmPopup');
    const Registries = require('point_of_sale.Registries');
    const PosComponent = require('point_of_sale.PosComponent');

    class WashingErrorPopupWidget extends Popup {

        constructor() {
            super(...arguments);
        }

        go_back_screen() {
            this.trigger('close-popup');
        }

    };
    WashingErrorPopupWidget.template = 'WashingErrorPopupWidget';

    Registries.Component.add(WashingErrorPopupWidget);

    return WashingErrorPopupWidget;
});
