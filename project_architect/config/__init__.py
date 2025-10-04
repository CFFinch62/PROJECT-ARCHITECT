"""
Project Architect Configuration Module

Handles application settings, user profiles, and configuration management.
Provides centralized configuration for the entire application.
"""

from .settings import Settings, AppSettings

__all__ = ['Settings', 'AppSettings']
