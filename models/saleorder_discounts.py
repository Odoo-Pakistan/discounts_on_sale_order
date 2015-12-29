# -*- coding: utf-8 -*-
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv


class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    def _calc_line_base_price(self, cr, uid, line, context=None):
        return line.price_unit * (1 - (line.discount or 0.0) / 100.0) - (line.fixed_discount / self._calc_line_quantity(cr, uid, line)) or 0.0

    _columns = {
        'fixed_discount': fields.float(u"Discount (=)", digits_compute=dp.get_precision('Product Price')),
    }


class sale_order(osv.osv):
    _inherit = "sale.order"
    _columns = {
        'global_discount_type': fields.selection((('fixed', 'Fixed'), ('percent', 'Percent')),
                                                 u"Global Discount (type)", required=False),
        'global_discount_amount': fields.float(u"Global Discount (value)",
                                               digits_compute=dp.get_precision('Product Price'))
    }

    def _amount_line_tax(self, cr, uid, line, context=None, order=None):
        val = 0.0
        line_obj = self.pool['sale.order.line']
        price = line_obj._calc_line_base_price(cr, uid, line, context=context) * ((1 - (order.global_discount_amount or 0.0) / 100.0) if (order and order.global_discount_type == 'percent') else 1)
        qty = line_obj._calc_line_quantity(cr, uid, line, context=context)
        for c in self.pool['account.tax'].compute_all(
                cr, uid, line.tax_id, price, qty, line.product_id,
                line.order_id.partner_id)['taxes']:
            val += c.get('amount', 0.0)
        return val

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                val1 += line.price_subtotal * ((1 - (order.global_discount_amount or 0.0) / 100.0) if (order and order.global_discount_type == 'percent') else 1)
                val += self._amount_line_tax(cr, uid, line, context=context, order=order)
            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        return res
