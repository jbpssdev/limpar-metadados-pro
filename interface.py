"""
interface.py - Interface Gráfica Moderna do LimpaMetadados
Construída com CustomTkinter + TkinterDnD2 para visual profissional tipo Dashboard,
suporte completo a Arrastar e Soltar (Drag and Drop), cards estilizados e métricas.
"""

import os
import sys
import re
import threading
import subprocess
from tkinter import messagebox, filedialog
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES

from core import verificar_ffmpeg, limpar_metadados, validar_arquivo_video, security_logger
from modal_metadata import ModalMetadata
from ui_theme import (
    FONT_FAMILY, FONT_TITLE, FONT_SUBTITLE, FONT_CARD_TITLE, FONT_BODY,
    FONT_CAPTION, FONT_BADGE, FONT_METRIC_VAL, FONT_METRIC_LBL,
    BG_APP, BG_SIDEBAR, BG_CARD, BG_CARD_HOVER, BG_HEADER, BG_EMPTY_DROP,
    BORDER_COLOR, BORDER_ACCENT, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    BTN_PRIMARY_BG, BTN_PRIMARY_HOVER, BTN_PRIMARY_TEXT,
    BTN_SECONDARY_BG, BTN_SECONDARY_HOVER, BTN_SECONDARY_TEXT,
    BTN_DANGER_BG, BTN_DANGER_HOVER, BTN_DANGER_TEXT,
    BTN_SUCCESS_BG, BTN_SUCCESS_HOVER, BTN_SUCCESS_TEXT,
    BADGE_PENDING_BG, BADGE_PENDING_TEXT,
    BADGE_PROCESSING_BG, BADGE_PROCESSING_TEXT,
    BADGE_SUCCESS_BG, BADGE_SUCCESS_TEXT,
    BADGE_ERROR_BG, BADGE_ERROR_TEXT,
    RADIUS_CARD, RADIUS_BUTTON, RADIUS_PILL, RADIUS_PROGRESS
)

from version import VERSION, APP_NAME

# Configurações iniciais do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LimpaMetadadosApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        
        # Configurações da Janela
        self.title(f"{APP_NAME} • Remoção Segura de Metadados")
        self.geometry("1060x780")
        self.minsize(920, 640)
        self.configure(fg_color=BG_APP)
        self._configurar_icone()
        
        # Variáveis de Estado
        self.arquivos_selecionados = []  # Lista de dicts {path, name, size, status, widget, ...}
        self.pasta_saida = None
        self.processando = False
        self.cancelar_solicitado = False
        self.filtro_atual = "Todos"
        
        # Layout em Grid Principal: 2 colunas (Sidebar fixa, Conteúdo flexível)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Criação dos Módulos da Interface
        self._criar_sidebar()
        self._criar_conteudo_principal()
        
        # Configurar Drag and Drop em toda a janela
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self._on_drop_files)
        
        # Verificação do FFmpeg ao iniciar
        self.after(200, self._verificar_ffmpeg_startup)

    # -------------------------------------------------------------------------
    # 1. BARRA LATERAL (SIDEBAR)
    # -------------------------------------------------------------------------
    def _criar_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(
            self, width=240, corner_radius=0, fg_color=BG_SIDEBAR,
            border_width=1, border_color=BORDER_COLOR
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(6, weight=1)  # Espaço flexível antes do rodapé
        
        # Identidade Visual / Logo
        brand_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        brand_frame.grid(row=0, column=0, padx=20, pady=(24, 16), sticky="ew")
        
        logo_icon = ctk.CTkLabel(brand_frame, text="🛡️", font=(FONT_FAMILY, 28))
        logo_icon.pack(side="left", padx=(0, 10))
        
        brand_text_box = ctk.CTkFrame(brand_frame, fg_color="transparent")
        brand_text_box.pack(side="left", fill="x")
        
        lbl_app_name = ctk.CTkLabel(brand_text_box, text="Limpar Metadados PRO", font=FONT_TITLE, text_color=TEXT_PRIMARY)
        lbl_app_name.pack(anchor="w")
        
        badge_ver = ctk.CTkLabel(brand_text_box, text="v1.0.4 PRO • 100% Offline", font=FONT_CAPTION, text_color=TEXT_SECONDARY)
        badge_ver.pack(anchor="w")
        
        # Separador visual
        sep1 = ctk.CTkFrame(self.sidebar_frame, height=1, fg_color=BORDER_COLOR)
        sep1.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        
        # Botão Principal: Adicionar Vídeos
        self.btn_add = ctk.CTkButton(
            self.sidebar_frame, text="+ Adicionar Vídeos", font=FONT_CARD_TITLE,
            fg_color=BTN_PRIMARY_BG, hover_color=BTN_PRIMARY_HOVER, text_color=BTN_PRIMARY_TEXT,
            height=44, corner_radius=RADIUS_BUTTON, command=self.selecionar_arquivos
        )
        self.btn_add.grid(row=2, column=0, padx=16, pady=(0, 12), sticky="ew")
        
        # Card de Pasta de Saída
        output_box = ctk.CTkFrame(self.sidebar_frame, fg_color=BG_CARD, corner_radius=RADIUS_BUTTON,
                                  border_width=1, border_color=BORDER_COLOR)
        output_box.grid(row=3, column=0, padx=16, pady=6, sticky="ew")
        
        lbl_out_title = ctk.CTkLabel(output_box, text="📁 Pasta de Destino:", font=FONT_CAPTION, text_color=TEXT_SECONDARY)
        lbl_out_title.pack(anchor="w", padx=12, pady=(10, 2))
        
        self.lbl_out_path = ctk.CTkLabel(output_box, text="Mesma pasta dos originais", font=FONT_BODY,
                                         text_color=TEXT_PRIMARY, wraplength=180, justify="left")
        self.lbl_out_path.pack(anchor="w", padx=12, pady=(0, 8))
        
        btn_change_out = ctk.CTkButton(
            output_box, text="Alterar Pasta", font=FONT_CAPTION,
            fg_color=BTN_SECONDARY_BG, hover_color=BTN_SECONDARY_HOVER, text_color=BTN_SECONDARY_TEXT,
            height=28, corner_radius=6, command=self.escolher_pasta_saida
        )
        btn_change_out.pack(fill="x", padx=10, pady=(0, 10))
        
        # Botão Limpar Fila
        self.btn_clear = ctk.CTkButton(
            self.sidebar_frame, text="🗑️ Limpar Fila", font=FONT_BODY,
            fg_color="transparent", hover_color=BTN_SECONDARY_HOVER, text_color=TEXT_SECONDARY,
            border_width=1, border_color=BORDER_COLOR, height=36, corner_radius=RADIUS_BUTTON,
            command=self.limpar_lista
        )
        self.btn_clear.grid(row=4, column=0, padx=16, pady=8, sticky="ew")
        
        # Rodapé da Sidebar: Seletor de Tema
        footer_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        footer_frame.grid(row=7, column=0, padx=16, pady=20, sticky="ew")
        
        lbl_theme = ctk.CTkLabel(footer_frame, text="Tema da Interface:", font=FONT_CAPTION, text_color=TEXT_SECONDARY)
        lbl_theme.pack(anchor="w", pady=(0, 4))
        
        self.theme_menu = ctk.CTkOptionMenu(
            footer_frame, values=["Escuro", "Claro", "Sistema"],
            font=FONT_CAPTION, fg_color=BTN_SECONDARY_BG, button_color=BTN_SECONDARY_HOVER,
            text_color=TEXT_PRIMARY, height=30, corner_radius=6,
            command=self._mudar_tema
        )
        self.theme_menu.pack(fill="x")
        self.theme_menu.set("Escuro")

    # -------------------------------------------------------------------------
    # 2. CONTEÚDO PRINCIPAL (DASHBOARD & LISTA)
    # -------------------------------------------------------------------------
    def _criar_conteudo_principal(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=24, pady=24)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)  # A lista de arquivos expande
        
        # --- TOP HEADER: 3 CARDS DE MÉTRICAS ---
        metrics_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        metrics_frame.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        metrics_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Card 1: Total na Fila
        self.card_total = self._criar_card_metrica(metrics_frame, 0, "📊 Fila de Vídeos", "0 arquivos", "0.0 MB total")
        # Card 2: Proteção
        self.card_prot = self._criar_card_metrica(metrics_frame, 1, "🛡️ Proteção Ativa", "Bitexact & Strip", "GPS, Câmera e Tags")
        # Card 3: Destino
        self.card_dest = self._criar_card_metrica(metrics_frame, 2, "📂 Saída", "Pasta Original", "Sufixo _limpo")
        
        # --- BARRA DE FILTROS & AÇÕES DA LISTA ---
        filter_bar = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=40)
        filter_bar.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        filter_bar.grid_columnconfigure(0, weight=1)
        
        lbl_section = ctk.CTkLabel(filter_bar, text="Arquivos Selecionados", font=FONT_CARD_TITLE, text_color=TEXT_PRIMARY)
        lbl_section.grid(row=0, column=0, sticky="w")
        
        self.filter_segmented = ctk.CTkSegmentedButton(
            filter_bar, values=["Todos (0)", "Pendentes (0)", "Concluídos (0)"],
            font=FONT_CAPTION, fg_color=BG_CARD, selected_color=BTN_PRIMARY_BG,
            selected_hover_color=BTN_PRIMARY_HOVER, unselected_color=BG_CARD,
            unselected_hover_color=BG_CARD_HOVER, text_color=TEXT_PRIMARY,
            command=self._filtrar_lista
        )
        self.filter_segmented.grid(row=0, column=1, sticky="e")
        self.filter_segmented.set("Todos (0)")
        
        # --- CONTAINER CENTRAL (DROP ZONE OU LISTA DE CARDS) ---
        self.list_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.list_container.grid(row=2, column=0, sticky="nsew")
        self.list_container.grid_columnconfigure(0, weight=1)
        self.list_container.grid_rowconfigure(0, weight=1)
        
        # Estado Vazio (Drop Zone Inicial)
        self.drop_zone_frame = ctk.CTkFrame(
            self.list_container, fg_color=BG_EMPTY_DROP, corner_radius=RADIUS_CARD,
            border_width=2, border_color=BORDER_COLOR
        )
        self.drop_zone_frame.grid(row=0, column=0, sticky="nsew")
        self._construir_drop_zone()
        
        # Scrollable Frame para os cards dos arquivos
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.list_container, fg_color="transparent", corner_radius=RADIUS_CARD
        )
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        # O scroll_frame é exibido apenas quando houver arquivos
        
        # --- PAINEL INFERIOR: PROGRESSO & AÇÕES ---
        self.bottom_frame = ctk.CTkFrame(
            self.main_frame, fg_color=BG_CARD, corner_radius=RADIUS_CARD,
            border_width=1, border_color=BORDER_COLOR
        )
        self.bottom_frame.grid(row=3, column=0, sticky="ew", pady=(16, 0))
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        
        # Barra de Progresso Superior no Card
        self.progress_bar = ctk.CTkProgressBar(
            self.bottom_frame, progress_color=BTN_PRIMARY_BG, fg_color=BG_EMPTY_DROP,
            height=8, corner_radius=RADIUS_PROGRESS
        )
        self.progress_bar.grid(row=0, column=0, columnspan=3, sticky="ew", padx=20, pady=(16, 12))
        self.progress_bar.set(0)
        
        # Status Text
        status_box = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        status_box.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 16))
        
        self.lbl_status_icon = ctk.CTkLabel(status_box, text="⚡", font=(FONT_FAMILY, 14))
        self.lbl_status_icon.pack(side="left", padx=(0, 6))
        
        self.status_label = ctk.CTkLabel(status_box, text="Pronto para processar", font=FONT_BODY, text_color=TEXT_SECONDARY)
        self.status_label.pack(side="left")
        
        # Botões de Ação Direita
        actions_box = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        actions_box.grid(row=1, column=2, sticky="e", padx=20, pady=(0, 16))
        
        self.btn_open_folder = ctk.CTkButton(
            actions_box, text="📂 Abrir Pasta", font=FONT_BODY,
            fg_color=BTN_SUCCESS_BG, hover_color=BTN_SUCCESS_HOVER, text_color=BTN_SUCCESS_TEXT,
            height=40, width=120, corner_radius=RADIUS_BUTTON, command=self.abrir_pasta_concluida
        )
        # O botão abrir pasta fica oculto até o final do processamento
        
        self.btn_cancel = ctk.CTkButton(
            actions_box, text="Cancelar", font=FONT_BODY,
            fg_color=BTN_DANGER_BG, hover_color=BTN_DANGER_HOVER, text_color=BTN_DANGER_TEXT,
            height=40, width=100, corner_radius=RADIUS_BUTTON, command=self.cancelar_processamento
        )
        # O botão cancelar começa oculto
        
        self.btn_process = ctk.CTkButton(
            actions_box, text="INICIAR LIMPEZA", font=FONT_CARD_TITLE,
            fg_color=BTN_PRIMARY_BG, hover_color=BTN_PRIMARY_HOVER, text_color=BTN_PRIMARY_TEXT,
            height=44, width=170, corner_radius=RADIUS_BUTTON, command=self.processar_arquivos
        )
        self.btn_process.pack(side="right")

    def _criar_card_metrica(self, parent, col, title, valor_padrao, subtitulo_padrao):
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=RADIUS_CARD,
                            border_width=1, border_color=BORDER_COLOR)
        card.grid(row=0, column=col, sticky="ew", padx=(0 if col == 0 else 8, 0 if col == 2 else 8))
        card.grid_columnconfigure(0, weight=1)
        
        lbl_title = ctk.CTkLabel(card, text=title, font=FONT_CAPTION, text_color=TEXT_SECONDARY, anchor="w")
        lbl_title.pack(anchor="w", padx=16, pady=(12, 2))
        
        lbl_val = ctk.CTkLabel(card, text=valor_padrao, font=FONT_METRIC_VAL, text_color=TEXT_PRIMARY, anchor="w")
        lbl_val.pack(anchor="w", padx=16, pady=(0, 2))
        
        lbl_sub = ctk.CTkLabel(card, text=subtitulo_padrao, font=FONT_CAPTION, text_color=TEXT_MUTED, anchor="w")
        lbl_sub.pack(anchor="w", padx=16, pady=(0, 12))
        
        return {'card': card, 'val': lbl_val, 'sub': lbl_sub}

    def _construir_drop_zone(self):
        content = ctk.CTkFrame(self.drop_zone_frame, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        icon_cloud = ctk.CTkLabel(content, text="🎬", font=(FONT_FAMILY, 52))
        icon_cloud.pack(pady=(0, 10))
        
        title = ctk.CTkLabel(content, text="Arraste e solte seus vídeos aqui",
                             font=FONT_TITLE, text_color=TEXT_PRIMARY)
        title.pack(pady=(0, 6))
        
        subtitle = ctk.CTkLabel(content, text="ou clique no botão '+ Adicionar Vídeos' na barra lateral",
                                font=FONT_BODY, text_color=TEXT_SECONDARY)
        subtitle.pack(pady=(0, 16))
        
        formats_pill = ctk.CTkLabel(
            content, text="Formatos: MP4 • MKV • MOV • AVI • WebM • WMV • FLV",
            font=FONT_CAPTION, text_color=TEXT_MUTED, fg_color=BG_CARD,
            corner_radius=RADIUS_PILL, padx=14, pady=6
        )
        formats_pill.pack()

    # -------------------------------------------------------------------------
    # 3. GERENCIAMENTO DE ARQUIVOS E CARDS NA LISTA
    # -------------------------------------------------------------------------
    def _on_drop_files(self, event):
        """Manipulador de evento de Arrastar e Soltar do TkinterDnD"""
        if self.processando:
            messagebox.showwarning("Aviso", "Aguarde o processamento atual terminar antes de adicionar novos arquivos.")
            return
            
        data = event.data
        if not data:
            return
            
        # Parse seguro de caminhos com ou sem chaves e espaços
        caminhos = []
        matches = re.findall(r'\{([^}]+)\}|(\S+)', data)
        for m in matches:
            caminho = m[0] if m[0] else m[1]
            if caminho:
                caminhos.append(caminho)
                
        if caminhos:
            self.adicionar_arquivos(caminhos)

    def selecionar_arquivos(self):
        if self.processando:
            return
        arquivos = filedialog.askopenfilenames(
            title="Selecionar Arquivos de Vídeo",
            filetypes=[("Vídeos Suportados", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"), ("Todos os Arquivos", "*.*")]
        )
        if arquivos:
            self.adicionar_arquivos(arquivos)

    def escolher_pasta_saida(self):
        pasta = filedialog.askdirectory(title="Escolher Pasta de Saída dos Vídeos Limpos")
        if pasta:
            self.pasta_saida = pasta
            nome_pasta = os.path.basename(pasta)
            if not nome_pasta:
                nome_pasta = pasta
            self.lbl_out_path.configure(text=f"📂 {nome_pasta}")
            self.card_dest['val'].configure(text=nome_pasta[:15] + ("..." if len(nome_pasta) > 15 else ""))
            self.card_dest['sub'].configure(text="Pasta personalizada")

    def adicionar_arquivos(self, caminhos):
        adicionados = 0
        rejeitados = []
        
        for p in caminhos:
            p = os.path.normpath(p.strip('"').strip("'"))
            # Evita duplicados na fila
            if p in [a['path'] for a in self.arquivos_selecionados]:
                continue
                
            sucesso, msg = validar_arquivo_video(p)
            if sucesso:
                try:
                    tam_bytes = os.path.getsize(p)
                    tam_mb = tam_bytes / (1024 * 1024)
                    tam_str = f"{tam_mb:.1f} MB" if tam_mb < 1024 else f"{(tam_mb/1024):.2f} GB"
                except Exception:
                    tam_str = "Desconhecido"
                    tam_bytes = 0
                    
                item = {
                    'path': p,
                    'name': os.path.basename(p),
                    'size_str': tam_str,
                    'size_bytes': tam_bytes,
                    'status': 'Pendente',
                    'frame_widget': None,
                    'badge_widget': None,
                    'badge_lbl': None
                }
                self.arquivos_selecionados.append(item)
                adicionados += 1
            else:
                rejeitados.append(f"• {os.path.basename(p)}: {msg}")
                
        if adicionados > 0:
            self._alternar_visao_lista(tem_itens=True)
            self._rerenderizar_todos_cards()
            self._atualizar_metricas()
            self.atualizar_status(f"{adicionados} arquivo(s) adicionado(s) com sucesso.")
            
        if rejeitados:
            messagebox.showwarning("Alguns arquivos foram rejeitados", "\n".join(rejeitados))

    def _alternar_visao_lista(self, tem_itens):
        """Alterna entre o estado vazio pontilhado e a lista rolável com cards"""
        if tem_itens:
            self.drop_zone_frame.grid_forget()
            self.scroll_frame.grid(row=0, column=0, sticky="nsew")
        else:
            self.scroll_frame.grid_forget()
            self.drop_zone_frame.grid(row=0, column=0, sticky="nsew")

    def _rerenderizar_todos_cards(self):
        """Renderiza novamente os cards de acordo com o filtro ativo"""
        for w in self.scroll_frame.winfo_children():
            w.destroy()
            
        filtro = self.filtro_atual
        for item in self.arquivos_selecionados:
            if filtro == "Pendentes" and item['status'] != "Pendente":
                continue
            if filtro == "Concluídos" and item['status'] != "Concluído":
                continue
            self._render_card_item(item)

    def _render_card_item(self, item):
        card = ctk.CTkFrame(
            self.scroll_frame, fg_color=BG_CARD, corner_radius=RADIUS_CARD,
            border_width=1, border_color=BORDER_COLOR
        )
        card.pack(fill="x", pady=5, padx=4)
        card.grid_columnconfigure(1, weight=1)
        
        # Ícone do formato
        ext = os.path.splitext(item['name'])[1].lower()
        icon_text = "🎬"
        if ext in ['.mkv', '.avi']:
            icon_text = "🎞️"
        elif ext in ['.mov', '.webm']:
            icon_text = "📹"
            
        lbl_icon = ctk.CTkLabel(card, text=icon_text, font=(FONT_FAMILY, 20))
        lbl_icon.grid(row=0, column=0, rowspan=2, padx=(16, 12), pady=12)
        
        # Título do Arquivo
        lbl_name = ctk.CTkLabel(card, text=item['name'], font=FONT_CARD_TITLE,
                                text_color=TEXT_PRIMARY, anchor="w")
        lbl_name.grid(row=0, column=1, sticky="w", pady=(10, 0))
        
        # Subtítulo (Tamanho e Diretório)
        pasta_curta = os.path.dirname(item['path'])
        if len(pasta_curta) > 40:
            pasta_curta = "..." + pasta_curta[-37:]
        info_text = f"{item['size_str']} • {pasta_curta}"
        
        lbl_sub = ctk.CTkLabel(card, text=info_text, font=FONT_CAPTION,
                               text_color=TEXT_SECONDARY, anchor="w")
        lbl_sub.grid(row=1, column=1, sticky="w", pady=(0, 10))
        
        # Área de Ações e Status na Direita
        right_box = ctk.CTkFrame(card, fg_color="transparent")
        right_box.grid(row=0, column=2, rowspan=2, padx=16, pady=12, sticky="e")
        
        # Badge Pill de Status
        badge_frame = ctk.CTkFrame(right_box, corner_radius=RADIUS_PILL)
        badge_frame.pack(side="left", padx=(0, 10))
        
        lbl_status = ctk.CTkLabel(badge_frame, font=FONT_BADGE, padx=12, pady=4)
        lbl_status.pack()
        self._aplicar_estilo_badge(badge_frame, lbl_status, item['status'])
        
        # Botão Inspecionar Metadados
        btn_inspect = ctk.CTkButton(
            right_box, text="🔍", width=34, height=34, corner_radius=RADIUS_BUTTON,
            font=(FONT_FAMILY, 13), fg_color=BTN_SECONDARY_BG, hover_color=BTN_SECONDARY_HOVER,
            text_color=TEXT_PRIMARY, command=lambda p=item['path']: self._abrir_modal_metadados(p)
        )
        btn_inspect.pack(side="left", padx=(0, 6))
        
        # Botão Remover Arquivo Individual
        btn_remove = ctk.CTkButton(
            right_box, text="✕", width=34, height=34, corner_radius=RADIUS_BUTTON,
            font=(FONT_FAMILY, 12, "bold"), fg_color=BTN_DANGER_BG, hover_color=BTN_DANGER_HOVER,
            text_color=BTN_DANGER_TEXT, command=lambda it=item: self.remover_arquivo(it)
        )
        btn_remove.pack(side="left")
        
        # Guarda referências para atualização dinâmica de status
        item['frame_widget'] = card
        item['badge_widget'] = badge_frame
        item['badge_lbl'] = lbl_status

    def _aplicar_estilo_badge(self, frame, label, status):
        """Aplica cores pastel suaves e elegantes ao pill badge"""
        if status == "Pendente":
            frame.configure(fg_color=BADGE_PENDING_BG)
            label.configure(text="Pendente", text_color=BADGE_PENDING_TEXT)
        elif status == "Processando...":
            frame.configure(fg_color=BADGE_PROCESSING_BG)
            label.configure(text="Processando...", text_color=BADGE_PROCESSING_TEXT)
        elif status == "Concluído":
            frame.configure(fg_color=BADGE_SUCCESS_BG)
            label.configure(text="Concluído", text_color=BADGE_SUCCESS_TEXT)
        elif status == "Erro":
            frame.configure(fg_color=BADGE_ERROR_BG)
            label.configure(text="Erro", text_color=BADGE_ERROR_TEXT)

    def _abrir_modal_metadados(self, file_path):
        ModalMetadata(self, file_path)

    def remover_arquivo(self, item):
        if self.processando:
            messagebox.showwarning("Aviso", "Não é possível remover arquivos durante o processamento.")
            return
        if item in self.arquivos_selecionados:
            self.arquivos_selecionados.remove(item)
            if item['frame_widget']:
                item['frame_widget'].destroy()
            self._atualizar_metricas()
            if not self.arquivos_selecionados:
                self._alternar_visao_lista(tem_itens=False)
                self.atualizar_status("Fila vazia.")

    def limpar_lista(self):
        if self.processando:
            messagebox.showwarning("Aviso", "Aguarde a conclusão ou cancele o processamento antes de limpar.")
            return
        self.arquivos_selecionados.clear()
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        self._alternar_visao_lista(tem_itens=False)
        self.progress_bar.set(0)
        self.btn_open_folder.pack_forget()
        self._atualizar_metricas()
        self.atualizar_status("Lista limpa.")

    def _filtrar_lista(self, valor):
        if "Todos" in valor:
            self.filtro_atual = "Todos"
        elif "Pendentes" in valor:
            self.filtro_atual = "Pendentes"
        elif "Concluídos" in valor:
            self.filtro_atual = "Concluídos"
        self._rerenderizar_todos_cards()

    def _atualizar_metricas(self):
        total = len(self.arquivos_selecionados)
        pendentes = sum(1 for a in self.arquivos_selecionados if a['status'] == 'Pendente')
        concluidos = sum(1 for a in self.arquivos_selecionados if a['status'] == 'Concluído')
        
        bytes_total = sum(a.get('size_bytes', 0) for a in self.arquivos_selecionados)
        mb_total = bytes_total / (1024 * 1024)
        tam_total_str = f"{mb_total:.1f} MB total" if mb_total < 1024 else f"{(mb_total/1024):.2f} GB total"
        
        self.card_total['val'].configure(text=f"{total} vídeo{'s' if total != 1 else ''}")
        self.card_total['sub'].configure(text=tam_total_str if total > 0 else "0.0 MB total")
        
        # Atualiza contadores no botão segmentado
        self.filter_segmented.configure(
            values=[f"Todos ({total})", f"Pendentes ({pendentes})", f"Concluídos ({concluidos})"]
        )

    # -------------------------------------------------------------------------
    # 4. PROCESSAMENTO EM LOTE COM THREAD-SAFETY & CANCELAMENTO
    # -------------------------------------------------------------------------
    def processar_arquivos(self):
        if not self.arquivos_selecionados:
            messagebox.showinfo("Fila Vazia", "Adicione vídeos à fila antes de iniciar a limpeza.")
            return
            
        pendentes = [a for a in self.arquivos_selecionados if a['status'] != 'Concluído']
        if not pendentes:
            messagebox.showinfo("Tudo Concluído", "Todos os vídeos da fila já foram processados!")
            return
            
        if self.processando:
            return
            
        self.processando = True
        self.cancelar_solicitado = False
        
        # UI State: Desabilita botões e exibe botão de Cancelar
        self.btn_process.configure(state="disabled", text="Limpando...")
        self.btn_add.configure(state="disabled")
        self.btn_clear.configure(state="disabled")
        self.btn_open_folder.pack_forget()
        self.btn_cancel.pack(side="right", padx=(0, 10))
        
        def job():
            total = len(self.arquivos_selecionados)
            concluidos_nesta_rodada = 0
            
            for i, item in enumerate(self.arquivos_selecionados):
                if self.cancelar_solicitado:
                    break
                    
                if item['status'] == 'Concluído':
                    continue
                    
                # Notifica início do item (Thread-safe)
                progresso_frac = i / total
                self.after(0, self._ui_item_iniciando, item, progresso_frac)
                
                # Gera caminho de saída preservando a extensão original do arquivo
                orig_name = item['name']
                base_name, ext = os.path.splitext(orig_name)
                novo_nome = f"{base_name}_limpo{ext}"
                
                if self.pasta_saida:
                    saida = os.path.join(self.pasta_saida, novo_nome)
                else:
                    saida = os.path.join(os.path.dirname(item['path']), novo_nome)
                    
                # Executa a limpeza via FFmpeg
                sucesso, msg = limpar_metadados(item['path'], saida)
                
                if sucesso:
                    item['status'] = 'Concluído'
                    concluidos_nesta_rodada += 1
                    self.after(0, self._ui_item_concluido, item, (i + 1) / total)
                else:
                    item['status'] = 'Erro'
                    self.after(0, self._ui_item_erro, item, (i + 1) / total, msg)
                    
            # Fim do lote
            self.after(0, self._ui_finalizar_lote, concluidos_nesta_rodada)

        threading.Thread(target=job, daemon=True).start()

    def cancelar_processamento(self):
        if self.processando:
            self.cancelar_solicitado = True
            self.atualizar_status("Cancelamento solicitado... Finalizando arquivo atual.")
            self.btn_cancel.configure(state="disabled", text="Cancelando...")

    # Callbacks despachados para a Main Thread (Thread-Safety)
    def _ui_item_iniciando(self, item, progresso):
        self.atualizar_status(f"Processando: {item['name']}", progresso)
        if item['badge_widget'] and item['badge_lbl']:
            self._aplicar_estilo_badge(item['badge_widget'], item['badge_lbl'], "Processando...")

    def _ui_item_concluido(self, item, progresso):
        self.atualizar_status(f"Concluído: {item['name']}", progresso)
        if item['badge_widget'] and item['badge_lbl']:
            self._aplicar_estilo_badge(item['badge_widget'], item['badge_lbl'], "Concluído")
        self._atualizar_metricas()

    def _ui_item_erro(self, item, progresso, erro_msg):
        self.atualizar_status(f"Erro em {item['name']}: {erro_msg}", progresso)
        if item['badge_widget'] and item['badge_lbl']:
            self._aplicar_estilo_badge(item['badge_widget'], item['badge_lbl'], "Erro")
        self._atualizar_metricas()

    def _ui_finalizar_lote(self, concluidos_count):
        self.processando = False
        self.btn_cancel.pack_forget()
        self.btn_cancel.configure(state="normal", text="Cancelar")
        
        self.btn_process.configure(state="normal", text="INICIAR LIMPEZA")
        self.btn_add.configure(state="normal")
        self.btn_clear.configure(state="normal")
        
        self._atualizar_metricas()
        
        if self.cancelar_solicitado:
            self.atualizar_status("Processamento interrompido pelo usuário.", self.progress_bar.get())
            messagebox.showwarning("Interrompido", "O processamento foi interrompido.")
        else:
            self.progress_bar.set(1.0)
            self.atualizar_status("Limpeza de metadados concluída com sucesso!", 1.0)
            self.btn_open_folder.pack(side="right", padx=(0, 10))
            messagebox.showinfo("Sucesso", f"Processamento concluído!\n{concluidos_count} arquivo(s) foram limpos.")

    def abrir_pasta_concluida(self):
        destino = self.pasta_saida
        if not destino and self.arquivos_selecionados:
            destino = os.path.dirname(self.arquivos_selecionados[0]['path'])
        if destino and os.path.exists(destino):
            if sys.platform == 'win32':
                os.startfile(destino)
            else:
                subprocess.run(['xdg-open', destino])

    def atualizar_status(self, texto, progress=None):
        self.status_label.configure(text=texto)
        if progress is not None:
            self.progress_bar.set(progress)

    def _mudar_tema(self, escolha):
        modo_map = {"Escuro": "dark", "Claro": "light", "Sistema": "system"}
        ctk.set_appearance_mode(modo_map.get(escolha, "dark"))

    def _configurar_icone(self):
        """Define o ícone oficial da aplicação na janela e barra de tarefas do Windows"""
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.ico")
        if getattr(sys, 'frozen', False):
            meipass = getattr(sys, '_MEIPASS', None)
            if meipass:
                cand = os.path.join(meipass, "assets", "icon.ico")
                if os.path.exists(cand):
                    icon_path = cand
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception as e:
                security_logger.warning(f"Não foi possível aplicar ícone da janela: {e}")

    def _verificar_ffmpeg_startup(self):
        sucesso, msg = verificar_ffmpeg()
        if not sucesso:
            messagebox.showerror("FFmpeg não encontrado", f"A engine FFmpeg é obrigatória:\n{msg}")

def main():
    app = LimpaMetadadosApp()
    app.mainloop()

if __name__ == "__main__":
    main()