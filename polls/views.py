from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.views.generic.list import ListView

class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model=Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model=Question
    template_name='polls/results.html'

class ResultsView2(ListView):
    model=Question
    context_object_name = 'latest_question_list'
    template_name='polls/results2.html'

def vote(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question':question,'error_message': "You didn't select a choice"})
    else:
        selected_choice.votes +=1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

#pie chart로 나타내기 위해 수동이 아닌 함수로 표현하기. 뷰에서 데이터 만들어주기
def make_chart_data(data_question):
    my_data=list() #사전형 형식의 데이터. 파이차트에 맞춰서 형식에 맞게 데이터 넣어주기. 파이차트가 인식할 수 있게
    for choice in data_question.choice_set.all(): #모든 정답지들을 하니씩 순회하기
        my_dict=dict() #사전형 데이터식으로
        my_dict['name']=choice.choice_text
        my_dict['y']=choice.votes
        my_data.append(my_dict) #리스트에다가 dict값 더해주기

    #chart_data에다가 각 값 넣어주기
    chart_data=[{
        'name':'Votes',
        'colorByPoint':'true',
        'data':my_data,
    }]

    return chart_data

#위에서 만든 데이터를 이 함수에서 templates로 전달
import json
def result_chart(request, question_id):
    question=get_object_or_404(Question, pk=question_id)

    chart_data=make_chart_data(question)
    #json형식으로 변환해주어야 javascript과 연결가능
    dump=json.dumps(chart_data) #파이썬 문자열을 dump형으로 만들어 파이차트로 넘기기

    #제목으로 만들어주기
    chart_title={
        'text':'투표결과<br>'+question.question_text
    }

    dump_title=json.dumps(chart_title)
    return render(request, 'polls/chart.html', {'chart_data':dump, 'chart_title':dump_title})




