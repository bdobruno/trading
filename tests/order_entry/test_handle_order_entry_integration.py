from unittest.mock import Mock

from alpaca.trading.enums import OrderSide

from hermes.context import TradingContext
from hermes.trading.order_entry import handle_order_entry


def test_handle_order_entry_buy():
    mock_client = Mock()
    mock_stock_data = Mock()
    mock_option_data = Mock()
    mock_quote = Mock()
    mock_quote.ask_price = 100
    mock_stock_data.get_stock_latest_quote.return_value = {"AAPL": mock_quote}

    risk_pct = 0.02
    account_value = 10000

    ctx = TradingContext(
        client=mock_client,
        stock_data=mock_stock_data,
        option_data=mock_option_data,
        risk_pct=0.02,
        is_paper=True,
        account_value=10000,
        risk_reward=3,
        risk_amount=risk_pct * account_value,
    )

    handle_order_entry(
        ctx, side="buy", stop_loss_price=98, symbol="AAPL", is_options=False
    )

    assert mock_client.submit_order.called
    order = mock_client.submit_order.call_args[0][0]
    assert order.symbol == "AAPL"
    assert order.side == OrderSide.BUY
    assert order.qty == 100  # risk_amount=200, delta=2, qty=100
    assert order.stop_loss.stop_price == 98
    assert order.take_profit.limit_price == 106  # entry=100, stop=98, RR=3, TP=100+(2*3)=106


def test_handle_order_entry_sell():
    mock_client = Mock()
    mock_stock_data = Mock()
    mock_option_data = Mock()
    mock_quote = Mock()
    mock_quote.bid_price = 200
    mock_stock_data.get_stock_latest_quote.return_value = {"TSLA": mock_quote}

    risk_pct = 0.02
    account_value = 10000

    ctx = TradingContext(
        client=mock_client,
        stock_data=mock_stock_data,
        option_data=mock_option_data,
        risk_pct=0.02,
        is_paper=True,
        account_value=10000,
        risk_reward=3,
        risk_amount=risk_pct * account_value,
    )

    handle_order_entry(
        ctx, side="sell", stop_loss_price=205, symbol="TSLA", is_options=False
    )

    assert mock_client.submit_order.called
    order = mock_client.submit_order.call_args[0][0]
    assert order.symbol == "TSLA"
    assert order.side == OrderSide.SELL
    assert order.qty == 40  # risk_amount=200, delta=5, qty=40
    assert order.stop_loss.stop_price == 205
    assert order.take_profit.limit_price == 185  # entry=200, stop=205, RR=3, TP=200-(5*3)=185
