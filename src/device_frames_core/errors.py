class DeviceFramesError(Exception):
    """Base error for device-frames-core."""


class TemplateNotFoundError(DeviceFramesError):
    """Raised when a template cannot be found for a device/variation."""


class TemplateAmbiguousError(DeviceFramesError):
    """Raised when multiple templates match without enough filters."""
