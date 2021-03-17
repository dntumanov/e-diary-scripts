from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson
from django.http import Http404


def get_child(full_name: str):
    """Достает из базы нужного ученика"""
    try:
        return Schoolkid.objects.get(full_name__contains=full_name)
    except Schoolkid.MultipleObjectsReturned:
        print('Было найдено больше 1-го ученика с похожим именем. Попробуйте указать имя, фамилию и отчество.')
    except Schoolkid.DoesNotExist:
        print('Имя указано не верно либо ученика с таким именем/фамилией не существует')


def fix_marks(full_name: str, marks, new_mark: int):
    """Исправляет отметки ученика"""
    child = get_child(full_name)
    Mark.objects.filter(schoolkid=child, points__in=marks).update(points=new_mark)
    print('Сделано. Проверяй')


def remove_chastisements(full_name: str):
    """Удаляет все замечания ученика"""
    child = get_child(full_name)
    chastisements = Chastisement.objects.filter(schoolkid=child)
    chastisements.delete()
    print('Сделано. Проверяй')


def create_commendation(full_name: str, subject: str, text: str, date: str):
    """Создает замечание для ученика"""
    child = get_child(full_name)
    lessons = list(Lesson.objects.filter(subject__title__contains=subject).order_by('subject__title'))
    if not lessons:
        raise Http404("Не найден такой урок")
    else:
        Commendation.objects.create(
            text=text,
            created=date,
            schoolkid=child,
            subject=lessons[0].subject,
            teacher=lessons[0].teacher
        )
        print('Сделано. Проверяй')
