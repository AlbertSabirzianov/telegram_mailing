def connection_problems_decorator(func):
    """
    Декоратор, который бесконечно повторяет выполнение функции
    до тех пор, пока она не выполнится успешно, перехватывая и
    выводя любые возникающие исключения.

    Аргументы:
        func (callable): Функция, которую нужно декорировать.

    Возвращает:
        callable: Обернутая функция, которая будет продолжать
        вызывать оригинальную функцию до тех пор, пока она не
        выполнится без ошибок.
    """
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as err:
                print(f'Exception in {func.__name__} \n {err}')
                continue

    return wrapper


def shorten_text_by_paragraphs(text: str, max_chars: int) -> str:
    """
    Сокращает текст до заданного максимального количества символов,
    обрезая только по абзацам.

    Функция разбивает исходный текст на абзацы (разделённые двумя переносами строки)
    и последовательно добавляет абзацы целиком, пока суммарная длина не превысит max_chars.
    Если добавление следующего абзаца превысит лимит, он не добавляется.

    Args:
        text (str): Исходный текст, содержащий один или несколько абзацев.
        max_chars (int): Максимально допустимое количество символов в итоговом тексте.

    Returns:
        str: Сокращённый текст, состоящий из целых абзацев, не превышающий max_chars символов.
    """
    paragraphs = text.split('\n\n')  # Разделяем текст на абзацы по двойному переносу строки
    result = []
    current_length = 0

    for para in paragraphs:
        para_length = len(para)
        # Если добавление абзаца не превысит лимит, добавляем его
        if current_length + para_length <= max_chars:
            result.append(para)
            current_length += para_length + 2  # +2 для учёта разделителя '\n\n'
        else:
            break

    return '\n\n'.join(result)