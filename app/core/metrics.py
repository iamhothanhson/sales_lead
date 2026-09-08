class HttpMetrics:
    def __init__(self) -> None:
        self.total_requests = 0
        self.http_errors = 0
        self.total_latency_ms = 0.0

    def observe(self, status_code: int, duration_ms: float) -> None:
        self.total_requests += 1
        if status_code >= 400:
            self.http_errors += 1
        self.total_latency_ms += duration_ms

    def snapshot(self) -> dict[str, int | float]:
        average_latency = (
            self.total_latency_ms / self.total_requests
            if self.total_requests
            else 0.0
        )
        return {
            "total_http_requests": self.total_requests,
            "http_errors": self.http_errors,
            "average_request_latency_ms": round(average_latency, 2),
        }


http_metrics = HttpMetrics()
