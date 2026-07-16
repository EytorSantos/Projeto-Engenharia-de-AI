#!/usr/bin/env python3
"""
Script para iniciar um servidor HTTP simples que serve o frontend.
Execute este script para servir os arquivos HTML, CSS e JS na porta 8080.
"""

import os
import sys
import http.server
import socketserver
from pathlib import Path

PORT = 8080
SRC_DIR = os.path.join(os.path.dirname(__file__), 'src')

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SRC_DIR, **kwargs)
    
    def end_headers(self):
        # Adicionar headers para evitar cache
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == "__main__":
    print("=" * 60)
    print("🩺 MedAssist RAG - Frontend Server")
    print("=" * 60)
    print(f"\n✅ Iniciando servidor na porta {PORT}...")
    print(f"📍 Acesse o frontend em: http://localhost:{PORT}")
    print(f"📂 Servindo arquivos de: {SRC_DIR}\n")
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"🚀 Servidor rodando. Pressione Ctrl+C para parar.\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n❌ Servidor interrompido pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)
