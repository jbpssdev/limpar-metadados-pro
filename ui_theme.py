"""
ui_theme.py - Sistema de Design e Cores do LimpaMetadados
Inspirado em interfaces modernas e limpas (SaaS / Apple / Dashboard)
com suporte nativo a Tema Claro e Escuro automático via CustomTkinter.
"""

# Tipografia
FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 18, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 12)
FONT_CARD_TITLE = (FONT_FAMILY, 13, "bold")
FONT_BODY = (FONT_FAMILY, 12)
FONT_CAPTION = (FONT_FAMILY, 11)
FONT_BADGE = (FONT_FAMILY, 11, "bold")
FONT_METRIC_VAL = (FONT_FAMILY, 16, "bold")
FONT_METRIC_LBL = (FONT_FAMILY, 11)

# Superfícies e Fundos (Claro, Escuro)
BG_APP = ("#F4F5F7", "#0B0F17")
BG_SIDEBAR = ("#FFFFFF", "#111722")
BG_CARD = ("#FFFFFF", "#161F2E")
BG_CARD_HOVER = ("#F9FAFB", "#1C273A")
BG_HEADER = ("#FFFFFF", "#161F2E")
BG_EMPTY_DROP = ("#F9FAFB", "#111722")

# Bordas e Separadores
BORDER_COLOR = ("#E5E7EB", "#222D3D")
BORDER_ACCENT = ("#C7D2FE", "#3B82F6")

# Textos
TEXT_PRIMARY = ("#111827", "#F9FAFB")
TEXT_SECONDARY = ("#6B7280", "#94A3B8")
TEXT_MUTED = ("#9CA3AF", "#64748B")

# Botões e Acentos
# Botão Primário (Estilo Moderno Escuro/Acento)
BTN_PRIMARY_BG = ("#18181B", "#3B82F6")
BTN_PRIMARY_HOVER = ("#27272A", "#2563EB")
BTN_PRIMARY_TEXT = ("#FFFFFF", "#FFFFFF")

# Botão Secundário
BTN_SECONDARY_BG = ("#F3F4F6", "#1E293B")
BTN_SECONDARY_HOVER = ("#E5E7EB", "#2B374A")
BTN_SECONDARY_TEXT = ("#1F2937", "#E2E8F0")

# Botão de Ação Suave (Ghost/Outline)
BTN_GHOST_HOVER = ("#F3F4F6", "#1E293B")

# Botão de Perigo / Cancelar
BTN_DANGER_BG = ("#FEE2E2", "#3B181A")
BTN_DANGER_HOVER = ("#FECDCD", "#502023")
BTN_DANGER_TEXT = ("#DC2626", "#F87171")

# Botão Sucesso (Abrir Pasta)
BTN_SUCCESS_BG = ("#DCFCE7", "#103520")
BTN_SUCCESS_HOVER = ("#BBF7D0", "#184A2D")
BTN_SUCCESS_TEXT = ("#15803D", "#4ADE80")

# Badges Semânticos (Pills com cores suaves pastel)
BADGE_PENDING_BG = ("#F3F4F6", "#232D3F")
BADGE_PENDING_TEXT = ("#4B5563", "#CBD5E1")

BADGE_PROCESSING_BG = ("#FEF3C7", "#3B2E0A")
BADGE_PROCESSING_TEXT = ("#B45309", "#FBBF24")

BADGE_SUCCESS_BG = ("#DCFCE7", "#0F3820")
BADGE_SUCCESS_TEXT = ("#15803D", "#4ADE80")

BADGE_ERROR_BG = ("#FEE2E2", "#3D1719")
BADGE_ERROR_TEXT = ("#B91C1C", "#F87171")

# Raio de Cantos (Border Radius)
RADIUS_CARD = 14
RADIUS_BUTTON = 10
RADIUS_PILL = 20
RADIUS_PROGRESS = 6
