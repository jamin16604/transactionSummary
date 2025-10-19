from datetime import datetime


def test_summary_invalid_userid_range_data(client):
    response = client.get(
        "/summary/9999",
        params={"start_date": "2023-01-01T00:00:00", "end_date": "2023-12-31T23:59:59"},
    )
    assert response.status_code == 404
    data = str(response.json()["detail"])
    assert response.json() == {
        "detail": "No data found for the given user_id and date range."
    }


def test_summary_invalid_date_range(client):
    response = client.get(
        "/summary/100",
        params={"start_date": "2023-12-31T23:59:59", "end_date": "2023-01-01T00:00:00"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "start_date must be before or equal to end_date."
    }


def test_summary_invalid_userid(client):
    response = client.get(
        "/summary/0",
        params={"start_date": "2023-01-01T00:00:00", "end_date": "2023-12-31T23:59:59"},
    )
    assert response.status_code == 422
    response = client.get(
        "/summary/a",
        params={"start_date": "2023-01-01T00:00:00", "end_date": "2023-12-31T23:59:59"},
    )
    assert response.status_code == 422


def test_summary_valid_data(client):
    response = client.get(
        "/summary/100",
        params={"start_date": "2020-01-01T00:00:00", "end_date": datetime.today()},
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["user_id"] == 100
    assert "max_transaction_amount" in json_response
    assert "min_transaction_amount" in json_response
    assert "mean_transaction_amount" in json_response
    assert "start_date" in json_response
    assert "end_date" in json_response


def test_summary_edge_case_dates(client):
    client.post(
        "/upload/",
        files={
            "file": (
                "edge_case.csv",
                b"transaction_id,user_id,product_id,timestamp,transaction_amount\n"
                b"1,100,200,'2025-01-01 00:00:00',100.0\n"
                b"2,100,201,'2025-01-01 00:00:00',200.0\n",
                "text/csv",
            )
        },
    )
    response = client.get(
        "/summary/100",
        params={"start_date": "2025-01-01T00:00:00", "end_date": "2025-01-01T00:00:00"},
    )
    assert response.status_code == 200
