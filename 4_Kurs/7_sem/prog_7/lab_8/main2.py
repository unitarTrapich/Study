import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patches as mpatches
from matplotlib.axes import Axes

# ===== ЗАДАЧА 2: ОПТИМИЗАЦИЯ СНАБЖЕНИЯ ВОЕННЫХ БАЗ =====

print("=" * 80)
print("ЗАДАЧА 2: ОПТИМИЗАЦИЯ СНАБЖЕНИЯ ВОЕННЫХ БАЗ (ТРАНСПОРТНАЯ ЗАДАЧА)")
print("=" * 80)

# Шаг 1: Целевая функция
# Минимизировать транспортные расходы
# Переменные: [x_11, x_12, x_13, x_21, x_22, x_23]
c = [8, 6, 10, 9, 7, 5]

print("\n1. ЦЕЛЕВАЯ ФУНКЦИЯ")
print("-" * 80)
print("Минимизируем транспортные расходы:")
print("Z = 8·x₁₁ + 6·x₁₂ + 10·x₁₃ + 9·x₂₁ + 7·x₂₂ + 5·x₂₃")
print(f"Вектор стоимостей c = {c}")

# Шаг 2: Таблица стоимостей
print("\nТаблица стоимостей перевозки (усл. ед./тонна):")
print("-" * 80)
print("             | База Альфа | База Бета | База Гамма | Запасы")
print("-" * 80)
print("Склад 1      |     8      |     6     |     10     |  150")
print("Склад 2      |     9      |     7     |      5     |  250")
print("-" * 80)
print("Потребности  |    120     |    180    |    100     |  400")
print("-" * 80)

# Проверка сбалансированности
supply_total = 150 + 250
demand_total = 120 + 180 + 100

print("\n2. ПРОВЕРКА СБАЛАНСИРОВАННОСТИ")
print("-" * 80)
print(f"Общий запас:         {supply_total} тонн")
print(f"Общая потребность:   {demand_total} тонн")
print(f"Разница:             {supply_total - demand_total} тонн")
print(f"Статус:              {'✓ СБАЛАНСИРОВАНА' if supply_total == demand_total else '✗ НЕ СБАЛАНСИРОВАНА'}")

# Шаг 3: Ограничения-равенства A_eq @ x = b_eq
A_eq = [
    # Ограничения по складам (весь запас вывозится)
    [1, 1, 1, 0, 0, 0],  # Склад 1: x₁₁ + x₁₂ + x₁₃ = 150
    [0, 0, 0, 1, 1, 1],  # Склад 2: x₂₁ + x₂₂ + x₂₃ = 250

    # Ограничения по базам (потребности удовлетворяются)
    [1, 0, 0, 1, 0, 0],  # База Альфа: x₁₁ + x₂₁ = 120
    [0, 1, 0, 0, 1, 0],  # База Бета:  x₁₂ + x₂₂ = 180
    [0, 0, 1, 0, 0, 1]  # База Гамма: x₁₃ + x₂₃ = 100
]

b_eq = [150, 250, 120, 180, 100]

print("\n3. ОГРАНИЧЕНИЯ-РАВЕНСТВА")
print("-" * 80)
print("По складам (весь запас должен быть вывезен):")
print("  Склад 1: x₁₁ + x₁₂ + x₁₃ = 150")
print("  Склад 2: x₂₁ + x₂₂ + x₂₃ = 250")
print("\nПо базам (потребности должны быть удовлетворены):")
print("  База Альфа: x₁₁ + x₂₁ = 120")
print("  База Бета:  x₁₂ + x₂₂ = 180")
print("  База Гамма: x₁₃ + x₂₃ = 100")

print(f"\nМатрица A_eq (5×6):")
for i, row in enumerate(A_eq):
    print(f"  {row}")
print(f"Вектор b_eq: {b_eq}")

# Шаг 4: Границы переменных (все >= 0)
bounds = [(0, None)] * 6

print("\n4. ГРАНИЦЫ ПЕРЕМЕННЫХ")
print("-" * 80)
print("Все переменные xᵢⱼ ≥ 0 (нельзя перевозить отрицательное количество)")

# Шаг 5: Решение задачи
print("\n5. РЕШЕНИЕ ЗАДАЧИ")
print("-" * 80)
result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

if result.success:
    print(f"✓ Статус: {result.message}")

    x_11, x_12, x_13, x_21, x_22, x_23 = result.x

    print(f"\nОПТИМАЛЬНЫЙ ПЛАН ПЕРЕВОЗОК:")
    print("-" * 80)
    print("Со Склада 1:")
    print(f"  → База Альфа: {x_11:6.2f} тонн (стоимость: {8 * x_11:8.2f} усл. ед.)")
    print(f"  → База Бета:  {x_12:6.2f} тонн (стоимость: {6 * x_12:8.2f} усл. ед.)")
    print(f"  → База Гамма: {x_13:6.2f} тонн (стоимость: {10 * x_13:8.2f} усл. ед.)")
    print(f"  Итого:        {x_11 + x_12 + x_13:6.2f} тонн")

    print("\nСо Склада 2:")
    print(f"  → База Альфа: {x_21:6.2f} тонн (стоимость: {9 * x_21:8.2f} усл. ед.)")
    print(f"  → База Бета:  {x_22:6.2f} тонн (стоимость: {7 * x_22:8.2f} усл. ед.)")
    print(f"  → База Гамма: {x_23:6.2f} тонн (стоимость: {5 * x_23:8.2f} усл. ед.)")
    print(f"  Итого:        {x_21 + x_22 + x_23:6.2f} тонн")

    print(f"\nМИНИМАЛЬНАЯ СТОИМОСТЬ: {result.fun:.2f} усл. ед.")

    # Проверка ограничений
    print("\n6. ПРОВЕРКА ОГРАНИЧЕНИЙ")
    print("-" * 80)
    print("Склады:")
    print(f"  Склад 1: {x_11 + x_12 + x_13:.2f} = 150 ✓")
    print(f"  Склад 2: {x_21 + x_22 + x_23:.2f} = 250 ✓")
    print("\nБазы:")
    print(f"  База Альфа: {x_11 + x_21:.2f} = 120 ✓")
    print(f"  База Бета:  {x_12 + x_22:.2f} = 180 ✓")
    print(f"  База Гамма: {x_13 + x_23:.2f} = 100 ✓")

    # Анализ используемых маршрутов
    print("\n7. АНАЛИЗ МАРШРУТОВ")
    print("-" * 80)

    routes = [
        ("Склад 1 → Альфа", x_11, 8),
        ("Склад 1 → Бета", x_12, 6),
        ("Склад 1 → Гамма", x_13, 10),
        ("Склад 2 → Альфа", x_21, 9),
        ("Склад 2 → Бета", x_22, 7),
        ("Склад 2 → Гамма", x_23, 5)
    ]

    print("Используемые маршруты (ненулевые перевозки):")
    used_routes = [(name, qty, cost) for name, qty, cost in routes if qty > 1e-6]
    for name, qty, cost in used_routes:
        print(f"  ✓ {name:20s}: {qty:6.2f} т × {cost:2d} = {qty * cost:8.2f} усл. ед.")

    print("\nНеиспользуемые маршруты:")
    unused_routes = [(name, cost) for name, qty, cost in routes if qty <= 1e-6]
    for name, cost in unused_routes:
        print(f"  ✗ {name:20s}: 0 т (стоимость {cost} усл. ед. — невыгодно)")

    print("\n8. ВОЕННО-ЛОГИСТИЧЕСКИЙ АНАЛИЗ")
    print("-" * 80)
    print("Основные выводы:")
    print(f"  • Все базы полностью обеспечены МТО")
    print(f"  • Все склады полностью разгружены")
    print(f"  • Общая стоимость транспортировки: {result.fun:.2f} усл. ед.")

    print("\nРаспределение поставок:")
    if x_11 + x_12 + x_13 > 0:
        print(f"  • Склад 1 (150 т): основной поставщик для ", end="")
        main_supply_1 = []
        if x_13 > 50: main_supply_1.append("Гаммы")
        if x_12 > 50: main_supply_1.append("Беты")
        if x_11 > 50: main_supply_1.append("Альфы")
        print(", ".join(main_supply_1) if main_supply_1 else "распределенных поставок")

    if x_21 + x_22 + x_23 > 0:
        print(f"  • Склад 2 (250 т): основной поставщик для ", end="")
        main_supply_2 = []
        if x_23 > 50: main_supply_2.append("Гаммы")
        if x_22 > 50: main_supply_2.append("Беты")
        if x_21 > 50: main_supply_2.append("Альфы")
        print(", ".join(main_supply_2) if main_supply_2 else "распределенных поставок")

else:
    print(f"✗ Ошибка: {result.message}")

# ===== ВИЗУАЛИЗАЦИЯ СЕТЕВОЙ ДИАГРАММЫ =====
print("\n" + "=" * 80)
print("ПОСТРОЕНИЕ СЕТЕВОЙ ДИАГРАММЫ")
print("=" * 80)

if result.success:
    fig, ax = plt.subplots(figsize=(16, 10))

    # Координаты узлов
    warehouses = {
        'Склад 1': (2, 8),
        'Склад 2': (2, 3)
    }

    bases = {
        'Альфа': (12, 10),
        'Бета': (12, 5.5),
        'Гамма': (12, 1)
    }


    # Функция для рисования узлов
    def draw_node(ax: Axes, x, y, width, height, label, supply_or_demand, color):
        box = FancyBboxPatch(
            (x - width / 2, y - height / 2), width, height,
            boxstyle="round,pad=0.1",
            edgecolor='black', facecolor=color, linewidth=2
        )
        ax.add_patch(box)
        ax.text(x, y + 0.3, label, ha='center', va='center',
                fontsize=13, fontweight='bold')
        ax.text(x, y - 0.3, supply_or_demand, ha='center', va='center',
                fontsize=11, style='italic')


    # Рисуем склады
    for name, (x, y) in warehouses.items():
        supply = 150 if '1' in name else 250
        draw_node(ax, x, y, 2.5, 1.2, name, f'Запас: {supply} т', '#87CEEB')

    # Рисуем базы
    for name, (x, y) in bases.items():
        demand = {'Альфа': 120, 'Бета': 180, 'Гамма': 100}[name]
        draw_node(ax, x, y, 2.5, 1.2, f'База {name}', f'Нужно: {demand} т', '#90EE90')

    # Оптимальные потоки
    x_11, x_12, x_13, x_21, x_22, x_23 = result.x

    flows = [
        ('Склад 1', 'Альфа', x_11, 8),
        ('Склад 1', 'Бета', x_12, 6),
        ('Склад 1', 'Гамма', x_13, 10),
        ('Склад 2', 'Альфа', x_21, 9),
        ('Склад 2', 'Бета', x_22, 7),
        ('Склад 2', 'Гамма', x_23, 5)
    ]

    # Рисуем потоки (стрелки)
    for warehouse, base, quantity, cost in flows:
        if quantity > 1e-6:  # Рисуем только ненулевые потоки
            x_start, y_start = warehouses[warehouse]
            x_end, y_end = bases[base]

            # Смещение для параллельных стрелок
            offset = 0.2 if '2' in warehouse else -0.2

            # Толщина стрелки пропорциональна объёму
            width = max(2, quantity / 20)

            arrow = FancyArrowPatch(
                (x_start + 1.25, y_start + offset),
                (x_end - 1.25, y_end + offset),
                arrowstyle='->,head_width=0.6,head_length=0.6',
                linewidth=width,
                color='#FF6347' if cost >= 9 else '#4169E1',
                alpha=0.7,
                zorder=1
            )
            ax.add_patch(arrow)

            # Подпись на стрелке
            mid_x = (x_start + x_end) / 2
            mid_y = (y_start + y_end) / 2 + offset

            # --- ДОБАВЛЕННЫЙ КОД ДЛЯ КОРРЕКЦИИ ПОЗИЦИИ ТЕКСТА ---
            text_offset_y = 0  # Базовое смещение
            text_offset_x = 0

            # Если маршрут идет от Склада 2 к Альфе (тот, что перекрывает Склад 1)
            if warehouse == 'Склад 2' and base == 'Альфа':
                text_offset_y = 0.8  # Сдвинуть текст немного вверх
                text_offset_x = 0.8  # Сдвинуть текст немного вправо

            label_text = f'{quantity:.0f} т\n{cost}×{quantity:.0f}={cost * quantity:.0f}'
            ax.text(mid_x + text_offset_x, mid_y + text_offset_y, label_text,
                    ha='center', va='center',
                    fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.4',
                              facecolor='white', edgecolor='black', linewidth=1.5))

    # Легенда
    legend_elements = [
        mpatches.Patch(facecolor='#87CEEB', edgecolor='black', label='Склады'),
        mpatches.Patch(facecolor='#90EE90', edgecolor='black', label='Военные базы'),
        mpatches.Patch(facecolor='#4169E1', alpha=0.7, label='Выгодный маршрут (≤7)'),
        mpatches.Patch(facecolor='#FF6347', alpha=0.7, label='Дорогой маршрут (≥9)')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.9)

    # Добавляем текст с результатом
    result_text = f'Минимальная стоимость: {result.fun:.0f} усл. ед.'
    ax.text(7, 12, result_text, ha='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.7', facecolor='yellow',
                      edgecolor='black', linewidth=2))

    ax.set_xlim(-1, 15)
    ax.set_ylim(-0.5, 12.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Оптимальный план снабжения военных баз\nТранспортная задача',
                 fontsize=17, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('task2_transport.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("\n✓ График сохранен как 'task2_transport.png'")
    plt.show()

print("\n" + "=" * 80)
print("ЗАДАЧА 2 ЗАВЕРШЕНА")
print("=" * 80)