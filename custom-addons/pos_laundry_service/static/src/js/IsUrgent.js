odoo.define('pos_laundry_service.IsUrgent', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const { useState } = owl.hooks;

    class IsUrgent extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }

        async onClick() {
            var washing_stages=[];
            var self=this;
            console.log("Is Urgent:-",self);
            var washing_ids = this.env.pos.config.washing_stage_ids;

            var washing =   await this.rpc({
            model: 'washing.stage',
            method: 'search_read',
            args: [[['id', 'in',washing_ids]]],
            });

            var order = this.env.pos.get_order();
            var lines = order.get_orderlines();
        }
    }

    IsUrgent.template = 'IsUrgent';
    ProductScreen.addControlButton({
        component: IsUrgent,
        condition: function() {
            return true;
        },
    });
    Registries.Component.add(IsUrgent);
    return IsUrgent;
});
