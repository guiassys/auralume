"""
Custom Gradio theme for Auralith to match a professional DAW's dark, industrial aesthetic.
"""
import gradio as gr
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes

class AuralithTheme(Base):
    def __init__(self):
        super().__init__(
            primary_hue=colors.blue,
            secondary_hue=colors.blue,
            neutral_hue=colors.gray,
            spacing_size=sizes.spacing_md,
            radius_size=sizes.radius_md,
            font=fonts.GoogleFont("Inter"),
        )
        self.name = "auralith_theme"
        self.set(
            # Colors
            body_background_fill="*neutral_950",
            body_background_fill_dark="*neutral_950",
            body_text_color="*neutral_50",
            body_text_color_dark="*neutral_50",

            background_fill_primary="*neutral_900",
            background_fill_primary_dark="*neutral_900",
            background_fill_secondary="*neutral_800",
            background_fill_secondary_dark="*neutral_800",

            border_color_accent="*primary_500",
            border_color_accent_dark="*primary_500",
            border_color_primary="*neutral_700",
            border_color_primary_dark="*neutral_700",

            color_accent_soft="*primary_800",
            color_accent_soft_dark="*primary_800",

            # Component-specific overrides
            button_primary_background_fill="linear-gradient(90deg, #4b6cb7 0%, #182848 100%)",
            button_primary_background_fill_dark="linear-gradient(90deg, #4b6cb7 0%, #182848 100%)",
            button_primary_text_color="white",
            button_primary_text_color_dark="white",

            slider_color="*primary_500",
            slider_color_dark="*primary_500",

            # Input fields
            input_background_fill="*neutral_800",
            input_background_fill_dark="*neutral_800",
            input_border_color="*neutral_700",
            input_border_color_dark="*neutral_700",
            input_placeholder_color="*neutral_400",
            input_placeholder_color_dark="*neutral_400",
        )

auralith_theme = AuralithTheme()

custom_css = """
/* --- Global Input Text Color --- */
.gradio-container .gr-input, .gradio-container .gr-textarea, .gradio-container .gr-dropdown {
    color: #ffffff !important; /* White text for all inputs */
}

.terminal-box textarea {
    background-color: #0b0f14 !important;
    color: #00ff41 !important; /* Neon Green */
    font-family: 'Courier New', monospace !important;
    border: 1px solid #182848 !important;
}
.main-header {
    text-align: center;
    margin-bottom: 20px;
    font-size: 2.5em;
    color: #ffffff;
    font-weight: bold;
}
/* Correctly target the slider's track fill for the progress bar effect */
.glowing-progress .track-fill {
    background-color: #00ff41 !important; /* Neon Green */
    box-shadow: 0 0 5px #00ff41, 0 0 10px #00ff41;
}
"""
