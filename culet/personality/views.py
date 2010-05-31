from django.contrib.auth import authenticate

def myselves(request):
    """List of current user's personalities."""

def become(request, alternate):
    """Log a user in as one of their alternates."""

def delete(request, alternate, confirmation=None):
    """Delete a personality."""

def create(request):
    """Create a personality."""

def update(request, alternate):
    """Update a personality."""
