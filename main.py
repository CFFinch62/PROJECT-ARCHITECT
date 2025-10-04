#!/usr/bin/env python3
"""
Project Architect - Main Application Entry Point

A comprehensive project template system that generates well-structured,
documented, and AI-friendly development projects.

Author: Chuck Finch - Fragillidae Software
Version: 1.0.0
"""

import sys
import os
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    import customtkinter as ctk
    from project_architect.gui.main_window import MainWindow
    from project_architect.config.settings import Settings
    from project_architect.utils.validation import setup_logging
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def setup_application():
    """Initialize application settings and logging."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Project Architect application")
    
    # Initialize settings
    settings = Settings()
    settings.load_settings()
    
    # Set CustomTkinter appearance
    ctk.set_appearance_mode(settings.get('appearance_mode', 'dark'))
    ctk.set_default_color_theme(settings.get('color_theme', 'blue'))
    
    return settings, logger


def main():
    """Main application entry point."""
    try:
        # Setup application
        settings, logger = setup_application()
        
        # Create and run main window
        app = MainWindow()
        logger.info("Application initialized successfully")
        
        # Start the application
        app.mainloop()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        print(f"An unexpected error occurred: {e}")
        print("Check the log file for more details.")
        sys.exit(1)
    finally:
        logging.info("Project Architect application shutting down")


if __name__ == "__main__":
    main()
