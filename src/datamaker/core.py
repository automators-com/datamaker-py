from typing import Callable, Dict, Optional, Any
from requests import Response  # Assuming you're using the 'requests' library for HTTP

Fetch = Callable[[str, Optional[dict]], Response]
HTTPMethod = str  # Could further restrict to specific strings like 'get', 'post', etc.

RequestClient = Dict[str, Fetch]
Headers = Dict[str, Optional[str]]
DefaultQuery = Dict[str, Optional[str]]

Agent = Any
