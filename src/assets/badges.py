circle_filled = '<svg width="14" height="14" style="margin-right: 4px; vertical-align: middle;" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10s10-4.47 10-10S17.53 2 12 2Z"/></svg>'
circle_nested = '<svg width="14" height="14" style="margin-right: 4px; vertical-align: middle;" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10s10-4.47 10-10S17.53 2 12 2m0 18a8 8 0 1 1 0-16a8 8 0 0 1 0 16m0-12a4 4 0 1 0 0 8a4 4 0 0 0 0-8"/></svg>'
circle_outline = '<svg width="14" height="14" style="margin-right: 4px; vertical-align: middle;" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10s10-4.47 10-10S17.53 2 12 2m0 18a8 8 0 1 1 0-16a8 8 0 0 1 0 16m0-14a6 6 0 1 0 0 12a6 6 0 0 0 0-12Z"/></svg>'

def make_badge(icon, text, bg_color, text_color): # needs to be one line to work in AgGrid markdown renderer
    return f"<span style='background-color: {bg_color}; color: {text_color}; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.9em; display: inline-flex; align-items: center; line-height: normal'>{icon} {text}</span>"

USER_BADGE = make_badge(circle_filled, "VERIFIERAD", "#E8F5E9", "#2E7D32")
AI_BADGE = make_badge(circle_nested, "AI-FÖRSLAG", "#E3F2FD", "#1565C0")
UNCERTAIN_BADGE = make_badge(circle_outline, "GRANSKA", "#FFF3E0", "#E65100")
