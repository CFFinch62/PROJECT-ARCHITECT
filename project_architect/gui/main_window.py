"""
Project Architect Main Window

The main GUI window for the Project Architect application, providing
an intuitive interface for creating and updating software projects.

Author: Chuck Finch - Fragillidae Software
"""

import logging
import tkinter as tk
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable

import customtkinter as ctk
from tkinter import filedialog, messagebox

from ..core.questionnaire import QuestionnaireEngine, QuestionnaireMode
from ..core.template_engine import TemplateEngine
from ..core.project_updater import ProjectUpdater, UpdateType
from ..config.settings import Settings
from .questionnaire_dialog import QuestionnaireDialog
from .settings_dialog import SettingsDialog
from .project_browser import ProjectBrowser


class MainWindow(ctk.CTk):
    """
    Main application window for Project Architect.
    
    Provides the primary user interface for creating new projects,
    updating existing projects, and managing templates.
    """
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        self.logger = logging.getLogger(__name__)
        
        # Initialize core components
        self.settings = Settings()
        self.questionnaire_engine = QuestionnaireEngine()
        self.template_engine = TemplateEngine()
        self.project_updater: Optional[ProjectUpdater] = None
        
        # UI state
        self.current_project_path: Optional[Path] = None
        self.current_mode = QuestionnaireMode.NEW_PROJECT
        
        # Setup window
        self._setup_window()
        self._create_widgets()
        self._setup_layout()
        self._bind_events()
        
        # Load settings
        self._load_settings()
        
        self.logger.info("MainWindow initialized")
    
    def _setup_window(self):
        """Configure main window properties."""
        self.title("Project Architect v1.0.0")
        self.geometry("1200x800")
        self.minsize(1000, 600)
        
        # Configure grid weights for responsive design
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Create main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Create header
        self._create_header()
        
        # Create sidebar
        self._create_sidebar()
        
        # Create main content area
        self._create_content_area()
        
        # Create status bar
        self._create_status_bar()
    
    def _create_header(self):
        """Create the application header."""
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Logo/Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏗️ Project Architect",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Professional Project Template System",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")
        
        # Settings button
        settings_btn = ctk.CTkButton(
            header_frame,
            text="⚙️ Settings",
            width=100,
            command=self._open_settings
        )
        settings_btn.grid(row=0, column=2, padx=20, pady=10, sticky="e")
    
    def _create_sidebar(self):
        """Create the sidebar with main navigation."""
        self.sidebar = ctk.CTkFrame(self.main_frame, width=250)
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=(5, 2), pady=5)
        self.sidebar.grid_propagate(False)
        
        # Sidebar title
        sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="Actions",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        sidebar_title.pack(pady=20)
        
        # New Project section
        new_project_frame = ctk.CTkFrame(self.sidebar)
        new_project_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            new_project_frame,
            text="Create New Project",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
        
        self.new_project_btn = ctk.CTkButton(
            new_project_frame,
            text="🆕 Start New Project",
            command=self._start_new_project,
            height=40
        )
        self.new_project_btn.pack(pady=10, padx=10, fill="x")
        
        # Update Project section
        update_project_frame = ctk.CTkFrame(self.sidebar)
        update_project_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            update_project_frame,
            text="Update Existing Project",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
        
        self.open_project_btn = ctk.CTkButton(
            update_project_frame,
            text="📂 Open Project",
            command=self._open_existing_project,
            height=40
        )
        self.open_project_btn.pack(pady=5, padx=10, fill="x")
        
        self.update_project_btn = ctk.CTkButton(
            update_project_frame,
            text="🔄 Update Project",
            command=self._start_project_update,
            height=40,
            state="disabled"
        )
        self.update_project_btn.pack(pady=5, padx=10, fill="x")
        
        self.update_tech_spec_btn = ctk.CTkButton(
            update_project_frame,
            text="📋 Update Tech Spec",
            command=self._start_tech_spec_update,
            height=40,
            state="disabled"
        )
        self.update_tech_spec_btn.pack(pady=5, padx=10, fill="x")
        
        # Templates section
        templates_frame = ctk.CTkFrame(self.sidebar)
        templates_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            templates_frame,
            text="Templates",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
        
        self.browse_templates_btn = ctk.CTkButton(
            templates_frame,
            text="🗂️ Browse Templates",
            command=self._browse_templates,
            height=40
        )
        self.browse_templates_btn.pack(pady=5, padx=10, fill="x")
        
        # Current project info
        self.project_info_frame = ctk.CTkFrame(self.sidebar)
        self.project_info_frame.pack(fill="x", padx=10, pady=20)
        
        self.project_info_label = ctk.CTkLabel(
            self.project_info_frame,
            text="No project loaded",
            font=ctk.CTkFont(size=12),
            wraplength=200
        )
        self.project_info_label.pack(pady=10)
    
    def _create_content_area(self):
        """Create the main content area."""
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=(2, 5), pady=5)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Create tabview for different content
        self.tabview = ctk.CTkTabview(self.content_frame)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Welcome tab
        self.welcome_tab = self.tabview.add("Welcome")
        self._create_welcome_content()
        
        # Questionnaire tab (initially hidden)
        self.questionnaire_tab = None
        
        # Project info tab (initially hidden)
        self.project_info_tab = None
    
    def _create_welcome_content(self):
        """Create welcome tab content."""
        welcome_frame = ctk.CTkScrollableFrame(self.welcome_tab)
        welcome_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Welcome message
        welcome_title = ctk.CTkLabel(
            welcome_frame,
            text="Welcome to Project Architect",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        welcome_title.pack(pady=20)
        
        welcome_text = ctk.CTkLabel(
            welcome_frame,
            text="Create professional, well-documented, and AI-friendly software projects\n"
                 "with comprehensive templates and automated setup.",
            font=ctk.CTkFont(size=16),
            wraplength=600
        )
        welcome_text.pack(pady=10)
        
        # Quick start section
        quick_start_frame = ctk.CTkFrame(welcome_frame)
        quick_start_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            quick_start_frame,
            text="Quick Start",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)
        
        # Available templates
        templates_label = ctk.CTkLabel(
            quick_start_frame,
            text="Available Project Types:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        templates_label.pack(pady=(10, 5))
        
        # Load and display available templates
        available_templates = self.template_engine.list_available_templates()
        
        for template in available_templates:
            template_btn = ctk.CTkButton(
                quick_start_frame,
                text=f"📁 {template.replace('_', ' ').title()}",
                command=lambda t=template: self._start_new_project_with_type(t),
                height=35,
                width=200
            )
            template_btn.pack(pady=2)
        
        # Recent projects section
        recent_frame = ctk.CTkFrame(welcome_frame)
        recent_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            recent_frame,
            text="Recent Projects",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)
        
        # TODO: Implement recent projects list
        no_recent_label = ctk.CTkLabel(
            recent_frame,
            text="No recent projects",
            font=ctk.CTkFont(size=14)
        )
        no_recent_label.pack(pady=10)
    
    def _create_status_bar(self):
        """Create the status bar."""
        self.status_frame = ctk.CTkFrame(self.main_frame, height=30)
        self.status_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.status_frame.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # Progress bar (initially hidden)
        self.progress_bar = ctk.CTkProgressBar(self.status_frame)
        self.progress_bar.pack(side="right", padx=10, pady=5)
        self.progress_bar.pack_forget()  # Hide initially
    
    def _setup_layout(self):
        """Configure the layout and responsive behavior."""
        # Configure main frame grid weights
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
    
    def _bind_events(self):
        """Bind event handlers."""
        # Window close event
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _load_settings(self):
        """Load application settings."""
        try:
            self.settings.load_settings()
            
            # Apply theme settings
            appearance_mode = self.settings.get('appearance_mode', 'dark')
            color_theme = self.settings.get('color_theme', 'blue')
            
            ctk.set_appearance_mode(appearance_mode)
            ctk.set_default_color_theme(color_theme)
            
            self.logger.info("Settings loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error loading settings: {e}")
            messagebox.showerror("Settings Error", f"Failed to load settings: {e}")
    
    def _start_new_project(self):
        """Start the new project creation process."""
        # TODO: Show project type selection dialog
        self._show_project_type_dialog()
    
    def _start_new_project_with_type(self, project_type: str):
        """Start new project creation with specified type."""
        try:
            self.current_mode = QuestionnaireMode.NEW_PROJECT
            self.current_project_type = project_type  # Store the project type

            # Load questionnaire for project type
            success = self.questionnaire_engine.load_questionnaire(project_type, self.current_mode)

            if not success:
                messagebox.showerror("Error", f"Failed to load questionnaire for {project_type}")
                return

            # Show questionnaire tab
            self._show_questionnaire_tab()

            self._update_status(f"Starting new {project_type} project")
            
        except Exception as e:
            self.logger.error(f"Error starting new project: {e}")
            messagebox.showerror("Error", f"Failed to start new project: {e}")
    
    def _open_existing_project(self):
        """Open an existing project for updates."""
        try:
            # Select project directory
            project_path = filedialog.askdirectory(
                title="Select Project Directory",
                mustexist=True
            )

            if not project_path:
                return

            project_path = Path(project_path)

            # Initialize project updater
            self.project_updater = ProjectUpdater(project_path)
            self.current_project_path = project_path

            # Check if this is a valid Project Architect project
            if not self.project_updater.is_valid_project():
                messagebox.showwarning(
                    "Not a Project Architect Project",
                    f"The selected folder does not contain Project Architect metadata.\n\n"
                    f"This may be a folder that wasn't created by Project Architect.\n"
                    f"Some features may not work correctly.\n\n"
                    f"For best results, select a project created with Project Architect."
                )

            # Enable update buttons
            self.update_project_btn.configure(state="normal")
            self.update_tech_spec_btn.configure(state="normal")

            # Update project info display
            project_info = self.project_updater.get_project_info()
            info_text = f"Project: {project_info['name']}\n"
            info_text += f"Type: {project_info['type']}\n"
            info_text += f"Version: {project_info['version']}"

            self.project_info_label.configure(text=info_text)

            # Show project info tab
            self._show_project_info_tab()

            self._update_status(f"Opened project: {project_info['name']}")

        except Exception as e:
            self.logger.error(f"Error opening project: {e}")
            messagebox.showerror("Error", f"Failed to open project: {e}")
    
    def _start_project_update(self):
        """Start project update process."""
        if not self.project_updater:
            messagebox.showerror("Error", "No project loaded")
            return
        
        # TODO: Show update type selection dialog
        self._show_update_type_dialog()
    
    def _start_tech_spec_update(self):
        """Start technical specification update process."""
        if not self.project_updater:
            messagebox.showerror("Error", "No project loaded")
            return
        
        try:
            # Start tech spec update interview
            success = self.project_updater.start_update_interview(UpdateType.TECH_SPEC_REVISION)
            
            if not success:
                messagebox.showerror("Error", "Failed to start tech spec update")
                return
            
            self.current_mode = QuestionnaireMode.TECH_SPEC_UPDATE
            
            # Show questionnaire tab
            self._show_questionnaire_tab()
            
            self._update_status("Starting technical specification update")
            
        except Exception as e:
            self.logger.error(f"Error starting tech spec update: {e}")
            messagebox.showerror("Error", f"Failed to start tech spec update: {e}")
    
    def _browse_templates(self):
        """Browse available templates."""
        try:
            browser = ProjectBrowser(
                self,
                self.template_engine,
                on_select=self._on_template_selected
            )
            browser.focus()
        except Exception as e:
            self.logger.error(f"Error opening template browser: {e}")
            messagebox.showerror("Error", f"Failed to open template browser: {e}")

    def _on_template_selected(self, template_type: str):
        """Handle template selection from browser."""
        self._start_new_project_with_type(template_type)

    def _open_settings(self):
        """Open settings dialog."""
        try:
            dialog = SettingsDialog(
                self,
                self.settings,
                on_save=self._on_settings_saved
            )
            dialog.focus()
        except Exception as e:
            self.logger.error(f"Error opening settings dialog: {e}")
            messagebox.showerror("Error", f"Failed to open settings: {e}")

    def _on_settings_saved(self):
        """Handle settings saved callback."""
        self.logger.info("Settings saved, applying changes...")
        self._load_settings()
    
    def _show_project_type_dialog(self):
        """Show project type selection dialog."""
        # TODO: Implement project type selection dialog
        # For now, default to desktop_gui
        self._start_new_project_with_type("desktop_gui")
    
    def _show_update_type_dialog(self):
        """Show update type selection dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Select Update Type")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.after(100, lambda: dialog.grab_set())

        # Header
        ctk.CTkLabel(
            dialog,
            text="Select Update Type",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            dialog,
            text="Choose the type of update you want to perform:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 20))

        # Update type buttons
        update_types = [
            (UpdateType.FEATURE_ADDITION, "➕ Add New Feature", "Add new features or functionality to your project"),
            (UpdateType.ARCHITECTURE_CHANGE, "🏗️ Architecture Change", "Modify project structure or architecture"),
            (UpdateType.DEPENDENCY_UPDATE, "📦 Update Dependencies", "Update or add project dependencies"),
            (UpdateType.DOCUMENTATION_UPDATE, "📝 Update Documentation", "Update project documentation"),
            (UpdateType.CONFIGURATION_CHANGE, "⚙️ Configuration Change", "Modify project configuration"),
        ]

        def select_update_type(update_type: UpdateType):
            dialog.destroy()
            self._perform_update(update_type)

        for update_type, label, description in update_types:
            btn_frame = ctk.CTkFrame(dialog)
            btn_frame.pack(fill="x", padx=40, pady=5)

            btn = ctk.CTkButton(
                btn_frame,
                text=label,
                command=lambda ut=update_type: select_update_type(ut),
                width=200,
                height=35
            )
            btn.pack(side="left", padx=5)

            ctk.CTkLabel(
                btn_frame,
                text=description,
                font=ctk.CTkFont(size=11)
            ).pack(side="left", padx=10)

        # Cancel button
        ctk.CTkButton(
            dialog,
            text="Cancel",
            command=dialog.destroy,
            width=100
        ).pack(pady=20)

    def _perform_update(self, update_type: UpdateType):
        """Perform the selected update type."""
        try:
            if not self.project_updater:
                messagebox.showerror("Error", "No project loaded")
                return

            # Start update interview
            success = self.project_updater.start_update_interview(update_type)

            if not success:
                messagebox.showerror("Error", f"Failed to start {update_type.value} update")
                return

            # Set mode based on update type
            self.current_mode = QuestionnaireMode.UPDATE_PROJECT

            # Show questionnaire
            self._show_questionnaire_tab()

            self._update_status(f"Starting {update_type.value} update")

        except Exception as e:
            self.logger.error(f"Error performing update: {e}")
            messagebox.showerror("Error", f"Failed to perform update: {e}")
    
    def _show_questionnaire_tab(self):
        """Show the questionnaire dialog."""
        # Use the project_updater's questionnaire engine if we're doing an update
        # otherwise use the main questionnaire engine for new projects
        if hasattr(self, 'project_updater') and self.project_updater is not None:
            if self.current_mode in [QuestionnaireMode.TECH_SPEC_UPDATE,
                                     QuestionnaireMode.UPDATE_PROJECT,
                                     QuestionnaireMode.FEATURE_ADDITION]:
                engine = self.project_updater.questionnaire_engine
            else:
                engine = self.questionnaire_engine
        else:
            engine = self.questionnaire_engine

        # Open the questionnaire dialog
        dialog = QuestionnaireDialog(
            self,
            engine,
            on_complete=self._on_questionnaire_complete
        )
        dialog.focus()

    def _on_questionnaire_complete(self):
        """Handle questionnaire completion - generate the project."""
        try:
            from ..core.questionnaire import QuestionnaireResponse
            from datetime import datetime

            # Get project type from stored value
            project_type = getattr(self, 'current_project_type', 'desktop_gui')
            project_name = self.questionnaire_engine.responses.get('project_name', 'Untitled')

            # Ask user for output directory
            output_dir = filedialog.askdirectory(
                title="Select Output Directory for Generated Project",
                mustexist=True
            )

            if not output_dir:
                messagebox.showwarning("Cancelled", "Project generation cancelled.")
                return

            # Create project folder with project name inside the selected directory
            # Convert project name to valid folder name (replace spaces with underscores, etc.)
            safe_project_name = project_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
            output_path = Path(output_dir) / safe_project_name

            # Create the project directory
            output_path.mkdir(parents=True, exist_ok=True)

            # Create QuestionnaireResponse object
            response = QuestionnaireResponse(
                project_name=project_name,
                project_type=project_type,
                mode=self.current_mode,
                responses=self.questionnaire_engine.responses,
                timestamp=datetime.now().isoformat()
            )

            # Generate the project using template engine
            self._update_status("Generating project...")

            success = self.template_engine.generate_project_structure(
                project_type=project_type,
                output_dir=output_path,
                responses=response
            )

            if success:
                messagebox.showinfo(
                    "Success",
                    f"Project generated successfully!\n\nLocation: {output_path}"
                )
                self._update_status(f"Project generated at {output_path}")
            else:
                messagebox.showerror("Error", "Failed to generate project. Check logs for details.")
                self._update_status("Project generation failed")

        except Exception as e:
            self.logger.error(f"Error generating project: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to generate project: {e}")
    
    def _show_project_info_tab(self):
        """Show project information tab."""
        if self.project_info_tab is None:
            self.project_info_tab = self.tabview.add("Project Info")
        else:
            # Clear existing content
            for widget in self.project_info_tab.winfo_children():
                widget.destroy()

        # Switch to project info tab
        self.tabview.set("Project Info")

        # Create scrollable content frame
        content_frame = ctk.CTkScrollableFrame(self.project_info_tab)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        if not self.project_updater:
            ctk.CTkLabel(
                content_frame,
                text="No project loaded",
                font=ctk.CTkFont(size=16)
            ).pack(expand=True)
            return

        # Get project info
        project_info = self.project_updater.get_project_info()

        # Project header
        header_frame = ctk.CTkFrame(content_frame)
        header_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            header_frame,
            text=f"📁 {project_info['name']}",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=10, padx=20, anchor="w")

        # Project details section
        details_frame = ctk.CTkFrame(content_frame)
        details_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            details_frame,
            text="Project Details",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10, padx=20, anchor="w")

        details = [
            ("Project Type:", project_info.get('type', 'Unknown')),
            ("Version:", project_info.get('version', '1.0.0')),
            ("Created:", project_info.get('created_at', 'Unknown')),
            ("Last Updated:", project_info.get('last_updated', 'Never')),
            ("Update Count:", str(project_info.get('update_count', 0))),
            ("Location:", str(self.project_updater.project_path)),
        ]

        for label, value in details:
            row_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=20, pady=2)
            ctk.CTkLabel(row_frame, text=label, font=ctk.CTkFont(weight="bold"), width=120, anchor="w").pack(side="left")
            ctk.CTkLabel(row_frame, text=value, anchor="w").pack(side="left", fill="x", expand=True)

        # Update history section
        history_frame = ctk.CTkFrame(content_frame)
        history_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            history_frame,
            text="Update History",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10, padx=20, anchor="w")

        update_history = self.project_updater.get_update_history()

        if not update_history:
            ctk.CTkLabel(
                history_frame,
                text="No updates yet",
                font=ctk.CTkFont(size=12)
            ).pack(pady=10, padx=20, anchor="w")
        else:
            for update in update_history[-5:]:  # Show last 5 updates
                update_row = ctk.CTkFrame(history_frame)
                update_row.pack(fill="x", padx=20, pady=2)

                update_type = update.update_type.value if hasattr(update.update_type, 'value') else str(update.update_type)
                ctk.CTkLabel(
                    update_row,
                    text=f"• {update_type}: {update.description} (v{update.new_version})",
                    anchor="w"
                ).pack(side="left", fill="x", expand=True)

                ctk.CTkLabel(
                    update_row,
                    text=update.timestamp[:10] if len(update.timestamp) > 10 else update.timestamp,
                    font=ctk.CTkFont(size=11)
                ).pack(side="right")

        # Actions section
        actions_frame = ctk.CTkFrame(content_frame)
        actions_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            actions_frame,
            text="Quick Actions",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10, padx=20, anchor="w")

        btn_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="🔄 Update Project",
            command=self._start_project_update,
            width=150
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="📋 Update Tech Spec",
            command=self._start_tech_spec_update,
            width=150
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="📂 Open in File Manager",
            command=lambda: self._open_in_file_manager(self.project_updater.project_path),
            width=180
        ).pack(side="left", padx=5)

    def _open_in_file_manager(self, path: Path):
        """Open path in system file manager."""
        import subprocess
        import sys
        try:
            if sys.platform == 'darwin':
                subprocess.run(['open', str(path)])
            elif sys.platform == 'win32':
                subprocess.run(['explorer', str(path)])
            else:
                subprocess.run(['xdg-open', str(path)])
        except Exception as e:
            self.logger.error(f"Error opening file manager: {e}")
            messagebox.showerror("Error", f"Could not open file manager: {e}")
    
    def _update_status(self, message: str):
        """Update status bar message."""
        self.status_label.configure(text=message)
        self.logger.info(f"Status: {message}")
    
    def _on_closing(self):
        """Handle window closing event."""
        try:
            # Save settings
            self.settings.save_settings()
            
            # Cleanup
            self.logger.info("MainWindow closing")
            
        except Exception as e:
            self.logger.error(f"Error during window closing: {e}")
        
        finally:
            self.destroy()
