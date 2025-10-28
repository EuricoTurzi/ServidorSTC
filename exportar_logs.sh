#!/bin/bash
# Script para exportar logs via HTTP na porta 8080

echo "🛑 Parando tudo que estiver rodando na porta 8080..."
sudo fuser -k 8080/tcp 2>/dev/null || true

echo ""
echo "🚀 Iniciando servidor HTTP na porta 8080..."
echo "📂 Servindo arquivos de: $(pwd)"
echo ""
echo "📥 Para baixar os logs, acesse no navegador:"
echo "   http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8080"
echo ""
echo "⚠️  Não esqueça de:"
echo "   1. Abrir porta 8080 no Security Group da AWS"
echo "   2. Fechar este servidor depois (Ctrl+C)"
echo "   3. Remover a porta 8080 do Security Group"
echo ""
echo "═══════════════════════════════════════════════════"

python3 -m http.server 8080
