"""
Provides a thread-safe log streaming mechanism using a queue.
This allows a worker thread to emit log messages that a UI thread can consume in real-time.
"""
import queue
from datetime import datetime
from typing import Generator

# A sentinel value to signal the end of the stream.
STREAM_END = None

class LogStream:
    """
    A thread-safe class to handle real-time log streaming.
    It uses a queue to pass messages from a producer (e.g., a generation task)
    to a consumer (e.g., a UI update loop).
    """
    def __init__(self):
        """Initializes a new instance of the LogStream with an empty queue."""
        self._queue = queue.Queue()

    def log(self, message: str, level: str = "INFO"):
        """
        Adds a formatted log message to the stream.

        Args:
            message (str): The log message content.
            level (str): The log level (e.g., "INFO", "WARN", "ERROR").
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{level}] [{timestamp}] {message}"
        self._queue.put(formatted_message)

    def end(self):
        """
        Signals that the logging process is complete by putting a sentinel
        value into the queue.
        """
        self._queue.put(STREAM_END)

    def stream_generator(self) -> Generator[str, None, None]:
        """
        A generator that yields log messages from the queue.
        This function will block and wait for new messages to arrive.
        It stops once the sentinel value (STREAM_END) is received.

        Yields:
            str: The next log message from the stream.
        """
        while True:
            message = self._queue.get()
            if message == STREAM_END:
                break
            yield message