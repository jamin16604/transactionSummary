REQUIRED_HEADERS = {
    "transaction_id",
    "user_id",
    "product_id",
    "timestamp",
    "transaction_amount",
}


def validate_headers(headers: set) -> None:
    lower_headers = {header.lower() for header in headers}
    missing_headers = REQUIRED_HEADERS - lower_headers
    if missing_headers:
        raise ValueError(f"Missing required headers: {missing_headers}")
