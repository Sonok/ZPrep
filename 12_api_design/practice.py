"""
=============================================================================
PATTERN 12: API DESIGN
=============================================================================

HOW TO RECOGNIZE:
- "Design an API for..." or "How would you expose this as a service?"
- Interviewer asks about REST endpoints, HTTP methods, status codes
- Focus is on resource modeling, pagination, rate limiting, error handling
- You're expected to think about scalability and backward compatibility

KEY IDEA:
  Identify the resources (nouns → URL paths), the operations on them
  (verbs → HTTP methods), and the edge cases (errors, pagination, auth).
  Design for the client's perspective — what would a developer using
  your API need?

APPROACH (use this framework every time):
  1. CLARIFY — What are the use cases? Public or internal API? Scale?
  2. RESOURCES — Identify the core entities (nouns)
  3. ENDPOINTS — Map HTTP methods to operations (CRUD)
  4. REQUEST/RESPONSE — Define payloads, status codes, error format
  5. EDGE CASES — Pagination, rate limiting, idempotency, versioning

AMAZON FAVORITES:
  - Design a URL Shortener (TinyURL)
  - Design a Rate Limiter
  - Design a Key-Value Store API
  - Design a Search/Catalog API with pagination
=============================================================================
"""

import time
import hashlib
import threading
from collections import defaultdict
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Problem 1: Design a URL Shortener API
# ---------------------------------------------------------------------------
# Design a URL shortening service (like TinyURL) with the following API:
#
#   POST   /urls          → shorten a URL, return short code
#   GET    /urls/:code    → resolve short code to original URL (redirect)
#   GET    /urls/:code/stats → get click count and metadata
#   DELETE /urls/:code    → delete a short URL
#
# Requirements:
#   - Generate a unique short code for each URL
#   - Same URL shortened twice should return the same code (idempotent)
#   - Support optional TTL (expiration)
#   - Track click count per short URL
#   - Validate URLs (must start with http:// or https://)
#   - Return appropriate HTTP status codes (201, 302, 404, 400, 410)
#
# Source: Glassdoor — "Design TinyURL" is one of the most common Amazon
#         system design questions, often asked as an API design variant.
#
# Hint: Hash the URL with MD5, base62 encode it for the short code.
#       Store a reverse map (original → code) for idempotency.
# ---------------------------------------------------------------------------

_BASE62_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def _base62_encode(num: int, length: int = 7) -> str:
    """Encode an integer into a base62 string of given length."""
    if num == 0:
        return _BASE62_CHARS[0] * length
    result = []
    while num > 0 and len(result) < length:
        result.append(_BASE62_CHARS[num % 62])
        num //= 62
    return "".join(reversed(result)).rjust(length, _BASE62_CHARS[0])


class URLEntry:
    """Stores metadata about a shortened URL."""
    def __init__(self, short_code: str, original_url: str, ttl_seconds: int | None = None):
        pass  # YOUR CODE HERE

    @property
    def is_expired(self) -> bool:
        pass  # YOUR CODE HERE

    def to_dict(self) -> dict:
        pass  # YOUR CODE HERE


class URLShortener:
    """
    URL Shortener service.

    API:
      POST   /urls          → shorten(original_url, ttl) → {"short_code": "abc1234"}
      GET    /urls/:code    → resolve(short_code)        → redirect to original URL
      GET    /urls/:code/stats → get_stats(short_code)   → {"click_count": 42, ...}
      DELETE /urls/:code    → delete(short_code)         → 204 No Content
    """
    def __init__(self, code_length: int = 7):
        pass  # YOUR CODE HERE

    def shorten(self, original_url: str, ttl_seconds: int | None = None) -> dict:
        """
        POST /urls — Create a short URL.
        Returns: {"short_code": "...", "status": 201}
        Idempotent: same URL returns the same short code (status 200).
        Error: {"error": "Invalid URL", "status": 400}
        """
        pass  # YOUR CODE HERE

    def resolve(self, short_code: str) -> dict:
        """
        GET /urls/:code — Look up and redirect.
        Returns: {"original_url": "...", "status": 302}
        Not found: {"error": "Not found", "status": 404}
        Expired: {"error": "URL has expired", "status": 410}
        """
        pass  # YOUR CODE HERE

    def get_stats(self, short_code: str) -> dict:
        """GET /urls/:code/stats — Get analytics for a short URL."""
        pass  # YOUR CODE HERE

    def delete(self, short_code: str) -> dict:
        """DELETE /urls/:code — Delete a short URL."""
        pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 2: Design a Rate Limiter
# ---------------------------------------------------------------------------
# Design a rate limiter using the TOKEN BUCKET algorithm:
#
# How token bucket works:
#   - Each client has a "bucket" with a max capacity of tokens
#   - Each request consumes 1 token
#   - Tokens refill at a fixed rate (e.g., 10 tokens/second)
#   - If the bucket is empty, the request is rejected (429 Too Many Requests)
#
# Requirements:
#   - Per-client rate limiting (identified by client_id)
#   - Configurable capacity and refill rate
#   - Thread-safe (multiple requests may come concurrently)
#   - Return rate limit headers (X-RateLimit-Limit, Remaining, Reset)
#   - Lazy refill: calculate tokens on each request, don't use timers
#
# Source: Glassdoor — Amazon asks about rate limiting in both system design
#         and API design interviews. Token bucket is the expected answer.
#
# Hint: tokens = min(capacity, tokens + elapsed_time * refill_rate)
#       Consume 1 token per request. Return False when tokens < 1.
# ---------------------------------------------------------------------------

class TokenBucket:
    """A single client's token bucket."""
    def __init__(self, capacity: int, refill_rate: float):
        pass  # YOUR CODE HERE

    def _refill(self) -> None:
        """Lazily refill tokens based on elapsed time since last refill."""
        pass  # YOUR CODE HERE

    def consume(self) -> bool:
        """Try to consume one token. Returns True if allowed, False if rate limited."""
        pass  # YOUR CODE HERE


class RateLimiter:
    """
    Rate limiter using token bucket algorithm.

    API (middleware-style):
      allow_request(client_id) → True (200 OK) / False (429 Too Many Requests)
      get_headers(client_id)   → rate limit headers for HTTP response
    """
    def __init__(self, capacity: int = 100, refill_rate: float = 10.0):
        pass  # YOUR CODE HERE

    def allow_request(self, client_id: str) -> bool:
        """Check if a request from client_id should be allowed."""
        pass  # YOUR CODE HERE

    def get_headers(self, client_id: str) -> dict[str, str]:
        """Return rate limit headers for the response."""
        pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 3: Design a Key-Value Store API
# ---------------------------------------------------------------------------
# Design a RESTful key-value store (like a simplified Redis) with:
#
#   PUT    /kv/:ns/:key     → set a value (with optional TTL)
#   GET    /kv/:ns/:key     → get a value
#   DELETE /kv/:ns/:key     → delete a key
#   POST   /kv/:ns/_batch   → batch get or batch put
#   GET    /kv/:ns          → list keys (with prefix filter)
#
# Requirements:
#   - Namespace isolation (different apps don't see each other's keys)
#   - Optional TTL per key (lazy expiration — check on access)
#   - Batch operations to avoid N+1 API calls
#   - List keys with prefix filtering and limit
#   - Thread-safe
#
# Source: Glassdoor — "Design a distributed key-value store" is a common
#         Amazon question. This focuses on the API layer.
#
# Hint: Use a nested dict {namespace: {key: KVEntry}}. KVEntry stores
#       value + created_at + ttl for expiration checks.
# ---------------------------------------------------------------------------

class KVEntry:
    """A single key-value entry with optional TTL."""
    def __init__(self, value: Any, ttl_seconds: int | None = None):
        pass  # YOUR CODE HERE

    @property
    def is_expired(self) -> bool:
        pass  # YOUR CODE HERE


class KeyValueStore:
    """
    Key-Value Store service.

    API:
      PUT    /kv/:ns/:key     → put(ns, key, value, ttl)
      GET    /kv/:ns/:key     → get(ns, key)
      DELETE /kv/:ns/:key     → delete(ns, key)
      POST   /kv/:ns/_batch   → batch_get(ns, keys) / batch_put(ns, items)
      GET    /kv/:ns          → list_keys(ns, prefix, limit)
    """
    def __init__(self):
        pass  # YOUR CODE HERE

    def put(self, namespace: str, key: str, value: Any,
            ttl_seconds: int | None = None) -> dict:
        """PUT /kv/:ns/:key — Set a key-value pair."""
        pass  # YOUR CODE HERE

    def get(self, namespace: str, key: str) -> dict:
        """GET /kv/:ns/:key — Get a value by key."""
        pass  # YOUR CODE HERE

    def delete(self, namespace: str, key: str) -> dict:
        """DELETE /kv/:ns/:key — Delete a key."""
        pass  # YOUR CODE HERE

    def batch_get(self, namespace: str, keys: list[str]) -> dict:
        """POST /kv/:ns/_batch (action=get) — Get multiple keys at once."""
        pass  # YOUR CODE HERE

    def batch_put(self, namespace: str, items: list[dict]) -> dict:
        """POST /kv/:ns/_batch (action=put) — Set multiple key-value pairs."""
        pass  # YOUR CODE HERE

    def list_keys(self, namespace: str, prefix: str = "",
                  limit: int = 100) -> dict:
        """GET /kv/:ns?prefix=...&limit=... — List keys in a namespace."""
        pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 4: Design a Paginated Search API
# ---------------------------------------------------------------------------
# Design a product catalog API with filtering, sorting, and pagination:
#
#   GET  /products?category=...&min_price=...&max_price=...
#                 &sort_by=price&order=asc
#                 &cursor=...&page_size=20
#        → {"products": [...], "next_cursor": ..., "has_more": true}
#
#   GET  /products/:id  → single product
#   POST /products      → create product
#
# Requirements:
#   - Filter by category, price range
#   - Sort by price or name (ascending or descending)
#   - Cursor-based pagination (NOT offset — offsets break with data changes)
#   - Cap page_size at MAX_PAGE_SIZE to prevent abuse
#   - Return has_more and next_cursor for clients to paginate
#
# Source: Glassdoor — Amazon loves pagination questions. They want to see
#         cursor-based pagination and proper query parameter handling.
#
# Hint: Filter → Sort → Paginate (in that order). Cursor is the index
#       into the sorted result list.
# ---------------------------------------------------------------------------

class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"


class Product:
    """A product in the catalog."""
    def __init__(self, product_id: str, name: str, category: str, price: float):
        pass  # YOUR CODE HERE

    def to_dict(self) -> dict:
        pass  # YOUR CODE HERE


class ProductCatalogAPI:
    """
    Product Catalog API with filtering, sorting, and pagination.
    """
    MAX_PAGE_SIZE = 100
    DEFAULT_PAGE_SIZE = 20

    def __init__(self):
        pass  # YOUR CODE HERE

    def create_product(self, product_id: str, name: str,
                       category: str, price: float) -> dict:
        """POST /products — Add a product to the catalog."""
        pass  # YOUR CODE HERE

    def get_product(self, product_id: str) -> dict:
        """GET /products/:id — Get a single product."""
        pass  # YOUR CODE HERE

    def search(
        self,
        category: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        sort_by: str = "name",
        order: SortOrder = SortOrder.ASC,
        cursor: int = 0,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> dict:
        """
        GET /products — Search with filters, sorting, and pagination.

        Returns: {
            "products": [...],
            "next_cursor": 20 | null,
            "has_more": true/false,
            "total_filtered": 150,
            "status": 200
        }
        """
        pass  # YOUR CODE HERE


# ===========================================================================
# TESTS — run with: python -m pytest 12_api_design/practice.py -v
# ===========================================================================
import unittest


class TestURLShortener(unittest.TestCase):
    def test_shorten_and_resolve(self):
        svc = URLShortener()
        result = svc.shorten("https://example.com/very/long/url")
        self.assertEqual(result["status"], 201)
        code = result["short_code"]
        resolved = svc.resolve(code)
        self.assertEqual(resolved["status"], 302)
        self.assertEqual(resolved["original_url"], "https://example.com/very/long/url")

    def test_idempotent_shorten(self):
        svc = URLShortener()
        r1 = svc.shorten("https://example.com/page")
        r2 = svc.shorten("https://example.com/page")
        self.assertEqual(r1["short_code"], r2["short_code"])

    def test_invalid_url(self):
        svc = URLShortener()
        result = svc.shorten("not-a-url")
        self.assertEqual(result["status"], 400)

    def test_resolve_not_found(self):
        svc = URLShortener()
        result = svc.resolve("nonexistent")
        self.assertEqual(result["status"], 404)

    def test_click_count(self):
        svc = URLShortener()
        code = svc.shorten("https://example.com")["short_code"]
        svc.resolve(code)
        svc.resolve(code)
        svc.resolve(code)
        stats = svc.get_stats(code)
        self.assertEqual(stats["click_count"], 3)

    def test_delete(self):
        svc = URLShortener()
        code = svc.shorten("https://example.com")["short_code"]
        result = svc.delete(code)
        self.assertEqual(result["status"], 204)
        self.assertEqual(svc.resolve(code)["status"], 404)


class TestRateLimiter(unittest.TestCase):
    def test_allows_requests_under_limit(self):
        limiter = RateLimiter(capacity=5, refill_rate=0)
        for _ in range(5):
            self.assertTrue(limiter.allow_request("client1"))

    def test_rejects_over_limit(self):
        limiter = RateLimiter(capacity=3, refill_rate=0)
        for _ in range(3):
            limiter.allow_request("client1")
        self.assertFalse(limiter.allow_request("client1"))

    def test_separate_clients(self):
        limiter = RateLimiter(capacity=2, refill_rate=0)
        limiter.allow_request("client1")
        limiter.allow_request("client1")
        # client2 should still have tokens
        self.assertTrue(limiter.allow_request("client2"))

    def test_headers(self):
        limiter = RateLimiter(capacity=10, refill_rate=1)
        limiter.allow_request("c1")
        headers = limiter.get_headers("c1")
        self.assertEqual(headers["X-RateLimit-Limit"], "10")
        self.assertIn("X-RateLimit-Remaining", headers)


class TestKeyValueStore(unittest.TestCase):
    def test_put_and_get(self):
        store = KeyValueStore()
        store.put("app1", "user:1", {"name": "Alice"})
        result = store.get("app1", "user:1")
        self.assertEqual(result["value"], {"name": "Alice"})
        self.assertEqual(result["status"], 200)

    def test_get_not_found(self):
        store = KeyValueStore()
        result = store.get("app1", "missing")
        self.assertEqual(result["status"], 404)

    def test_delete(self):
        store = KeyValueStore()
        store.put("app1", "key1", "value1")
        result = store.delete("app1", "key1")
        self.assertEqual(result["status"], 204)
        self.assertEqual(store.get("app1", "key1")["status"], 404)

    def test_batch_get(self):
        store = KeyValueStore()
        store.put("app1", "a", 1)
        store.put("app1", "b", 2)
        result = store.batch_get("app1", ["a", "b", "c"])
        self.assertEqual(result["results"]["a"], 1)
        self.assertEqual(result["results"]["b"], 2)
        self.assertIsNone(result["results"]["c"])

    def test_namespace_isolation(self):
        store = KeyValueStore()
        store.put("app1", "key", "value1")
        store.put("app2", "key", "value2")
        self.assertEqual(store.get("app1", "key")["value"], "value1")
        self.assertEqual(store.get("app2", "key")["value"], "value2")

    def test_list_keys_with_prefix(self):
        store = KeyValueStore()
        store.put("app1", "user:1", "Alice")
        store.put("app1", "user:2", "Bob")
        store.put("app1", "order:1", "Pizza")
        result = store.list_keys("app1", prefix="user:")
        self.assertEqual(result["keys"], ["user:1", "user:2"])


class TestProductCatalogAPI(unittest.TestCase):
    def _make_catalog(self) -> ProductCatalogAPI:
        api = ProductCatalogAPI()
        api.create_product("p1", "Laptop", "electronics", 999.99)
        api.create_product("p2", "Mouse", "electronics", 29.99)
        api.create_product("p3", "Desk", "furniture", 249.99)
        api.create_product("p4", "Chair", "furniture", 199.99)
        api.create_product("p5", "Keyboard", "electronics", 79.99)
        return api

    def test_create_and_get_product(self):
        api = ProductCatalogAPI()
        result = api.create_product("p1", "Laptop", "electronics", 999.99)
        self.assertEqual(result["status"], 201)
        product = api.get_product("p1")
        self.assertEqual(product["product"]["name"], "Laptop")

    def test_duplicate_product(self):
        api = ProductCatalogAPI()
        api.create_product("p1", "Laptop", "electronics", 999.99)
        result = api.create_product("p1", "Duplicate", "electronics", 0)
        self.assertEqual(result["status"], 409)

    def test_filter_by_category(self):
        api = self._make_catalog()
        result = api.search(category="electronics")
        self.assertEqual(result["total_filtered"], 3)

    def test_sort_by_price_asc(self):
        api = self._make_catalog()
        result = api.search(sort_by="price", order=SortOrder.ASC)
        prices = [p["price"] for p in result["products"]]
        self.assertEqual(prices, sorted(prices))

    def test_pagination(self):
        api = self._make_catalog()
        r1 = api.search(page_size=2, cursor=0, sort_by="name")
        self.assertEqual(len(r1["products"]), 2)
        self.assertTrue(r1["has_more"])
        r2 = api.search(page_size=2, cursor=r1["next_cursor"], sort_by="name")
        self.assertEqual(len(r2["products"]), 2)

    def test_product_not_found(self):
        api = ProductCatalogAPI()
        result = api.get_product("nonexistent")
        self.assertEqual(result["status"], 404)


if __name__ == "__main__":
    unittest.main()
