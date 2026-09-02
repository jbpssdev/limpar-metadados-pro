# 📦 Pasta de Versões e Distribuição (Releases)

Esta pasta armazena os arquivos binários compilados (`.exe` e pacotes `.zip`) gerados a cada nova versão para distribuição pública via **GitHub Releases**.

> **Nota:** Arquivos executáveis e compactados são ignorados pelo Git (`.gitignore`) para evitar inchar o histórico do repositório. O local correto para disponibilizá-los aos usuários finais é na aba **Releases** do GitHub.

---

## 🚀 Como Gerar uma Nova Versão

1. Execute o script de build:
   ```bash
   python build.py
   ```
2. O script compilará a aplicação e colocará os arquivos diretamente nesta pasta:
   - `versoes/LimparMetadadosPRO_vX.X.X.exe` (Executável avulso)
   - `versoes/LimparMetadadosPRO_vX.X.X.zip` (Pacote completo com documentação)

---

## 🌐 Como Publicar a Versão no GitHub Releases

1. Acesse o seu repositório:
   👉 **[github.com/jbpssdev/limpar-metadados-pro/releases/new](https://github.com/jbpssdev/limpar-metadados-pro/releases/new)**
2. Preencha os campos da Release:
   - **Choose a tag:** Digite a tag da versão (ex: `v1.0.4`) e selecione *"Create new tag"*.
   - **Release title:** Digite o título (ex: `Limpar Metadados PRO v1.0.4 - Nova Interface & Drag-and-Drop`).
   - **Description:** Descreva as principais novidades e melhorias da versão.
3. **Anexar Binários:**
   - Arraste o arquivo `.exe` e o arquivo `.zip` desta pasta `versoes/` para o campo **"Attach binaries by dropping them here or selecting them"**.
4. Clique no botão verde **"Publish release"**.

Pronto! Qualquer pessoa poderá baixar o programa diretamente pelo link de download do GitHub sem precisar instalar Python nem clonar código.
