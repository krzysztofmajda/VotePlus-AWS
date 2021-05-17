"""
Routes and views for the flask application.
"""

import numpy as np
from flask import render_template, flash, redirect, url_for, request, session
import app, fun_base, fun, message, fun_mail

PYTHONIOENCODING="UTF-8"

@app.route('/')
@app.route('/strona_startowa')
def strona_startowa():
    if 'log_in_user_id' in session or 'activate_user_id' in session:
        loged_in = True
    else:
        loged_in = False
    return render_template('strona_startowa.html', info=message.main_page(), loged_in=loged_in)

@app.route('/logowanie', methods=['GET','POST'])
def logowanie():
    if 'log_in_user_id' in session or 'active_user_id' in session:
        return redirect('/zalogowany')
    session['logging'] = 'begin'
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')
        out = fun_base.if_loging(login, password)
        if out[0]:
            session.pop('logging', None)
            if not out[2]:
                session['log_in_user_id'] = out[1]
                return redirect('/zalogowany')
            else:
                session['activate_user_id'] = out[1]
                return redirect('/aktywacja_konta')
        else:
            session['log_error'] = "Error"
            return redirect('/blad_log')
    return render_template('logowanie.html')

@app.route('/blad_log')
def blad_log():
    if not 'log_error' in session:
        return redirect('/logowanie')
    return render_template('blad.html', info=message.log_in_fail(), site_type='logowanie')

@app.route('/rejestracja', methods=['GET','POST'])
def rejestracja():
    if 'log_in_user_id' in session or 'active_user_id' in session:
        return redirect('/zalogowany')
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('user_name')
        surname = request.form.get('user_surname')
        email = request.form.get('user_email')
        sex = request.form.get('user_sex')
        birth_year = request.form.get('user_year')
        password = request.form.get('new_password')
        out = fun_base.register(username,name,surname,sex,email,birth_year,password)
        if out == '0':
            session['reg_success'] = "Success"
            return redirect('/udana_rejestracja')
        else:
            session['reg_error_id'] = out[0]
            return redirect('/blad_rej')
    return render_template('rejestracja.html')

@app.route('/blad_rej')
def blad_rej():
    if not 'reg_error_id' in session:
        return redirect('/rejestracja')
    info = message.register_fail(int(session['reg_error_id']))
    session.pop('reg_error_id', None)
    return render_template('blad.html', info=info, site_type='rejestracja')

@app.route('/udana_rejestracja')
def udana_rejestracja():
    if not 'reg_success' in session:
        return redirect('/rejestracja')
    return render_template('potwierdzenie.html', info=message.register_success(), site_type='rejestracja')

@app.route('/zapomniane_haslo', methods=['GET','POST'])
def zapomniane_haslo():
    if not 'logging' in session:
        return redirect('/logowanie')
    if request.method == "POST":
        email = request.form.get('user_email')
        code = fun.random_number(6)
        session['forgot_code_id'] = code
        uid = fun_base.get_user_id_for_reset(email,code)
        if len(uid) > 0:
            session['forgot_user_id'] = uid
        session.pop('loging', None)
        return redirect('reset_hasla')
    return render_template('zapomniane.html', info=message.forgotten_info())

@app.route('/reset_hasla', methods=['GET','POST'])
def reset_hasla():
    if not 'forgot_code_id' in session:
        return redirect('/logowanie')
    if request.method == "POST":
        writecode = request.form.get('reset_code')
        code = session['forgot_code_id']
        password = request.form.get('new_password')
        if 'forgot_user_id' in session:
            uid = session['forgot_user_id']
            if code == writecode:
                if not fun_base.change_password(uid,password):
                    session['pass_change_fail'] = '1'
                    session['pass_change_fail_type'] = 'reset'
                    return redirect('/blad_zmiany_hasla')
        else:
            return redirect('/koniec_resetu_hasla')
    return render_template('reset.html', info=message.reset_info())

@app.route('/koniec_resetu_hasla')
def koniec_resetu_hasla():
    if not 'forgot_code_id' in session:
        return redirect('/logowanie')
    session.pop('forgot_code_id', None)
    session.pop('forgot_user_id', None)
    return render_template('koniec_resetu_hasla.html', info=message.after_reset_password())

@app.route('/anulowanie_resetu_hasla')
def anulowanie_resetu_hasla():
    session.pop('forgot_code_id', None)
    session.pop('forgot_user_id', None)
    return redirect('/logowanie')

@app.route('/zalogowany', methods=['GET','POST'])
def zalogowany():
    if 'activate_user_id' in session:
        return redirect('/aktywacja_konta')
    if not 'log_in_user_id' in session:
        return redirect('/logowanie')
    if request.method == "POST":
        poll_id = request.form.get('choose_poll')
        session['poll_id'] = poll_id
        return redirect('/glosuj')
    full_name = fun_base.get_full_name(session['log_in_user_id'])
    if fun_base.if_admin(session['log_in_user_id']):
        user_type = 0
        session['log_in_admin'] = 'admin'
    elif fun_base.if_editor(session['log_in_user_id']):
        user_type = 2
        session['log_in_editor'] = 'editor'
    else:
        user_type = 1
    return render_template('zalogowany.html', info=message.user_page(), name=full_name, user_type=user_type, polls=fun_base.polls_for_user_to_vote(session['log_in_user_id']))

@app.route('/aktywacja_konta', methods=['GET','POST'])
def aktywacja_konta():
    if not 'activate_user_id' in session:
        return redirect('/zalogowany')
    if request.method == "POST":
        code = request.form.get('act_code')
        if fun_base.activate_user(session['activate_user_id'], code):
            session['activate_success'] = 'Success'
            return redirect('/udana_aktywacja')
        else:
            session['activate_fail'] = 'Fail'
            return redirect('/blad_aktywacji_konta')
    return render_template('aktywacja.html', info=message.activate_info())

@app.route('/udana_aktywacja')
def udana_aktywacja():
    if not 'activate_success' in session:
        return redirect('/zalogowany')
    session['log_in_user_id'] = session['activate_user_id']
    session.pop('activate_user_id', None)
    session.pop('activate_success', None)
    return render_template('potwierdzenie.html', info=message.activate_user_success(), site_type='aktywacja')

@app.route('/blad_aktywacji_konta')
def blad_aktywacji_konta():
    if not 'activate_fail' in session:
        return redirect('/zalogowany')
    session.pop('activate_user_id', None)
    session.pop('activate_fail', None)
    return render_template('blad.html', info=message.activate_user_fail(), site_type='aktywacja')

@app.route('/wyloguj')
def wyloguj():
    session.pop('log_in_user_id', None)
    session.pop('activate_user_id', None)
    return redirect('/strona_startowa')

@app.route('/zmien_haslo', methods=['GET','POST'])
def zmien_haslo():
    if not 'log_in_user_id' in session:
        return redirect('/logowanie')
    if request.method == "POST":
        previous_password = request.form.get('previous_password')
        new_password = request.form.get('new_password')
        if fun_base.if_password(session['log_in_user_id'],previous_password):
            if not fun_base.change_password(session['log_in_user_id'],new_password):
                session['pass_change_fail'] = '1'
                session['pass_change_fail_type'] = 'zmiana'
                return redirect('/blad_zmiany_hasla')
            else:
                session['pass_change_success'] = 'zmiana'
                return redirect('/poprawna_zmiana_hasla')
        else:
            session['pass_change_fail'] = '0'
            session['pass_change_fail_type'] = 'change'
            return redirect('/blad_zmiany_hasla')
    return render_template('zmiana_hasla.html', info=message.change_password_info())

@app.route('/poprawna_zmiana_hasla')
def poprawna_zmiana_hasla():
    if not 'pass_change_success' in session:
        return redirect('/zmien_haslo')
    session.pop('pass_change_success', None)
    return render_template('potwierdzenie.html', info=message.change_password_success(), site_type='zmien_haslo')

@app.route('/blad_zmiany_hasla')
def blad_zmiany_hasla():
    if not 'pass_change_fail' in session:
        return redirect('/zmien_haslo')
    info = message.change_password_fail(int(session['pass_change_fail']))
    change_type = session['pass_change_fail_type']
    session.pop('pass_change_fail', None)
    session.pop('pass_change_fail_type', None)
    return render_template('blad.html', info=info, site_type='zmien_haslo', change_type=change_type)

@app.route('/wybierz_uzytkownika', methods=['GET','POST'])
def wybierz_uzytkownika():
    if not 'log_in_admin' in session:
        return redirect('/zalogowany')
    if request.method == "POST":
        if 'edit_pid' in request.form:
            session['edit_pid'] = request.form.get('edit_pid')
            return redirect('/edytuj_uzytkownika')
        elif 'delete_pid' in request.form:
            session['delete_pid'] = request.form.get('delete_pid')
            return redirect('/usun_uzytkownika')
        elif 'template' in request.form:
            search_data = request.form.get('template')
            users = fun_base.get_email_and_username_for_edit_user(search_data)
    else:
        users = fun_base.get_email_and_username_for_edit_user()
    return render_template('wyszukiwarka.html', users=users)

@app.route('/edytuj_uzytkownika', methods=['GET','POST'])
def edytuj_uzytkownika():
    if not 'edit_pid' in session:
        return redirect('/zalogowany')
    data = fun_base.get_full_info_user(session['edit_pid'])
    if request.method == "POST":
        changed = 0
        name = request.form.get('user_name')
        if name == '':
            name = data[0]
        else:
            changed = 1
        surname = request.form.get('user_surname')
        if surname == '':
            surname = data[1]
        else:
            changed = 1
        role = request.form.get('role')
        if role == '':
            if data[6] is None:
                role = "Nie"
            else:
                role = data[6]
        else:
            changed = 1
        sex = request.form.get('user_sex')
        if sex == '':
            sex = data[2]
        else:
            changed = 1
        year = request.form.get('user_year')
        if year == '':
            year = data[3]
        else:
            changed = 1
        fun_base.update_user(session['edit_pid'], name, surname, role, sex, year, changed)
        session.pop('edit_pid', None)
        return redirect('/wybierz_uzytkownika')
    return render_template('edycja.html', data=data, info=message.edit_user())

@app.route('/anuluj_edycje_uzytkownika')
def anuluj_edycje_uzytkownika():
    session.pop('edit_pid', None)
    return redirect('/wybierz_uzytkownika')

@app.route('/usun_uzytkownika', methods=['GET','POST'])
def usun_uzytkownika():
    if not 'delete_pid' in session:
        return redirect('/zalogowany')
    if request.method == "POST":
        fun_base.delete_user(session['delete_pid'])
        session.pop('delete_pid', None)
        return redirect('/wybierz_uzytkownika')
    data = fun_base.get_full_info_user(session['delete_pid'])
    return render_template('usuniecie.html', data=data, info=message.delete_user())

@app.route('/anuluj_usuniecie_uzytkownika')
def anuluj_usuniecie_uzytkownika():
    session.pop('delete_pid', None)
    return redirect('/wybierz_uzytkownika')

@app.route('/informacje_o_systemie')
def informacje_o_systemie():
    if not 'log_in_admin' in session:
        return redirect('/zalogowany')
    return render_template('informacje.html', info=message.system_info())

@app.route('/usun_nieaktywnych')
def usun_nieaktywnych():
    if not 'log_in_admin' in session:
        return redirect('/zalogowany')
    fun_base.delete_serially_user()
    return redirect('/informacje_o_systemie')

@app.route('/utworz_glosowanie', methods=['GET','POST'])
def utworz_glosowanie():
    if not ('log_in_admin' in session or 'log_in_editor' in session):
        return redirect('/zalogowany')
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('more')
        poll_type = request.form.get('type')
        start_date = request.form.get('start_date')
        start_time = request.form.get('start_time')
        end_date = request.form.get('finish_date')
        end_time = request.form.get('finish_time')
        start = fun.str_for_date_and_time(start_date, start_time, False)
        end = fun.str_for_date_and_time(end_date, end_time, True)
        session['edit_poll_id'] = fun_base.create_poll(title, description, poll_type, start, end, int(session['log_in_user_id']))
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('tworzenie_glosowania.html')

@app.route('/zarzadzaj_glosowaniem', methods=['GET','POST'])
def zarzadzaj_glosowaniem():
    if not 'edit_poll_id' in session:
        return redirect('/glosowanie_do_edycji')
    if request.method == "POST":
        if 'edit_question_id' in request.form:
            session['edit_question_id'] = request.form.get('edit_question_id')
            return redirect('/edytuj_pytanie')
        elif 'delete_question_id' in request.form:
            session['delete_question_id'] = request.form.get('delete_question_id')
            return redirect('/usun_pytanie')
        elif 'edit_answer_id' in request.form:
            session['edit_answer_id'] = request.form.get('edit_answer_id')
            session['edit_answer_question_id'] = request.form.get('edit_answer_question_id')
            return redirect('/edytuj_odpowiedz')
        elif 'delete_answer_id' in request.form:
            session['delete_answer_id'] = request.form.get('delete_answer_id')
            return redirect('/usun_odpowiedz')
        elif 'question_id_for_add_answer' in request.form:
            session['question_id_for_add_answer'] = request.form.get('question_id_for_add_answer')
            return redirect('/dodaj_odpowiedz')
    return render_template('edytowanie_glosowania.html', questions=fun_base.get_all_question_with_answers_for_poll(session['edit_poll_id']), data=fun_base.get_poll_full_info(session['edit_poll_id']))

@app.route('/zakonczenie_edycji_glosowania')
def zakonczenie_edycji_glosowania():
    session.pop('edit_poll_id', None)
    return redirect('/zalogowany')

@app.route('/zarzadzaj_uczestnikami', methods=['GET','POST'])
def zarzadzaj_uczestnikami():
    if not 'edit_poll_id' in session:
        return redirect('/zalogowany') #zmienić
    if request.method == "POST":
        if 'edit_pid' in request.form:
            add_pid_for_poll = request.form.get('edit_pid')
            fun_base.add_user_for_poll(add_pid_for_poll,session['edit_poll_id'])
            users = fun_base.get_full_name_for_add_to_poll()
        elif 'delete_pid' in request.form:
            delete_pid_from_poll = request.form.get('delete_pid')
            fun_base.delete_user_from_poll(delete_pid_from_poll,session['edit_poll_id'])
            users = fun_base.get_full_name_for_add_to_poll()
        elif 'template' in request.form:
            search_data = request.form.get('template')
            users = fun_base.get_full_name_for_add_to_poll(search_data)
    else:
        users = fun_base.get_full_name_for_add_to_poll()
    return render_template('dodawanie_uczestnikow.html', users=users, added_users=fun_base.added_user_to_poll(session['edit_poll_id']),poll_id=fun_base.get_poll_name(session['edit_poll_id']))

@app.route('/wybierz_grupe', methods=['GET','POST'])
def wybierz_grupe():
    if not 'edit_poll_id' in session:
        return redirect('/glosowanie_do_edycji')
    if request.method == "POST":
        if 'edit_pid' in request.form:
            session['copy_group_id'] = request.form.get('edit_pid')
            return redirect('/kopiuj_grupe')
    return render_template('kopiuj_grupy.html', info=message.group_copy(), groups=fun_base.get_group_for_select(session['edit_poll_id']))

@app.route('/kopiuj_grupe', methods=['GET','POST'])
def kopiuj_grupe():
    if not 'copy_group_id' in session:
        return redirect('/zarzadzaj_uczestnikami')
    if request.method == "POST":
        count = fun_base.copy_users_from_another_group(session['copy_group_id'], session['edit_poll_id'])
        session['copy_count'] = count
        session.pop('copy_group_id', None)
        return redirect('/potwierdzenie_kopiowania_grupy')
    return render_template('kopiuj_grupy_potwierdz.html', glosowanie=fun_base.get_poll_name(session['edit_poll_id']), users=fun_base.get_users_full_name_from_group(session['copy_group_id']))

@app.route('/potwierdzenie_kopiowania_grupy')
def potwierdzenie_kopiowania_grupy():
     if not 'copy_count' in session:
        return redirect('/zarzadzaj_uczestnikami')
     info = message.copy_users_info(session['copy_count'])
     session.pop('copy_count', None)
     return render_template('potwierdzenie.html', info=info, site_type='kopiowanie_grupy')

@app.route('/anuluj_kopiowanie_grupy')
def anuluj_kopiowanie_grupy():
    session.pop('copy_group_id', None)
    return redirect('/wybierz_grupe')

@app.route('/glosowanie_do_edycji', methods=['GET','POST'])
def glosowanie_do_edycji():
    if not ('log_in_admin' in session or 'log_in_editor' in session):
        return redirect('/zalogowany')
    if request.method == "POST":
        if 'edit_id' in request.form:
            session['edit_poll_id'] = request.form.get('edit_id')
            return redirect('/zarzadzaj_glosowaniem')
        elif 'template' in request.form:
            search_data = request.form.get('template')
            polls = fun_base.get_polls_for_edit(session['log_in_user_id'], search_data)
    else:
        polls = fun_base.get_polls_for_edit(session['log_in_user_id'])
    return render_template('wybor_glosowania.html', polls=polls)

@app.route('/dodaj_pytanie', methods=['GET','POST'])
def dodaj_pytanie():
    if not 'edit_poll_id' in session:
        return redirect('/glosowanie_do_edycji')
    if request.method == "POST":
        question = request.form.get('question')
        fun_base.add_question(session['edit_poll_id'], question)
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('dodawanie_pytania.html', nazwa=fun_base.get_poll_name(session['edit_poll_id']))

@app.route('/dodaj_odpowiedz', methods=['GET','POST'])
def dodaj_odpowiedz():
    if not 'question_id_for_add_answer' in session:
        return redirect('/edytuj_glosowanie')
    if request.method == "POST":
        answer = request.form.get('answer')
        fun_base.add_answer(session['question_id_for_add_answer'], answer, session['edit_poll_id'])
        session.pop('question_id_for_add_answer', None)
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('dodawanie_odpowiedzi.html', nazwa=fun_base.get_question_name(session['question_id_for_add_answer']))

@app.route('/edytuj_pytanie', methods=['GET','POST'])
def edytuj_pytanie():
    if not 'edit_question_id' in session:
        return redirect('/edytuj_glosowanie')
    if request.method == "POST":
        question = request.form.get('question')
        fun_base.edit_question(session['edit_question_id'], question)
        session.pop('edit_question_id', None)
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('edycja_pytania_odpowiedzi.html', czy_pytanie=True, pytanie=fun_base.get_question_name(session['edit_question_id']))

@app.route('/edytuj_odpowiedz', methods=['GET','POST'])
def edytuj_odpowiedz():
    if not 'edit_answer_id' in session:
        return redirect('/edytuj_glosowanie')
    if request.method == "POST":
        answer = request.form.get('question')
        fun_base.edit_answer(session['edit_answer_id'], answer)
        session.pop('edit_answer_id', None)
        session.pop('edit_answer_question_id', None)
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('edycja_pytania_odpowiedzi.html', czy_pytanie=False, pytanie=fun_base.get_question_name(session['edit_answer_question_id']), odpowiedz=fun_base.get_answer_name(session['edit_answer_id']))

@app.route('/edytuj_dane_glosowania')
def edytuj_dane_glosowania():
    return "Edytuj dane głosowania " + str(session['edit_poll_id'])

@app.route('/usun_pytanie')
def usun_pytanie():
    return "Usuń pytanie " + str(session['delete_question_id'])

@app.route('/usun_odpowiedz')
def usun_odpowiedz():
    return "Usuń odpowiedź " + str(session['delete_answer_id'])

@app.route('/tmp', methods=['GET','POST'])
def tmp():
    #return "tmp"
    return render_template('edytowanie_glosowania.html')
    



@app.route('/glosuj') #tmp
def glosuj(): #tmp
    return "Głosowanie " + session['poll_id'] #tmp

@app.route('/sledz_glosowanie') #tmp
def sledz_glosowanie(): #tmp
    return "Śledź głosowanie" #tmp

@app.route('/usun_glosowanie') #tmp
def usun_glosowanie(): #tmp
    return "Usuń głosowanie" #tmp

@app.route('/wyniki_glosowania') #tmp
def wyniki_glosowania(): #tmp
    return "Wyniki głosowania" #tmp

#przekierowanie, gdy adres URL nie istnieje
@app.errorhandler(404)
def strona_nie_istnieje(e):
    return redirect('/strona_startowa')
