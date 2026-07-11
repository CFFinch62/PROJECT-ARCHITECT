"""
Project Architect Questionnaire Dialog

Interactive multi-step questionnaire dialog for gathering project requirements.

Author: Chuck Finch - Fragillidae Software
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable

import customtkinter as ctk
from tkinter import filedialog, messagebox

from ..core.questionnaire import QuestionnaireEngine, Question, QuestionType


class QuestionnaireDialog(ctk.CTkToplevel):
    """
    Interactive questionnaire dialog with multi-step wizard interface.
    
    Displays questions organized by section with navigation and validation.
    """
    
    def __init__(self, parent, questionnaire_engine: QuestionnaireEngine,
                 on_complete: Optional[Callable] = None):
        """
        Initialize questionnaire dialog.
        
        Args:
            parent: Parent window
            questionnaire_engine: Engine instance with loaded questionnaire
            on_complete: Callback function when questionnaire is completed
        """
        super().__init__(parent)
        
        self.logger = logging.getLogger(__name__)
        self.questionnaire_engine = questionnaire_engine
        self.on_complete_callback = on_complete
        
        # Get sections
        self.sections = self.questionnaire_engine.get_sections()
        self.current_section_index = 0
        
        # Widget storage
        self.question_widgets: Dict[str, Any] = {}
        
        # Setup window
        self._setup_window()
        self._create_widgets()
        self._show_current_section()
        
        self.logger.info("QuestionnaireDialog initialized")
    
    def _setup_window(self):
        """Configure dialog window properties."""
        self.title("Project Questionnaire")
        self.geometry("800x600")
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
        # Header with progress
        self._create_header()
        
        # Main content scrollable frame
        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Navigation buttons
        self._create_navigation()
    
    def _create_header(self):
        """Create header with section info and progress."""
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Section title
        self.section_title = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.section_title.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")
        
        # Progress label
        self.progress_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.grid(row=1, column=0, pady=5, sticky="w")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(header_frame)
        self.progress_bar.grid(row=1, column=1, pady=5, padx=(10, 0), sticky="ew")
    
    def _create_navigation(self):
        """Create navigation buttons."""
        nav_frame = ctk.CTkFrame(self)
        nav_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        nav_frame.grid_columnconfigure(1, weight=1)
        
        # Back button
        self.back_button = ctk.CTkButton(
            nav_frame,
            text="← Back",
            command=self._go_back,
            width=100
        )
        self.back_button.grid(row=0, column=0, padx=5)
        
        # Next button
        self.next_button = ctk.CTkButton(
            nav_frame,
            text="Next →",
            command=self._go_next,
            width=100
        )
        self.next_button.grid(row=0, column=2, padx=5)
        
        # Finish button (initially hidden)
        self.finish_button = ctk.CTkButton(
            nav_frame,
            text="✓ Finish",
            command=self._finish,
            width=100,
            fg_color="green",
            hover_color="dark green"
        )
        self.finish_button.grid(row=0, column=3, padx=5)
        self.finish_button.grid_remove()
    
    def _show_current_section(self):
        """Display questions for current section."""
        # Clear existing widgets
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        section = self.sections[self.current_section_index]
        questions = self.questionnaire_engine.get_questions_by_section(section)
        
        # Update header
        self.section_title.configure(text=f"Section: {section.replace('_', ' ').title()}")
        
        # Update progress
        progress = (self.current_section_index + 1) / len(self.sections)
        self.progress_bar.set(progress)
        self.progress_label.configure(
            text=f"Section {self.current_section_index + 1} of {len(self.sections)}"
        )
        
        # Update navigation buttons
        self.back_button.configure(state="normal" if self.current_section_index > 0 else "disabled")
        
        is_last_section = self.current_section_index == len(self.sections) - 1
        if is_last_section:
            self.next_button.grid_remove()
            self.finish_button.grid()
        else:
            self.next_button.grid()
            self.finish_button.grid_remove()
        
        # Display questions
        for question in questions:
            if self.questionnaire_engine.should_show_question(question):
                self._create_question_widget(question)
    
    def _create_question_widget(self, question: Question):
        """
        Create widget for a question.
        
        Args:
            question: Question to create widget for
        """
        # Question frame
        q_frame = ctk.CTkFrame(self.content_frame)
        q_frame.grid(sticky="ew", pady=10, padx=10)
        q_frame.grid_columnconfigure(0, weight=1)
        
        # Question label
        label_text = question.prompt
        if question.required:
            label_text += " *"
        
        label = ctk.CTkLabel(
            q_frame,
            text=label_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
        
        # Description (if provided)
        if question.description:
            desc_label = ctk.CTkLabel(
                q_frame,
                text=question.description,
                font=ctk.CTkFont(size=11),
                text_color="gray",
                anchor="w",
                wraplength=600
            )
            desc_label.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 5))
        
        # Input widget based on question type
        widget = self._create_input_widget(q_frame, question)
        
        if widget:
            widget.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
            self.question_widgets[question.id] = widget
    
    def _create_input_widget(self, parent, question: Question):
        """Create appropriate input widget for question type."""
        # Get existing response
        existing_value = self.questionnaire_engine.get_response(question.id, question.default)
        
        if question.type == QuestionType.TEXT or question.type == QuestionType.EMAIL \
           or question.type == QuestionType.IDENTIFIER or question.type == QuestionType.VERSION:
            # Text entry
            widget = ctk.CTkEntry(parent, placeholder_text=question.default or "")
            if existing_value:
                widget.insert(0, str(existing_value))
            return widget
        
        elif question.type == QuestionType.CHOICE:
            # Radio buttons
            widget = ctk.CTkFrame(parent)
            var = ctk.StringVar(value=existing_value or question.default or "")
            
            for option in question.options:
                rb = ctk.CTkRadioButton(
                    widget,
                    text=option,
                    variable=var,
                    value=option
                )
                rb.pack(anchor="w", pady=2)
            
            widget.var = var  # Store variable reference
            return widget
        
        elif question.type == QuestionType.MULTIPLE_CHOICE:
            # Checkboxes
            widget = ctk.CTkFrame(parent)
            widget.vars = {}
            
            existing_selections = existing_value if isinstance(existing_value, list) else []
            
            for option in question.options:
                var = ctk.BooleanVar(value=option in existing_selections)
                cb = ctk.CTkCheckBox(
                    widget,
                    text=option,
                    variable=var
                )
                cb.pack(anchor="w", pady=2)
                widget.vars[option] = var
            
            return widget
        
        elif question.type == QuestionType.BOOLEAN:
            # Switch
            widget = ctk.CTkSwitch(
                parent,
                text="Yes" if existing_value else "No",
                command=lambda: widget.configure(
                    text="Yes" if widget.get() == 1 else "No"
                )
            )
            if existing_value:
                widget.select()
            else:
                widget.deselect()
            return widget
        
        elif question.type == QuestionType.FILE_PATH or question.type == QuestionType.DIRECTORY_PATH:
            # File/directory picker
            widget = ctk.CTkFrame(parent)
            
            entry = ctk.CTkEntry(widget)
            entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
            if existing_value:
                entry.insert(0, str(existing_value))
            
            browse_btn = ctk.CTkButton(
                widget,
                text="Browse",
                width=80,
                command=lambda: self._browse_path(entry, question.type == QuestionType.DIRECTORY_PATH)
            )
            browse_btn.pack(side="right")
            
            widget.entry = entry  # Store entry reference
            return widget
        
        return None
    
    def _browse_path(self, entry: ctk.CTkEntry, is_directory: bool):
        """Browse for file or directory."""
        if is_directory:
            path = filedialog.askdirectory(title="Select Directory")
        else:
            path = filedialog.askopenfilename(title="Select File")
        
        if path:
            entry.delete(0, 'end')
            entry.insert(0, path)
    
    def _get_widget_value(self, question_id: str, question: Question):
        """Get value from question widget."""
        widget = self.question_widgets.get(question_id)
        if not widget:
            return None
        
        question_type = question.type
        
        if question_type in [QuestionType.TEXT, QuestionType.EMAIL, 
                            QuestionType.IDENTIFIER, QuestionType.VERSION]:
            return widget.get()
        
        elif question_type == QuestionType.CHOICE:
            return widget.var.get()
        
        elif question_type == QuestionType.MULTIPLE_CHOICE:
            return [option for option, var in widget.vars.items() if var.get()]
        
        elif question_type == QuestionType.BOOLEAN:
            return widget.get() == 1
        
        elif question_type in [QuestionType.FILE_PATH, QuestionType.DIRECTORY_PATH]:
            return widget.entry.get()
        
        return None
    
    def _validate_current_section(self) -> bool:
        """Validate all questions in current section."""
        section = self.sections[self.current_section_index]
        questions = self.questionnaire_engine.get_questions_by_section(section)
        
        for question in questions:
            if not self.questionnaire_engine.should_show_question(question):
                continue
            
            value = self._get_widget_value(question.id, question)
            
            # Validate
            is_valid, error_msg = self.questionnaire_engine.validate_response(question, value)
            
            if not is_valid:
                messagebox.showerror("Validation Error", f"{question.prompt}:\n{error_msg}")
                return False
            
            # Store response
            self.questionnaire_engine.set_response(question.id, value)
        
        return True
    
    def _go_back(self):
        """Navigate to previous section."""
        if self.current_section_index > 0:
            self.current_section_index -= 1
            self._show_current_section()
    
    def _go_next(self):
        """Navigate to next section."""
        if not self._validate_current_section():
            return
        
        if self.current_section_index < len(self.sections) - 1:
            self.current_section_index += 1
            self._show_current_section()
    
    def _finish(self):
        """Finish questionnaire and close dialog."""
        if not self._validate_current_section():
            return
        
        # Check if questionnaire is complete
        if not self.questionnaire_engine.is_complete():
            messagebox.showerror("Incomplete", "Please answer all required questions.")
            return
        
        # Call completion callback
        if self.on_complete_callback:
            try:
                self.on_complete_callback()
            except Exception as e:
                self.logger.error(f"Error in completion callback: {e}")
                messagebox.showerror("Error", f"Error completing questionnaire: {e}")
                return
        
        # Close dialog
        self.grab_release()
        self.destroy()
