import math
import random
import sys
import time
import os


class Shape:
    def calculate_area(self):
        raise NotImplementedError("Must be implemented in subclasses")


class Circle(Shape):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def calculate_area(self):
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def calculate_area(self):
        return abs(self.x2 - self.x1) * abs(self.y2 - self.y1)


class Triangle(Shape):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

    def calculate_area(self):
        return abs((self.x1 * (self.y2 - self.y3) +
                    self.x2 * (self.y3 - self.y1) +
                    self.x3 * (self.y1 - self.y2)) / 2.0)


class Object:
    def __init__(self, obj_type, shape, color):
        self.obj_type = obj_type
        self.shape = shape
        self.color = color
        self.area = shape.calculate_area()


def generate_file(filename, count):
    colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    with open(filename, 'w') as file:
        for _ in range(count):
            shape_type = random.choice(["Circle", "Rectangle", "Triangle"])
            color = random.choice(colors)

            if shape_type == "Circle":
                x = random.randint(0, 100)
                y = random.randint(0, 100)
                radius = random.randint(1, 50)
                file.write(f"Circle {x} {y} {radius} {color}\n")
            elif shape_type == "Rectangle":
                x1 = random.randint(0, 100)
                y1 = random.randint(0, 100)
                x2 = x1 + random.randint(1, 50)
                y2 = y1 + random.randint(1, 50)
                file.write(f"Rectangle {x1} {y1} {x2} {y2} {color}\n")
            elif shape_type == "Triangle":
                x1 = random.randint(0, 100)
                y1 = random.randint(0, 100)
                x2 = random.randint(0, 100)
                y2 = random.randint(0, 100)
                x3 = random.randint(0, 100)
                y3 = random.randint(0, 100)
                file.write(f"Triangle {x1} {y1} {x2} {y2} {x3} {y3} {color}\n")


def read_objects(filename):
    objects = []
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        parts = line.strip().split(' ')
        if not parts or len(parts) < 2:
            continue
        obj_type = parts[0]
        color = parts[-1]
        if obj_type == "Circle" and len(parts) >= 5:
            x, y, radius = map(int, parts[1:4])
            objects.append(Object(obj_type, Circle(x, y, radius), color))
        elif obj_type == "Rectangle" and len(parts) >= 6:
            x1, y1, x2, y2 = map(int, parts[1:5])
            objects.append(Object(obj_type, Rectangle(x1, y1, x2, y2), color))
        elif obj_type == "Triangle" and len(parts) >= 8:
            x1, y1, x2, y2, x3, y3 = map(int, parts[1:7])
            objects.append(Object(obj_type, Triangle(x1, y1, x2, y2, x3, y3), color))
    return objects


def write_objects(filename, objects, flag):
    mode = 'w' if flag == 0 else 'a'
    with open(filename, mode) as file:
        if flag == 0:
            file.write(f"Number of objects: {len(objects)}\n\n")
            file.write("Initial data:\n")
            for obj in objects:
                if isinstance(obj.shape, Circle):
                    file.write(f"{obj.obj_type} {obj.shape.x} {obj.shape.y} {obj.shape.radius} {obj.color}\n")
                elif isinstance(obj.shape, Rectangle):
                    file.write(f"{obj.obj_type} {obj.shape.x1} {obj.shape.y1} {obj.shape.x2} {obj.shape.y2} {obj.color}\n")
                elif isinstance(obj.shape, Triangle):
                    file.write(f"{obj.obj_type} {obj.shape.x1} {obj.shape.y1} {obj.shape.x2} {obj.shape.y2} {obj.shape.x3} {obj.shape.y3} {obj.color}\n")
        elif flag == 1:
            file.write("\nSorted data:\n")
            for obj in objects:
                file.write(f"{obj.obj_type} {obj.color} Area: {obj.area:.2f}\n")


def bubble_sort(objects, ascending=True):
    for i in range(len(objects)):
        for j in range(len(objects) - i - 1):
            if (ascending and objects[j].area > objects[j + 1].area) or \
                    (not ascending and objects[j].area < objects[j + 1].area):
                objects[j], objects[j + 1] = objects[j + 1], objects[j]


def get_int(min, max):
    while True:
        try:
            user_input = int(input())
            if min <= user_input <= max:
                return user_input
            else:
                print(f"Число должно быть в диапазоне от {min} до {max}. Попробуйте снова.")
        except ValueError:
            print("Ошибка! Введите целое число.")


import os
import time


def print_statistics(filename, start_time, end_time,pause_duration, program_filename):
    # Открываем файл для записи статистики
    try:
        with open(filename, "w") as stat_file:
            # Получаем размер программы
            try:

                execution_time_ms = int((end_time - start_time - pause_duration) * 1000)
                stat_file.write(f"Execution time: {execution_time_ms} ms\n")

                program_size = os.path.getsize(program_filename)
                stat_file.write(f"Program size: {program_size} bytes\n")
            except FileNotFoundError:
                stat_file.write("Failed to get program size: file not found.\n")
                return



            # Подсчёт строк и символов
            try:
                with open(program_filename, "r") as program_file:
                    lines = 0
                    characters = 0
                    for line in program_file:
                        lines += 1
                        characters += len(line)
                    stat_file.write(f"Lines of code: {lines}\n")
                    stat_file.write(f"Characters in code: {characters}\n")
            except FileNotFoundError:
                stat_file.write("Failed to open program file for statistics.\n")
                return

            # Дополнительное сообщение
            stat_file.write(
                "The approximate time spent on writing and debugging the program is 4 hours, learning the syntax for 1.5 hours.\n")
    except OSError as e:
        print(f"Failed to open output file: {e}")


def main():
    start_time = time.time()
    INT_MAX = sys.maxsize
    input_file = "input.txt"
    output_file = "output.txt"
    print("Enter the number of shapes to generate: ")
    start_pause = time.time()
    count = get_int(1, INT_MAX);
    end_pause = time.time()
    pause_duration = end_pause - start_pause
    generate_file(input_file, count)
    objects = read_objects(input_file)
    print("Choose sorting order (1 for ascending, 0 for descending): ")
    start_pause = time.time()
    sort_order = get_int(0, 1)
    end_pause = time.time()
    pause_duration += end_pause - start_pause
    ascending = sort_order == 1
    write_objects(output_file, objects, 0)
    bubble_sort(objects, ascending=ascending)
    write_objects(output_file, objects, 1)
    end_time = time.time()
    program_filename = __file__  # Имя текущего файла Python
    print_statistics("stat.txt", start_time, end_time,pause_duration, program_filename)


if __name__ == "__main__":
    main()
