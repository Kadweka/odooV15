odoo.define('pos_laundry_service.WashingStageButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const { useState } = owl.hooks;


    class WashingStageButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }

        async onClick() {
            var washing_stages=[];
            var self=this;
            console.log("READ SELF:-",self);
            var washing_ids = this.env.pos.config.washing_stage_ids;

            var washing =   await this.rpc({
            model: 'washing.stage',
            method: 'search_read',
            args: [[['id', 'in',washing_ids]]],
            });

            var order = this.env.pos.get_order();
            var lines = order.get_orderlines();

            if(lines.length > 0) {
                var selected_line = order.get_selected_orderline();
                var product_id = selected_line.product.id;
//    			var urgent_product_id = self.env.pos.config.laundry_service_product[0];
//    			var delivery_id = self.env.pos.config.laundry_homedelivery[0];
                    console.log("washing",washing);
                    await  this.showPopup('WashingStagePopupWidget', {washing});
            }
            else{
                self.showPopup('SelectClothPopupWidget');
            }
        }
    }

    WashingStageButton.template = 'WashingStageButton';
    ProductScreen.addControlButton({
        component: WashingStageButton,
        condition: function() {
            return true;
        },
    });
    Registries.Component.add(WashingStageButton);
    return WashingStageButton;
});
