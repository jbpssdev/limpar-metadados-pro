"""
tests/test_validation.py - Testes automatizados para validação de segurança e manipulação de arquivos.
"""

import os
import sys
import unittest
import tempfile

# Adiciona o diretório raiz ao sys.path para importação dos módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import (
    sanitize_filename,
    validate_file_security,
    validar_arquivo_video,
    obter_info_sistema,
    get_ffmpeg_path,
    verificar_ffmpeg
)

class TestLimparMetadadosCore(unittest.TestCase):
    def test_sanitize_filename_caracteres_perigosos(self):
        caminho = os.path.join("videos", "video;rm -rf;$(calc).mp4")
        sanitizado = sanitize_filename(caminho)
        self.assertNotIn(";", os.path.basename(sanitizado))
        self.assertNotIn("$(", os.path.basename(sanitizado))
        self.assertEqual(os.path.dirname(sanitizado), "videos")

    def test_validate_file_security_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            validate_file_security("arquivo_inexistente_12345.mp4")

    def test_validate_file_security_path_traversal(self):
        # Caminho relativo com .. para um arquivo existente na pasta pai
        traversal_path = os.path.join("..", os.path.basename(os.getcwd()), "main.py")
        if os.path.exists(traversal_path):
            with self.assertRaises(ValueError):
                validate_file_security(traversal_path)

    def test_validar_arquivo_video_vazio(self):
        sucesso, msg = validar_arquivo_video("")
        self.assertFalse(sucesso)
        self.assertIn("inválido", msg.lower())

    def test_obter_info_sistema(self):
        info = obter_info_sistema()
        self.assertIn("versao", info)
        self.assertIn("plataforma", info)
        self.assertEqual(info["versao"], "1.0.4")

    def test_get_ffmpeg_path(self):
        path = get_ffmpeg_path()
        self.assertTrue(bool(path))

    def test_verificar_ffmpeg(self):
        sucesso, msg = verificar_ffmpeg()
        self.assertTrue(sucesso, f"Falha na detecção do FFmpeg: {msg}")

if __name__ == "__main__":
    unittest.main()
