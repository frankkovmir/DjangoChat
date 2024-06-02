from django.shortcuts import render
from .forms import ChatForm
from .utils import get_avatar
from .llm_chains import load_pdf_chat_chain


def index(request):
    if request.method == 'POST':
        chat_form = ChatForm(request.POST)

        if chat_form.is_valid():
            user_input = chat_form.cleaned_data['user_input']
            llm_chain = load_pdf_chat_chain()
            try:
                llm_answer, documents = llm_chain.run(user_input=user_input)
                document_names = ", ".join(documents)
                llm_answer += f"\nAnswer found in document(s): {document_names}"
            except ValueError:
                llm_answer = "Information not in the document base."

            context = {
                'chat_form': chat_form,
                'user_input': user_input,
                'llm_answer': llm_answer,
                'avatar_user': get_avatar("human"),
                'avatar_bot': get_avatar("ai"),
            }
            return render(request, 'chat/index.html', context)

    else:
        chat_form = ChatForm()

    context = {
        'chat_form': chat_form,
    }

    return render(request, 'chat/index.html', context)
