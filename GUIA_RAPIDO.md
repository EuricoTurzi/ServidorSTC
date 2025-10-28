# 📋 Guia Rápido - Servidor TCP Suntech

## 🚀 Comandos Essenciais na AWS

### Ver se o servidor está rodando
```bash
ps aux | grep tcp_server
```

### Ver logs em tempo real
```bash
cd ~/ServidorSTC
tail -f comunicacao_rastreadores.txt
```

### Ver logs do sistema (erros)
```bash
tail -f servidor.log
```

### Verificar porta 8800
```bash
sudo ss -tulpn | grep 8800
```

---

## 🔄 Atualizar o Servidor

### No Windows (após fazer mudanças no código)
```bash
git add .
git commit -m "descrição da mudança"
git push origin main
```

### Na AWS (puxar atualizações e reiniciar)
```bash
cd ~/ServidorSTC
git pull origin main
pkill -f tcp_server.py
nohup python3 tcp_server.py > servidor.log 2>&1 &
```

---

## 🛑 Parar o Servidor
```bash
pkill -f tcp_server.py
```

---

## ▶️ Iniciar o Servidor
```bash
cd ~/ServidorSTC
nohup python3 tcp_server.py > servidor.log 2>&1 &
```

---

## 📥 Exportar Logs para Windows

### 1. Na AWS - Subir servidor HTTP
```bash
cd ~/ServidorSTC
./exportar_logs.sh
```

### 2. No Navegador do Windows
```
http://SEU-IP-AWS:8080
```
Clica em `comunicacao_rastreadores.txt` para baixar

### 3. Depois de baixar - Parar o servidor HTTP
Aperta **Ctrl+C** na AWS

### ⚠️ Lembrete
- Abrir porta **8080** no Security Group (temporário)
- Fechar porta **8080** depois de baixar os logs

---

## 🔧 Troubleshooting

### Porta ocupada
```bash
# Matar processo na porta 8800
sudo fuser -k 8800/tcp

# Matar processo na porta 8080
sudo fuser -k 8080/tcp
```

### Servidor não responde
```bash
# Ver se está rodando
ps aux | grep tcp_server

# Ver erros
cat servidor.log

# Reiniciar
pkill -f tcp_server.py
nohup python3 tcp_server.py > servidor.log 2>&1 &
```

### Limpar logs antigos
```bash
cd ~/ServidorSTC
> comunicacao_rastreadores.txt  # Esvazia o arquivo
# ou
rm comunicacao_rastreadores.txt  # Deleta (será recriado)
```

---

## 🌐 Informações da Instância AWS

### Ver IP público
```bash
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

### Ver IP privado
```bash
curl http://169.254.169.254/latest/meta-data/local-ipv4
```

---

## ⚙️ Configuração dos Rastreadores Suntech

**IP do Servidor:** [Seu IP público da AWS]  
**Porta:** 8800  
**Protocolo:** TCP  

---

## 📂 Estrutura de Arquivos

```
~/ServidorSTC/
├── tcp_server.py                    # Servidor principal
├── comunicacao_rastreadores.txt     # Log de comunicações
├── servidor.log                     # Log de erros/sistema
├── exportar_logs.sh                 # Script para exportar logs
└── README.md                        # Documentação completa
```

---

## 🔐 Security Group na AWS (Portas)

**Obrigatório:**
- Porta **8800** (TCP) → Para os rastreadores
- Porta **22** (SSH) → Para você acessar

**Temporário (só quando for exportar logs):**
- Porta **8080** (TCP) → Para baixar logs via HTTP

---

## 💡 Dicas

1. **Sempre use `nohup`** para rodar em background
2. **`tail -f`** para ver logs em tempo real
3. **Faça backup dos logs** antes de limpar
4. **Teste localmente** antes de fazer push
5. **Documente mudanças** nos commits

---

## 🆘 Contatos/Links Úteis

- **Repositório:** https://github.com/EuricoTurzi/ServidorSTC
- **AWS Console:** https://console.aws.amazon.com/ec2
- **Documentação Suntech:** [adicionar se tiver]

---

## 📝 Notas

- Servidor criado em: 28/10/2025
- Porta padrão: 8800
- Resposta automática: ACK
- Sem banco de dados (apenas logs em .txt)

---

**Última atualização:** 28/10/2025
