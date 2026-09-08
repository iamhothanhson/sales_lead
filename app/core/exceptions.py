class ApplicationError(Exception):
    status_code = 500
    code = "INTERNAL_SERVER_ERROR"
    message = "An unexpected error occurred."


class DatabaseUnavailableError(ApplicationError):
    status_code = 503
    code = "DATABASE_UNAVAILABLE"
    message = "Database is unavailable."


class ActivityDatabaseError(DatabaseUnavailableError):
    """Raised when an activity database operation fails."""


class LeadDatabaseError(DatabaseUnavailableError):
    """Raised when a lead database operation fails."""


class LeadNotFoundError(ApplicationError):
    status_code = 404
    code = "LEAD_NOT_FOUND"
    message = "Lead was not found."


class LeadConflictError(ApplicationError):
    status_code = 409
    code = "LEAD_CONFLICT"
    message = "Lead conflicts with existing data."


class LeadPersistenceError(LeadDatabaseError):
    """Raised when a lead cannot be safely persisted."""
