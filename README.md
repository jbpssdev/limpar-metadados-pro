# Limpar Metadados PRO

[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-blue?logo=python&logoColor=white)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/UI-CustomTkinter%20%2B%20TkinterDnD2-indigo)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows&logoColor=blue)](https://github.com/jbpssdev/limpar-metadados-pro)

> **Aplicação Desktop profissional para remoção completa e segura de metadados e rastros digitais em arquivos de vídeo, com interface moderna e processamento 100% offline.**

---

## 👨‍💻 Sobre o Projeto

O **Limpar Metadados PRO** foi concebido e desenvolvido por **Jackson Porciuncula** como resultado de estudos e aprofundamento prático em programação com **Python** na **Faculdade Pitágoras**. 

O projeto une conceitos fundamentais da ciência da computação e engenharia de software aplicados a um problema real do dia a dia:
- **Privacidade e Segurança Digital:** eliminação de vetores de vazamento de dados pessoais (coordenadas de geolocalização GPS, identificadores de câmera/dispositivo, data/hora exata de captura e dados de edição).
- **Processamento Concorrente e Thread-Safety:** execução assíncrona desacoplada da thread principal de interface para garantir fluidez e responsividade da interface.
- **Validação Defensiva (*Defense in Depth*):** sanitização de entradas, prevenção contra ataques de injeção de comandos em subprocessos, detecção de *path traversal* e validação estrita de assinaturas binárias de arquivo (*magic bytes*).

---

## ✨ Funcionalidades Principais

* **Remoção Completa de Metadados:** Strip de todas as tags internas, capítulos, dispositivos e coordenadas geográficas via FFmpeg com parâmetro `+bitexact`.
* **Preservação de Qualidade (Stream Copy):** Os fluxos de vídeo e áudio são copiados sem recodificação (`-c copy`), mantendo 100% da resolução original em fração de segundos.
* **Interface Moderna e Elegante:** Construída com `CustomTkinter` e design baseado em cards arredondados e badges informativos em formato *pill*.
* **Suporte a Arrastar e Soltar (Drag & Drop):** Integração nativa via `tkinterdnd2`, permitindo arrastar arquivos do Windows Explorer direto para a aplicação.
* **Inspeção Prévia de Metadados:** Janela modal integrada para inspecionar exatamente quais tags estão embutidas no arquivo antes de iniciar o processo de limpeza.
* **Processamento em Lote:** Limpeza de múltiplos arquivos em sequência com barra de progresso em tempo real e opção de cancelamento imediato.
* **Temas Claro e Escuro:** Seletor intuitivo na barra lateral adaptando toda a paleta de cores harmoniosamente.
* **100% Offline:** Sem conexões de rede, sem rastreadores, sem telemetria.

---

## 📁 Formatos de Vídeo Suportados

| Formato | Extensão | Validação Binária (Magic Bytes) |
|---|---|---|
| **MP4** | `.mp4` | `ftypmp4`, `ftypisom`, `v1/v2` |
| **MKV** | `.mkv` | EBML Header (`\x1a\x45\xdf\xa3`) |
| **MOV** | `.mov` | QuickTime (`ftypqt`) |
| **AVI** | `.avi` | RIFF Container |
| **WebM** | `.webm` | EBML Header |
| **WMV** | `.wmv` | ASF Specification |
| **FLV** | `.flv` | Flash Video Signature |

---

## 📦 Download & Instalação (Para Usuários Finais)

Para quem deseja apenas utilizar o aplicativo, **não é necessário ter Python nem usar terminal**:

1. Acesse a página oficial de **[Releases](https://github.com/jbpssdev/limpar-metadados-pro/releases)**.
2. Baixe o instalador oficial: **`LimparMetadadosPRO-Setup-1.0.4.exe`**.
3. Execute o instalador (duplo clique), escolha se deseja criar atalho na Área de Trabalho e conclua.
4. Abra o **Limpar Metadados PRO** pelo Menu Iniciar ou atalho na Área de Trabalho!

---

## 🚀 Execução em Modo de Desenvolvimento (Programadores)

### Pré-requisitos
- **Python 3.11+** instalado
- **FFmpeg:** O programa utiliza o `ffmpeg.exe` local ou detecta automaticamente qualquer instalação do FFmpeg presente no `PATH` do sistema.

### 1. Clonar o Repositório
```bash
git clone https://github.com/jbpssdev/limpar-metadados-pro.git
cd limpar-metadados-pro
```

### 2. Criar e Ativar Ambiente Virtual
```bash
python -m venv .venv

# No Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# No Windows (CMD):
.\.venv\Scripts\activate.bat
```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação
```bash
python main.py
```

---

## 🖥️ Como Usar

1. **Adicionar Vídeos:** Arraste e solte seus arquivos na janela principal ou clique em **"+ Adicionar Vídeos"** na barra lateral.
2. **Inspecionar Metadados (Opcional):** Clique no ícone de lupa `🔍` ao lado de qualquer arquivo na fila para visualizar os metadados existentes.
3. **Definir Pasta de Saída (Opcional):** Por padrão, os arquivos limpos são salvos na mesma pasta do arquivo original com o sufixo `_limpo`. Você pode escolher uma pasta de destino específica clicando em **"Alterar Pasta"**.
4. **Processar:** Clique em **"INICIAR LIMPEZA"**.
5. **Acessar os Arquivos:** Ao término do lote, utilize o botão **"📂 Abrir Pasta"** para visualizar seus vídeos higienizados.

---

## 🏗️ Arquitetura do Projeto

```
limpar-metadados-pro/
├── docs/                     # Documentação de arquitetura e segurança
│   ├── RELEASE_NOTES.md      # Histórico de lançamentos e versões
│   ├── SEGURANCA.md          # Especificação técnica das defesas de segurança
│   └── SETUP.md              # Guia para contribuidores
├── tests/                    # Suíte de testes automatizados (unittest)
│   └── test_validation.py    # Testes de sanitização, segurança e validação
├── core.py                   # Motor de processamento seguro (FFmpeg + hashing)
├── interface.py              # Interface gráfica moderna (CustomTkinter + Drag & Drop)
├── ui_theme.py               # Design System centralizado (Tokens de cores e temas)
├── modal_metadata.py         # Janela modal para inspeção de metadados
├── main.py                   # Ponto de entrada da aplicação
├── build.py                  # Script de automação de compilação
├── LimparMetadadosPRO.spec    # Especificação do PyInstaller para build portátil
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação principal
```

---

## 🧪 Testes Automatizados

Para rodar a suíte de testes unitários:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📦 Gerando o Executável (.exe)

O projeto inclui rotina completa para compilação em executável único e portátil para Windows utilizando o PyInstaller:

```bash
python build.py
```

O executável final será gerado dentro da pasta `dist/LimparMetadadosPRO.exe`.

---

## 🛡️ Segurança e Auditoria

Para detalhes completos sobre a arquitetura de segurança, sanitização de inputs e mitigação de vulnerabilidades, consulte o documento [docs/SEGURANCA.md](docs/SEGURANCA.md).

---

## 👤 Autor

**Jackson Porciuncula**
* Projeto desenvolvido para fins práticos e acadêmicos — **Faculdade Pitágoras**.
* Repositório: [github.com/jbpssdev/limpar-metadados-pro](https://github.com/jbpssdev/limpar-metadados-pro)

---

## 📄 Licença

Distribuído sob a licença MIT. Consulte o arquivo de licença para mais detalhes.