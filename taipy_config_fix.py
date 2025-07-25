"""
Taipy GUI Configuration Handler

This module provides configuration handling for Taipy GUI applications,
specifically fixing the run_browser configuration issue where environment
file settings were being overridden by command line argument processing.
"""
import os
import sys
import re
from typing import Dict, Any, Optional
from argparse import Namespace


class ConfigHandler:
    """Handles configuration parsing and validation for Taipy GUI."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize configuration handler.
        
        Args:
            config: Initial configuration dictionary
        """
        self.config = config or {}
        self._port_pattern = re.compile(r'^(auto|\d+)$')
    
    def handle_argparse(self, args: Namespace) -> None:
        """Process command line arguments and update configuration.
        
        Args:
            args: Parsed command line arguments
        """
        self._handle_port(args)
        self._handle_host(args)
        self._handle_debug(args)
        self._handle_reloader(args)
        self._handle_run_browser(args)
        self._handle_dark_mode(args)
        self._handle_ngrok_token(args)
        self._handle_webapp_path(args)
        self._handle_upload_folder(args)
        self._handle_client_url(args)
    
    def _handle_port(self, args: Namespace) -> None:
        """Handle port configuration from command line arguments.
        
        Args:
            args: Parsed command line arguments
        """
        if hasattr(args, 'taipy_port') and args.taipy_port:
            port_str = str(args.taipy_port).strip()
            if port_str == "auto":
                self.config["port"] = "auto"
            elif self._port_pattern.match(port_str):
                self.config["port"] = int(port_str) if port_str.isdigit() else port_str
            else:
                print("Warning: Port value for --port option is not valid.")
    
    def _handle_host(self, args: Namespace) -> None:
        """Handle host configuration from command line arguments.
        
        Args:
            args: Parsed command line arguments
        """
        if hasattr(args, 'taipy_host') and args.taipy_host:
            self.config["host"] = args.taipy_host
    
    def _handle_debug(self, args: Namespace) -> None:
        """Handle debug configuration from command line arguments.
        
        Args:
            args: Parsed command line arguments
        """
        if hasattr(args, 'taipy_debug') and args.taipy_debug:
            self.config["debug"] = True
        if hasattr(args, 'taipy_no_debug') and args.taipy_no_debug:
            self.config["debug"] = False
    
    def _handle_reloader(self, args: Namespace) -> None:
        """Handle reloader configuration from command line arguments.
        
        Args:
            args: Parsed command line arguments
        """
        if hasattr(args, 'taipy_use_reloader') and args.taipy_use_reloader:
            self.config["use_reloader"] = True
        if hasattr(args, 'taipy_no_reloader') and args.taipy_no_reloader:
            self.config["use_reloader"] = False
    
    def _handle_run_browser(self, args: Namespace) -> None:
        """Handle run_browser configuration from command line arguments.
        
        This method fixes the original issue where run_browser was always
        set to True, overriding environment file configurations.
        
        Args:
            args: Parsed command line arguments
        """
        # Only override if explicitly set via command line
        if "--run-browser" in sys.argv:
            self.config["run_browser"] = True
        elif "--no-run-browser" in sys.argv:
            self.config["run_browser"] = False
        elif hasattr(args, "taipy_run_browser") and args.taipy_run_browser:
            self.config["run_browser"] = True
        elif hasattr(args, "taipy_no_run_browser") and args.taipy_no_run_browser:
            self.config["run_browser"] = False
        # If no command line args, preserve existing config value
    
    def _handle_dark_mode(self, args: Namespace) -> None:
        """Handle dark mode configuration from command line arguments.
        
        Args:
            args: Parsed command line arguments
        """
        if hasattr(args, 'taipy_dark_mode') and args.taipy_dark_mode:
            self.config["dark_mode"] = True
        elif hasattr(args, 'taipy_light_mode') and args.taipy_light_mode:
            self.config["dark_mode"] = False
    
    def _handle_ngrok_token(self, args: Namespace) -> None:
        """Handle ngrok token configuration from command line arguments.
        
        Args:
            args: Parsed command line arguments
        """
        if hasattr(args, 'taipy_ngrok_token') and args.taipy_ngrok_token:
            self.config["ngrok_token"] = args.taipy_ngrok_token
    
    def _handle_webapp_path(self, args: Namespace) -> None:
        """Handle webapp path configuration from command line and environment.
        
        Args:
            args: Parsed command line arguments
        """
        if hasattr(args, 'taipy_webapp_path') and args.taipy_webapp_path:
            self.config["webapp_path"] = args.taipy_webapp_path
        elif os.environ.get("TAIPY_GUI_WEBAPP_PATH"):
            self.config["webapp_path"] = os.environ.get("TAIPY_GUI_WEBAPP_PATH")
    
    def _handle_upload_folder(self, args: Namespace) -> None:
        """Handle upload folder configuration from command line and environment.
        
        Args:
            args: Parsed command line arguments
        """
        if hasattr(args, 'taipy_upload_folder') and args.taipy_upload_folder:
            self.config["upload_folder"] = args.taipy_upload_folder
        elif os.environ.get("TAIPY_GUI_UPLOAD_FOLDER"):
            self.config["upload_folder"] = os.environ.get("TAIPY_GUI_UPLOAD_FOLDER")
    
    def _handle_client_url(self, args: Namespace) -> None:
        """Handle client URL configuration from command line arguments.
        
        Args:
            args: Parsed command line arguments
        """
        if hasattr(args, 'taipy_client_url') and args.taipy_client_url:
            self.config["client_url"] = args.taipy_client_url


# Unit Tests
import unittest
from unittest.mock import Mock, patch


class TestConfigHandler(unittest.TestCase):
    """Unit tests for ConfigHandler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.handler = ConfigHandler()
    
    def test_port_handling_valid_number(self):
        """Test port handling with valid numeric port."""
        args = Mock()
        args.taipy_port = "8080"
        self.handler._handle_port(args)
        self.assertEqual(self.handler.config["port"], 8080)
    
    def test_port_handling_auto(self):
        """Test port handling with 'auto' value."""
        args = Mock()
        args.taipy_port = "auto"
        self.handler._handle_port(args)
        self.assertEqual(self.handler.config["port"], "auto")
    
    @patch('builtins.print')
    def test_port_handling_invalid(self, mock_print):
        """Test port handling with invalid port value."""
        args = Mock()
        args.taipy_port = "invalid"
        self.handler._handle_port(args)
        mock_print.assert_called_with("Warning: Port value for --port option is not valid.")
        self.assertNotIn("port", self.handler.config)
    
    def test_run_browser_preserves_env_config(self):
        """Test that run_browser preserves environment file configuration."""
        self.handler.config = {"run_browser": False}
        args = Mock()
        args.taipy_run_browser = False
        args.taipy_no_run_browser = False
        
        with patch('sys.argv', ['script.py']):
            self.handler._handle_run_browser(args)
        
        self.assertFalse(self.handler.config["run_browser"])
    
    @patch('sys.argv', ['script.py', '--run-browser'])
    def test_run_browser_command_line_override(self):
        """Test that command line --run-browser overrides config."""
        self.handler.config = {"run_browser": False}
        args = Mock()
        self.handler._handle_run_browser(args)
        self.assertTrue(self.handler.config["run_browser"])
    
    @patch('sys.argv', ['script.py', '--no-run-browser'])
    def test_no_run_browser_command_line_override(self):
        """Test that command line --no-run-browser overrides config."""
        self.handler.config = {"run_browser": True}
        args = Mock()
        self.handler._handle_run_browser(args)
        self.assertFalse(self.handler.config["run_browser"])


if __name__ == "__main__":
    unittest.main()