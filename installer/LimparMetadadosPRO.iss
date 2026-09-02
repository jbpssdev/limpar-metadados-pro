; =====================================================================
; Script Inno Setup 6 - Limpar Metadados PRO
; Desenvolvido por Jackson Porciuncula
; Gera instalador profissional para Windows (sem necessidade de Python/Terminal)
; =====================================================================

#define MyAppName "Limpar Metadados PRO"
#define MyAppVersion "1.0.4"
#define MyAppPublisher "Jackson Porciuncula"
#define MyAppURL "https://github.com/jbpssdev/limpar-metadados-pro"
#define MyAppExeName "LimparMetadadosPRO.exe"
#define MySetupBaseName "LimparMetadadosPRO-Setup-" + MyAppVersion

[Setup]
; Identificador único da aplicação (GUID gerado especificamente para Limpar Metadados PRO)
AppId={{D37E5528-9842-4D3B-B03F-8C1A8A2B6F9E}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases

; Instalação por padrão no diretório de programas do usuário (%LOCALAPPDATA%\Programs)
; Evita exigir privilégios de administrador/UAC para instalação do usuário comum
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\LICENSE

; Configurações de Privilégios (lowest = instala para o usuário atual sem pedir UAC)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog commandline

; Destino e compactação do executável do Setup
OutputDir=..\release
OutputBaseFilename={#MySetupBaseName}
SetupIconFile=..\assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

; Metadados de versão do instalador (.exe)
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Instalador do {#MyAppName}
VersionInfoTextVersion={#MyAppVersion}
VersionInfoCopyright=Copyright (c) 2026 {#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

; Compactação máxima estável (LZMA2 Ultra)
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
DisableWelcomePage=no

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Executável principal compilado pelo PyInstaller
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Documentação e Licença
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion; DestName: "LEIA-ME.txt"

; Ícone do aplicativo
Source: "..\assets\icon.ico"; DestDir: "{app}\assets"; Flags: ignoreversion

[Icons]
; Atalho no Menu Iniciar
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"

; Atalho opcional na Área de Trabalho
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Opção para iniciar o programa automaticamente ao término da instalação
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
