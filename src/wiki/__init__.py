import difflib
import warnings

import wikipedia

wikipedia.set_lang("ru")


def normalize(text):
    """
    Нормализует текст для упрощения сравнения строк.

    Приводит строку к нижнему регистру, удаляет запятые и сортирует слова в алфавитном порядке.
    Это помогает сравнивать строки, игнорируя порядок слов и пунктуацию.

    Args:
        text (str): Исходный текст для нормализации.

    Returns:
        str: Нормализованная строка с отсортированными словами в нижнем регистре без запятых.
    """
    return ' '.join(sorted(text.lower().replace(',', '').split()))


def find_best_match_normalized(query, choices):
    """
    Находит наиболее похожую строку из списка на основе нормализованного сравнения.

    Для каждого варианта из списка выполняется нормализация (через функцию normalize),
    затем вычисляется коэффициент схожести с нормализованным запросом с помощью SequenceMatcher.
    Возвращается строка с максимальным коэффициентом схожести.

    Args:
        query (str): Строка запроса для поиска наиболее похожего варианта.
        choices (list of str): Список строк, среди которых ищется наиболее подходящее совпадение.

    Returns:
        str or None: Наиболее похожая строка из choices, либо None, если список пуст.
    """
    norm_query = normalize(query)
    norm_choices = {choice: normalize(choice) for choice in choices}
    best_choice = None
    best_ratio = 0

    for choice, norm_choice in norm_choices.items():
        ratio = difflib.SequenceMatcher(None, norm_query, norm_choice).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_choice = choice
    return best_choice


def get_article_from_wiki(query: str) -> str:
    """
    Выполняет поиск и получение содержимого статьи Википедии на русском языке по заданному запросу.

    Функция сначала выполняет поиск статей с помощью модуля wikipedia,
    получая список возможных совпадений и, при наличии, предложение исправления запроса.
    Если предложение исправления присутствует, поиск повторяется по исправленному запросу.
    Затем из списка найденных статей выбирается наиболее подходящая по степени текстового сходства с
    исходным запросом с помощью функции find_best_match_normalized.
    Возвращается содержимое страницы с названием, наиболее близким к запросу.
    Если статьи не найдены, выводится предупреждение и возвращается пустая строка.

    Args:
        query (str): Запрос для поиска статьи в Википедии.

    Returns:
        str: Текстовое содержимое наиболее релевантной статьи Википедии на русском языке,
             либо пустая строка, если статьи не найдены.
    """

    s, r = wikipedia.search(query, suggestion=True)
    if r:
        s = wikipedia.search(query)

    if not s:
        warnings.warn("Не найдено статей")
        return ""

    best_match = find_best_match_normalized(query=query,choices=s)
    return wikipedia.page(best_match).content