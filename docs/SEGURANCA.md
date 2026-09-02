# 🛡️ Arquitetura de Segurança & Privacidade - Limpar Metadados PRO

O **Limpar Metadados PRO** foi projetado com o princípio de *Privacy by Design* e *Defense in Depth*, assegurando que a manipulação de arquivos de vídeo externos ocorra de forma segura, determinística e sem risco para o ambiente do usuário.

---

## 🔒 Pilares de Proteção

### 1. Sanitização Rigorosa de Caminhos e Nomes de Arquivo
- **Função**: `sanitize_filename()` em [core.py](file:///d:/SSD%202/WEBSITES/limpa-metadados/core.py)
- **Mitigação**: Previne injeção de comandos em subprocessos e manipulação inadequada de argumentos.
- **Caracteres Neutralizados**: `|`, `&`, `;`, `$`, `` ` ``, `(`, `)`, `{`, `}`, `[`, `]`, `<`, `>`, `"`, `'`.
- **Prevenção de Path Traversal**: Detecção de sequências `..` para garantir que o processamento fique restrito aos diretórios legítimos informados pelo usuário.

### 2. Validação Binária de Tipos de Arquivo (Magic Bytes / Assinatura)
- **Função**: `validate_file_security()`
- **Mitigação**: Arquivos maliciosos renomeados com extensões de vídeo (ex.: `.exe` renomeado para `.mp4`) são rejeitados antes de serem submetidos ao decodificador.
- **Assinaturas Suportadas**:
  - MP4 (ISO Base Media, ftypmp4, ftypisom, v1/v2)
  - MKV / WebM (EBML Header `\x1a\x45\xdf\xa3`)
  - AVI (RIFF Header)
  - QuickTime MOV (`ftypqt`)
  - WMV / ASF (`\x30\x26\xb2\x75`)
  - FLV (`FLV\x01`)

### 3. Integridade e Auditoria Criptográfica (SHA-256)
- **Função**: `calculate_file_hash()`
- **Auditoria**: Cada arquivo adicionado à fila tem seu hash SHA-256 calculado via leitura em chunks de 4 KB (evitando estouro de memória).
- **Rastreabilidade**: Os hashes antes e após a limpeza são registrados localmente em log para verificação de integridade e auditoria de conformidade.

### 4. Controle de Recursos e Prevenção de DoS
- **Limite por Arquivo**: Bloqueio de arquivos anômalos que ultrapassem 10 GB.
- **Timeouts Controlados**:
  - 5 segundos para sondagem e extração de metadados.
  - 5 minutos máximo para processamento por arquivo individual (evitando travamentos em streams malformados).
- **Isolamento de Processo**: No Windows, processos filhos do FFmpeg são instanciados com `CREATE_NO_WINDOW`, sem acoplar consoles interativos.

### 5. Operação 100% Offline e Sem Telemetria
- O software não inicializa sockets de rede, não possui chamadas HTTP/HTTPS de rastreamento e não coleta nenhuma informação de uso.
- Todos os metadados removidos são descartados na memória local sem persistência externa.
