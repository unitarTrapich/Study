# Отчет по заданию: создание UML-диаграмм для ВКР

## Тема ВКР

**«Разработка системы хранения и извлечения знаний из учебных материалов на основе графовой базы данных.»**

## 1. Описание предметной области

Разрабатываемая система представляет собой веб-платформу для хранения и извлечения знаний из учебных материалов.  
Авторизованный пользователь загружает учебные документы (PDF, DOCX, презентации, текстовые файлы), после чего серверная часть выполняет интеллектуальную обработку содержимого: извлечение сущностей, терминов, связей, тем и фактов с использованием NLP/ML-подходов.

Извлеченные знания сохраняются в графовой базе данных в виде узлов и ребер. Это позволяет:

- выполнять семантический поиск по знаниям;
- выявлять связи между понятиями и источниками;
- ускорять доступ к релевантной учебной информации;
- повторно обрабатывать материалы при обновлении моделей;
- формировать структурированное представление предметной области.

Ключевая ценность системы состоит в преобразовании неструктурированных учебных материалов в структурированную сеть знаний, удобную для поиска, анализа и поддержки образовательного процесса.

## 2. Подход к выполнению задания


1. Определены основные роли пользователей и границы системы.
2. Выделены ключевые сущности предметной области и их связи.
3. Построены статическая и динамические модели системы:
   - диаграмма вариантов использования;
   - диаграмма классов;
   - диаграмма последовательности;
   - диаграмма состояний;
   - диаграмма деятельности.
4. Для диаграммы классов подготовлен программный код на языке **Python**.


---

## 3. Диаграмма вариантов использования (Use Case / Диаграмма прецедентов)

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam actorStyle awesome

actor "Гость" as Guest
actor "Пользователь" as User
actor "Администратор" as Admin
actor "NLP/ML сервис" as AI

rectangle "Система хранения и извлечения знаний" {
  usecase "Регистрация" as UC_Register
  usecase "Вход в систему" as UC_Login
  usecase "Загрузка учебного материала" as UC_Upload
  usecase "Запуск извлечения знаний" as UC_Extract
  usecase "Просмотр графа знаний" as UC_ViewGraph
  usecase "Семантический поиск" as UC_Search
  usecase "Экспорт результатов" as UC_Export
  usecase "Управление пользователями" as UC_ManageUsers
  usecase "Модерация материалов" as UC_Moderate
  usecase "Повторная обработка материала" as UC_Reprocess
}

Guest --> UC_Register
Guest --> UC_Login

User --> UC_Login
User --> UC_Upload
User --> UC_Extract
User --> UC_ViewGraph
User --> UC_Search
User --> UC_Export

Admin --> UC_Login
Admin --> UC_ManageUsers
Admin --> UC_Moderate
Admin --> UC_Reprocess
Admin --> UC_ViewGraph

AI --> UC_Extract
AI --> UC_Reprocess

UC_Extract .> UC_Upload : <<include>>
UC_Reprocess .> UC_Extract : <<extend>>
UC_Search .> UC_ViewGraph : <<extend>>
@enduml
```

![Диаграмма вариантов использования](images/use-case.png)

---

## 4. Диаграмма классов (Class Diagram / Диаграмма классов)

```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam shadowing false

class Пользователь {
  +id: UUID
  +email: str
  +хешПароля: str
  +роль: Role
  +создан: datetime
  +проверитьДоступ(): bool
}

class УчебныйМатериал {
  +id: UUID
  +название: str
  +тип: str
  +путьФайла: str
  +статусОбработки: ProcessingStatus
  +датаЗагрузки: datetime
  +пометитьОбработанным(): void
}

class ЗадачаОбработки {
  +id: UUID
  +статус: ProcessingStatus
  +создана: datetime
  +завершена: datetime
  +запустить(): void
  +завершить(): void
  +ошибка(текст: str): void
}

class СущностьЗнаний {
  +id: UUID
  +тип: str
  +значение: str
  +уверенность: float
}

class СвязьЗнаний {
  +id: UUID
  +тип: str
  +вес: float
}

class ГрафЗнаний {
  +id: UUID
  +версия: int
  +датаОбновления: datetime
  +добавитьСущность(): void
  +добавитьСвязь(): void
}

class ПоисковыйЗапрос {
  +id: UUID
  +текст: str
  +дата: datetime
}

class РезультатПоиска {
  +id: UUID
  +ранг: float
  +фрагмент: str
}

class NLPСервис {
  +извлечьСущности(текст: str): List<СущностьЗнаний>
  +извлечьСвязи(текст: str): List<СвязьЗнаний>
}

enum Role {
  Гость
  Пользователь
  Администратор
}

enum ProcessingStatus {
  Создано
  ВОчереди
  ВОбработке
  Завершено
  Ошибка
}

Пользователь "1" -- "0..*" УчебныйМатериал : загружает >
УчебныйМатериал "1" -- "0..*" ЗадачаОбработки : обрабатывается >
ЗадачаОбработки "1" ..> "1" NLPСервис : использует >
ЗадачаОбработки "1" --> "1" ГрафЗнаний : обновляет >
ГрафЗнаний "1" *-- "0..*" СущностьЗнаний : содержит >
ГрафЗнаний "1" *-- "0..*" СвязьЗнаний : содержит >
СвязьЗнаний "1" --> "1" СущностьЗнаний : источник >
СвязьЗнаний "1" --> "1" СущностьЗнаний : назначение >
Пользователь "1" --> "0..*" ПоисковыйЗапрос : выполняет >
ПоисковыйЗапрос "1" --> "0..*" РезультатПоиска : возвращает >
РезультатПоиска "0..*" --> "0..1" СущностьЗнаний : ссылается >
@enduml
```

![Диаграмма классов](images/class-diagram.png)

### 4.1 Программный код на Python для реализации модели классов

```python
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4


class Role(str, Enum):
    GUEST = "Гость"
    USER = "Пользователь"
    ADMIN = "Администратор"


class ProcessingStatus(str, Enum):
    CREATED = "Создано"
    QUEUED = "ВОчереди"
    RUNNING = "ВОбработке"
    DONE = "Завершено"
    ERROR = "Ошибка"


@dataclass
class User:
    id: UUID
    email: str
    password_hash: str
    role: Role
    created_at: datetime

    def has_access(self) -> bool:
        return self.role in {Role.USER, Role.ADMIN}


@dataclass
class LearningMaterial:
    id: UUID
    title: str
    file_type: str
    file_path: str
    status: ProcessingStatus
    uploaded_at: datetime
    owner_id: UUID

    def mark_done(self) -> None:
        self.status = ProcessingStatus.DONE


@dataclass
class KnowledgeEntity:
    id: UUID
    entity_type: str
    value: str
    confidence: float


@dataclass
class KnowledgeRelation:
    id: UUID
    relation_type: str
    weight: float
    source_entity_id: UUID
    target_entity_id: UUID


@dataclass
class KnowledgeGraph:
    id: UUID
    version: int
    updated_at: datetime
    entities: List[KnowledgeEntity] = field(default_factory=list)
    relations: List[KnowledgeRelation] = field(default_factory=list)

    def add_entity(self, entity: KnowledgeEntity) -> None:
        self.entities.append(entity)
        self.updated_at = datetime.utcnow()

    def add_relation(self, relation: KnowledgeRelation) -> None:
        self.relations.append(relation)
        self.updated_at = datetime.utcnow()


@dataclass
class ProcessingTask:
    id: UUID
    material_id: UUID
    status: ProcessingStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    def start(self) -> None:
        self.status = ProcessingStatus.RUNNING

    def finish(self) -> None:
        self.status = ProcessingStatus.DONE
        self.completed_at = datetime.utcnow()

    def fail(self, message: str) -> None:
        self.status = ProcessingStatus.ERROR
        self.error_message = message
        self.completed_at = datetime.utcnow()


class NLPService:
    def extract_entities(self, text: str) -> List[KnowledgeEntity]:
        # Заглушка: здесь может быть вызов модели NER/LLM
        return []

    def extract_relations(self, text: str) -> List[KnowledgeRelation]:
        # Заглушка: здесь может быть извлечение семантических связей
        return []


@dataclass
class SearchQuery:
    id: UUID
    user_id: UUID
    text: str
    created_at: datetime


@dataclass
class SearchResult:
    id: UUID
    query_id: UUID
    rank: float
    snippet: str
    entity_id: Optional[UUID] = None


if __name__ == "__main__":
    admin = User(
        id=uuid4(),
        email="admin@example.com",
        password_hash="hashed_password",
        role=Role.ADMIN,
        created_at=datetime.utcnow(),
    )
    print("Доступ администратора:", admin.has_access())
```

---

## 5. Диаграмма последовательности (Sequence Diagram / Диаграмма последовательности)

```plantuml
@startuml
skinparam shadowing false

actor "Пользователь" as User
participant "Веб-интерфейс" as UI
participant "API сервер" as API
participant "Сервис обработки" as Processor
participant "NLP/ML сервис" as AI
database "Графовая БД" as GraphDB

User -> UI : Загружает учебный файл
UI -> API : POST /materials
API -> GraphDB : Сохранить метаданные файла
GraphDB --> API : material_id
API --> UI : Материал принят

User -> UI : Запустить извлечение знаний
UI -> API : POST /materials/{id}/extract
API -> Processor : Создать задачу обработки
Processor -> AI : Извлечь сущности и связи
AI --> Processor : Сущности, связи, уверенности
Processor -> GraphDB : Записать узлы и ребра
GraphDB --> Processor : OK
Processor -> API : Задача завершена
API --> UI : Статус: Завершено

User -> UI : Выполнить семантический поиск
UI -> API : GET /search?q=...
API -> GraphDB : Запрос по графу знаний
GraphDB --> API : Результаты
API --> UI : Список релевантных фрагментов
@enduml
```

![Диаграмма последовательности](images/sequence-diagram.png)

---

## 6. Диаграмма состояний (State Diagram / Диаграмма состояний)

```plantuml
@startuml
skinparam shadowing false

[*] --> Создан

Создан --> ВОчереди : материал загружен
ВОчереди --> ВОбработке : воркер взял задачу
ВОбработке --> Завершено : извлечение успешно
ВОбработке --> Ошибка : сбой NLP/валидации/БД

Ошибка --> ВОчереди : повторный запуск
Завершено --> ВОчереди : запрос на переобработку

Завершено --> [*]
@enduml
```

![Диаграмма состояний](images/state-diagram.png)

---

## 7. Диаграмма деятельности (Activity Diagram / Диаграмма активности)

```plantuml
@startuml
skinparam shadowing false

start
:Авторизация пользователя;

if (Успешная авторизация?) then (Да)
  :Загрузка учебного материала;
  :Проверка формата и целостности файла;

  if (Файл валиден?) then (Да)
    :Постановка задачи в очередь;
    :Извлечение текста;
    :NLP/ML анализ (сущности, связи, темы);
    :Нормализация и валидация знаний;
    :Запись в графовую БД;
    :Индексация для поиска;
    :Показ результата пользователю;
  else (Нет)
    :Сообщение об ошибке загрузки;
  endif

else (Нет)
  :Отказ в доступе;
endif

stop
@enduml
```

![Диаграмма деятельности](images/activity-diagram.png)
