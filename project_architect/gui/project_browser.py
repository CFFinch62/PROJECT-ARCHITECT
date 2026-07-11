"""
Project Architect Project Browser

Browse and preview available project templates.

Author: Chuck Finch - Fragillidae Software
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable

import customtkinter as ctk
from tkinter import messagebox

from ..core.template_engine import TemplateEngine


class ProjectBrowser(ctk.CTkToplevel):
    """
    Template browsing dialog.
    
    Displays available templates with descriptions and allows selection.
    """
    
    def __init__(self, parent, template_engine: TemplateEngine,
                 on_select: Optional[Callable[[str], None]] = None):
        """
        Initialize project browser.
        
        Args:
            parent: Parent window
            template_engine: Template engine instance
            on_select: Callback when template is selected
        """
        super().__init__(parent)
        
        self.logger = logging.getLogger(__name__)
        self.template_engine = template_engine
        self.on_select_callback = on_select
        
        self.selected_template = None
        
        # Setup window
        self._setup_window()
        self._create_widgets()
        self._load_templates()
        
        self.logger.info("ProjectBrowser initialized")
    
    def _setup_window(self):
        """Configure dialog window properties."""
        self.title("Browse Project Templates")
        self.geometry("900x600")
        self.minsize(700, 500)

        # Make modal - transient makes this a child of parent
        self.transient(self.master)

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Delay grab_set until window is visible to avoid "grab failed" error
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
            text="📚 Available Project Templates",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Select a template to create a new project",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(pady=5)
        
        # Main content area with template list and preview
        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Template list (left side)
        list_label = ctk.CTkLabel(
            content_frame,
            text="Templates",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        list_label.grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w")
        
        self.template_list_frame = ctk.CTkScrollableFrame(content_frame, width=250)
        self.template_list_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
        
        # Template preview (right side)
        preview_label = ctk.CTkLabel(
            content_frame,
            text="Template Details",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        preview_label.grid(row=0, column=1, padx=10, pady=(0, 5), sticky="w")
        
        self.preview_frame = ctk.CTkScrollableFrame(content_frame)
        self.preview_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        button_frame.grid_columnconfigure(1, weight=1)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._cancel,
            width=100
        )
        cancel_btn.grid(row=0, column=0, padx=5)
        
        self.select_btn = ctk.CTkButton(
            button_frame,
            text="Select Template",
            command=self._select_template,
            width=150,
            state="disabled"
        )
        self.select_btn.grid(row=0, column=2, padx=5)
    
    def _load_templates(self):
        """Load and display available templates."""
        try:
            templates = self.template_engine.list_available_templates()
            
            if not templates:
                no_templates_label = ctk.CTkLabel(
                    self.template_list_frame,
                    text="No templates found",
                    font=ctk.CTkFont(size=14)
                )
                no_templates_label.pack(pady=20)
                return
            
            for template in templates:
                self._create_template_item(template)
            
        except Exception as e:
            self.logger.error(f"Error loading templates: {e}")
            messagebox.showerror("Error", f"Failed to load templates: {e}")
    
    def _create_template_item(self, template_type: str):
        """Create clickable template item."""
        try:
            # Load template config
            config = self.template_engine.load_template_config(template_type)
            if not config:
                return
            
            template_info = config.get('template', {})
            name = template_info.get('name', template_type)
            description = template_info.get('description', 'No description available')
            
            # Create button for template
            btn = ctk.CTkButton(
                self.template_list_frame,
                text=name,
                command=lambda: self._show_template_preview(template_type, config),
                anchor="w",
                height=40
            )
            btn.pack(fill="x", pady=2, padx=5)
            
        except Exception as e:
            self.logger.error(f"Error creating template item for {template_type}: {e}")
    
    def _show_template_preview(self, template_type: str, config: Dict[str, Any]):
        """Show template details in preview pane."""
        # Clear preview
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        
        self.selected_template = template_type
        self.select_btn.configure(state="normal")
        
        template_info = config.get('template', {})
        
        # Template name
        name_label = ctk.CTkLabel(
            self.preview_frame,
            text=template_info.get('name', template_type),
            font=ctk.CTkFont(size=20, weight="bold")
        )
        name_label.pack(pady=(10, 5), anchor="w")
        
        # Description
        desc_frame = ctk.CTkFrame(self.preview_frame)
        desc_frame.pack(fill="x", pady=10)
        
        desc_label = ctk.CTkLabel(
            desc_frame,
            text="Description:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        desc_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        desc_text = ctk.CTkLabel(
            desc_frame,
            text=template_info.get('description', 'No description available'),
            font=ctk.CTkFont(size=12),
            wraplength=400,
            justify="left"
        )
        desc_text.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Frameworks/Technologies
        frameworks = template_info.get('frameworks', [])
        if frameworks:
            fw_frame = ctk.CTkFrame(self.preview_frame)
            fw_frame.pack(fill="x", pady=5)
            
            fw_label = ctk.CTkLabel(
                fw_frame,
                text="Supported Frameworks:",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            fw_label.pack(anchor="w", padx=10, pady=(10, 5))
            
            for framework in frameworks:
                fw_item = ctk.CTkLabel(
                    fw_frame,
                    text=f"• {framework}",
                    font=ctk.CTkFont(size=12)
                )
                fw_item.pack(anchor="w", padx=20, pady=2)
            
            fw_label.pack(pady=(0, 10))
        
        # Project structure preview
        structure = config.get('structure', [])
        if structure:
            struct_frame = ctk.CTkFrame(self.preview_frame)
            struct_frame.pack(fill="x", pady=5)
            
            struct_label = ctk.CTkLabel(
                struct_frame,
                text="Project Structure:",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            struct_label.pack(anchor="w", padx=10, pady=(10, 5))
            
            # Show first few structure items
            for item in structure[:10]:
                path = item.get('path', '')
                item_type = item.get('type', 'file')
                icon = "📁" if item_type == 'directory' else "📄"
                
                struct_item = ctk.CTkLabel(
                    struct_frame,
                    text=f"{icon} {path}",
                    font=ctk.CTkFont(size=11, family="monospace")
                )
                struct_item.pack(anchor="w", padx=20, pady=1)
            
            if len(structure) > 10:
                more_label = ctk.CTkLabel(
                    struct_frame,
                    text=f"... and {len(structure) - 10} more items",
                    font=ctk.CTkFont(size=11),
                    text_color="gray"
                )
                more_label.pack(anchor="w", padx=20, pady=5)
            
            struct_label.pack(pady=(0, 10))
        
        # Version
        version = template_info.get('version', 'Unknown')
        version_label = ctk.CTkLabel(
            self.preview_frame,
            text=f"Template Version: {version}",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        version_label.pack(anchor="w", pady=(10, 5))
    
    def _select_template(self):
        """Select template and close dialog."""
        if not self.selected_template:
            messagebox.showwarning("No Selection", "Please select a template first.")
            return
        
        # Call selection callback
        if self.on_select_callback:
            try:
                self.on_select_callback(self.selected_template)
            except Exception as e:
                self.logger.error(f"Error in selection callback: {e}")
                messagebox.showerror("Error", f"Error selecting template: {e}")
                return
        
        # Close dialog
        self.grab_release()
        self.destroy()
    
    def _cancel(self):
        """Cancel and close dialog."""
        self.grab_release()
        self.destroy()
