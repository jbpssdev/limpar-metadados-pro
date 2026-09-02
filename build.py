#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
import zipfile
from datetime import datetime

def verificar_dependencias():
    """Verifica e instala dependências necessárias"""
    print("Verificando dependencias...")
    
    try:
        import PyInstaller
        print("PyInstaller instalado")
    except ImportError:
        print("PyInstaller nao encontrado. Instalando...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("PyInstaller instalado com sucesso")
        except subprocess.CalledProcessError:
            print("Falha ao instalar PyInstaller")
            return False
    
    ffmpeg_path = "ffmpeg.exe"
    if not os.path.exists(ffmpeg_path):
        print(f"❌ {ffmpeg_path} não encontrado na pasta raiz")
        print("   Download FFmpeg em: https://ffmpeg.org/download.html")
        return False
    
    print(f"✅ {ffmpeg_path} encontrado")
    return True

def limpar_build():
    """Remove arquivos de build anteriores"""
    print("🧹 Limpando arquivos de build anteriores...")
    
    pastas_para_remover = ['build', 'dist', '__pycache__']
    
    for pasta in pastas_para_remover:
        if os.path.exists(pasta):
            shutil.rmtree(pasta)
            print(f"✅ Removido: {pasta}")
    
    # Remove arquivos .pyc
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def compilar_executavel():
    """Compila o executável com PyInstaller"""
    print("🔨 Compilando executável...")
    print("⏳ Isso pode demorar alguns minutos...")
    
    # Usa o arquivo .spec customizado
    comando = [
        sys.executable, 
        "-m", 
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "LimparMetadadosPRO.spec"
    ]
    
    try:
        print(f"🚀 Executando: {' '.join(comando)}")
        resultado = subprocess.run(
            comando, 
            check=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        print("✅ Compilação concluída com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro durante a compilação:")
        print(f"   STDOUT: {e.stdout}")
        print(f"   STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def verificar_executavel():
    """Verifica se o executável foi criado corretamente"""
    executavel = os.path.join("dist", "LimparMetadadosPRO.exe")
    
    if os.path.exists(executavel):
        tamanho = os.path.getsize(executavel) / (1024 * 1024)
        print(f"✅ Executável criado: {executavel} ({tamanho:.1f} MB)")
        return True, executavel
    else:
        print("❌ Executável não foi criado")
        return False, None

def criar_readme_distribuicao():
    """Cria README para distribuição"""
    readme_content = """# Limpar Metadados PRO v1.0.4
Desenvolvido por Jackson Porciuncula

## 📋 Sobre
Aplicação desktop profissional para remoção completa e segura de metadados de arquivos de vídeo, garantindo privacidade total ao compartilhar mídias digitais.

## 🚀 Como Usar
1. Execute LimparMetadadosPRO.exe
2. Arraste seus arquivos de vídeo para a janela (ou clique em "Adicionar Vídeos")
3. Opcionalmente selecione uma pasta de destino
4. Clique em "INICIAR LIMPEZA"
5. Aguarde a conclusão e acerte seus arquivos protegidos!

## 📁 Formatos Suportados
- MP4, AVI, MKV, MOV, WMV, FLV, WebM

## 🛡️ Segurança e Privacidade
- Funciona 100% offline
- Não realiza conexões com a internet
- Preserva a qualidade original (bitexact / sem recodificação de streams)
- Elimina coordenadas GPS, modelo da câmera, timestamps e dados de autor
"""
    
    with open('README_DISTRIBUICAO.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README de distribuição criado")

def criar_pacote_zip(executavel_path):
    """Cria arquivo ZIP para distribuição"""
    data_atual = datetime.now().strftime("%Y%m%d")
    nome_zip = f"LimparMetadadosPRO_v1.0.4_{data_atual}.zip"
    
    print(f"📦 Criando pacote: {nome_zip}")
    
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        # Adiciona o executável
        zipf.write(executavel_path, "LimparMetadadosPRO.exe")
        
        # Adiciona README
        if os.path.exists('README_DISTRIBUICAO.txt'):
            zipf.write('README_DISTRIBUICAO.txt', 'README.txt')
    
    tamanho_zip = os.path.getsize(nome_zip) / (1024 * 1024)
    print(f"✅ Pacote criado: {nome_zip} ({tamanho_zip:.1f} MB)")
    return nome_zip

def main():
    """Função principal de build"""
    print("=" * 50)
    print("BUILD LIMPAR METADADOS PRO v1.0.4")
    print("=" * 50)
    print()
    
    if not verificar_dependencias():
        print("\n" + "=" * 50)
        print("❌ BUILD FALHOU")
        print("   Resolva os problemas acima e tente novamente")
        print("=" * 50)
        return False
    
    limpar_build()
    
    if not compilar_executavel():
        print("\n" + "=" * 50)
        print("❌ BUILD FALHOU")
        print("=" * 50)
        return False
    
    sucesso, executavel_path = verificar_executavel()
    if not sucesso:
        print("\n" + "=" * 50)
        print("❌ BUILD FALHOU")
        print("=" * 50)
        return False
    
    # Cria arquivos de distribuição
    criar_readme_distribuicao()
    nome_zip = criar_pacote_zip(executavel_path)
    
    print("\n" + "=" * 50)
    print("🎉 BUILD CONCLUÍDO COM SUCESSO!")
    print("=" * 50)
    print(f"📁 Executável: {executavel_path}")
    print(f"📦 Pacote ZIP: {nome_zip}")
    print("\n💡 Dicas:")
    print("   • Teste o executável antes de distribuir")
    print("   • O ZIP está pronto para distribuição")
    print("   • Alguns antivírus podem dar falso positivo")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    sucesso = main()
    if not sucesso:
        sys.exit(1) 