import socket      # библиотека для работы с сетью
import threading   # библиотека для работы с потоками

# ── Глобальные переменные ──────────────────────────────────────────────────────

# Список всех подключённых клиентов (сокетов)
# Сервер смотрит в этот список, когда нужно разослать сообщение всем
clients = []

# Блокировка (замок) — защищает список clients от одновременного изменения
# двумя потоками сразу (защита от race condition)
client_lock = threading.Lock()


# ── Функция рассылки сообщения всем клиентам ──────────────────────────────────

def broadcast(message, sender_socket):
    """
    Рассылает сообщение всем клиентам, кроме отправителя.
    message       — байтовое сообщение (уже закодированное)
    sender_socket — сокет того, кто написал (ему НЕ отправляем)
    """
    # Захватываем блокировку, чтобы никто не менял список в это время
    with client_lock:
        for client in clients:
            # Пропускаем самого отправителя — он и так знает, что написал
            if client != sender_socket:
                try:
                    client.send(message)
                except Exception:
                    # Если клиент отвалился — просто пропускаем
                    pass


# ── Функция обработки одного клиента (запускается в отдельном потоке) ─────────

def handle_client(client_socket, client_address):
    """
    Эта функция работает в отдельном потоке для каждого клиента.
    Она принимает все сообщения от клиента и рассылает их остальным.
    """
    print(f"[+] Новый клиент подключился: {client_address}")

    # Отправляем приветствие только новому клиенту
    welcome = "Добро пожаловать в чат!".encode("utf-8")
    client_socket.send(welcome)

    # Сообщаем ОСТАЛЬНЫМ клиентам, что появился новый участник
    notify = f"[Сервер]: Участник {client_address} вошёл в чат.".encode("utf-8")
    broadcast(notify, client_socket)

    # Добавляем нового клиента в список (с блокировкой, для безопасности)
    with client_lock:
        clients.append(client_socket)

    # ── Бесконечный цикл приёма сообщений от этого клиента ───────────────────
    while True:
        try:
            # recv(1024) — ждём сообщение, максимум 1024 байта за раз
            # Это блокирующий вызов: поток «засыпает» здесь, пока нет данных
            data = client_socket.recv(1024)

            # Если recv вернул пустые данные — клиент закрыл соединение
            if not data:
                break

            # Декодируем байты в текст (уровень 6 OSI — представительский)
            message_text = data.decode("utf-8")
            print(f"[{client_address}]: {message_text}")

            # Формируем сообщение вида «Клиент (адрес): текст»
            # и рассылаем его всем остальным
            full_message = f"Клиент {client_address}: {message_text}".encode("utf-8")
            broadcast(full_message, client_socket)

        except Exception as e:
            # Произошла ошибка (например, клиент внезапно отключился)
            print(f"[!] Ошибка с клиентом {client_address}: {e}")
            break  # выходим из цикла

    # ── Клиент отключился — убираем его ──────────────────────────────────────
    with client_lock:
        if client_socket in clients:
            clients.remove(client_socket)

    client_socket.close()
    print(f"[-] Клиент отключился: {client_address}")

    # Уведомляем оставшихся участников об уходе
    goodbye = f"[Сервер]: Участник {client_address} покинул чат.".encode("utf-8")
    broadcast(goodbye, client_socket)


# ── Главная функция — запуск сервера ──────────────────────────────────────────

def main():
    HOST = "127.0.0.1"   # localhost — работаем только на этом компьютере
    PORT = 5001           # номер порта, на котором слушаем

    # Создаём сокет: AF_INET = IPv4 (уровень 3 OSI), SOCK_STREAM = TCP (уровень 4)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Разрешаем переиспользовать порт сразу после закрытия программы
    # (без этого будет ошибка «Address already in use»)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Привязываем сокет к адресу и порту (уровень 3–4 OSI)
    server_socket.bind((HOST, PORT))

    # Начинаем слушать входящие подключения (уровень 5 OSI — сеансовый)
    # 5 — максимальное число «ожидающих в очереди» подключений
    server_socket.listen(5)

    print(f"[*] Сервер запущен на {HOST}:{PORT}")
    print("[*] Ожидаем подключений...")

    # ── Главный цикл: принимаем новых клиентов ────────────────────────────────
    while True:
        # accept() блокирует поток до тех пор, пока кто-то не подключится
        # Возвращает: сокет нового клиента + его адрес (IP, порт)
        client_socket, client_address = server_socket.accept()

        # Создаём отдельный поток для нового клиента
        # target=handle_client — функция, которую поток будет выполнять
        # args=(client_socket, client_address) — аргументы для функции
        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )

        # daemon=True — поток завершится автоматически, если остановить сервер
        thread.daemon = True

        # Запускаем поток
        thread.start()

        print(f"[*] Активных клиентов: {len(clients) + 1}")


# Запускаем сервер при прямом запуске файла
if __name__ == "__main__":
    main()
