"""
Custom error handling module for job application automation.
Provides specialized exception classes and retry logic.
"""

import time
from enum import Enum
from typing import Optional, Callable, Any
from logger_setup import get_system_logger
from config import Config

logger = get_system_logger()

class ErrorCategory(Enum):
    """Categories of errors that can occur during job applications."""
    NETWORK = "network"
    FORM_VALIDATION = "form_validation"
    CAPTCHA = "captcha"
    AUTHENTICATION = "authentication"
    ELEMENT_NOT_FOUND = "element_not_found"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"

class ApplicationError(Exception):
    """Base exception for application-related errors."""
    def __init__(self, message: str, category: ErrorCategory = ErrorCategory.UNKNOWN):
        self.message = message
        self.category = category
        super().__init__(self.message)

class NetworkError(ApplicationError):
    """Raised when network-related issues occur."""
    def __init__(self, message: str):
        super().__init__(message, ErrorCategory.NETWORK)

class FormValidationError(ApplicationError):
    """Raised when form validation fails."""
    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        super().__init__(message, ErrorCategory.FORM_VALIDATION)

class CaptchaError(ApplicationError):
    """Raised when CAPTCHA is encountered."""
    def __init__(self, message: str = "CAPTCHA detected - manual intervention required"):
        super().__init__(message, ErrorCategory.CAPTCHA)

class AuthenticationError(ApplicationError):
    """Raised when authentication is required."""
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, ErrorCategory.AUTHENTICATION)

class ElementNotFoundError(ApplicationError):
    """Raised when expected element is not found on page."""
    def __init__(self, message: str, element_description: Optional[str] = None):
        self.element_description = element_description
        super().__init__(message, ErrorCategory.ELEMENT_NOT_FOUND)

class TimeoutError(ApplicationError):
    """Raised when operation times out."""
    def __init__(self, message: str):
        super().__init__(message, ErrorCategory.TIMEOUT)

def retry_with_backoff(
    func: Callable,
    max_attempts: int = None,
    initial_delay: float = None,
    backoff_multiplier: float = None,
    exceptions: tuple = (Exception,)
) -> Any:
    """
    Retry a function with exponential backoff.
    
    Args:
        func: Function to retry
        max_attempts: Maximum number of retry attempts (defaults to Config.MAX_RETRY_ATTEMPTS)
        initial_delay: Initial delay in seconds (defaults to Config.INITIAL_RETRY_DELAY)
        backoff_multiplier: Multiplier for exponential backoff (defaults to Config.RETRY_BACKOFF_MULTIPLIER)
        exceptions: Tuple of exceptions to catch and retry
    
    Returns:
        Result of the function call
    
    Raises:
        The last exception if all retries fail
    """
    if max_attempts is None:
        max_attempts = Config.MAX_RETRY_ATTEMPTS
    if initial_delay is None:
        initial_delay = Config.INITIAL_RETRY_DELAY
    if backoff_multiplier is None:
        backoff_multiplier = Config.RETRY_BACKOFF_MULTIPLIER
    
    last_exception = None
    delay = initial_delay
    
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"Attempt {attempt}/{max_attempts} for {func.__name__}")
            return func()
        except exceptions as e:
            last_exception = e
            logger.warning(f"Attempt {attempt} failed: {str(e)}")
            
            if attempt < max_attempts:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= backoff_multiplier
            else:
                logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
    
    raise last_exception

def handle_error(error: Exception, context: str = "") -> dict:
    """
    Handle an error and return structured error information.
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
    
    Returns:
        Dictionary with error details
    """
    error_info = {
        "error_type": type(error).__name__,
        "message": str(error),
        "context": context,
        "category": ErrorCategory.UNKNOWN.value,
        "requires_manual_intervention": False
    }
    
    if isinstance(error, ApplicationError):
        error_info["category"] = error.category.value
        
        # Determine if manual intervention is required
        if error.category in [ErrorCategory.CAPTCHA, ErrorCategory.AUTHENTICATION]:
            error_info["requires_manual_intervention"] = True
    
    logger.error(f"Error handled: {error_info}")
    return error_info

def is_retryable_error(error: Exception) -> bool:
    """
    Determine if an error is retryable.
    
    Args:
        error: The exception to check
    
    Returns:
        True if the error should be retried, False otherwise
    """
    # Don't retry CAPTCHA or authentication errors
    if isinstance(error, (CaptchaError, AuthenticationError)):
        return False
    
    # Retry network and timeout errors
    if isinstance(error, (NetworkError, TimeoutError)):
        return True
    
    # Retry element not found errors (page might still be loading)
    if isinstance(error, ElementNotFoundError):
        return True
    
    # Don't retry form validation errors
    if isinstance(error, FormValidationError):
        return False
    
    # Default: retry unknown errors
    return True
