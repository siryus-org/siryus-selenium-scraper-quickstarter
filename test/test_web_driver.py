import os
import sys
from unittest.mock import Mock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from actions import web_driver


def test_get_page_closes_driver_when_navigation_fails(monkeypatch):
    driver = Mock()
    driver.get.side_effect = RuntimeError('navigation failed')
    close_driver = Mock()

    monkeypatch.setattr(web_driver, 'get_driver_firefox', lambda: driver)
    monkeypatch.setattr(web_driver, 'close_driver', close_driver)

    with pytest.raises(RuntimeError, match='navigation failed'):
        web_driver.get_page('firefox')

    close_driver.assert_called_once_with(driver)


def test_close_driver_does_not_propagate_quit_errors(monkeypatch):
    driver = Mock()
    driver.quit.side_effect = RuntimeError('driver already stopped')

    monkeypatch.setattr(web_driver, '_get_driver_processes', lambda _: [])

    web_driver.close_driver(driver)

    driver.quit.assert_called_once_with()


def test_close_driver_terminates_surviving_processes(monkeypatch):
    driver = Mock()
    process = Mock()
    terminate_processes = Mock()

    monkeypatch.setattr(web_driver, '_get_driver_processes', lambda _: [process])
    monkeypatch.setattr(
        web_driver.psutil, 'wait_procs', lambda processes, timeout: ([], processes)
    )
    monkeypatch.setattr(web_driver, '_terminate_processes', terminate_processes)

    web_driver.close_driver(driver)

    terminate_processes.assert_called_once_with([process])
