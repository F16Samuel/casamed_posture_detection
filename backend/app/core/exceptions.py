class InvalidVideoFormat(Exception):
    """Raised when uploaded video format is not supported."""
    def __init__(self, message: str = "Invalid video format. Supported formats are: mp4, mov, avi."):
        self.message = message
        super().__init__(self.message)


class InvalidVideoDuration(Exception):
    """Raised when video duration is outside allowed range."""
    def __init__(self, message: str = "Video duration must be between 10 and 15 seconds."):
        self.message = message
        super().__init__(self.message)


class NoPersonDetected(Exception):
    """Raised when no human pose is detected in the video."""
    def __init__(self, message: str = "No person detected in the video. Please ensure full body is visible."):
        self.message = message
        super().__init__(self.message)


class MultiplePersonsDetected(Exception):
    """Raised when multiple people are detected in the video."""
    def __init__(self, message: str = "Multiple persons detected. Please upload a video with a single individual."):
        self.message = message
        super().__init__(self.message)