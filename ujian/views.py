from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ujian, Pertanyaan


@login_required
def ujian_list(request):
    ujian_all = Ujian.objects.all()
    return render(request, 'ujian/list.html', {'ujian_all': ujian_all})

# View for ujian detail
@login_required
def ujian_detail(request, pk):
    ujian = get_object_or_404(Ujian, pk=pk)
    first_question = ujian.pertanyaan_set.order_by('id').first()
    return render(request, 'ujian/detail.html', {
    'ujian': ujian,
    'first_question_id': first_question.id if first_question else None,

    })


@login_required
def ujian_take(request, pk, question_id):
    ujian = get_object_or_404(Ujian, pk=pk)

    # Ambil pertanyaan spesifik berdasarkan question_id
    current_question = get_object_or_404(Pertanyaan, id=question_id, ujian=ujian)
    questions = ujian.pertanyaan_set.all().order_by('id')

    # Ambil jawaban yang tersimpan di session
    stored_answers = request.session.get(f'ujian_{pk}_answers', {})

    if request.method == "POST":
        # Simpan jawaban dari form saat tombol navigasi diklik
        answer = request.POST.get(f'question_{current_question.id}')
        if answer:
            stored_answers[current_question.id] = answer
            request.session[f'ujian_{pk}_answers'] = stored_answers           
            
           

        # Cek apakah pengguna menekan tombol "Simpan dan Selesai"
        if request.POST.get('finish_exam'):
            # Redirect ke halaman hasil ujian
            return redirect('ujian_result', pk=pk)

        # Redirect ke pertanyaan yang dipilih
        next_question_id = request.POST.get('next_question_id')
        if next_question_id:
            return redirect('ujian_take', pk=pk, question_id=next_question_id)
        
    print("Current Question ID:", current_question.id)
    print("Is Last Question:", current_question == questions.last())
 

    return render(request, 'ujian/take.html', {
        'ujian': ujian,
        'current_question': current_question,
        'questions': questions,
        'stored_answers': stored_answers,
    })



@login_required
def ujian_result(request, pk):
    ujian = get_object_or_404(Ujian, pk=pk)
    stored_answers = request.session.get(f'ujian_{pk}_answers', {})
    questions = ujian.pertanyaan_set.all()

    correct_answers = 0
    total_questions = questions.count()

    for question in questions:
        if stored_answers.get(str(question.id)) == question.correct_answer:
            correct_answers += 1

    score = (correct_answers / total_questions) * 100

    return render(request, 'ujian/result.html', {
        'ujian': ujian,
        'score': score,
        'correct_answers': correct_answers,
        'total_questions': total_questions,
    })


@login_required
def ujian_reset(request, pk):
    ujian = get_object_or_404(Ujian, pk=pk)

    # Hapus semua jawaban dari session untuk ujian ini
    if f'ujian_{pk}_answers' in request.session:
        del request.session[f'ujian_{pk}_answers']

    # Redirect kembali ke halaman ujian
    return redirect('ujian_list')
