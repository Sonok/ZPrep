"""
=============================================================================
PATTERN 12: API DESIGN — SOLUTIONS
=============================================================================

GENERAL TIPS FOR AMAZON API DESIGN INTERVIEWS:
  1. CLARIFY scope — "Is this a public or internal API? What scale?"
  2. Start with the resource model — what are the nouns (entities)?
  3. Define endpoints with clear HTTP methods (GET, POST, PUT, DELETE)
  4. Think about pagination, filtering, error handling, and idempotency
  5. Discuss rate limiting, authentication, and versioning
  6. Consider backward compatibility — can you add fields without breaking?

PATTERNS AMAZON LOVES TO SEE:
  - RESTful resource naming (plural nouns, no verbs in URLs)
  - Proper HTTP status codes (201 Created, 404 Not Found, 429 Too Many Requests)
  - Pagination with cursors or offset/limit
  - Idempotency keys for POST/PUT
  - Rate limiting with token bucket or sliding window
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
# APPROACH:
#   Core entities: URL mapping (short_code -> original_url)
#   Operations: shorten (POST), redirect/lookup (GET), stats (GET), delete
#   Use a hash-based approach for generating short codes.
#
# DESIGN DECISIONS:
#   - Base62 encoding of a hash for short codes (a-z, A-Z, 0-9)
#   - Counter-based fallback if hash collides
#   - Track click count for analytics
#   - Expiration support via TTL
#
# TRICK TO REMEMBER: "Hash the URL, base62 encode, store the mapping."
#
# COMMON MISTAKES:
#   - Not handling collisions (two URLs hash to same short code)
#   - Not validating URLs before shortening
#   - Forgetting about expiration/TTL
#   - Using sequential IDs (predictable, security concern)
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
        self.short_code = short_code
        self.original_url = original_url
        self.created_at = time.time()
        self.ttl_seconds = ttl_seconds
        self.click_count = 0

    @property
    def is_expired(self) -> bool:
        if self.ttl_seconds is None:
            return False
        return time.time() - self.created_at > self.ttl_seconds

    def to_dict(self) -> dict:
        return {
            "short_code": self.short_code,
            "original_url": self.original_url,
            "click_count": self.click_count,
            "created_at": self.created_at,
            "expired": self.is_expired,
        }


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
        self._code_length = code_length
        self._url_map: dict[str, URLEntry] = {}       # short_code -> URLEntry
        self._reverse_map: dict[str, str] = {}         # original_url -> short_code
        self._counter = 0

    def shorten(self, original_url: str, ttl_seconds: int | None = None) -> dict:
        """
        POST /urls — Create a short URL.
        Returns: {"short_code": "...", "short_url": "https://short.url/..."}
        Idempotent: same URL returns the same short code.
        """
        if not original_url or not original_url.startswith(("http://", "https://")):
            return {"error": "Invalid URL", "status": 400}

        # Idempotent: return existing code if URL already shortened
        if original_url in self._reverse_map:
            code = self._reverse_map[original_url]
            if not self._url_map[code].is_expired:
                return {"short_code": code, "status": 200}

        # Generate short code from hash
        hash_val = int(hashlib.md5(original_url.encode()).hexdigest(), 16)
        code = _base62_encode(hash_val, self._code_length)

        # Handle collision
        while code in self._url_map:
            self._counter += 1
            hash_val = int(hashlib.md5(f"{original_url}{self._counter}".encode()).hexdigest(), 16)
            code = _base62_encode(hash_val, self._code_length)

        entry = URLEntry(code, original_url, ttl_seconds)
        self._url_map[code] = entry
        self._reverse_map[original_url] = code

        return {"short_code": code, "status": 201}

    def resolve(self, short_code: str) -> dict:
        """
        GET /urls/:code — Look up and redirect.
        Returns: {"original_url": "...", "status": 302} or {"error": ..., "status": 404}
        """
        if short_code not in self._url_map:
            return {"error": "Not found", "status": 404}

        entry = self._url_map[short_code]
        if entry.is_expired:
            return {"error": "URL has expired", "status": 410}

        entry.click_count += 1
        return {"original_url": entry.original_url, "status": 302}

    def get_stats(self, short_code: str) -> dict:
        """
        GET /urls/:code/stats — Get analytics for a short URL.
        """
        if short_code not in self._url_map:
            return {"error": "Not found", "status": 404}
        return {**self._url_map[short_code].to_dict(), "status": 200}

    def delete(self, short_code: str) -> dict:
        """
        DELETE /urls/:code — Delete a short URL.
        """
        if short_code not in self._url_map:
            return {"error": "Not found", "status": 404}
        entry = self._url_map.pop(short_code)
        self._reverse_map.pop(entry.original_url, None)
        return {"status": 204}


# ---------------------------------------------------------------------------
# Problem 2: Design a Rate Limiter
# ---------------------------------------------------------------------------
# APPROACH:
#   Token bucket algorithm — each client gets a bucket of tokens.
#   Tokens refill at a fixed rate. Each request consumes one token.
#   If the bucket is empty, the request is rejected (429).
#
# DESIGN DECISIONS:
#   - Token bucket chosen over sliding window (simpler, handles bursts)
#   - Lazy refill: tokens are calculated on each request, not via a timer
#   - Per-client buckets identified by client_id (IP, API key, user ID)
#   - Configurable capacity and refill rate
#
# TRICK TO REMEMBER: "Bucket starts full. Each request drains 1 token.
#   Refill = elapsed_time * rate. Cap at max capacity."
#
# COMMON MISTAKES:
#   - Using a timer thread for refills (wasteful; use lazy calculation)
#   - Not handling the first request (bucket should start full)
#   - Integer overflow on elapsed time calculations
#   - Forgetting to cap tokens at max capacity after refill
# ---------------------------------------------------------------------------

class TokenBucket:
    """A single client's token bucket."""
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.tokens = float(capacity)
        self.last_refill = time.time()

    def _refill(self) -> None:
        """Lazily refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def consume(self) -> bool:
        """Try to consume one token. Returns True if allowed, False if rate limited."""
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


class RateLimiter:
    """
    Rate limiter using token bucket algorithm.

    API (middleware-style):
      allow_request(client_id) → True/False
      get_headers(client_id)   → rate limit headers for response

    Typical HTTP headers returned:
      X-RateLimit-Limit: 100
      X-RateLimit-Remaining: 57
      X-RateLimit-Reset: 1625097600
    """
    def __init__(self, capacity: int = 100, refill_rate: float = 10.0):
        self._capacity = capacity
        self._refill_rate = refill_rate
        self._buckets: dict[str, TokenBucket] = {}
        self._lock = threading.Lock()

    def _get_bucket(self, client_id: str) -> TokenBucket:
        if client_id not in self._buckets:
            self._buckets[client_id] = TokenBucket(self._capacity, self._refill_rate)
        return self._buckets[client_id]

    def allow_request(self, client_id: str) -> bool:
        """
        Check if a request from client_id should be allowed.
        Returns True (200 OK) or False (429 Too Many Requests).
        """
        with self._lock:
            bucket = self._get_bucket(client_id)
            return bucket.consume()

    def get_headers(self, client_id: str) -> dict[str, str]:
        """Return rate limit headers for the response."""
        with self._lock:
            bucket = self._get_bucket(client_id)
            bucket._refill()
            remaining = int(bucket.tokens)
            reset_in = (self._capacity - bucket.tokens) / self._refill_rate
            return {
                "X-RateLimit-Limit": str(self._capacity),
                "X-RateLimit-Remaining": str(remaining),
                "X-RateLimit-Reset": str(int(time.time() + reset_in)),
            }


# ---------------------------------------------------------------------------
# Problem 3: Design a Key-Value Store API
# ---------------------------------------------------------------------------
# APPROACH:
#   RESTful API for a key-value store with TTL, batch operations,
#   and basic querying. Think Redis-like but simpler.
#
# DESIGN DECISIONS:
#   - Keys are strings, values are any JSON-serializable data
#   - Optional TTL per key (lazy expiration on access)
#   - Batch GET/SET for efficiency
#   - Namespace support to isolate different apps/services
#
# TRICK TO REMEMBER: "Dict with TTL. Lazy expiration. Namespace = prefix."
#
# COMMON MISTAKES:
#   - Not handling TTL expiration (stale data returned)
#   - Exposing internal data structures (return copies, not references)
#   - Missing batch operations (N+1 API call problem)
#   - Not considering thread safety for concurrent access
# ---------------------------------------------------------------------------

class KVEntry:
    """A single key-value entry with optional TTL."""
    def __init__(self, value: Any, ttl_seconds: int | None = None):
        self.value = value
        self.created_at = time.time()
        self.ttl_seconds = ttl_seconds

    @property
    def is_expired(self) -> bool:
        if self.ttl_seconds is None:
            return False
        return time.time() - self.created_at > self.ttl_seconds


class KeyValueStore:
    """
    Key-Value Store service.

    API:
      PUT    /kv/:ns/:key     → put(ns, key, value, ttl)   → 200/201
      GET    /kv/:ns/:key     → get(ns, key)               → {"value": ...} or 404
      DELETE /kv/:ns/:key     → delete(ns, key)             → 204 or 404
      POST   /kv/:ns/_batch   → batch_get(ns, keys)         → {"results": {...}}
      POST   /kv/:ns/_batch   → batch_put(ns, items)        → 200
      GET    /kv/:ns          → list_keys(ns, prefix, limit) → {"keys": [...]}
    """
    def __init__(self):
        self._store: dict[str, dict[str, KVEntry]] = defaultdict(dict)
        self._lock = threading.Lock()

    def _full_key(self, namespace: str, key: str) -> tuple[str, str]:
        return namespace, key

    def put(self, namespace: str, key: str, value: Any,
            ttl_seconds: int | None = None) -> dict:
        """
        PUT /kv/:ns/:key — Set a key-value pair.
        Returns: {"status": 201} for new, {"status": 200} for update.
        """
        with self._lock:
            is_new = key not in self._store[namespace]
            self._store[namespace][key] = KVEntry(value, ttl_seconds)
            return {"status": 201 if is_new else 200}

    def get(self, namespace: str, key: str) -> dict:
        """
        GET /kv/:ns/:key — Get a value by key.
        Returns: {"value": ..., "status": 200} or {"error": ..., "status": 404}
        """
        with self._lock:
            ns_store = self._store.get(namespace, {})
            if key not in ns_store:
                return {"error": "Key not found", "status": 404}
            entry = ns_store[key]
            if entry.is_expired:
                del ns_store[key]
                return {"error": "Key not found", "status": 404}
            return {"value": entry.value, "status": 200}

    def delete(self, namespace: str, key: str) -> dict:
        """
        DELETE /kv/:ns/:key — Delete a key.
        """
        with self._lock:
            ns_store = self._store.get(namespace, {})
            if key not in ns_store:
                return {"error": "Key not found", "status": 404}
            del ns_store[key]
            return {"status": 204}

    def batch_get(self, namespace: str, keys: list[str]) -> dict:
        """
        POST /kv/:ns/_batch (action=get) — Get multiple keys at once.
        Returns: {"results": {key: value_or_None, ...}, "status": 200}
        """
        results = {}
        with self._lock:
            ns_store = self._store.get(namespace, {})
            for key in keys:
                entry = ns_store.get(key)
                if entry and not entry.is_expired:
                    results[key] = entry.value
                else:
                    results[key] = None
        return {"results": results, "status": 200}

    def batch_put(self, namespace: str,
                  items: list[dict]) -> dict:
        """
        POST /kv/:ns/_batch (action=put) — Set multiple key-value pairs.
        items: [{"key": "k", "value": "v", "ttl": 60}, ...]
        """
        with self._lock:
            for item in items:
                key = item["key"]
                value = item["value"]
                ttl = item.get("ttl")
                self._store[namespace][key] = KVEntry(value, ttl)
        return {"status": 200, "count": len(items)}

    def list_keys(self, namespace: str, prefix: str = "",
                  limit: int = 100) -> dict:
        """
        GET /kv/:ns?prefix=...&limit=... — List keys in a namespace.
        """
        with self._lock:
            ns_store = self._store.get(namespace, {})
            keys = []
            for key, entry in ns_store.items():
                if entry.is_expired:
                    continue
                if key.startswith(prefix):
                    keys.append(key)
                    if len(keys) >= limit:
                        break
            return {"keys": sorted(keys), "status": 200}


# ---------------------------------------------------------------------------
# Problem 4: Design a Paginated Search API
# ---------------------------------------------------------------------------
# APPROACH:
#   Build a product catalog API with filtering, sorting, and cursor-based
#   pagination. This tests REST API design, query parameter handling,
#   and pagination strategies.
#
# DESIGN DECISIONS:
#   - Cursor-based pagination (not offset) — more resilient to data changes
#   - Cursor = index into the sorted result set (in practice, use opaque tokens)
#   - Filter by category, price range; sort by price or name
#   - Response includes next_cursor and has_more for pagination
#
# TRICK TO REMEMBER: "Filter → Sort → Paginate. Cursor = position in sorted list."
#
# COMMON MISTAKES:
#   - Using offset pagination (breaks when items are inserted/deleted)
#   - Not returning has_more flag (client doesn't know when to stop)
#   - Sorting after pagination (inconsistent results across pages)
#   - Not validating page_size (DoS via page_size=999999)
# ---------------------------------------------------------------------------

class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"


class Product:
    """A product in the catalog."""
    def __init__(self, product_id: str, name: str, category: str, price: float):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
        }


class ProductCatalogAPI:
    """
    Product Catalog API with filtering, sorting, and pagination.

    API:
      GET  /products?category=...&min_price=...&max_price=...
                    &sort_by=price&order=asc
                    &cursor=...&page_size=20
           → {"products": [...], "next_cursor": "...", "has_more": true}

      GET  /products/:id  → single product
      POST /products      → create product
    """
    MAX_PAGE_SIZE = 100
    DEFAULT_PAGE_SIZE = 20

    def __init__(self):
        self._products: dict[str, Product] = {}

    def create_product(self, product_id: str, name: str,
                       category: str, price: float) -> dict:
        """POST /products — Add a product to the catalog."""
        if product_id in self._products:
            return {"error": "Product already exists", "status": 409}
        if price < 0:
            return {"error": "Price must be non-negative", "status": 400}
        self._products[product_id] = Product(product_id, name, category, price)
        return {"product": self._products[product_id].to_dict(), "status": 201}

    def get_product(self, product_id: str) -> dict:
        """GET /products/:id — Get a single product."""
        if product_id not in self._products:
            return {"error": "Product not found", "status": 404}
        return {"product": self._products[product_id].to_dict(), "status": 200}

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
        # Validate page_size
        page_size = max(1, min(page_size, self.MAX_PAGE_SIZE))

        # 1. FILTER
        results = list(self._products.values())
        if category is not None:
            results = [p for p in results if p.category == category]
        if min_price is not None:
            results = [p for p in results if p.price >= min_price]
        if max_price is not None:
            results = [p for p in results if p.price <= max_price]

        total_filtered = len(results)

        # 2. SORT
        reverse = (order == SortOrder.DESC)
        if sort_by == "price":
            results.sort(key=lambda p: p.price, reverse=reverse)
        else:
            results.sort(key=lambda p: p.name, reverse=reverse)

        # 3. PAGINATE (cursor-based)
        page = results[cursor: cursor + page_size]
        next_cursor = cursor + page_size if cursor + page_size < total_filtered else None
        has_more = next_cursor is not None

        return {
            "products": [p.to_dict() for p in page],
            "next_cursor": next_cursor,
            "has_more": has_more,
            "total_filtered": total_filtered,
            "status": 200,
        }


# ===========================================================================
# TESTS — run with: python -m pytest 12_api_design/solutions.py -v
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

    def test_expired_url(self):
        svc = URLShortener()
        code = svc.shorten("https://example.com", ttl_seconds=0)["short_code"]
        # TTL=0 means already expired
        time.sleep(0.01)
        result = svc.resolve(code)
        self.assertEqual(result["status"], 410)


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

    def test_refill(self):
        limiter = RateLimiter(capacity=2, refill_rate=1000)  # fast refill
        limiter.allow_request("c1")
        limiter.allow_request("c1")
        self.assertFalse(limiter.allow_request("c1"))
        time.sleep(0.01)  # allow some refill
        self.assertTrue(limiter.allow_request("c1"))

    def test_headers(self):
        limiter = RateLimiter(capacity=10, refill_rate=1)
        limiter.allow_request("c1")
        headers = limiter.get_headers("c1")
        self.assertEqual(headers["X-RateLimit-Limit"], "10")
        self.assertIn("X-RateLimit-Remaining", headers)
        self.assertIn("X-RateLimit-Reset", headers)


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

    def test_ttl_expiration(self):
        store = KeyValueStore()
        store.put("app1", "temp", "data", ttl_seconds=0)
        time.sleep(0.01)
        result = store.get("app1", "temp")
        self.assertEqual(result["status"], 404)

    def test_batch_get(self):
        store = KeyValueStore()
        store.put("app1", "a", 1)
        store.put("app1", "b", 2)
        result = store.batch_get("app1", ["a", "b", "c"])
        self.assertEqual(result["results"]["a"], 1)
        self.assertEqual(result["results"]["b"], 2)
        self.assertIsNone(result["results"]["c"])

    def test_batch_put(self):
        store = KeyValueStore()
        items = [
            {"key": "x", "value": 10},
            {"key": "y", "value": 20},
        ]
        store.batch_put("app1", items)
        self.assertEqual(store.get("app1", "x")["value"], 10)
        self.assertEqual(store.get("app1", "y")["value"], 20)

    def test_list_keys_with_prefix(self):
        store = KeyValueStore()
        store.put("app1", "user:1", "Alice")
        store.put("app1", "user:2", "Bob")
        store.put("app1", "order:1", "Pizza")
        result = store.list_keys("app1", prefix="user:")
        self.assertEqual(result["keys"], ["user:1", "user:2"])

    def test_namespace_isolation(self):
        store = KeyValueStore()
        store.put("app1", "key", "value1")
        store.put("app2", "key", "value2")
        self.assertEqual(store.get("app1", "key")["value"], "value1")
        self.assertEqual(store.get("app2", "key")["value"], "value2")


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

    def test_filter_by_price_range(self):
        api = self._make_catalog()
        result = api.search(min_price=50, max_price=300)
        names = [p["name"] for p in result["products"]]
        self.assertIn("Desk", names)
        self.assertIn("Chair", names)
        self.assertIn("Keyboard", names)
        self.assertNotIn("Mouse", names)

    def test_sort_by_price_asc(self):
        api = self._make_catalog()
        result = api.search(sort_by="price", order=SortOrder.ASC)
        prices = [p["price"] for p in result["products"]]
        self.assertEqual(prices, sorted(prices))

    def test_sort_by_price_desc(self):
        api = self._make_catalog()
        result = api.search(sort_by="price", order=SortOrder.DESC)
        prices = [p["price"] for p in result["products"]]
        self.assertEqual(prices, sorted(prices, reverse=True))

    def test_pagination(self):
        api = self._make_catalog()
        # Page 1
        r1 = api.search(page_size=2, cursor=0, sort_by="name")
        self.assertEqual(len(r1["products"]), 2)
        self.assertTrue(r1["has_more"])
        self.assertEqual(r1["next_cursor"], 2)
        # Page 2
        r2 = api.search(page_size=2, cursor=r1["next_cursor"], sort_by="name")
        self.assertEqual(len(r2["products"]), 2)
        self.assertTrue(r2["has_more"])
        # Page 3 (last)
        r3 = api.search(page_size=2, cursor=r2["next_cursor"], sort_by="name")
        self.assertEqual(len(r3["products"]), 1)
        self.assertFalse(r3["has_more"])

    def test_page_size_capped(self):
        api = self._make_catalog()
        result = api.search(page_size=9999)
        # Should be capped at MAX_PAGE_SIZE, but still return all 5
        self.assertEqual(len(result["products"]), 5)

    def test_product_not_found(self):
        api = ProductCatalogAPI()
        result = api.get_product("nonexistent")
        self.assertEqual(result["status"], 404)


if __name__ == "__main__":
    unittest.main()
