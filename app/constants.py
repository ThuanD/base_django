# Endpoint to health check API service
HEALTH_CHECK_API = "/api/health_check/"

TRUE_VALUES = ["1", "t", "true", "True", "TRUE", "y", "yes", "Yes", "YES"]


class CacheKey:
    REQUEST_COUNT = "APP:REQUEST_COUNT"


class Pagination:
    MAX_PAGE_SIZE = 100
    PAGE_SIZE_QUERY_PARAM = "page_size"
