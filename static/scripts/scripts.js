var lata = document.getElementById('lata');
if (typeof (lata) != 'undefined' && lata != null) {
    var podaj = "Podaj datę urodzenia";
    var x = "", i;
    var data = new Date();
    x = x + "<select id=\"user_year\" name=\"user_year\" class=\"formField\">";
    x = x + "<option selected></option>"
    for (i = 1901; i <= data.getFullYear(); i++) {
        x = x + "<option value=\"" + i + "\">" + i + "</option>"
    }
    x = x + "</select>"
    document.getElementById("lata").innerHTML = x;
}


function checkPassword(registerForm) {
    password1 = registerForm.new_password.value;
    password2 = registerForm.new_password_repeat.value;


    if (password1 != password2) {
        alert("\nPodane hasła nie są identyczne!")
        return false;
    }
    if (registerForm.user_year.value != 'undefined' && lata != null)
        birthyear = registerForm.user_year.value;
    if (birthyear.length == 0) {
        alert("\nPodaj rok urodzenia!")
        return false;
    }
}

var calculateComplexity = function (password) {
    var complexity = 0;
    var regExps = [
        /[a-z]/,
        /[A-Z]/,
        /[0-9]/,
        /.{8}/,
        /[!-//:-@[-`{-ÿ]/
    ];
    regExps.forEach(function (regexp) {
        if (regexp.test(password)) {
            complexity++;
        }
    });
    return {
        value: complexity,
        max: regExps.length
    };
};
var checkPasswordStregth = function (password) {
    var progress = document.querySelector('#passwordComplexity'),
        complexity = calculateComplexity(this.value);
    progress.value = complexity.value;
    progress.max = complexity.max;
};

var input = document.querySelector('#new_password');
if (typeof (input) != 'undefined' && input != null)
    input.addEventListener('keyup', checkPasswordStregth);

function checkDates() {
    let startDate = new Date(document.getElementById("start_date").value)
    let finishDate = new Date(document.getElementById("finish_date").value)
    let formStartTime = document.getElementById("start_time").value
    let formFinishTime = document.getElementById("finish_time").value
    let startTimeHour = formStartTime[0].concat(formStartTime[1])
    let startTimeMinute = formStartTime[3].concat(formStartTime[4])
    let finishTimeHour = formFinishTime[0].concat(formFinishTime[1])
    let finishTimeMinute = formFinishTime[3].concat(formFinishTime[4])
    startDate.setHours(parseInt(startTimeHour))
    startDate.setMinutes(parseInt(startTimeMinute))
    finishDate.setHours(parseInt(finishTimeHour))
    finishDate.setMinutes(parseInt(finishTimeMinute))
    let now = new Date();
    if (startDate > finishDate) {
        alert("\nPodane daty rozpoczęcia i zakończenia głosowania są nieprawidłowe!")
        return false
    }
    if (startDate < now) {
        alert("\nPodane daty rozpoczęcia i zakończenia głosowania są nieprawidłowe!")
        return false
    }
    if (finishDate - startDate < 300000) {
        alert("\nMinimalny czas trwania głosowania wynosi 5 minut!")
        return false
    }
    if (startDate - now < 600000) {
        alert("\nMinimalny czas startu głosowania od teraz to 10 minut!")
        return false
    }

}
