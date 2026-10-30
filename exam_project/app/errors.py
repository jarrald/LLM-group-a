"""Application errors.

Every failure the app can explain has its own type here, so the UI can render a useful
message instead of a traceback, and so "retrieval failed" can never be mistaken for
"retrieval returned nothing".
"""

from __future__ import annotations


class StudyGraphError(Exception):
    """Base class for all application errors."""


class ConfigError(StudyGraphError):
    """An environment variable or configuration value is invalid."""


class ValidationError(StudyGraphError):
    """User-supplied data (a Buddy, a message) is not valid."""


class PersistenceError(StudyGraphError):
    """Reading or writing application data failed."""


class LlmUnavailableError(StudyGraphError):
    """The local Ollama server is not reachable or the model is not available."""


class LlmGenerationError(StudyGraphError):
    """The model was reachable but the generation request failed."""


class EmbeddingError(StudyGraphError):
    """An embedding could not be produced, or its dimension is inconsistent."""


class RetrievalError(StudyGraphError):
    """The vector store could not be reached or queried."""
