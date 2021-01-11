from django import template
from notes.models import Note, Group

register = template.Library()

@register.inclusion_tag('notes/notes.html')
def get_notes_list(request):
    notes = request.user.notes.order_by('planned_date')
    context = {}
    context[Group.objects.get(id=1)] = []
    for note in notes:
        if note.group not in context:
            context[note.group] = [note]
        else:
            context[note.group].append(note)
    return {'notes': context}
