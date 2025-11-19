# Инструкции для AI-агентов (репозиторий audio_notes_saver)

Короткая цель: помочь AI-агенту быстро вникнуть в архитектуру, конвенции и рабочие сценарии репозитория.

- **Главная структура:** приложение — FastAPI в `src/`.
  - Точка входа: `src/main.py` — инициализация Supertokens и создание `FastAPI` `app`.
  - Роутеры: `src/api/` (основной `main_router` в `src/api/__init__.py`, конкретные роуты в файлах вроде `src/api/notes.py`).
  - Модели/схемы: SQLAlchemy-модели в `src/models/`, Pydantic-схемы в `src/schemas/`.
  - DB и сессии: `src/database.py` задаёт `engine`, `new_async_session` и `get_session()`; базовый класс `Base` уже содержит `created_at/updated_at`.

- **Ключевые интеграции и ожидания:**
  - Аутентификация через Supertokens (настроена в `src/main.py`). Защищённые эндпойнты используют `src.core.security.get_current_user_id`.
  - Асинхронный SQLAlchemy (`asyncpg`) — все DB операции должны работать в `async`/`await` контексте.
  - Конфигурация читается через Pydantic `Settings` в `src/config.py`. Ожидаемые env-переменные: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`. `.env` должен находиться в корне репозитория (путь указываем в `SettingsConfigDict`).

- **Принятые паттерны / важные детали (копировать при изменениях):**
  - Зависимость для сессии экспортируется как `SessionDep = Annotated[AsyncSession, Depends(get_session)]` в `src/api/dependencies.py`. Используйте её в эндпойнтах для доступа к сессии.
  - Эндпойнты регистрируются через отдельные роутеры и затем `main_router.include_router(...)` в `src/api/__init__.py`.
  - Pydantic-модели используются как `response_model` и (в проекте) иногда объявляются как `Annotated[NoteSchema, Depends()]` — следуйте существующему синтаксису при добавлении/изменении эндпойнтов.
  - DB setup/tear-down для разработки реализован в `POST /setup` (`src/api/notes.py`) — он вызывает `Base.metadata.drop_all` и `create_all` через `engine.begin()`.
  - Модели используют `mapped_column` и `Mapped[...]` типы (см. `src/models/notes.py`), а не старую декларативную форму. Будьте аккуратны с типами полей (например `ARRAY(String)` для `tags`).

- **Как запускать локально (Windows PowerShell):**
  - Активировать venv (пример):
    `& .venv\Scripts\Activate.ps1`
  - Запустить сервер: `uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`
  - Сначала заполните `.env` с базой Postgres. Для разработки можно использовать эндпойнт `POST /setup` чтобы создать таблицы.

- **Что важно при изменении кода:**
  - Если добавляете роутер — создайте файл в `src/api/`, экспортируйте `router` и подключите в `src/api/__init__.py`.
  - Если нужен доступ к сессии — используйте `SessionDep` и не создавайте новый синхронный сеанс.
  - Для защищённых эндпойнтов добавляйте `Depends(get_current_user_id)` (именно так используют текущий код).
  - Не менять расположение `.env` без изменения `src/config.py` (там жёстко указан путь — корень репозитория).

- **Примеры: короткие сниппеты (следуйте им при генерации кода):**
  - Подключение сессии в endpoint:
    `async def my_endpoint(session: SessionDep):`
  - Регистрация нового роутера:
    `main_router.include_router(my_router, prefix="/my", tags=["my"])` (в `src/api/__init__.py`).
  - Получение id текущего пользователя:
    `current_user_id: str = Depends(get_current_user_id)`

- **Компоненты, требующие осторожности / место для ручной проверки:**
  - Работа с `supertokens_python` — конфиг в `src/main.py`. Локальная разработка может требовать изменения `connection_uri` и доменов.
  - SQLAlchemy async patterns: при изменениях операций записи — проверяйте `await session.commit()` и использование `execution_options(synchronize_session="fetch")` при `update()`.
  - Типы полей в моделях (особенно `ARRAY`, `JSON`, `UUID`) — проверяйте совместимость с `asyncpg`.

Если нужно, внесу дополнения (например: примеры миграций, CI команды или шаблоны PR) — скажите, какие разделы добавить или какие фрагменты кода прояснить. 

***
Файл сгенерирован автоматически/обновлён для ускорения работы AI-агентов. Оставьте обратную связь, если что-то не соответствует текущему процессу разработки.
