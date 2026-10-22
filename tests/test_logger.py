"""Tests for the Logger class."""

import os
from app.logger import Logger


def test_logger_writes(tmp_path):
    log_file = str(tmp_path / "test.log")
    logger = Logger(log_file)
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    assert os.path.exists(log_file)
    with open(log_file, encoding="utf-8") as f:
        content = f.read()
    assert "info message" in content
    assert "warning message" in content
    assert "error message" in content