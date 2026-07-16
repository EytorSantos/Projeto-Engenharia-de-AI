#!/usr/bin/env python3
"""
Script para iniciar o backend FastAPI do MedAssist RAG.
Execute este script para iniciar o servidor na porta 8000.
"""

import os
import sys
import subprocess

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    print("=" * 60)
    print("🩺 MedAssist RAG - Backend FastAPI")
    print("=" * 60)
    print("\n✅ Iniciando servidor na porta 8000...")
    print("📍 Acesse o frontend em: http://localhost:8000/docs")
    print("🔌 API disponível em: http://localhost:8000\n")
    
    try:
        subprocess.run([
            "uvicorn",
            "src.backend:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n❌ Servidor interrompido pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)
