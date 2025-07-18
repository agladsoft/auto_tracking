# 🚢 Auto Tracking

Система автоматического отслеживания и обработки данных терминалов для импорта, экспорта и каботажных операций.

## 📋 Описание проекта

Auto Tracking - это автоматизированная система для мониторинга и обработки Excel/XLS файлов с данными о грузовых операциях различных терминалов. Система циклически сканирует указанную папку на наличие новых файлов, обрабатывает их и сортирует по терминалам и направлениям операций.

### ⚡ Основные функции

- **📁 Мониторинг файлов**: Автоматическое обнаружение новых Excel/XLS файлов в указанной директории
- **📊 Обработка данных**: Парсинг и валидация данных из Excel файлов
- **🏢 Классификация по терминалам**: Разделение данных по терминалам (НУТЭП, ВСК, ПКТ, УЛКТ, ПЛП)
- **📦 Группировка по направлениям**: Сортировка по операциям импорта, экспорта и каботажа
- **🔄 Автоматическое перемещение**: Обработанные файлы перемещаются в папку `done`, а файлы с ошибками получают префикс `error_`

### 🏭 Поддерживаемые терминалы

- **⛽ НУТЭП** - Новороссийский универсальный терминал экспорта нефтепродуктов
- **🏗️ ВСК** - Восточная стивидорная компания  
- **📦 ПКТ** - Петролеспорт контейнерный терминал
- **🚢 УЛКТ** - Усть-Лужский контейнерный терминал
- **🏢 ПЛП** - Портовая логистическая площадка

### 🧭 Направления операций

- **📥 ИМПОРТ** - Импортные операции
- **📤 ЭКСПОРТ** - Экспортные операции  
- **🔄 Каботаж** - Каботажные перевозки

## 🏗️ Архитектура проекта

```
auto_tracking/
├── scripts/
│   └── main.py              # Основной модуль обработки данных
├── bash/
│   ├── run_auto_tracking.sh # Скрипт запуска с циклическим мониторингом
│   └── flat_auto_tracking.sh # Скрипт обработки одного цикла
├── requirements.txt         # Python зависимости
├── Dockerfile              # Конфигурация Docker контейнера
├── docker-compose.yml      # Docker Compose конфигурация
└── README.md               # Документация проекта
```

### 🧩 Основные компоненты

#### 🐍 AutoTracking (scripts/main.py)
Главный класс системы, реализующий:
- 📖 Чтение Excel файлов с помощью pandas
- ✅ Валидацию и приведение типов данных
- 📊 Группировку данных по терминалам и направлениям
- 💾 Сохранение обработанных данных в новые Excel файлы

#### 🔧 Bash скрипты
- `run_auto_tracking.sh`: 🔄 Запускает бесконечный цикл мониторинга с интервалом 1 секунда
- `flat_auto_tracking.sh`: ⚡ Выполняет один цикл обработки - сканирует папку, обрабатывает найденные файлы

#### 🐙 Docker Compose
- `docker-compose.yml`: 🚀 Оркестрация контейнеров с автоматическим restart и volume mapping
- Поддержка внешней сети `postgres` для интеграции с базой данных
- 🔧 Переменные окружения через `.env` файл
- 📊 Проброс порта 8011 для мониторинга (если необходимо)

## 📋 Требования к системе

### 💻 Программное обеспечение
- 🐍 Python 3.8+
- 🐳 Docker (опционально, для контейнеризации)
- 🐙 Docker Compose (рекомендуется для production)
- 💻 Bash shell (для запуска скриптов мониторинга)

### 📚 Python зависимости
```txt
numpy==1.24.2      # Численные вычисления
pandas==1.4.3      # Обработка данных
openpyxl==3.1.2     # Чтение/запись Excel файлов (xlsx)
xlwt==1.3.0         # Запись старых Excel файлов (xls)
xlsxwriter==3.1.9   # Запись Excel файлов с расширенными возможностями
```

### 🌍 Переменные окружения

Система требует настройки следующих переменных окружения:

```bash
# Основные пути
export XL_IDP_PATH_AUTO_TRACKING="/path/to/input/folder"           # Папка для мониторинга входящих файлов
export XL_IDP_PATH_AUTO_TRACKING_SCRIPTS="/path/to/scripts"        # Путь к скриптам проекта

# Пути для экспорта по терминалам
export XL_IDP_PATH_EXPORT="/path/to/export"                       # Базовый путь для экспорта
export XL_IDP_PATH_VSK_EXPORT="/path/to/vsk/export"              # Путь для экспорта ВСК
export XL_IDP_PATH_NW_EXPORT="/path/to/nw/export"                # Путь для экспорта северо-западных терминалов

# Пути для импорта по терминалам  
export XL_IDP_PATH_IMPORT="/path/to/import"                       # Базовый путь для импорта
export XL_IDP_PATH_VSK_IMPORT="/path/to/vsk/import"              # Путь для импорта ВСК
export XL_IDP_PATH_NW_IMPORT="/path/to/nw/import"                # Путь для импорта северо-западных терминалов

# Для Docker
export XL_IDP_PATH_DOCKER="/path/to/docker/workdir"              # Рабочая директория в контейнере

# Для Docker Compose (корневые пути на хосте)
export XL_IDP_ROOT_AUTO_TRACKING="/host/path/to/auto_tracking"   # Корневой путь для автотрекинга на хосте
export XL_IDP_ROOT="/host/path/to/import"                        # Корневой путь для импорта на хосте
export XL_IDP_ROOT_VSK_IMPORT="/host/path/to/vsk/import"         # Корневой путь ВСК импорт на хосте
export XL_IDP_ROOT_NW_IMPORT="/host/path/to/nw/import"           # Корневой путь СЗ импорт на хосте
export XL_IDP_ROOT_EXPORT="/host/path/to/export"                 # Корневой путь для экспорта на хосте
export XL_IDP_ROOT_VSK_EXPORT="/host/path/to/vsk/export"         # Корневой путь ВСК экспорт на хосте
export XL_IDP_ROOT_NW_EXPORT="/host/path/to/nw/export"           # Корневой путь СЗ экспорт на хосте

# Telegram интеграция (опционально)
export TOKEN_TELEGRAM="your_telegram_bot_token"                  # Токен Telegram бота для уведомлений
```

## 🚀 Установка и настройка

### 💾 Локальная установка

1. **📥 Клонирование репозитория**
   ```bash
   git clone <repository_url>
   cd auto_tracking
   ```

 2. **🐍 Создание виртуального окружения** (рекомендуется)
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # или
    venv\Scripts\activate     # Windows
    ```

 3. **📦 Установка зависимостей**
    ```bash
    pip install -r requirements.txt
    ```

 4. **⚙️ Настройка переменных окружения**
    ```bash
    # Создайте файл .env или добавьте в ~/.bashrc
    export XL_IDP_PATH_AUTO_TRACKING="/home/user/auto_tracking_data"
    export XL_IDP_PATH_AUTO_TRACKING_SCRIPTS="/home/user/auto_tracking"
    # ... остальные переменные
    ```

 5. **📁 Создание необходимых директорий**
   ```bash
   mkdir -p $XL_IDP_PATH_AUTO_TRACKING/done
   mkdir -p $XL_IDP_PATH_VSK_IMPORT/flat_import_vsk_tracking_update
   mkdir -p $XL_IDP_PATH_VSK_EXPORT/flat_export_vsk_tracking_update
   # ... создайте все необходимые директории согласно переменным окружения
   ```

### 🐳 Docker установка

1. **🔨 Сборка Docker образа**
   ```bash
   docker build --build-arg XL_IDP_PATH_DOCKER=/app/workdir -t auto-tracking .
   ```

2. **🚀 Запуск контейнера**
   ```bash
   docker run -d \
     --name auto-tracking-container \
     -v /host/path/to/data:/app/workdir \
     -e XL_IDP_PATH_AUTO_TRACKING=/app/workdir/input \
     -e XL_IDP_PATH_AUTO_TRACKING_SCRIPTS=/app \
     # ... добавьте все необходимые переменные окружения
     auto-tracking
   ```

### 🐳 Docker Compose установка (рекомендуемый для production)

1. **🚀 Запуск с Docker Compose**
    ```yaml
    version: "3.9"
    services:
        auto_tracking:
        container_name: auto_tracking
        restart: always
        ports:
            - "8011:8011"
        volumes:
            - ${XL_IDP_PATH_AUTO_TRACKING_SCRIPTS}:${XL_IDP_PATH_DOCKER}
            - ${XL_IDP_ROOT_AUTO_TRACKING}:${XL_IDP_PATH_AUTO_TRACKING}
            - ${XL_IDP_ROOT}:${XL_IDP_PATH_IMPORT}
            - ${XL_IDP_ROOT_VSK_IMPORT}:${XL_IDP_PATH_VSK_IMPORT}
            - ${XL_IDP_ROOT_NW_IMPORT}:${XL_IDP_PATH_NW_IMPORT}
            - ${XL_IDP_ROOT_EXPORT}:${XL_IDP_PATH_EXPORT}
            - ${XL_IDP_ROOT_VSK_EXPORT}:${XL_IDP_PATH_VSK_EXPORT}
            - ${XL_IDP_ROOT_NW_EXPORT}:${XL_IDP_PATH_NW_EXPORT}
        environment:
            XL_IDP_PATH_AUTO_TRACKING_SCRIPTS: ${XL_IDP_PATH_DOCKER}
            XL_IDP_PATH_AUTO_TRACKING: ${XL_IDP_PATH_AUTO_TRACKING}
            XL_IDP_PATH_IMPORT: ${XL_IDP_PATH_IMPORT}
            XL_IDP_PATH_VSK_IMPORT: ${XL_IDP_PATH_VSK_IMPORT}
            XL_IDP_PATH_NW_IMPORT: ${XL_IDP_PATH_NW_IMPORT}
            XL_IDP_PATH_EXPORT: ${XL_IDP_PATH_EXPORT}
            XL_IDP_PATH_VSK_EXPORT: ${XL_IDP_PATH_VSK_EXPORT}
            XL_IDP_PATH_NW_EXPORT: ${XL_IDP_PATH_NW_EXPORT}
            TOKEN_TELEGRAM: ${TOKEN_TELEGRAM}
        build:
        context: auto_tracking
        dockerfile: ./Dockerfile
        args:
            XL_IDP_PATH_DOCKER: ${XL_IDP_PATH_DOCKER}
        command:
        bash -c "sh ${XL_IDP_PATH_DOCKER}/bash/run_auto_tracking.sh"
        networks:
        - postgres
    ```

   ```bash
   # Сборка и запуск в фоновом режиме
   docker-compose up -d --build
   
   # Просмотр логов
   docker-compose logs -f auto_tracking
   
   # Остановка сервисов
   docker-compose down
   ```


## ▶️ Запуск системы

### 🔄 Способ 1: Непрерывный мониторинг (рекомендуемый)
```bash
# Запуск бесконечного цикла мониторинга
bash bash/run_auto_tracking.sh
```

### ⚡ Способ 2: Разовая обработка
```bash
# Выполнение одного цикла обработки
bash bash/flat_auto_tracking.sh
```

### 🐍 Способ 3: Прямой вызов Python скрипта
```bash
# Обработка конкретного файла
python3 scripts/main.py /path/to/excel/file.xlsx
```

### 🐳 Способ 4: Запуск в Docker
```bash
# После настройки контейнера
docker start auto-tracking-container

# Просмотр логов
docker logs -f auto-tracking-container
```

### 🐳 Способ 5: Запуск с Docker Compose (рекомендуемый)
```bash
# Запуск всего стека
docker-compose up -d

# Перезапуск только auto_tracking сервиса
docker-compose restart auto_tracking

# Просмотр логов в реальном времени
docker-compose logs -f auto_tracking

# Остановка всех сервисов
docker-compose down
```

## 👨‍💻 Разработка

### 📊 Структура данных

Входящие Excel файлы должны содержать следующие колонки:
- `enforce_auto_tracking` (bool) - 🔧 Принудительное автоотслеживание
- `is_auto_tracking` (bool) - ✅ Флаг автоотслеживания  
- `is_auto_tracking_ok` (bool) - ✔️ Статус успешности автоотслеживания
- `original_file_name` (str) - 📄 Оригинальное имя файла
- `terminal` (str) - 🏢 Код терминала (НУТЭП, ВСК, ПКТ, УЛКТ, ПЛП)
- `direction` (str) - 🧭 Направление операции
- `year` (int) - 📅 Год операции
- `month` (int) - 📅 Месяц операции

### 🐛 Отладка

1. **🌍 Проверка переменных окружения**
   ```bash
   env | grep XL_IDP_PATH
   ```

2. **📋 Мониторинг логов**
   ```bash
   # При запуске bash скриптов логи выводятся в консоль
   bash bash/flat_auto_tracking.sh
   ```

3. **📁 Проверка обработанных файлов**
   - ✅ Успешно обработанные файлы перемещаются в `$XL_IDP_PATH_AUTO_TRACKING/done/`
   - ❌ Файлы с ошибками получают префикс `error_` в той же папке

## 🔧 Устранение неполадок

### ⚠️ Частые проблемы

1. **🌍 Ошибка "переменная окружения не найдена"**
   - ✅ Убедитесь, что все необходимые переменные окружения установлены
   - 🔍 Проверьте, что переменные доступны в текущей сессии shell

2. **📁 Ошибка "папка не найдена"**
   - 📂 Создайте все необходимые директории согласно переменным окружения
   - 🔐 Проверьте права доступа к папкам

3. **📊 Ошибка чтения Excel файла**
   - 🔍 Убедитесь, что файл не поврежден
   - 📄 Проверьте формат файла (поддерживаются .xls, .xlsx, .xml)
   - ✅ Убедитесь, что файл содержит необходимые колонки

4. **🐍 Проблемы с Python зависимостями**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

5. **🐳 Docker Compose: ошибка "network postgres not found"**
   ```bash
   # Создайте внешнюю сеть postgres, если она не существует
   docker network create postgres
   
   # Или измените docker-compose.yml, чтобы создать сеть локально:
   # Замените "external: true" на "driver: bridge" в секции networks
   ```

6. **🔒 Проблемы с правами доступа в Docker**
   ```bash
   # Убедитесь, что Docker имеет права на монтируемые папки
   sudo chown -R $USER:$USER /host/data/
   chmod -R 755 /host/data/
   ```

### 📋 Логирование

Для улучшения отладки рекомендуется перенаправлять вывод в лог файлы:

```bash
# Запуск с логированием (локально)
bash bash/run_auto_tracking.sh > auto_tracking.log 2>&1 &

# Мониторинг логов в реальном времени (локально)
tail -f auto_tracking.log

# Логирование в Docker Compose
docker-compose logs -f auto_tracking

# Сохранение логов Docker Compose в файл
docker-compose logs auto_tracking > docker_auto_tracking.log
```

### 🐳 Docker Compose специфические команды

```bash
# Перестроить и перезапустить сервис
docker-compose up -d --build auto_tracking

# Выполнить команду внутри контейнера
docker-compose exec auto_tracking bash

# Проверить статус сервисов
docker-compose ps

# Просмотреть использование ресурсов
docker-compose top

# Очистить остановленные контейнеры и сети
docker-compose down --remove-orphans
```