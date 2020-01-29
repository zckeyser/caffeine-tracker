import os

from mock import patch
import pytest

from logger import get_logger


class TestLogger():
    def test_logs_to_file_when_passed_file(self, tmpdir):
        log_filepath = os.path.join(tmpdir, "test.log")
        logger = get_logger(log_filepath)

        logger.info("My first log!")

        assert os.path.exists(log_filepath)

        with open(log_filepath) as f:
            line = f.readline().strip()

            assert line == "My first log!"

        os.remove(log_filepath)

    @patch("os.path.expanduser")
    @pytest.mark.skip(reason="Need to figure out how to do this w/captured output")
    def test_logs_to_correct_default_file(self, mock_expanduser, tmpdir):
        mock_expanduser.return_value = tmpdir

        log_filepath = os.path.join(tmpdir, "test.log")
        logger = get_logger()

        logger.info("My first log!")

        assert os.path.exists(log_filepath)

        with open(log_filepath) as f:
            line = f.readline().strip()

            assert line == "My first log!"

        os.remove(log_filepath)
