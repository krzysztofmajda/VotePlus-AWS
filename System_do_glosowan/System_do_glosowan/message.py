from System_do_glosowan import app, fun_base

def register_fail(i):
    out = [" ", "Konto o takiej nazwie użytkownika już istnieje!", "Konto o takim adresie e-mail już istnieje!"]
    return out[i]

def register_success():
    out = "Udało Ci się poprawnie zarejestrować, na podany adres e-mail została wysłana wiadomość z potwierdzeniem rejestracji wraz z kodem potrzebnym do aktywacji konta przy pierwszym logowaniu do systemu."
    return out

def log_in_fail():
    out = "Podane dane logowania są nieprawidłowe!"
    return out

def after_reset_password():
    out = "Jeżeli dane w poprzednich krokach zostały podane prawidłowo, Twoje hasło zostało zresetowane."
    return out

def main_page():
    out = [" VotePlus to nasz autorski system do obsługi głosowań.", "Nie wymaga instalacji, gdyż zarządzany jest w całości z poziomu przeglądarki internetowej. Przeprowadzaj głosowania łatwiej niż kiedykolwiek wcześniej oraz prezentuj wyniki na przystępnych wykresach!",
           "Wszystkie pytania prosimy kierować na adres: voteplus.info@gmail.com",
           "Aby oddać głos zaloguj się na swoje konto.",
           "Nie masz konta? Zarejestruj się i korzystaj z pełni funkcjonalności już dziś.",
           "Jesteś już zalogowany. Przejdź do swojego konta lub się wyloguj."]
    return out

def user_page():
    out = ["Tu możesz sprawdzić wyniki i statystyki głosowań.", "Tu możesz utworzyć nowe głosowanie.",
           "Tu możesz edytować ustawienia głosowania, pytania i możliwe odpowiedzi oraz dodawać osoby do głosowania.",
           "Tu możesz na bierząco śledzić przebieg oraz statystyki głosowania.",
           "Tu możesz zmienić swoje hasło do systemu.", "Tu możesz wylogować sie z systemu.",
           "Tu możesz nadać bądź odebrać użytkownikom uprawnienia do funkcjonalności systemu oraz usunąć konta użytkowników.",
           "Tu możesz usunąć głosowanie.", "Tu możesz sprawdzić bierzące informacje o systemie."]
    return out

def change_password_info():
    out = "Rozpoczynasz procedurę zmiany hasła. Aby tego dokonać, wypełnij poniższy formularz."
    return out

def change_password_success():
    out = "Hasło zostało zmienione poprawnie."
    return out

def change_password_fail(i):
    out = ["Błąd zmiany hasła. Obecne hasło podane niepoprawnie.", "Błąd zmiany hasła. Nowe hasło identyczne z obecnym."]
    return out[i]

def reset_info():
    out = "Na swój adres mailowy otrzymałeś/aś wiadomość z kodem umożliwiającym zmianę hasła. Wpisz go poniżej oraz stwórz nowe hasło."
    return out

def forgotten_info():
    out = "Wpisz poniżej adres e-mail przypisany do Twojego konta, a my wyślemy Ci instrukcję resetowania hasła."
    return out

def edit_user():
    out = "W poniższym formularzu uzupełnij tylko te dane, które chcesz edytować."
    return out

def delete_user():
    out = "Czy chcesz trwale usunąć to konto?"
    return out

def activate_info():
    out = "Na wprowadzony przez Ciebie adres e-mail, wysłany został kod aktywacyjny. Aby aktywować swoje konto wpisz go poniżej."
    return out

def activate_user_fail():
    out = "Podany kod aktywacji konta jest nieprawidłowy. Aby ponowić próbę aktywacji, zaloguj się ponownie do systemu."
    return out

def activate_user_success():
    out = "Udało Ci się poprawnie aktywować konto. Możesz teraz w pełni korzystać z funkcjonalności systemu."
    return out

def system_info():
    out = ["Liczba głosowań: " + str(fun_base.count_poll()),
           "W tym głosowań aktywnych: " + str(fun_base.count_active_poll()),
           "Liczba kont użytkowników: " + str(fun_base.count_users()),
           "W tym nieaktywnych kont: " + str(fun_base.count_inactive_users())]
    return out

def group_copy():
    out = "Wybierz grupę, której użytkownicy zostaną dodani do głosowania"
    return out

def copy_users_info(i):
    out = ("Kopiowanie użytkowników zakończone pomyślnie. " + str(i) + " użytkowników zostało dodanych do głosowania.")
    return out