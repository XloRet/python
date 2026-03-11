# -*- coding: utf-8 -*-
from mytrans.m2 import TransLate, LangDetect, CodeLang, LanguageList

print("=== Тест модуля m2 (googletrans 3.1.0a0) ===")

# Демонстрація перекладу
print("Переклад (uk -> en):", TransLate("Сьогодні гарна погода", "uk", "en"))

# Демонстрація визначення мови
print("Визначення мови:", LangDetect("Bonjour tout le monde", "all"))

# Демонстрація кодів
print("Код для 'Ukrainian':", CodeLang("Ukrainian"))
print("Назва для 'de':", CodeLang("de"))

# Таблиця
print("\nТаблиця мов:")
LanguageList("screen", "Привіт")