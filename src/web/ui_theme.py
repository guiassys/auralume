"""
Custom Gradio theme for Auratune to match a professional DAW's aesthetic.
Using a softer, lighter theme as requested.
"""
import gradio as gr
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes

class AuratuneTheme(Base):
    def __init__(self):
        super().__init__(
            primary_hue=colors.indigo,
            secondary_hue=colors.slate,
            neutral_hue=colors.slate,
            spacing_size=sizes.spacing_md,
            radius_size=sizes.radius_md,
            font=fonts.GoogleFont("Inter"),
        )
        self.name = "auratune_theme"
        self.set(
            # Colors - Soft Light Theme
            body_background_fill="*neutral_50",
            body_text_color="*neutral_800",

            background_fill_primary="white",
            background_fill_secondary="*neutral_100",

            border_color_accent="*primary_500",
            border_color_primary="*neutral_200",

            color_accent_soft="*primary_100",

            # Component-specific overrides
            button_primary_background_fill="*primary_500",
            button_primary_text_color="white",
            
            button_secondary_background_fill="white",
            button_secondary_text_color="*neutral_800",

            slider_color="*primary_500",

            # Input fields
            input_background_fill="white",
            input_border_color="*neutral_300",
            input_placeholder_color="*neutral_400",
        )

auratune_theme = AuratuneTheme()

custom_css = """
/* --- Global Input Text Color --- */
.gradio-container .gr-input, .gradio-container .gr-textarea, .gradio-container .gr-dropdown {
    color: #1e293b !important; /* Dark text for all inputs in light mode */
}

.terminal-box textarea {
    background-color: #f1f5f9 !important;
    color: #334155 !important; /* Dark slate */
    font-family: 'Courier New', monospace !important;
    border: 1px solid #cbd5e1 !important;
}
.main-header {
    text-align: center;
    margin-bottom: 20px;
    font-size: 2.5em;
    color: #1e293b;
    font-weight: bold;
}

/* --- Pipeline Container Alignment --- */
#pipeline-container {
    align-items: center !important;
}

/* Remove background from instrument checkboxes */
.gradio-container .gr-checkboxgroup .gr-checkbox-label {
    background-color: transparent !important;
}

/* --- Compact Progress Indicator --- */
.gradio-container .compact {
    min-height: 0 !important;
    height: var(--size-8) !important; /* Match button height */
    padding: 0 !important;
}

.gradio-container .progress-indicator textarea {
    border: none !important;
    background-color: transparent !important;
    text-align: left !important;
    padding: 0 !important;
    line-height: var(--size-8) !important; /* Vertically center text */
    color: var(--body-text-color) !important;
}
"""
