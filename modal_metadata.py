"""
modal_metadata.py - Janela modal moderna para inspeção de metadados de vídeo.
"""

import os
import customtkinter as ctk
from core import obter_metadados
from ui_theme import (
    BG_APP, BG_CARD, BORDER_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    BTN_PRIMARY_BG, BTN_PRIMARY_HOVER, BTN_PRIMARY_TEXT, FONT_TITLE,
    FONT_CARD_TITLE, FONT_BODY, FONT_CAPTION, RADIUS_CARD, RADIUS_BUTTON
)

class ModalMetadata(ctk.CTkToplevel):
    def __init__(self, parent, file_path):
        super().__init__(parent)
        
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        
        self.title(f"Metadados: {self.filename}")
        self.geometry("640x520")
        self.minsize(500, 400)
        self.configure(fg_color=BG_APP)
        
        # Centraliza na tela do pai
        self.transient(parent)
        self.grab_set()
        
        # Layout Principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=RADIUS_CARD,
                                         border_width=1, border_color=BORDER_COLOR)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        icon_label = ctk.CTkLabel(self.header_frame, text="🔍", font=(FONT_TITLE[0], 26))
        icon_label.grid(row=0, column=0, rowspan=2, padx=(16, 12), pady=14)
        
        title_label = ctk.CTkLabel(self.header_frame, text=self.filename, font=FONT_CARD_TITLE,
                                   text_color=TEXT_PRIMARY, anchor="w")
        title_label.grid(row=0, column=1, sticky="w", pady=(12, 0))
        
        try:
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            size_str = f"{size_mb:.2f} MB"
        except Exception:
            size_str = "Desconhecido"
            
        subtitle_label = ctk.CTkLabel(self.header_frame, 
                                      text=f"Tamanho: {size_str} • Caminho: {os.path.dirname(file_path)}",
                                      font=FONT_CAPTION, text_color=TEXT_SECONDARY, anchor="w")
        subtitle_label.grid(row=1, column=1, sticky="w", pady=(0, 12), padx=(0, 16))
        
        # Área de Conteúdo dos Metadados (Scrollable)
        self.content_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=RADIUS_CARD,
                                          border_width=1, border_color=BORDER_COLOR)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=0)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        content_header = ctk.CTkLabel(self.content_frame, text="Tags e Informações Encontradas (FFmpeg):",
                                     font=FONT_CARD_TITLE, text_color=TEXT_PRIMARY, anchor="w")
        content_header.grid(row=0, column=0, sticky="w", padx=16, pady=(14, 8))
        
        self.textbox = ctk.CTkTextbox(self.content_frame, fg_color=("f8f9fa", "#0D1117"),
                                     text_color=TEXT_PRIMARY, font=("Consolas", 11),
                                     border_width=1, border_color=BORDER_COLOR, corner_radius=8)
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        
        # Botões de Ação Inferiores
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=16)
        self.footer_frame.grid_columnconfigure(0, weight=1)
        
        btn_close = ctk.CTkButton(self.footer_frame, text="Fechar", font=FONT_BODY,
                                  fg_color=BTN_PRIMARY_BG, hover_color=BTN_PRIMARY_HOVER,
                                  text_color=BTN_PRIMARY_TEXT, height=36, width=110,
                                  corner_radius=RADIUS_BUTTON, command=self.destroy)
        btn_close.grid(row=0, column=1, sticky="e")
        
        # Carrega os metadados de forma assíncrona ou rápida
        self.carregar_metadados()

    def carregar_metadados(self):
        self.textbox.insert("1.0", "Extraindo metadados do arquivo via FFmpeg...\n")
        raw_metadata = obter_metadados(self.file_path)
        
        self.textbox.delete("1.0", "end")
        if not raw_metadata or "Input #" not in raw_metadata:
            self.textbox.insert("1.0", raw_metadata if raw_metadata else "Nenhum metadado detectado.")
            return

        # Filtra e organiza o output do ffmpeg para ficar amigável
        linhas = raw_metadata.splitlines()
        filtrado = []
        capturando = False
        
        for linha in linhas:
            if "Input #" in linha or "Metadata:" in linha or "Stream #" in linha:
                capturando = True
            if "At least one output file must be specified" in linha or "Output #" in linha:
                capturando = False
            if capturando:
                filtrado.append(linha)
                
        if filtrado:
            self.textbox.insert("1.0", "\n".join(filtrado))
        else:
            self.textbox.insert("1.0", raw_metadata)
