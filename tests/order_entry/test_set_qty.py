from oec.order_entry import set_qty

def test_set_qty():
    entry_price, stop_loss_price, risk_amount = 100, 98, 1000
    qty = set_qty(entry_price, stop_loss_price, risk_amount)
    assert qty == 500  # 1000 / |100 - 98| = 1000 / 2 = 500
    assert qty * abs(entry_price - stop_loss_price) == risk_amount

def test_set_qty_sell():
    entry_price, stop_loss_price, risk_amount = 100, 105, 500
    qty = set_qty(entry_price, stop_loss_price, risk_amount)
    assert qty == 100  # 500 / |100 - 105| = 500 / 5 = 100
    assert qty * abs(entry_price - stop_loss_price) == risk_amount
