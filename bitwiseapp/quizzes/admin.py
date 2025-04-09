
from django.contrib import admin
from django.forms import inlineformset_factory, ModelForm
from django.utils.safestring import mark_safe
from .models import Quiz, Question, MultipleChoiceOption, QuizAttempt, Answer

class MultipleChoiceOptionInline(admin.TabularInline):
    model = MultipleChoiceOption
    extra = 3

class QuestionInlineForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question_text'].widget.attrs['style'] = 'width: 80%;'

class QuestionInline(admin.StackedInline):
    model = Question
    form = QuestionInlineForm
    extra = 1
    show_change_link = True

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="auto" style="max-height: 150px;" />')
        return None
    image_preview.short_description = 'Image Preview'
    readonly_fields = ['image_preview']
    fields = ['order', 'question_text', 'question_type', 'image', 'image_preview']

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'image_preview')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]
    prepopulated_fields = {'title': ('title',)}

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" height="auto" style="max-height: 200px;" />')
        return None
    image_preview.short_description = 'Quiz Image Preview'
    readonly_fields = ['image_preview']
    fields = ['title', 'description', 'image', 'image_preview', 'created_by'] # Ensure 'created_by' is included if you want to edit it

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'question_type', 'order', 'image_preview')
    list_filter = ('quiz', 'question_type')
    search_fields = ('question_text',)
    inlines = [MultipleChoiceOptionInline]
    form = QuestionInlineForm

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" height="auto" style="max-height: 200px;" />')
        return None
    image_preview.short_description = 'Image Preview'
    readonly_fields = ['image_preview']
    fields = ['quiz', 'order', 'question_text', 'question_type', 'image', 'image_preview']

class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'start_time', 'end_time', 'score', 'total_questions')
    list_filter = ('quiz', 'user')
    search_fields = ('quiz__title', 'user__username')
    readonly_fields = ('start_time', 'end_time', 'score', 'total_questions')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'essay_answer')
    list_filter = ('attempt__quiz', 'question')
    search_fields = ('attempt__quiz__title', 'question__question_text', 'essay_answer')
    readonly_fields = ('attempt', 'question')

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(MultipleChoiceOption)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(Answer, AnswerAdmin)