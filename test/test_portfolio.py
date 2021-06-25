from app.daily_portfolio import fetch_data


def test_fetch_data():
    parsed_response=fetch_data("MU")
    assert "Time Series (Daily)" in list(parsed_response.keys())