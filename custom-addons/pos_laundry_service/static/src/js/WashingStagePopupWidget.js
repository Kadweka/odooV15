odoo.define('pos_laundry_service.WashingStagePopupWidget', function(require) {
    "use strict";

    const Popup = require('point_of_sale.ConfirmPopup');
    const Registries = require('point_of_sale.Registries');
    const PosComponent = require('point_of_sale.PosComponent');

    class WashingStagePopupWidget extends Popup {
        constructor(data = "") {
            super(...arguments);
        }

        go_back_screen() {
            this.trigger('close-popup');
        }

        get currentOrder(){
            return this.env.pos.get_order();
        }

        click_confirm(){
          var order    = this.env.pos.get_order();
  	    	var selected_line = order.get_selected_orderline();
  	    	var value = $('input[name="washing_type"]:checked').val();
  	    	var amount = $('input[name="washing_type"]:checked')[0].dataset.amount;
  	    	var wash_id = $('input[name="washing_type"]:checked')[0].dataset.id;
          selected_line.set_washing_stage(value);
  	    	selected_line.set_washing_amount(amount);
  	    	selected_line.set_washing_id(wash_id);
  	    	selected_line.set_unit_price(parseFloat(selected_line.product.lst_price) + parseFloat(amount));
  	    	this.trigger('close-popup');
        }
    };
    
    WashingStagePopupWidget.template = 'WashingStagePopupWidget';
    WashingStagePopupWidget.defaultProps = {
        washing: '',
    };
    Registries.Component.add(WashingStagePopupWidget);

    return WashingStagePopupWidget;
});
