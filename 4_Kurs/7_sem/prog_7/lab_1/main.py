import math
import time
import timeit
import threading
import asyncio
import os
import json
import random
from datetime import datetime
from functools import partial
from typing import Callable, List
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

import urllib.request
import requests
import aiohttp
import asyncpg
from termcolor import colored
from pynput import keyboard


# ======================================================
# ЧАСТЬ 1. Численное интегрирование
# ======================================================

def integrate(f: Callable, a: float, b: float, *, n_iter: int = 1000) -> float:
    """Численное интегрирование методом прямоугольников"""
    dx = (b - a) / n_iter
    result = 0.0

    for i in range(n_iter):
        x = a + i * dx
        result += f(x) * dx

    return result


def integrate2(f: Callable, a: float, b: float, n_iter: int = 1000) -> float:
    """Версия без keyword-only аргумента"""
    return integrate(f, a, b, n_iter=n_iter)


def time_integration():
    """Сравнение времени интегрирования"""
    test_cases = [
        (math.sin, 0, math.pi),
        (math.cos, 0, math.pi),
        (math.tan, 0, math.pi / 4),
    ]

    n_iters = [10 ** 4, 10 ** 5, 10 ** 6]

    for func, a, b in test_cases:
        print(f"\nФункция: {func.__name__}, интервал [{a}, {b}]")
        for n_iter in n_iters:
            t = timeit.timeit(
                lambda: integrate(func, a, b, n_iter=n_iter),
                number=10
            )
            print(f"  n_iter={n_iter:<7} → {t:.4f} сек")


# ======================================================
# ЧАСТЬ 2. Потоки
# ======================================================

def print_thread_names():
    """Вывод имён потоков"""

    def worker(idx: int):
        print(f"Поток {idx}: {threading.current_thread().name}")

    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def download_files_threaded(urls: List[str]):
    """Загрузка файлов с использованием потоков"""

    def download(url: str, filename: str):
        try:
            urllib.request.urlretrieve(url, filename)
            print(f"Загружено: {filename}")
        except Exception as e:
            print(f"Ошибка загрузки {url}: {e}")

    threads = []
    for i, url in enumerate(urls):
        filename = f"download_{i}.jpg"
        t = threading.Thread(target=download, args=(url, filename))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def factorial_threaded(n: int, num_threads: int = 4) -> int:
    """Вычисление факториала с использованием потоков"""

    def part(start, end):
        res = 1
        for i in range(start, end + 1):
            res *= i
        return res

    chunk = n // num_threads
    results = [1] * num_threads
    threads = []

    for i in range(num_threads):
        start = i * chunk + 1
        end = n if i == num_threads - 1 else (i + 1) * chunk
        t = threading.Thread(
            target=lambda idx, s, e: results.__setitem__(idx, part(s, e)),
            args=(i, start, end)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total = 1
    for r in results:
        total *= r

    return total


# ======================================================
# ЧАСТЬ 3. Futures и синхронизация
# ======================================================

def integrate_async(
    f: Callable,
    a: float,
    b: float,
    *,
    n_jobs: int = 2,
    n_iter: int = 1000,
    executor_class=ThreadPoolExecutor
) -> float:
    """Асинхронное интегрирование"""
    step = (b - a) / n_jobs
    part_integrate = partial(integrate, f, n_iter=n_iter // n_jobs)

    with executor_class(max_workers=n_jobs) as executor:
        futures = [
            executor.submit(
                part_integrate,
                a + i * step,
                a + (i + 1) * step
            )
            for i in range(n_jobs)
        ]
        return sum(f.result() for f in as_completed(futures))


class BankAccount:
    """Потокобезопасный банковский счёт"""

    def __init__(self, balance: int = 0):
        self.balance = balance
        self.lock = threading.Lock()

    def deposit(self, amount: int):
        with self.lock:
            self.balance += amount
            print(f"Внесено {amount}, баланс: {self.balance}")


# ======================================================
# ЧАСТЬ 4. Асинхронность
# ======================================================

async def async_clock_colored():
    """Асинхронные часы с цветом и выходом по ESC"""
    stop_event = asyncio.Event()

    def on_press(key):
        if key == keyboard.Key.esc:
            stop_event.set()

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        while not stop_event.is_set():
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\r{colored(now, 'green', 'on_red')}", end="", flush=True)
            await asyncio.sleep(1)
    finally:
        listener.stop()


# ======================================================
# MAIN
# ======================================================

def main():
    print("=== Демонстрация возможностей Python Concurrency ===")

    print("\n[1] Интегрирование")
    res = integrate(math.sin, 0, math.pi / 2, n_iter=10_000)
    print(f"∫ sin(x) dx = {res:.6f}")

    print("\n[2] Потоки")
    print_thread_names()

    print("\n[3] Futures")
    res_async = integrate_async(math.sin, 0, math.pi / 2, n_jobs=4, n_iter=10_000)
    print(f"Асинхронный результат: {res_async:.6f}")

    print("\n[4] Банковский счёт")
    acc = BankAccount(1000)
    threads = [threading.Thread(target=acc.deposit, args=(100,)) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
