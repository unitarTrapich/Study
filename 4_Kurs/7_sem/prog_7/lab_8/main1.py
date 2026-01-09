import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


print("Задача 1: Оптимизация производства электроники")

c = [-8000, -12000]

print("\n1. Целевая функция")
print("-" * 70)
print("Максимизируем прибыль: P(x₁, x₂) = 8000·x₁ + 12000·x₂")
print("Для linprog: минимизируем f = -8000·x₁ - 12000·x₂")
print(f"Вектор c = {c}")

A_ub = [
    [2, 3],  # Процессорное время: 2x₁ + 3x₂ ≤ 240
#    [4, 6],  # Оперативная память: 4x₁ + 6x₂ ≤ 480 - избыточно
    [1, 2]  # Аккумуляторы: x₁ + 2x₂ ≤ 150
]

b_ub = [240, 150]

print("\n2. Ограничения")
print("-" * 70)
print("2x₁ + 3x₂ ≤ 240  (процессорное время)")
print("4x₁ + 6x₂ ≤ 480  (оперативная память)")
print("x₁ + 2x₂ ≤ 150   (аккумуляторы)")
print(f"\nМатрица A_ub:\n{np.array(A_ub)}")
print(f"Вектор b_ub: {b_ub}")

bounds = [(0, None), (0, None)]  # x₁ ≥ 0, x₂ ≥ 0

print("\n3. Границы переменных")
print("-" * 70)
print("x₁ ≥ 0 (количество смартфонов)")
print("x₂ ≥ 0 (количество планшетов)")

print("\n4. РЕШЕНИЕ ЗАДАЧИ ...")
print("-" * 70)
result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

if result.success:
    print(f"✓ Статус: {result.message}")
    print(f"\n Оптимальное решение:")
    print(f"   x₁ (смартфоны)  = {result.x[0]:.2f} шт")
    print(f"   x₂ (планшеты)   = {result.x[1]:.2f} шт")
    print(f"\n Максимальная прибыль: {-result.fun:.2f} руб.")

    # Проверка использования ресурсов
    print("\n5. Использование ресурсов")
    print("-" * 70)

    x1_opt, x2_opt = result.x[0], result.x[1]

    cpu_used = 2 * x1_opt + 3 * x2_opt
    ram_used = 4 * x1_opt + 6 * x2_opt
    battery_used = x1_opt + 2 * x2_opt

    print(f"Процессорное время: {cpu_used:.2f} / 240 часов "
          f"({'✓ полностью' if abs(cpu_used - 240) < 1e-6 else f'остаток {240 - cpu_used:.2f}'})")
    print(f"Оперативная память: {ram_used:.2f} / 480 ГБ "
          f"({'✓ полностью' if abs(ram_used - 480) < 1e-6 else f'остаток {480 - ram_used:.2f}'})")
    print(f"Аккумуляторы:       {battery_used:.2f} / 150 шт "
          f"({'✓ полностью' if abs(battery_used - 150) < 1e-6 else f'остаток {150 - battery_used:.2f}'})")

    # Анализ активных ограничений
    print("\n6. Анализ активных ограничений")
    print("-" * 70)
    active_constraints = []

    if abs(cpu_used - 240) < 1e-6:
        active_constraints.append("Процессорное время")
    if abs(ram_used - 480) < 1e-6:
        active_constraints.append("Оперативная память")
    if abs(battery_used - 150) < 1e-6:
        active_constraints.append("Аккумуляторы")

    if active_constraints:
        print("Активные ограничения (используются полностью):")
        for constraint in active_constraints:
            print(f"  • {constraint} — теневая цена μ > 0")

    inactive_constraints = []
    if abs(cpu_used - 240) >= 1e-6:
        inactive_constraints.append("Процессорное время")
    if abs(ram_used - 480) >= 1e-6:
        inactive_constraints.append("Оперативная память")
    if abs(battery_used - 150) >= 1e-6:
        inactive_constraints.append("Аккумуляторы")

    if inactive_constraints:
        print("\nНеактивные ограничения (есть остаток):")
        for constraint in inactive_constraints:
            print(f"  • {constraint} — теневая цена μ = 0")

    print("\n7. Интерпретация")
    print("-" * 70)
    print("Оптимальная стратегия:")
    print(f"  Производить {x1_opt:.0f} смартфонов и {x2_opt:.0f} планшетов ежемесячно")
    print(f"  Это принесет максимальную прибыль {-result.fun:,.0f} руб/месяц")
    print("\nРекомендации:")
    if "Процессорное время" in active_constraints:
        print("  • Инвестировать в увеличение процессорного времени")
    if "Аккумуляторы" in active_constraints:
        print("  • Закупить больше аккумуляторов")
    if "Оперативная память" in inactive_constraints:
        print("  • НЕ закупать дополнительную оперативную память (избыток)")

else:
    print(f"✗ Ошибка: {result.message}")

# ВИЗУАЛИЗАЦИЯ
print("\n" + "=" * 70)
print("ПОСТРОЕНИЕ ГРАФИКА ДОПУСТИМОЙ ОБЛАСТИ")
print("=" * 70)

fig, ax = plt.subplots(figsize=(12, 10))

# Диапазон значений
x1 = np.linspace(0, 160, 400)

# Границы ограничений (выразим x₂ через x₁)
x2_constraint1 = (240 - 2 * x1) / 3  # Процессорное время
x2_constraint2 = (480 - 4 * x1) / 6  # Память
x2_constraint3 = (150 - x1) / 2  # Аккумуляторы

# Обрезаем отрицательные значения
x2_constraint1 = np.maximum(x2_constraint1, 0)
x2_constraint2 = np.maximum(x2_constraint2, 0)
x2_constraint3 = np.maximum(x2_constraint3, 0)

# Построение линий ограничений
ax.plot(x1, x2_constraint1, 'b-', linewidth=2, label='Процессорное время: 2x₁ + 3x₂ = 240')
ax.plot(x1, x2_constraint2, 'purple', linewidth=2, label='Оперативная память: 4x₁ + 6x₂ = 480')
ax.plot(x1, x2_constraint3, 'g-', linewidth=2, label='Аккумуляторы: x₁ + 2x₂ = 150')

# Находим вершины допустимой области
vertices = []

# Пересечение с осями
vertices.append([0, 0])
vertices.append([0, min(240 / 3, 480 / 6, 150 / 2)])
vertices.append([min(240 / 2, 480 / 4, 150), 0])

# Пересечение процессорного времени и аккумуляторов
# 2x₁ + 3x₂ = 240 и x₁ + 2x₂ = 150
# Решаем систему: x₁ = 60, x₂ = 40
vertices.append([60, 40])

# Пересечение памяти и аккумуляторов
# 4x₁ + 6x₂ = 480 и x₁ + 2x₂ = 150
# Решаем: x₁ = 30, x₂ = 60
vertices.append([30, 60])

# Пересечение процессорного времени и памяти
# 2x₁ + 3x₂ = 240 и 4x₁ + 6x₂ = 480
# Совпадают (одна прямая)

# Фильтруем допустимые вершины
valid_vertices = []
for v in vertices:
    x1_v, x2_v = v
    if (x1_v >= 0 and x2_v >= 0 and
            2 * x1_v + 3 * x2_v <= 240 + 1e-6 and
            4 * x1_v + 6 * x2_v <= 480 + 1e-6 and
            x1_v + 2 * x2_v <= 150 + 1e-6):
        valid_vertices.append(v)

# Сортируем вершины по углу для правильного построения многоугольника
valid_vertices = sorted(set(map(tuple, valid_vertices)))
if len(valid_vertices) > 2:
    polygon = Polygon(valid_vertices, alpha=0.3, facecolor='lightgreen',
                      edgecolor='green', linewidth=2, label='Допустимая область')
    ax.add_patch(polygon)

# Оптимальная точка
if result.success:
    ax.plot(result.x[0], result.x[1], 'ro', markersize=15,
            label=f'Оптимум ({result.x[0]:.1f}, {result.x[1]:.1f})', zorder=5)
    ax.annotate(f'Оптимум\n({result.x[0]:.0f}, {result.x[1]:.0f})\nПрибыль: {-result.fun:,.0f} руб',
                xy=(result.x[0], result.x[1]), xytext=(result.x[0] + 15, result.x[1] + 10),
                fontsize=11, fontweight='bold', color='red',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))

# Линии уровня целевой функции (изопрофиты)
profit_levels = [200000, 400000, 600000, 800000, 960000]
for profit in profit_levels:
    x2_profit = (profit - 8000 * x1) / 12000
    x2_profit = np.maximum(x2_profit, 0)
    ax.plot(x1, x2_profit, '--', alpha=0.4, linewidth=1, color='gray')

ax.set_xlabel('x₁ (смартфоны, шт)', fontsize=13, fontweight='bold')
ax.set_ylabel('x₂ (планшеты, шт)', fontsize=13, fontweight='bold')
ax.set_title('Задача оптимизации производства: Геометрическое представление',
             fontsize=15, fontweight='bold', pad=20)
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(-5, 160)
ax.set_ylim(-5, 100)

plt.tight_layout()
plt.savefig('task1_optimization.png', dpi=300, bbox_inches='tight')
print("\n✓ График сохранен как 'task1_optimization.png'")
plt.show()

print("\n" + "=" * 70)
print("ЗАДАЧА 1 ЗАВЕРШЕНА")
print("=" * 70)