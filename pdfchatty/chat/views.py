from django.shortcuts import render, redirect
from .models import ChatSession, Message
from .forms import ChatForm
from .utils import get_timestamp, get_avatar
from .database_operations import load_last_k_text_messages, save_text_message, load_messages, get_all_chat_history_ids, \
    delete_chat_history, initialize_db
from .llm_chains import load_pdf_chat_chain
from .pdf_handler import add_documents_to_db
from django.conf import settings

# Initialize the database
initialize_db()


def index(request):
    add_documents_to_db()  # Load and add PDFs to the database on startup

    if request.method == 'POST':
        chat_form = ChatForm(request.POST)

        if chat_form.is_valid():
            user_input = chat_form.cleaned_data['user_input']
            session_key = request.session.get('session_key', 'new_session')
            if session_key == 'new_session':
                session_key = get_timestamp()
                request.session['session_key'] = session_key

            chat_session, created = ChatSession.objects.get_or_create(session_key=session_key)
            llm_chain = load_pdf_chat_chain()
            chat_history = load_last_k_text_messages(session_key, settings.CHAT_CONFIG['chat_memory_length'])
            llm_answer = llm_chain.run(user_input=user_input, chat_history=chat_history)
            save_text_message(session_key, 'human', user_input)
            save_text_message(session_key, 'ai', llm_answer)
            return redirect('index')

    else:
        chat_form = ChatForm()

    session_key = request.session.get('session_key', 'new_session')
    chat_history = load_messages(session_key) if session_key != 'new_session' else []
    all_sessions = get_all_chat_history_ids()

    context = {
        'chat_form': chat_form,
        'chat_history': chat_history,
        'all_sessions': all_sessions,
        'session_key': session_key,
    }

    return render(request, 'chat/index.html', context)
