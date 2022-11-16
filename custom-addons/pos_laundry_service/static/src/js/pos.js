odoo.define('aces_pos_note.addnote', function (require) {
"use strict";

var gui = require('point_of_sale.Gui');
var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var core = require('web.core');

const PosComponent = require('point_of_sale.PosComponent');
var rpc = require('web.rpc');
var QWeb = core.qweb;
var OrderWidget = require('point_of_sale.OrderWidget');
models.load_fields('res.partner',['gender']);



class CustomPosComponent extends PosComponent {
		// showScreen(name, props) {
		// 		this.trigger('show-main-screen', { name, props });
		// }
		// the other commented codes i deleted :)

}

    var AddNoteButton = screens.ActionButtonWidget.extend({
        template: 'AddNoteButton',
        button_click: function(){
            var order    = this.pos.get_order();
            var lines    = order.get_orderlines();
            if(lines.length > 0) {
                var selected_line = order.get_selected_orderline();
                if (selected_line) {
                	this.gui.show_popup('add_note_popup');
                }
            } else {
                alert("Please select the product !");
            }
        },
    });

    screens.define_action_button({
        'name': 'addnoteline',
        'widget': AddNoteButton,
        'condition': function(){
            return this.pos.config.enable_product_note;
        },
    });
//
  screens.ProductScreenWidget.include({
	  click_product: function(product) {
	       if(product.to_weight && this.pos.config.iface_electronic_scale){
	           this.gui.show_screen('scale',{product: product});
	       }
	       else{
	    	   var washing_ids = this.pos.config.washing_stage_ids;
	    	   var self = this;
	    	   rpc.query({
    				model: 'washing.stage',
    				method: 'search_read',
    				args: [[['id', 'in',washing_ids]]],
    			}).then(function(datas){
	            	if(washing_ids.length > 0){
		 	    	   _.each(datas,function(key,value){
		 	    		   if(key.name == "Wash and Iron Both"){
		 	    			  self.pos.get_order().add_product(product,{ price : (parseFloat(product.price) + parseFloat(key.amount))});
		 	    			  var order = self.pos.get_order();
		 	    			  var orderlines = order.get_orderlines();
		 	    			  _.each(orderlines,function(line,ids){
		 	    				  if(line.product.id == product.id){
		 	    					 line.set_washing_stage(key.name);
		 	    					 line.set_washing_amount(key.amount);
		 	    					 line.set_washing_id(parseInt(key.id));
		 	    					 line.set_unit_price(parseFloat(product.lst_price) + parseFloat(key.amount));
		 	    				  }
		 	    			  });
		 	    		   }
		 	    	   });
	            	}
	            	else{
	            		$.alert({
	            		    title: 'Warning',
	            		    content: 'Please set your washing type in pos configuration',
	            		});
	            	}
	            });
	       }
	    },
  });

    var ProductNotePopupWidget = PopupWidget.extend({
	    template: 'ProductNotePopupWidget',
	    show: function(options){
	        options = options || {};
	        this._super(options);

	        this.renderElement();
	        var order    = this.pos.get_order();
	    	var selected_line = order.get_selected_orderline();
	    	$('textarea#textarea_note').focus();
	        $('textarea#textarea_note').html(selected_line.get_line_note());
	    },
	    click_confirm: function(){
	    	var order    = this.pos.get_order();
	    	var selected_line = order.get_selected_orderline();
	    	var value = this.$('#textarea_note').val();
	    	selected_line.set_line_note(value);
	    	this.gui.close_popup();
	    },
	    renderElement: function() {
            var self = this;
            this._super();
    	},

	});
	gui.define_popup({name:'add_note_popup', widget: ProductNotePopupWidget});

    var WashingStageButton = screens.ActionButtonWidget.extend({
        template: 'WashingStageButton',
         button_click: function(){
            var washing_stages=[];
            var self=this;
            var washing_ids = this.pos.config.washing_stage_ids;
            var order    = this.pos.get_order();
            var lines    = order.get_orderlines();

            rpc.query({
				model: 'washing.stage',
				method: 'search_read',
				args: [[['id', 'in',washing_ids]]],
			}).then(function(datas){
				 if(lines.length > 0) {
		                var selected_line = order.get_selected_orderline();
		                var product_id = selected_line.product.id;
		    			var urgent_product_id = self.pos.config.laundry_service_product[0];
		    			var delivery_id = self.pos.config.laundry_homedelivery[0];
			        		 if(product_id == urgent_product_id){
			        			 self.gui.show_popup('washing_error_popup');
			                     }
			        		 else if(product_id == delivery_id){
			        			 self.gui.show_popup('washing_error_popup');
			                     }
			        		 else{
			        			 self.pos.washing = datas;
			                     self.gui.show_popup('add_washing_popup');
			        		 }
		                }
		             else{
		                    self.gui.show_popup('select_product_popup');
		                }
				});
        },
    });

     screens.define_action_button({
        'name': 'washingstage',
        'widget': WashingStageButton,
    });


    var WashingStagePopupWidget = PopupWidget.extend({
	    template: 'WashingStagePopupWidget',
	    show: function(options){
	        options = options || {};
	        this._super(options);

	        this.renderElement();
	        this.renderWashing();
	        var order = this.pos.get_order();
	        var washing = this.pos.washing;
	    	var selected_line = order.get_selected_orderline();

	    },
	    click_confirm: function(){
	    	var order    = this.pos.get_order();
	    	var selected_line = order.get_selected_orderline();
	    	var value = this.$('input[name="washing_type"]:checked').val();
	    	var amount = this.$('input[name="washing_type"]:checked')[0].dataset.amount;
	    	var wash_id = this.$('input[name="washing_type"]:checked')[0].dataset.id;
	    	selected_line.set_washing_stage(value);
	    	selected_line.set_washing_amount(amount);
	    	selected_line.set_washing_id(wash_id);
	    	selected_line.set_unit_price(parseFloat(selected_line.product.lst_price) + parseFloat(amount));
	    	this.gui.close_popup();
	    },
	    renderElement: function() {
            var self = this;
            this._super();
    	},

    	renderWashing : function() {
            var self = this;
            var washing = this.pos.washing;
            var html ='<div class="container" align="left"><form>';
            _.each(washing,function(key,value){
                html += '<div class="radio" style="padding:20px;"><label>' + '<input style="box-shadow:unset; width:5%;margin-top: -9px;float:left;" class="form-control" type="radio" name="washing_type" data-id="'+ key.id + '" data-amount="' + key.amount + '" value="' + key.name + '"/>' + key.name + '&nbsp;' + '(&nbsp;'  + key.amount + self.pos.currency.symbol + '&nbsp;)</label></div>';
            });
            html += "</form></div>";
            this.$('.title').after(html);
        },
	});
	gui.define_popup({name:'add_washing_popup', widget: WashingStagePopupWidget});


	var SelectClothPopupWidget = PopupWidget.extend({
	    template: 'SelectClothPopupWidget',
	    show: function(options){
	        options = options || {};
	        this._super(options);

	        this.renderElement();
	    },

	    click_confirm: function(){
	    	this.gui.close_popup();
	    },

	    renderElement: function() {
            var self = this;
            this._super();
    	},
	});
	gui.define_popup({name:'select_product_popup', widget: SelectClothPopupWidget});


	var SelectNullPopupWidget = PopupWidget.extend({
	    template: 'SelectNullPopupWidget',
	    show: function(options){
	        options = options || {};
	        this._super(options);

	        this.renderElement();
	    },

	    click_confirm: function(){
	    	this.gui.close_popup();
	    },

	    renderElement: function() {
            var self = this;
            this._super();
    	},
	});
	gui.define_popup({name:'select_null_popup', widget: SelectNullPopupWidget});


	var WashingErrorPopupWidget = PopupWidget.extend({
	    template: 'WashingErrorPopupWidget',
	    show: function(options){
	        options = options || {};
	        this._super(options);
	        this.renderElement();
	    },

	    click_confirm: function(){
	    	this.gui.close_popup();
	    },

	    renderElement: function() {
            var self = this;
            this._super();
    	},
	});
	gui.define_popup({name:'washing_error_popup', widget: WashingErrorPopupWidget});

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function(attr,options){
            //this.line_note = '';
            //this.washing_stage= '';
        	this.get_washing_stage();
            _super_orderline.initialize.call(this, attr, options);
        },
        set_line_note: function(line_note) {
            this.set('line_note', line_note);
        },

        set_washing_stage:function(washing_stage){
            this.set('washing_stage',washing_stage);
        },

        set_washing_amount:function(washing_amount){
            this.set('washing_amount',washing_amount);
        },

        set_washing_id:function(washing_id){
            this.set('washing_id',parseInt(washing_id));
        },

        get_line_note: function() {
            return this.get('line_note');
        },

        get_washing_stage: function() {
            return this.get('washing_stage');
        },

        get_washing_id: function() {
            return this.get('washing_id');
        },
        get_washing_amount: function() {
            return this.get('washing_amount');
        },
        export_as_JSON: function() {
            var lines = _super_orderline.export_as_JSON.call(this);
            var new_attr = {
                line_note: this.get_line_note(),
                washing_stage : this.get_washing_stage(),
                washing_amount : this.get_washing_amount(),
                washing_id : this.get_washing_id(),
            }
            $.extend(lines, new_attr);
            return lines;
        },
        export_for_printing: function() {
            var lines = _super_orderline.export_for_printing.call(this);
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

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        set_order_note: function(order_note) {
            this.order_note = $('#order_note').val();
        },
        get_order_note: function() {
            return this.order_note;
        },
        export_as_JSON: function() {
            var submitted_order = _super_order.export_as_JSON.call(this);
            var new_val = {
                order_note: $('#order_note').val(),
                invoice_note: $('#order_note').val(),
            }
            $.extend(submitted_order, new_val);
            return submitted_order;
        },
        export_for_printing: function(){
            var orders = _super_order.export_for_printing.call(this)
            var notesss = $('#order_note').val();
            var new_val = {
            	order_note: $('#order_note').val() || false,
            };
            $.extend(orders, new_val);
            return orders;
        },
    });

    screens.PaymentScreenWidget.include({
        show: function() {
            var self = this;
            this._super();
            $("textarea#order_note").focus(function(e) {
            	e.stopPropagation();
            	$('body').off('keypress', this.keyboard_handler);
                $('body').off('keydown', this.keyboard_keydown_handler);
                window.document.body.removeEventListener('keypress',self.keyboard_handler);
                window.document.body.removeEventListener('keydown',self.keyboard_keydown_handler);
            });
            $("textarea#order_note").focusout(function() {
            	$('body').on('keypress', this.keyboard_handler);
                $('body').on('keydown', this.keyboard_keydown_handler);
                window.document.body.addEventListener('keypress',self.keyboard_handler);
                window.document.body.addEventListener('keydown',self.keyboard_keydown_handler);
            });
        },
        validate_order: function(force_validation) {
            if(this.pos.config.enable_order_note) {
                var currentOrder = this.pos.get_order();
                currentOrder.set_order_note($('#order_note').val());
            }
            this._super(force_validation);
        },
    });
});
