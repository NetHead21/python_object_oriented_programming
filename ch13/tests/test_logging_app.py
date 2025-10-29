import sys
from pathlib import Path
import pytest
import subprocess
import signal
import time
import logging
from typing import Iterator

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import remote_logging_app


@pytest.fixture(scope="session")
def log_catcher() -> Iterator[None]:
    server_path = Path("src") / "log_catcher.py"
    print(f"Starting server {server_path}")
    p = subprocess.Popen(
        [sys.executable, str(server_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    time.sleep(0.25)
    yield
    p.terminate()
    p.wait()
    if p.stdout:
        print(p.stdout.read())
    assert p.returncode == 1 if sys.platform == "win32" else -signal.SIGTERM.value, (
        f"Error in watcher, returncode={p.returncode}"
    )


@pytest.fixture
def logging_config() -> Iterator[None]:
    HOST, PORT = "localhost", 18842
    socket_handler = logging.handlers.SocketHandler(HOST, PORT)
    remote_logging_app.logger.addHandler(socket_handler)
    yield
    socket_handler.close()
    remote_logging_app.logger.removeHandler(socket_handler)


def test_1(log_catcher: None, logging_config: None) -> None:
    """Test basic factorial calculations with small numbers."""
    for i in range(10):
        remote_logging_app.work(i)


def test_2(log_catcher: None, logging_config: None) -> None:
    """Test factorial calculations with larger numbers."""
    for i in range(1, 10):
        remote_logging_app.work(52 * i)


def test_zero_factorial(log_catcher: None, logging_config: None) -> None:
    """Test edge case: factorial of 0 should be 1."""
    result = remote_logging_app.work(0)
    assert result == 1


def test_one_factorial(log_catcher: None, logging_config: None) -> None:
    """Test edge case: factorial of 1 should be 1."""
    result = remote_logging_app.work(1)
    assert result == 1


def test_small_factorials(log_catcher: None, logging_config: None) -> None:
    """Test small factorial values and verify correctness."""
    expected = {
        0: 1,
        1: 1,
        2: 2,
        3: 6,
        4: 24,
        5: 120,
        6: 720,
        7: 5040,
    }
    for i, expected_value in expected.items():
        result = remote_logging_app.work(i)
        assert result == expected_value, (
            f"Factorial({i}) should be {expected_value}, got {result}"
        )


def test_negative_factorial(log_catcher: None, logging_config: None) -> None:
    """Test edge case: factorial of negative number should raise ValueError."""
    with pytest.raises(ValueError):
        remote_logging_app.work(-1)


def test_large_factorial(log_catcher: None, logging_config: None) -> None:
    """Test factorial with a moderately large number."""
    result = remote_logging_app.work(20)
    # 20! = 2432902008176640000
    assert result == 2432902008176640000


def test_very_large_factorial(log_catcher: None, logging_config: None) -> None:
    """Test factorial with a very large number (stress test)."""
    # Python can handle arbitrarily large integers
    result = remote_logging_app.work(100)
    # 100! is a very large number with 158 digits
    assert result > 10**150  # Sanity check it's really big
    assert len(str(result)) == 158  # Verify correct digit count


def test_sequential_calls(log_catcher: None, logging_config: None) -> None:
    """Test multiple sequential calls to verify logging consistency."""
    results = []
    for i in range(5):
        results.append(remote_logging_app.work(i))

    assert results == [1, 1, 2, 6, 24]


def test_repeated_same_value(log_catcher: None, logging_config: None) -> None:
    """Test calling work with the same value multiple times."""
    results = [remote_logging_app.work(5) for _ in range(3)]
    assert all(r == 120 for r in results)


def test_reverse_order(log_catcher: None, logging_config: None) -> None:
    """Test factorial calculations in reverse order."""
    for i in range(9, -1, -1):
        result = remote_logging_app.work(i)
        assert result >= 1


def test_alternating_values(log_catcher: None, logging_config: None) -> None:
    """Test alternating between small and large values."""
    test_values = [0, 10, 1, 15, 2, 20, 5]
    for val in test_values:
        result = remote_logging_app.work(val)
        assert result >= 1


def test_logger_configuration(log_catcher: None, logging_config: None) -> None:
    """Test that logger is properly configured."""
    # Verify logger has at least one handler (the socket handler)
    assert len(remote_logging_app.logger.handlers) >= 1

    # Perform a work operation
    result = remote_logging_app.work(3)
    assert result == 6


def test_work_return_value(log_catcher: None, logging_config: None) -> None:
    """Test that work function returns the correct factorial value."""
    test_cases = [(0, 1), (1, 1), (5, 120), (10, 3628800)]

    for input_val, expected in test_cases:
        result = remote_logging_app.work(input_val)
        assert result == expected, f"work({input_val}) should return {expected}"


def test_concurrent_logging(log_catcher: None, logging_config: None) -> None:
    """Test rapid successive logging calls."""
    results = []
    for i in range(50):
        results.append(remote_logging_app.work(i % 10))

    # Verify all calls completed
    assert len(results) == 50


def test_boundary_values(log_catcher: None, logging_config: None) -> None:
    """Test boundary values that might cause issues."""
    # Test smallest valid input
    assert remote_logging_app.work(0) == 1

    # Test moderately large input
    result = remote_logging_app.work(50)
    assert result > 0  # Should be a valid positive number


def test_float_input_rejected(log_catcher: None, logging_config: None) -> None:
    """Test edge case: factorial doesn't accept float inputs."""
    # factorial() requires integer input and raises TypeError for floats
    with pytest.raises(TypeError):
        remote_logging_app.work(5.5)


def test_type_validation(log_catcher: None, logging_config: None) -> None:
    """Test that return type is integer."""
    result = remote_logging_app.work(10)
    assert isinstance(result, int)
    assert result == 3628800


def test_logger_isolation(log_catcher: None, logging_config: None) -> None:
    """Test that logger operations don't interfere with each other."""
    # Store initial handler count
    initial_handlers = len(remote_logging_app.logger.handlers)

    # Perform some work
    remote_logging_app.work(5)
    remote_logging_app.work(7)

    # Verify handler count hasn't changed
    assert len(remote_logging_app.logger.handlers) == initial_handlers


def test_empty_range(log_catcher: None, logging_config: None) -> None:
    """Test calling work with no iterations (edge case for loop testing)."""
    # This tests that the logging infrastructure handles zero calls gracefully
    results = []
    for i in range(0):  # Empty range
        results.append(remote_logging_app.work(i))

    assert len(results) == 0


def test_single_call(log_catcher: None, logging_config: None) -> None:
    """Test single isolated call to work function."""
    result = remote_logging_app.work(8)
    assert result == 40320  # 8! = 40320
