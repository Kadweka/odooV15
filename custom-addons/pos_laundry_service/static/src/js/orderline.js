odoo.define('pos_laundry_service.Custom_Orderline', function (require) {
"use strict";
    var pos_model = require('point_of_sale.models');
    var core = require('web.core');
    var _t = core._t;
    var SuperOrder = pos_model.Order;
    const ProductScreen = require('point_of_sale.ProductScreen');
    var SuperOrderline = pos_model.Orderline;
    const { useListener } = require('web.custom_hooks');


    pos_model.Order = pos_model.Order.extend({
      set_order_note: function(order_note) {
          this.order_note = $('#order_note').val();
      },
      get_order_note: function() {
          return this.order_note;
      },
      export_as_JSON: function() {
          var submitted_order = SuperOrder.prototype.export_as_JSON.call(this);
          var new_val = {
              order_note: $('#order_note').val(),
              invoice_note: $('#order_note').val(),
          }
          $.extend(submitted_order, new_val);
          return submitted_order;
      },
      export_for_printing: function(){
          var orders = SuperOrder.prototype.export_for_printing.call(this)

          if (!this.order_note_laundry) {
            var notesss = $('#order_note').val();
            this.order_note_laundry = notesss
          }
          var new_val = {
            order_note: this.order_note_laundry || false,
          };
          $.extend(orders, new_val);
          return orders;
        },
    });

    pos_model.Orderline = pos_model.Orderline.extend({

      initialize: function (attributes, options) {
      SuperOrderline.prototype.initialize.apply(this, arguments);
        if (options.json != undefined){
            this.line_note = options.json.line_note;
            this.washing_stage = options.json.washing_stage;
        }
      },
      export_as_JSON: function () {
        const json = SuperOrderline.prototype.export_as_JSON.apply(this, arguments);
        json.line_note = this.line_note;
        json.washing_stage = this.washing_stage;
        json.washing_amount = this.washing_amount;
        json.washing_id = this.washing_id;
        return json;
      },
      set_line_note: function(line_note) {
          this.line_note = line_note
      },
      
      set_washing_stage:function(washing_stage){
          this.washing_stage = washing_stage
      },
      
      set_washing_amount:function(washing_amount){
        this.washing_amount  = washing_amount
      },
      
      set_washing_id:function(washing_id){
        this.washing_id = washing_id
      },
      
      get_line_note: function() {
          return this.line_note
      },
      
      get_washing_stage: function() {
        return this.washing_stage
      },
      
      get_washing_id: function() {
        return this.washing_id
      },
      get_washing_amount: function() {
        return this.washing_amount
      },

      export_for_printing: function() {
          var lines = SuperOrderline.prototype.export_for_printing.call(this);
          var new_attr = {
              line_note: this.get_line_note(),
              washing_stage : this.get_washing_stage(),
              washing_amount : this.get_washing_amount(),
              washing_id : this.get_washing_id(),
          }
          $.extend(lines, new_attr);
          return lines;
      },
    });


    var _super_posmodel = pos_model.PosModel.prototype;
    pos_model.PosModel = pos_model.PosModel.extend({
        after_load_server_data: async function() {
            var res = await _super_posmodel.after_load_server_data.call(this);
            console.log("It is Called:-",res,this);
            return res;
        },
    });

});
