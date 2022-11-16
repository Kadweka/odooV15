odoo.define('pos_laundry_service.AddNoteButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const { useState } = owl.hooks;

    class AddNoteButton extends PosComponent {
      constructor() {
          super(...arguments);
      }
      
      button_click(){
          var order    = this.env.pos.get_order();
          var lines    = order.get_orderlines();
          if(lines.length > 0) {
              var selected_line = order.get_selected_orderline();
              if (selected_line) {
                this.showPopup('ProductNotePopupWidget');
              }
          } else {
              alert("Please select the product !");
          }
      }
    }
    AddNoteButton.template = 'AddNoteButton';

    ProductScreen.addControlButton({
        component: AddNoteButton,
        condition: function() {
            return this.env.pos.config.enable_product_note;
        },
    });

    Registries.Component.add(AddNoteButton);

    return AddNoteButton;
});
