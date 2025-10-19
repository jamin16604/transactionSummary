from httpx import ASGITransport, AsyncClient
import pytest
from app.main import app
import asyncio


@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="module")
async def uploaded_data(async_client):
    # Upload sample data before running concurrency tests
    csv_content = (
        b"transaction_id,user_id,product_id,timestamp,transaction_amount\n"
        b"1,100,200,'2023-01-01 10:00:00',150.0\n"
        b"2,101,201,'2023-02-01 11:00:00',250.0\n"
        b"3,102,202,'2023-03-01 12:00:00',350.0\n"
        b"4,103,203,'2023-04-01 13:00:00',450.0\n"
        b"5,104,204,'2023-05-01 14:00:00',550.0\n"
    )
    response = await async_client.post(
        "/upload/",
        files={"file": ("test_transactions.csv", csv_content, "text/csv")},
    )
    assert response.status_code == 200
    return response


@pytest.mark.anyio
async def test_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_concurrent_summary_requests(async_client):
    user_ids = [200, 201, 202, 203, 204]
    start_date = "2020-01-01T00:00:00"
    end_date = "2025-12-31T23:59:59"

    async def fetch_summary(user_id):
        response = await async_client.get(
            f"/summary/{user_id}",
            params={"start_date": start_date, "end_date": end_date},
        )
        return response

    tasks = [fetch_summary(uid) for uid in user_ids]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        assert response.status_code == (200)


@pytest.mark.anyio
async def upload_and_fetch_summary(async_client, large_csv_path):
    # Upload large CSV file
    with open(large_csv_path, "rb") as f:
        upload_response = await async_client.post(
            "/upload/",
            files={
                "file": f,
            },
        )
    assert upload_response.status_code == 200

    # Fetch summary for a specific user
    user_id = 100
    start_date = "2020-01-01T00:00:00"
    end_date = "2025-12-31T23:59:59"
    summary_response = await async_client.get(
        f"/summary/{user_id}", params={"start_date": start_date, "end_date": end_date}
    )
    assert summary_response.status_code == 200

    async def summary_task():
        tasks = []
        for _ in range(5):
            tasks.append(
                async_client.get(
                    f"/summary/{user_id}",
                    params={"start_date": start_date, "end_date": end_date},
                )
            )
        responses = await asyncio.gather(*tasks)
        for response in responses:
            assert response.status_code == 200

    async def upload_task():
        with open(large_csv_path, "rb") as f:
            response = await async_client.post(
                "/upload/",
                files={
                    "file": f,
                },
            )
        assert response.status_code == 200

    await asyncio.gather(summary_task(), upload_task())
