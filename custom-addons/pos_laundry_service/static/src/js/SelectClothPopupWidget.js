odoo.define('pos_laundry_service.SelectClothPopupWidget', function(require) {
    "use strict";

    const Popup = require('point_of_sale.ConfirmPopup');
    const Registries = require('point_of_sale.Registries');
    const PosComponent = require('point_of_sale.PosComponent');

    class SelectClothPopupWidget extends Popup {

        constructor() {
            super(...arguments);
        }

        go_back_screen() {
            this.trigger('close-popup');
        }

    };
    SelectClothPopupWidget.template = 'SelectClothPopupWidget';

    Registries.Component.add(SelectClothPopupWidget);

    return SelectClothPopupWidget;
});
