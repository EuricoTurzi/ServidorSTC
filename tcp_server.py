"""
Servidor TCP simples para testar rastreadores Suntech
Salva todas as comunicações em arquivo .txt
"""

import socket
import datetime
import threading
import os

# Configurações
HOST = '0.0.0.0'  # Escuta em todas as interfaces
PORT = 8800       # Porta padrão Suntech (pode mudar se necessário)
LOG_FILE = 'comunicacao_rastreadores.txt'

def log_message(client_addr, message, direction="RECEBIDO"):
    """Registra mensagem no arquivo de log"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"\n{'='*80}\n"
    log_entry += f"[{timestamp}] {direction} de {client_addr[0]}:{client_addr[1]}\n"
    log_entry += f"{'-'*80}\n"
    log_entry += f"{message}\n"
    log_entry += f"{'='*80}\n"
    
    print(log_entry)  # Mostra no console também
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def handle_client(client_socket, client_addr):
    """Gerencia a conexão com um cliente (rastreador)"""
    print(f"\n[NOVA CONEXÃO] {client_addr[0]}:{client_addr[1]} conectado")
    log_message(client_addr, "CONEXÃO ESTABELECIDA", "STATUS")
    
    try:
        while True:
            # Recebe dados do rastreador
            data = client_socket.recv(4096)
            
            if not data:
                break
            
            # Decodifica a mensagem
            try:
                message = data.decode('utf-8')
            except:
                message = data.hex()  # Se não for texto, mostra em hexadecimal
            
            # Registra a mensagem recebida
            log_message(client_addr, message, "RECEBIDO")
            
            # Resposta simples (ACK) - muitos rastreadores esperam confirmação
            # Suntech geralmente espera ACK após receber dados
            response = b'ACK\r\n'
            client_socket.send(response)
            log_message(client_addr, response.decode('utf-8'), "ENVIADO")
            
    except Exception as e:
        error_msg = f"ERRO: {str(e)}"
        print(f"[ERRO] {client_addr}: {error_msg}")
        log_message(client_addr, error_msg, "ERRO")
    
    finally:
        client_socket.close()
        print(f"[DESCONEXÃO] {client_addr[0]}:{client_addr[1]} desconectado")
        log_message(client_addr, "CONEXÃO ENCERRADA", "STATUS")

def start_server():
    """Inicia o servidor TCP"""
    # Cria o arquivo de log se não existir
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write(f"LOG DE COMUNICAÇÕES - Iniciado em {datetime.datetime.now()}\n")
    
    # Cria o socket do servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"\n{'='*80}")
        print(f"🚀 SERVIDOR TCP INICIADO!")
        print(f"{'='*80}")
        print(f"📡 Escutando em: {HOST}:{PORT}")
        print(f"📝 Log salvando em: {LOG_FILE}")
        print(f"⏰ Horário: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        print("Aguardando conexões dos rastreadores...\n")
        
        while True:
            # Aceita nova conexão
            client_socket, client_addr = server.accept()
            
            # Cria uma thread para gerenciar o cliente
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_addr)
            )
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\n\n[SERVIDOR] Encerrando servidor...")
    except Exception as e:
        print(f"\n[ERRO FATAL] {str(e)}")
    finally:
        server.close()
        print("[SERVIDOR] Servidor encerrado")

if __name__ == "__main__":
    start_server()
