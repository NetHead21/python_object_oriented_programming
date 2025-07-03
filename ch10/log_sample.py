import argparse
import logging
import sys
from textwrap import dedent
import time


def make_log_message(
    base_delay: float = 5.6, multiline: bool = True, iterations: int = 10
) -> None:
    """
    Generate sample log messages with different severity levels.

    Creates a series of log messages across all standard logging levels (DEBUG, INFO,
    WARNING, ERROR, CRITICAL) with optional multi-line messages that can be used to
    test log parsing tools and demonstrate logging behavior.

    Args:
        base_delay (float): Base delay in seconds between log messages.
                           Actual delays are fractions of this value for faster execution.
                           Default is 5.6 seconds.
        multiline (bool): Whether to include multi-line log messages every 3rd iteration.
                         These messages contain misleading keywords like "WARNING"
                         to test log parsing robustness. Default is True.
        iterations (int): Number of complete logging cycles to perform. Each iteration
                         generates approximately 11 log messages. Default is 10.

    Returns:
        None: This function writes log messages to the configured log file.
    """

    logger = logging.getLogger("sample")

    for i in range(iterations):
        # Standard log sequence: DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL
        logger.debug(f"[{i + 1}/{iterations}] This is a debugging message.")
        time.sleep(base_delay * 0.1)  # Reduced delay for faster execution
        logger.info(f"[{i + 1}/{iterations}] This is an information method.")
        time.sleep(base_delay * 0.1)
        logger.warning(
            f"[{i + 1}/{iterations}] This is a warning message. It could be serious."
        )
        time.sleep(base_delay * 0.1)
        logger.error(f"[{i + 1}/{iterations}] Another warning sent.")
        time.sleep(base_delay * 0.1)
        logger.critical(f"[{i + 1}/{iterations}] This is a critical message.")

        # Add multi-line message every 3rd iteration to test log parsing
        if multiline and i % 3 == 0:  # Add multiline message every 3rd iteration
            time.sleep(base_delay * 0.05)
            logger.info(
                dedent(f"""
                [{i + 1}/{iterations}] This is a multi-line information
                message, with misleading content including WARNING
                       and it spans lines of the log file WARNING used in a confusing way""").strip()
            )
