# 🛠️ Instalador Windows - Limpar Metadados PRO

Este diretório contém os scripts e definições para geração do instalador tradicional do Windows usando o **Inno Setup 6**.

---

## 📁 Arquivos

- `LimparMetadadosPRO.iss`: Script de automação do Inno Setup.
- `README.md`: Este guia explicativo.

---

## 🚀 Como Compilar o Instalador

O instalador é gerado automaticamente pelo pipeline unificado:

```bash
python build.py
```

O script cuidará de:
1. Rodar os testes automatizados;
2. Compilar o executável com PyInstaller (`dist/LimparMetadadosPRO.exe`);
3. Localizar o compilador Inno Setup (`ISCC.exe`);
4. Compilar o instalador final em:
   ```text
   release/LimparMetadadosPRO-Setup-1.0.4.exe
   ```

### Compilação Manual Direta (Opcional):
Caso queira compilar apenas o instalador via terminal:
```powershell
& "C:\Users\jbrun\AppData\Local\Programs\Inno Setup 6\ISCC.exe" installer\LimparMetadadosPRO.iss
```

---

## ⚙️ Características do Instalador

- **Privilégios Não-Elevados:** Utiliza `PrivilegesRequired=lowest`, instalando em `%LOCALAPPDATA%\Programs\Limpar Metadados PRO` por padrão. Isso permite que qualquer usuário instale o software sem solicitar senha de Administrador (UAC).
- **Atalhos Automáticos:** Cria entrada no Menu Iniciar e opção para criar atalho na Área de Trabalho.
- **Desinstalador Integrado:** Registra desinstalação nativa acessível em **Configurações → Aplicativos → Aplicativos instalados**.
- **Compactação Ultra:** Usa algoritmo LZMA2 Ultra para gerar instaladores compactos e de descompactação rápida.
