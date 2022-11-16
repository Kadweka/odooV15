odoo.define('pos_laundry_service.ProductNotePopupWidget', function(require) {
    "use strict";

    const Popup = require('point_of_sale.ConfirmPopup');
    const Registries = require('point_of_sale.Registries');
    const PosComponent = require('point_of_sale.PosComponent');

    class ProductNotePopupWidget extends Popup {

      constructor() {
          super(...arguments);
      }

      go_back_screen() {
          this.trigger('close-popup');
      }
      async mounted() {
            var order    = this.env.pos.get_order();
          var selected_line = order.get_selected_orderline();
          $('textarea#textarea_note').focus();
            $('textarea#textarea_note').html(selected_line.get_line_note());

      }

      note_done(){
        var order    = this.env.pos.get_order();
        var selected_line = order.get_selected_orderline();
        var value = $('#textarea_note').val();
        selected_line.set_line_note(value);
        this.trigger('close-popup');
      }
    };
    ProductNotePopupWidget.template = 'ProductNotePopupWidget';

    Registries.Component.add(ProductNotePopupWidget);

    return ProductNotePopupWidget;
});
