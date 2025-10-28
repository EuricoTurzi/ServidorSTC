# 🚀 Servidor TCP para Rastreadores Suntech

Servidor TCP simples para receber e logar comunicações de rastreadores Suntech.

## 📋 Pré-requisitos

- Python 3.6 ou superior
- Instância AWS EC2 (Ubuntu/Amazon Linux)
- Rastreadores Suntech configurados

---

## 🔧 Instalação Local (Teste)

```bash
# 1. Clone ou baixe este repositório
cd Servidor

# 2. Execute o servidor
python tcp_server.py
```

---

## ☁️ Instalação na AWS EC2

### Passo 1: Configurar Security Group
No painel da AWS EC2, configure o Security Group da sua instância:

```
Inbound Rules:
- Type: Custom TCP
- Port: 8800 (ou a porta que você escolher)
- Source: 0.0.0.0/0 (ou IPs específicos dos rastreadores)

- Type: SSH
- Port: 22
- Source: Seu IP (para acesso SSH)
```

### Passo 2: Conectar na Instância

```bash
# Windows (usando Git Bash ou PowerShell)
ssh -i "sua-chave.pem" ubuntu@seu-ip-publico-aws

# Se der erro de permissão no Windows, ajuste a permissão da chave:
# No PowerShell como Admin:
icacls "sua-chave.pem" /inheritance:r
icacls "sua-chave.pem" /grant:r "%USERNAME%:R"
```

### Passo 3: Instalar Python (se necessário)

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip -y

# Amazon Linux
sudo yum update -y
sudo yum install python3 -y
```

### Passo 4: Transferir o Servidor

#### Opção A: Usando SCP (Simples)
```bash
# No seu Windows (Git Bash ou PowerShell)
scp -i "sua-chave.pem" tcp_server.py ubuntu@seu-ip-aws:~/
```

#### Opção B: Usando Git (Recomendado)

**No seu Windows:**
```bash
# 1. Inicialize o repositório Git (se ainda não fez)
cd c:\Users\eurico.dante\Desktop\Development\Servidor
git init
git add .
git commit -m "Servidor TCP inicial"

# 2. Crie um repositório no GitHub/GitLab e faça push
git remote add origin https://github.com/seu-usuario/seu-repo.git
git branch -M main
git push -u origin main
```

**Na AWS:**
```bash
# Clone o repositório
cd ~
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo

# Para atualizações futuras, basta:
git pull origin main
```

### Passo 5: Executar o Servidor

```bash
# Teste rápido (para no Ctrl+C)
python3 tcp_server.py

# Executar em background (continua rodando após fechar SSH)
nohup python3 tcp_server.py > servidor.log 2>&1 &

# Ver o processo rodando
ps aux | grep tcp_server

# Ver logs em tempo real
tail -f comunicacao_rastreadores.txt
```

### Passo 6: Gerenciar o Servidor

```bash
# Parar o servidor
pkill -f tcp_server.py

# Reiniciar (parar e iniciar novamente)
pkill -f tcp_server.py
nohup python3 tcp_server.py > servidor.log 2>&1 &

# Ver logs
cat comunicacao_rastreadores.txt

# Baixar logs para seu Windows
# (executar no Windows)
scp -i "sua-chave.pem" ubuntu@seu-ip-aws:~/comunicacao_rastreadores.txt .
```

---

## 🔄 Sincronização Automática com AWS (Git)

### Setup Inicial

1. **No seu Windows:**
```bash
cd c:\Users\eurico.dante\Desktop\Development\Servidor
git init
git add .
git commit -m "Initial commit"
```

2. **Criar repositório no GitHub** (mais fácil):
   - Vá em github.com e crie um novo repositório
   - Siga as instruções para fazer push

3. **Na AWS, configure pull automático:**
```bash
# Crie um script de atualização
cat > ~/atualizar_servidor.sh << 'EOF'
#!/bin/bash
cd ~/seu-repo
git pull origin main
pkill -f tcp_server.py
sleep 2
nohup python3 tcp_server.py > servidor.log 2>&1 &
echo "Servidor atualizado e reiniciado!"
EOF

chmod +x ~/atualizar_servidor.sh

# Agora basta executar quando atualizar o código:
./atualizar_servidor.sh
```

### Workflow Diário

```bash
# 1. No Windows - Fazer alterações e push
git add .
git commit -m "Descrição das mudanças"
git push origin main

# 2. Na AWS - Atualizar
./atualizar_servidor.sh
```

---

## 📊 Configurar os Rastreadores Suntech

Configure seus rastreadores com:
- **IP do Servidor**: O IP público da sua instância EC2
- **Porta**: 8800 (ou a que você definiu no código)
- **Protocolo**: TCP

---

## 🛠️ Customizações

### Mudar a Porta
Edite `tcp_server.py` e altere:
```python
PORT = 8800  # Mude para a porta desejada
```

### Mudar o Arquivo de Log
```python
LOG_FILE = 'comunicacao_rastreadores.txt'  # Mude o nome
```

### Mudar a Resposta (ACK)
```python
response = b'ACK\r\n'  # Mude para outra resposta se necessário
```

---

## 📝 Verificar Logs

```bash
# Ver todo o log
cat comunicacao_rastreadores.txt

# Ver últimas 50 linhas
tail -n 50 comunicacao_rastreadores.txt

# Acompanhar em tempo real
tail -f comunicacao_rastreadores.txt

# Buscar por IP específico
grep "192.168.1.100" comunicacao_rastreadores.txt
```

---

## 🐛 Troubleshooting

### Servidor não inicia
```bash
# Verificar se a porta está em uso
netstat -tulpn | grep 8800

# Matar processo na porta
sudo fuser -k 8800/tcp
```

### Rastreador não conecta
- Verificar Security Group na AWS
- Verificar IP público da instância
- Testar conexão: `telnet seu-ip-aws 8800`
- Verificar firewall da rede do rastreador

### Logs não aparecem
```bash
# Verificar permissões
ls -la comunicacao_rastreadores.txt

# Ver erros do servidor
cat servidor.log
```

---

## 📱 Testar Localmente

```bash
# Em outro terminal, simule um rastreador:
telnet localhost 8800

# Ou use netcat:
echo "ST300STT;100850000;02;010;20190804;21:25:10;+37.478519;-122.151709;0.00;0.00;0;0.00;0.00;0.00;0" | nc localhost 8800
```

---

## 🎯 Pronto!

Agora você tem um servidor TCP rodando que vai:
- ✅ Aceitar conexões dos rastreadores
- ✅ Salvar todas as mensagens em `comunicacao_rastreadores.txt`
- ✅ Enviar ACK para cada mensagem recebida
- ✅ Mostrar tudo no console em tempo real

**Dúvidas?** É só perguntar! 🚀
