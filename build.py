#!/usr/bin/env python3
"""
build.py - Pipeline Automatizado de Compilação e Empacotamento
Limpar Metadados PRO - Jackson Porciuncula

Etapas executadas:
1. Limpeza de builds e temporários anteriores
2. Execução obrigatória dos testes automatizados (unittest)
3. Sincronização e validação de metadados/ícones
4. Compilação do executável com PyInstaller (Windowed / sem console)
5. Validação da integridade do executável
6. Compilação do Instalador Profissional com Inno Setup 6 (ISCC.exe)
7. Organização das versões em release/ e versoes/
"""

import os
import sys
import shutil
import zipfile
import subprocess
from datetime import datetime

# Garante suporte a UTF-8 no console do Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Importa dados centralizados de versão
try:
    from version import VERSION, APP_NAME, AUTHOR, ORIGINAL_FILENAME, SETUP_FILENAME
except ImportError:
    VERSION = "1.0.4"
    APP_NAME = "Limpar Metadados PRO"
    AUTHOR = "Jackson Porciuncula"
    ORIGINAL_FILENAME = "LimparMetadadosPRO.exe"
    SETUP_FILENAME = f"LimparMetadadosPRO-Setup-{VERSION}.exe"


def localizar_iscc():
    """Localiza o executável do compilador Inno Setup (ISCC.exe)"""
    candidatos = [
        shutil.which('ISCC.exe'),
        shutil.which('iscc'),
        os.path.expandvars(r'%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe'),
        r'C:\Program Files (x86)\Inno Setup 6\ISCC.exe',
        r'C:\Program Files\Inno Setup 6\ISCC.exe',
        r'C:\Program Files (x86)\Inno Setup 5\ISCC.exe',
        r'C:\Program Files\Inno Setup 5\ISCC.exe',
    ]
    for c in candidatos:
        if c and os.path.exists(c):
            return os.path.normpath(c)
    return None


def verificar_dependencias():
    """Verifica e instala dependências necessárias"""
    print("🔍 [1/6] Verificando dependências do ambiente...")
    
    try:
        import PyInstaller
        print("  ✓ PyInstaller instalado")
    except ImportError:
        print("  ⚠️ PyInstaller não encontrado. Instalando...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("  ✓ PyInstaller instalado com sucesso")
        except subprocess.CalledProcessError:
            print("  ❌ Falha ao instalar PyInstaller via pip")
            return False

    ffmpeg_path = "ffmpeg.exe"
    if not os.path.exists(ffmpeg_path):
        system_ffmpeg = shutil.which("ffmpeg")
        if system_ffmpeg:
            print(f"  ✓ FFmpeg localizado no PATH do sistema: {system_ffmpeg}")
        else:
            print(f"  ❌ {ffmpeg_path} não encontrado na pasta raiz e nem no PATH")
            print("     Baixe o FFmpeg em https://ffmpeg.org/download.html")
            return False
    else:
        print(f"  ✓ {ffmpeg_path} presente na pasta raiz")

    return True


def executar_testes():
    """Executa suíte de testes automatizados antes do build"""
    print("\n🧪 [2/6] Executando testes automatizados...")
    cmd = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    
    if res.returncode != 0:
        print("  ❌ Os testes unitários FALHARAM! Abortando compilação.")
        print(res.stderr or res.stdout)
        return False
    
    print("  ✓ Todos os testes automatizados passaram com sucesso!")
    return True


def limpar_build():
    """Remove arquivos de build anteriores"""
    print("\n🧹 [3/6] Limpando arquivos de compilação anteriores...")
    pastas_remover = ['build', '__pycache__']
    
    for pasta in pastas_remover:
        if os.path.exists(pasta):
            shutil.rmtree(pasta, ignore_errors=True)
            print(f"  ✓ Removido: {pasta}")
            
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, file))
                except Exception:
                    pass


def compilar_executavel():
    """Compila o executável standalone com PyInstaller"""
    print("\n🔨 [4/6] Compilando executável com PyInstaller...")
    print("  ⏳ Isso pode levar cerca de 30 a 60 segundos...")
    
    spec_file = "LimparMetadadosPRO.spec"
    if not os.path.exists(spec_file):
        print(f"  ❌ Arquivo de especificação '{spec_file}' não encontrado")
        return False
        
    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "--noconfirm", spec_file]
    
    try:
        resultado = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print("  ✓ Executável PyInstaller compilado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Erro durante a compilação do PyInstaller:")
        print(e.stderr or e.stdout)
        return False


def verificar_executavel():
    """Verifica se o executável foi criado corretamente"""
    executavel = os.path.join("dist", ORIGINAL_FILENAME)
    
    if os.path.exists(executavel):
        tamanho = os.path.getsize(executavel) / (1024 * 1024)
        print(f"  ✓ Executável verificado: {executavel} ({tamanho:.1f} MB)")
        return True, executavel
    else:
        print(f"  ❌ Executável não encontrado em: {executavel}")
        return False, None


def compilar_instalador():
    """Compila o instalador oficial Windows com Inno Setup 6"""
    print("\n📦 [5/6] Compilando Instalador Profissional com Inno Setup 6...")
    iscc = localizar_iscc()
    
    if not iscc:
        print("  ⚠️ Compilador Inno Setup (ISCC.exe) não encontrado no computador!")
        print("     Para gerar o arquivo LimparMetadadosPRO-Setup.exe, instale o Inno Setup:")
        print("     Opção 1: winget install JRSoftware.InnoSetup")
        print("     Opção 2: Baixe em https://jrsoftware.org/isdl.php")
        return False, None
        
    iss_script = os.path.join("installer", "LimparMetadadosPRO.iss")
    if not os.path.exists(iss_script):
        print(f"  ❌ Script do Inno Setup não encontrado: {iss_script}")
        return False, None
        
    os.makedirs("release", exist_ok=True)
    
    cmd = [iscc, iss_script]
    print(f"  🚀 Executando Inno Setup: {iscc}")
    
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    if res.returncode != 0:
        print("  ❌ Falha na compilação do instalador Inno Setup:")
        print(res.stderr or res.stdout)
        return False, None
        
    setup_path = os.path.join("release", SETUP_FILENAME)
    if os.path.exists(setup_path):
        tamanho = os.path.getsize(setup_path) / (1024 * 1024)
        print(f"  ✓ Instalador gerado com sucesso: {setup_path} ({tamanho:.1f} MB)")
        return True, setup_path
    else:
        # Tenta localizar qualquer setup na pasta release
        for f in os.listdir("release"):
            if f.endswith(".exe") and "Setup" in f:
                setup_path = os.path.join("release", f)
                tamanho = os.path.getsize(setup_path) / (1024 * 1024)
                print(f"  ✓ Instalador gerado: {setup_path} ({tamanho:.1f} MB)")
                return True, setup_path
        return False, None


def organizar_versoes(executavel_path, setup_path):
    """Copia e organiza os arquivos prontos para a pasta versoes/"""
    print("\n📁 [6/6] Organizando pacotes na pasta versoes/...")
    os.makedirs("versoes", exist_ok=True)
    data_atual = datetime.now().strftime("%Y%m%d")
    
    # 1. Executável avulso
    exe_versao = os.path.join("versoes", f"LimparMetadadosPRO_v{VERSION}_{data_atual}.exe")
    shutil.copy2(executavel_path, exe_versao)
    print(f"  ✓ Executável copiado: {exe_versao}")
    
    # 2. Pacote ZIP
    zip_versao = os.path.join("versoes", f"LimparMetadadosPRO_v{VERSION}_{data_atual}.zip")
    with zipfile.ZipFile(zip_versao, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write(executavel_path, ORIGINAL_FILENAME)
        if os.path.exists("README.md"):
            zipf.write("README.md", "LEIA-ME.txt")
        if os.path.exists("LICENSE"):
            zipf.write("LICENSE", "LICENCA.txt")
    print(f"  ✓ Pacote ZIP criado: {zip_versao}")
    
    # 3. Instalador Setup
    if setup_path and os.path.exists(setup_path):
        setup_versao = os.path.join("versoes", os.path.basename(setup_path))
        shutil.copy2(setup_path, setup_versao)
        print(f"  ✓ Instalador copiado para versoes: {setup_versao}")


def main():
    """Execução do pipeline completo"""
    print("=" * 64)
    print(f"🚀 BUILD & RELEASE PIPELINE: {APP_NAME} v{VERSION}")
    print(f"   Autor: {AUTHOR}")
    print("=" * 64)
    
    if not verificar_dependencias():
        return False
        
    if not executar_testes():
        return False
        
    limpar_build()
    
    if not compilar_executavel():
        return False
        
    sucesso_exe, executavel_path = verificar_executavel()
    if not sucesso_exe:
        return False
        
    sucesso_setup, setup_path = compilar_instalador()
    
    organizar_versoes(executavel_path, setup_path)
    
    print("\n" + "=" * 64)
    print("🎉 PIPELINE CONCLUÍDO COM SUCESSO!")
    print("=" * 64)
    print(f"⭐ Executável Standalone: {executavel_path}")
    if sucesso_setup and setup_path:
        tamanho_setup = os.path.getsize(setup_path) / (1024 * 1024)
        print(f"📦 INSTALADOR WINDOWS:   {setup_path} ({tamanho_setup:.1f} MB)")
        print("\n👉 Para enviar aos usuários leigos, basta distribuir o arquivo:")
        print(f"   {setup_path}")
    else:
        print("⚠️ O executável foi gerado, mas o instalador Setup não pôde ser compilado.")
    print("=" * 64 + "\n")
    return True


if __name__ == "__main__":
    sucesso = main()
    if not sucesso:
        sys.exit(1)