# Vector CLI Tool

Инструмент командной строки для работы с векторными фигурами.

## Требования

- Python 3.12
- Зависимости: `pip install -r requirements.txt`

## Установка

1. Клонируйте репозиторий
2. Установите зависимости:
```bash
pip install -r requirements.txt
```

**Примечание**: Для работы визуализации требуется библиотека matplotlib. Убедитесь, что зависимости установлены корректно.
## Структура проекта
```
app/
├── cli.py        # Основной CLI интерфейс
├── manage.py     # Логика работы с фигурами
└── shape.py      # Классы фигур
```

## Запуск
```bash
python cli.py
```

## Список команд

### Основные команды

| Команда  | Описание                   | Пример                |
| -------- | -------------------------- | --------------------- |
| `help`   | Справка по фигурам         | `help`                |
| `create` | Создание фигуры            | `create circle 0 0 5` |
| `delete` | Удаление фигуры по индексу | `delete 2`            |
| `list`   | Показать все фигуры        | `list`                |
| `save`   | Сохранить фигуры в JSON    | `save my_shapes`      |
| `load`   | Загрузить фигуры из JSON   | `load saved_shapes`   |
| `draw`   | Визуализировать фигуры     | `draw --size 10`      |
| `exit`   | Выход с автосохранением    | `exit`                |

### Создание фигур

Доступные типы:
- **Point**: `create point <x> <y>`
- **Segment**: `create segment <start_x> <start_y> <end_x> <end_y>`
- **Circle**: `create circle <center_x> <center_y> <radius>`
- **Polygon**: `create polygon <x1> <y1> <x2> <y2>...` (минимум 3 точки)

### Визуализация (draw)
```bash
draw [--save <filename.png>] [--size <N>]
```
- `--save` - сохранить в PNG файл
- `--size` - размер графика в дюймах

## Пример работы
```bash
cli_shape: create point 1 2
Создано: Point (x=1.0, y=2.0)

cli_shape: create circle 0 0 5
Создано: Circle (center point=Point (x=0.0, y=0.0), radius=5.0)

cli_shape: list
0: Point (x=1.0, y=2.0)
1: Circle (center point=Point (x=0.0, y=0.0), radius=5.0)

cli_shape: delete 1
Удалено: Circle (center point=Point (x=0.0, y=0.0), radius=5.0)

cli_shape: list
0: Point (x=1.0, y=2.0)

cli_shape: exit
До свидания!
Сохранено 1 фигуры
График сохранен в 2025-03-19_05-21-42.png
```

## Автоматическое сохранение
При выходе через `exit`:
1. Автоматически сохраняет все фигуры в JSON
2. Генерирует PNG-визуализацию
3. Использует временную метку в имени файла

Формат имен:
- `ГГГГ-ММ-ДД_ЧЧ-ММ-СС.json`
- `ГГГГ-ММ-ДД_ЧЧ-ММ-СС.png`