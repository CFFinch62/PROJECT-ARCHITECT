"""
Project Architect Settings Dialog

Dialog for managing application settings and preferences.

Author: Chuck Finch - Fragillidae Software
"""

import logging
from pathlib import Path
from typing import Optional, Callable

import customtkinter as ctk
from tkinter import filedialog, messagebox

from ..config.settings import Settings


class SettingsDialog(ctk.CTkToplevel):
    """
    Settings configuration dialog.
    
    Allows users to modify application settings like appearance,
    default directories, and other preferences.
    """
    
    def __init__(self, parent, settings: Settings,
                 on_save: Optional[Callable[[], None]] = None):
        """
        Initialize settings dialog.
        
        Args:
            parent: Parent window
            settings: Settings instance
            on_save: Callback when settings are saved
        """
        super().__init__(parent)
        
        self.logger = logging.getLogger(__name__)
        self.settings = settings
        self.on_save_callback = on_save
        
        # Setup window
        self._setup_window()
        self._create_widgets()
        self._load_current_settings()
        
        self.logger.info("SettingsDialog initialized")
    
    def _setup_window(self):
        """Configure dialog window properties."""
        self.title("Settings")
        self.geometry("600x500")
        self.minsize(500, 400)
        
        # Make modal
        self.transient(self.master)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Delay grab_set until window is visible
        self.after(100, self._make_modal)
    
    def _make_modal(self):
        """Make the dialog modal after it's visible."""
        try:
            self.grab_set()
        except Exception as e:
            self.logger.warning(f"Could not set grab: {e}")
    
    def _create_widgets(self):
        """Create dialog widgets."""
        # Header
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚙️ Application Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Scrollable settings frame
        self.settings_frame = ctk.CTkScrollableFrame(self)
        self.settings_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.settings_frame.grid_columnconfigure(1, weight=1)
        
        # Appearance section
        self._create_section_header("Appearance", 0)
        
        # Appearance mode
        ctk.CTkLabel(self.settings_frame, text="Appearance Mode:").grid(
            row=1, column=0, sticky="w", padx=10, pady=5)
        self.appearance_var = ctk.StringVar(value="dark")
        self.appearance_menu = ctk.CTkOptionMenu(
            self.settings_frame,
            variable=self.appearance_var,
            values=["dark", "light", "system"],
            width=200
        )
        self.appearance_menu.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Color theme
        ctk.CTkLabel(self.settings_frame, text="Color Theme:").grid(
            row=2, column=0, sticky="w", padx=10, pady=5)
        self.theme_var = ctk.StringVar(value="blue")
        self.theme_menu = ctk.CTkOptionMenu(
            self.settings_frame,
            variable=self.theme_var,
            values=["blue", "green", "dark-blue"],
            width=200
        )
        self.theme_menu.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # Project Defaults section
        self._create_section_header("Project Defaults", 3)
        
        # Default output directory
        ctk.CTkLabel(self.settings_frame, text="Default Output Directory:").grid(
            row=4, column=0, sticky="w", padx=10, pady=5)
        
        dir_frame = ctk.CTkFrame(self.settings_frame)
        dir_frame.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        
        self.output_dir_var = ctk.StringVar(value="generated_projects")
        self.output_dir_entry = ctk.CTkEntry(dir_frame, textvariable=self.output_dir_var, width=250)
        self.output_dir_entry.pack(side="left", padx=(0, 5))
        
        browse_btn = ctk.CTkButton(dir_frame, text="Browse", width=70, command=self._browse_output_dir)
        browse_btn.pack(side="left")
        
        # Auto git init
        self.git_init_var = ctk.BooleanVar(value=True)
        self.git_init_check = ctk.CTkCheckBox(
            self.settings_frame, text="Auto-initialize Git repository",
            variable=self.git_init_var
        )
        self.git_init_check.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        # Auto venv create
        self.venv_var = ctk.BooleanVar(value=True)
        self.venv_check = ctk.CTkCheckBox(
            self.settings_frame, text="Auto-create virtual environment",
            variable=self.venv_var
        )
        self.venv_check.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        # Python version
        ctk.CTkLabel(self.settings_frame, text="Default Python Version:").grid(
            row=7, column=0, sticky="w", padx=10, pady=5)
        self.python_var = ctk.StringVar(value="3.12")
        self.python_menu = ctk.CTkOptionMenu(
            self.settings_frame,
            variable=self.python_var,
            values=["3.9", "3.10", "3.11", "3.12", "3.13"],
            width=200
        )
        self.python_menu.grid(row=7, column=1, sticky="w", padx=10, pady=5)

        # Logging section
        self._create_section_header("Logging", 8)

        # Enable logging
        self.logging_var = ctk.BooleanVar(value=True)
        self.logging_check = ctk.CTkCheckBox(
            self.settings_frame, text="Enable logging",
            variable=self.logging_var
        )
        self.logging_check.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Log level
        ctk.CTkLabel(self.settings_frame, text="Log Level:").grid(
            row=10, column=0, sticky="w", padx=10, pady=5)
        self.log_level_var = ctk.StringVar(value="INFO")
        self.log_level_menu = ctk.CTkOptionMenu(
            self.settings_frame,
            variable=self.log_level_var,
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            width=200
        )
        self.log_level_menu.grid(row=10, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)

        save_btn = ctk.CTkButton(
            button_frame, text="Save", command=self._save_settings, width=100
        )
        save_btn.pack(side="right", padx=5)

        cancel_btn = ctk.CTkButton(
            button_frame, text="Cancel", command=self._cancel, width=100
        )
        cancel_btn.pack(side="right", padx=5)

        reset_btn = ctk.CTkButton(
            button_frame, text="Reset to Defaults", command=self._reset_defaults, width=150
        )
        reset_btn.pack(side="left", padx=5)

    def _create_section_header(self, title: str, row: int):
        """Create a section header."""
        header = ctk.CTkLabel(
            self.settings_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=(15, 5))

    def _browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(title="Select Default Output Directory")
        if directory:
            self.output_dir_var.set(directory)

    def _load_current_settings(self):
        """Load current settings into UI."""
        self.appearance_var.set(self.settings.get('appearance_mode', 'dark'))
        self.theme_var.set(self.settings.get('color_theme', 'blue'))
        self.output_dir_var.set(self.settings.get('default_output_dir', 'generated_projects'))
        self.git_init_var.set(self.settings.get('auto_git_init', True))
        self.venv_var.set(self.settings.get('auto_venv_create', True))
        self.python_var.set(self.settings.get('default_python_version', '3.12'))
        self.logging_var.set(self.settings.get('enable_logging', True))
        self.log_level_var.set(self.settings.get('log_level', 'INFO'))

    def _save_settings(self):
        """Save settings and close dialog."""
        try:
            # Update settings
            self.settings.set('appearance_mode', self.appearance_var.get())
            self.settings.set('color_theme', self.theme_var.get())
            self.settings.set('default_output_dir', self.output_dir_var.get())
            self.settings.set('auto_git_init', self.git_init_var.get())
            self.settings.set('auto_venv_create', self.venv_var.get())
            self.settings.set('default_python_version', self.python_var.get())
            self.settings.set('enable_logging', self.logging_var.get())
            self.settings.set('log_level', self.log_level_var.get())

            # Save to file
            self.settings.save_settings()

            # Apply appearance changes immediately
            ctk.set_appearance_mode(self.appearance_var.get())

            # Call callback
            if self.on_save_callback:
                self.on_save_callback()

            messagebox.showinfo("Settings", "Settings saved successfully!")
            self._close()

        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def _reset_defaults(self):
        """Reset settings to defaults."""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            self.settings.reset_to_defaults()
            self._load_current_settings()
            messagebox.showinfo("Settings", "Settings reset to defaults.")

    def _cancel(self):
        """Cancel and close dialog."""
        self._close()

    def _close(self):
        """Close the dialog."""
        try:
            self.grab_release()
        except Exception:
            pass
        self.destroy()

