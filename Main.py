import os
import msvcrt

# ! ANSI цвета 
RESET = '\033[0m'   
COLOR_NORMAL = '\033[37m'   # ? Белый текст
COLOR_HIGHLIGHT = '\033[44m\033[37m'  # ? Белый на синем фоне

menu_items = [
    "Ввод данных",
    "Просмотр всех данных",
    "Вывод данных по ключу (ФИО)",
    "Удаление данных по ключу (ФИО)",
    "Поиск: средний балл > 4.0",
    "Поиск: одинаковые номера групп",
    "Выход"
]

students = {}


def clear_screen():
    os.system('cls')


def print_menu(selected_index):
    clear_screen()
    print("=== Меню ===")
    for i, item in enumerate(menu_items):
        if i == selected_index:
            print(f"{COLOR_HIGHLIGHT}● {item}{RESET}")
        else:
            print(f"{COLOR_NORMAL}  {item}{RESET}")


def wait_for_menu_key():
    # ! Ждёт нажатие стрелок вверх/вниз, Enter или Esc.
    while True:
        key = msvcrt.getch()
        if key == b'\xe0':  # * Специальная клавиша (стрелки)
            arrow = msvcrt.getch()
            if arrow == b'H':
                return 'up'
            elif arrow == b'P':
                return 'down'
        elif key == b'\r':  # * Enter
            return 'enter'
        elif key == b'\x1b':  # * Esc
            return 'esc'
        # ? Игнорируем всё остальное


# * Функции обработки
def input_student():
    try:
        fio = input("Введите ФИО студента: ").strip()
        if not fio:
            print("ФИО не может быть пустым.")
            input("Нажмите Enter, чтобы продолжить...")
            return

        if fio in students:
            print("Студент с таким ФИО уже существует.")
            input("Нажмите Enter...")
            return

        group = input("Введите номер группы: ").strip()
        if not group:
            print("Номер группы не может быть пустым.")
            input("Нажмите Enter...")
            return

        grades_str = input("Введите 5 оценок через пробел: ").strip()
        grades = list(map(float, grades_str.split()))
        if len(grades) != 5 or not all(2 <= g <= 5 for g in grades):
            print("Ошибка: должно быть ровно 5 оценок от 2 до 5.")
            input("Нажмите Enter...")
            return

        students[fio] = {
            "ФИО": fio,
            "номер группы": group,
            "успеваемость": grades
        }
        print("Данные успешно добавлены.")
        input("Нажмите Enter, чтобы вернуться в меню...")
    except ValueError:
        print("Ошибка: оценки должны быть числами (например, 4.5).")
        input("Нажмите Enter...")
    except Exception as e:
        print(f"Ошибка: {e}")
        input("Нажмите Enter...")


def view_all():
    if not students:
        print("Список студентов пуст.")
    else:
        for data in students.values():
            avg = sum(data["успеваемость"]) / len(data["успеваемость"])
            print(f"\nФИО: {data['ФИО']}")
            print(f"Группа: {data['номер группы']}")
            print(f"Оценки: {data['успеваемость']}")
            print(f"Средний балл: {avg:.2f}")
    input("\nНажмите Enter, чтобы вернуться в меню...")


def view_by_key():
    fio = input("Введите ФИО студента: ").strip()
    if fio in students:
        data = students[fio]
        avg = sum(data["успеваемость"]) / len(data["успеваемость"])
        print(f"\nФИО: {data['ФИО']}")
        print(f"Группа: {data['номер группы']}")
        print(f"Оценки: {data['успеваемость']}")
        print(f"Средний балл: {avg:.2f}")
    else:
        print("Студент с таким ФИО не найден.")
    input("\nНажмите Enter...")


def delete_by_key():
    fio = input("Введите ФИО для удаления: ").strip()
    if fio in students:
        del students[fio]
        print("Студент удалён.")
    else:
        print("Студент не найден.")
    input("Нажмите Enter...")


def search_avg_above_4():
    found = False
    for data in students.values():
        avg = sum(data["успеваемость"]) / len(data["успеваемость"])
        if avg > 4.0:
            print(f"{data['ФИО']} ({data['номер группы']}) — средний балл: {avg:.2f}")
            found = True
    if not found:
        print("Нет студентов со средним баллом выше 4.0.")
    input("Нажмите Enter...")


def search_same_group():
    from collections import defaultdict
    groups = defaultdict(list)
    for fio, data in students.items():
        groups[data["номер группы"]].append((fio, sum(data["успеваемость"]) / len(data["успеваемость"])))

    found = False
    for group, members in groups.items():
        if len(members) > 1:
            print(f"\nГруппа {group}:")
            for name, avg in members:
                print(f"  - {name} (ср. балл: {avg:.2f})")
            found = True
    if not found:
        print("Нет студентов с одинаковыми номерами групп.")
    input("Нажмите Enter...")


# * Основной цикл
def main():
    # ! Активируем поддержку ANSI-цветов
    os.system('')

    current = 0
    while True:
        print_menu(current)
        key = wait_for_menu_key()

        if key == 'up':
            current = (current - 1) % len(menu_items)
        elif key == 'down':
            current = (current + 1) % len(menu_items)
        elif key == 'enter':
            clear_screen()
            match current:
                case 0:
                    input_student()
                case 1:
                    view_all()
                case 2:
                    view_by_key()
                case 3:
                    delete_by_key()
                case 4:
                    search_avg_above_4()
                case 5:
                    search_same_group()
                case 6:  # ! Выход
                    clear_screen()
                    print("До свидания!")
                    break
        elif key == 'esc':
            clear_screen()
            print("До свидания!")
            break


if __name__ == "__main__":
    main()