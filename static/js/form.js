const addMoreBtn = document.getElementById("add-form");
const removeBtn = document.getElementById("remove-form");
const totalNewForms = document.getElementById("id_sig-TOTAL_FORMS");
const formCounter = document.getElementById("form-counter")

formCounter.setAttribute('value', totalNewForms.value)

addMoreBtn.addEventListener('click', function () {
    this.previousElementSibling.stepUp();
    add_new_form("signatories", "signatory", "sig", totalNewForms, "empty-form", 30)
});
removeBtn.addEventListener('click', function () {
    this.nextElementSibling.stepDown();
    remove_form("signatories", "signatory", "sig", totalNewForms, 2)
});

function add_new_form(container, element, prefix, forms, template, max) {
    const currentForms = document.getElementsByClassName(element);
    const currentFormCount = currentForms.length;
    if (currentFormCount >= max) {
        return false;
    }

    const formCopyTarger = document.getElementById(container);
    const copyEmptyFormEl = document.getElementById(template).cloneNode(true);
    copyEmptyFormEl.setAttribute('class', element);
    copyEmptyFormEl.setAttribute('id', `${prefix}-${currentFormCount}`);

    const regex = new RegExp('__prefix__', 'g');
    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, currentFormCount);
    forms.setAttribute('value', currentFormCount + 1);
    formCopyTarger.append(copyEmptyFormEl);
    document.getElementById(`${element}-index-${currentFormCount}`).innerHTML = currentFormCount + 1;
}

function remove_form(container, element, prefix, forms, min) {
    if (event) {
        event.preventDefault();
    }
    const currentForms = document.getElementsByClassName(element);
    const currentFormCount = currentForms.length;
    if (currentFormCount <= min) {
        return false;
    }

    $(`#${container} #${prefix}-${currentFormCount - 1}:last`).remove();
    forms.setAttribute('value', currentFormCount - 1);

}

const honoredGuestsYes = document.getElementById('honoredGuestsYes');
const honoredGuestsNo = document.getElementById('honoredGuestsNo');

const addMoreGuestBtn = document.getElementById("add-guest");
const removeGuestBtn = document.getElementById("remove-guest");

const guestCounter = document.getElementById("guests-counter");

const totalNewGuestsForms = document.getElementById("id_guests-TOTAL_FORMS");
totalNewGuestsForms.setAttribute('value', 0);


addMoreGuestBtn.addEventListener("click", function () {
    this.previousElementSibling.stepUp();
    add_new_form("honoredGuests", "honoredGuest", "guest", totalNewGuestsForms, "empty-form-guest", 10)
})
removeGuestBtn.addEventListener("click", function () {
    this.nextElementSibling.stepDown();
    remove_form("honoredGuests", "honoredGuest", "guest", totalNewGuestsForms, 0)
})

function checkhonoredGuestsYes() {
    if (honoredGuestsYes.checked == true) {
        honoredGuestsYes.disabled = true;
        honoredGuestsForm = document.getElementById('honoredGuestsForm');
        honoredGuestsForm.setAttribute('class', 'form-row');
    }
}

function checkhonoredGuestsNo() {
    if (honoredGuestsNo.checked == true) {
        honoredGuestsYes.disabled = false;
        honoredGuestsForm = document.getElementById('honoredGuestsForm');
        for (var i = 0; i < 10; i++) {
            guestCounter.stepDown();
        }
        honoredGuestsForm.setAttribute('class', 'form-row hidden');
        document.getElementById('honoredGuests').innerHTML = '';
        totalNewGuestsForms.setAttribute('value', 0);
    }
}



function checkWordToTheParticipantsYes()//Функция наличия слово учатникам
{

    var checkboxParticipants = document.getElementById("wordToTheParticipantsYes");
    const numberParticipants = document.getElementById("participants");

    if (checkboxParticipants.checked == true) {
        checkboxParticipants.disabled = true;
        document.getElementById("participantsTrue").setAttribute("class", "");

        const select = getSelect();
        const participantDiv = document.createElement('div'); // Создание обертки для элементов
        participantDiv.id = 'participant1';
        participantDiv.innerHTML =
            '<hr> <h2>Участник 1</h2>' +
            '<p>Фамилия, имя, отчество:</p><br>';
        participantDiv.appendChild(select); // Добавление элемента <select> в обертку

        // Добавление оберток в основной контейнер
        numberParticipants.appendChild(participantDiv);
    }

}
function checkWordToTheParticipantsNo()//Функция отсутствия слово учатникам
{
    var checkboxParticipantsYes = document.getElementById("wordToTheParticipantsYes");
    var checkboxParticipantsNo = document.getElementById("wordToTheParticipantsNo");
    if (checkboxParticipantsNo.checked == true) {
        checkboxParticipantsYes.disabled = false;
    }
    var removeParticipants = document.getElementById("participantsTrue");
    var listParticipants = document.getElementById("participants");

    removeParticipants.setAttribute("class", "hidden")
    listParticipants.innerHTML = '';

}

function checkAdditionalSpeakerYes() {
    var checkboxAdditionalSpeaker = document.getElementById("additionalSpeakerYes");
    if (checkboxAdditionalSpeaker.checked == true) {
        checkAdditionalSpeakerYes.disabled = true;
        var participant1 = document.getElementById('participant1');
        const participantDiv = document.createElement('div');
        participantDiv.innerHTML =
            '<hr> <h2>Участник 1 (<i>Дополнительный спикер</i>)</h2>' +
            '<p><span style="color: red">*</span> Фамилия, имя, отчество:</p><br>' +
            '<textarea rows="1"  class = "form-application" cols="100" placeholder="Введите текст" required ></textarea> <br>' +
            '<p><span style="color: red">*</span> Должность с указанием организации:</p><br>' +
            '<textarea rows="1"  class = "form-application" cols="100" placeholder="Введите текст" required ></textarea> <br>';
        participant1.innerHTML = participantDiv.innerHTML;
    }
}

function checkAdditionalSpeakerNo() {
    var checkboxAdditionalSpeakerYes = document.getElementById("additionalSpeakerYes");
    var checkboxAdditionalSpeakerNo = document.getElementById("additionalSpeakerNo");
    if (checkboxAdditionalSpeakerNo.checked == true) {
        checkboxAdditionalSpeakerYes.disabled = false;
    }
    var participant1 = document.getElementById('participant1');
    const select = getSelect();
    const participantDiv = document.createElement('div');
    participantDiv.id = 'participant1';
    participantDiv.innerHTML =
        '<hr> <h2>Участник 1</h2>' +
        '<p>Фамилия, имя, отчество:</p><br>';
    participantDiv.appendChild(select); // Добавление элемента <select> в обертку
    participant1.innerHTML = participantDiv.innerHTML;
}

function getSelect() {
    const select = document.createElement('select'); // Создание элемента <select>
    select.className = "form-application"; // Присвоение класса

    var countSigning = totalNewForms.value;


    for (i = 0; i < countSigning; i++) {
        console.log("id_sig-" + i + "-signatory_surname");
        const lastnameSigning = document.getElementById("id_sig-" + i + "-signatory_surname").value;
        const nameSigning = document.getElementById("id_sig-" + i + "-signatory_name").value;
        const middleNameSigning = document.getElementById("id_sig-" + i + "-signatory_middlename").value;

        const option = document.createElement('option'); // Создание элемента <option>
        option.setAttribute('value', i);
        if (middleNameSigning == "-" || middleNameSigning == "_") {
            fioSigning = lastnameSigning + " " + nameSigning;
        } else {
            fioSigning = lastnameSigning + " " + nameSigning + " " + middleNameSigning;
        }
        option.textContent = fioSigning; // Присвоение текста элементу <option>
        select.appendChild(option); // Добавление элемента <option> в элемент <select>
    }
    return select;
}

