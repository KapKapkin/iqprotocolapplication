function AddSigningParty()//Функция добавления подписанта
{
  var quantity = document.getElementById("quantityOfPartiesSigningTheDocument").value;
  const newDiv = document.getElementById("clients");
  if (quantity < 30) {
    quantity = parseInt(quantity) + 1;
    newDiv.innerHTML +=
      '<div  id = ' + 'client' + quantity + '>'
      + '<h2 style="font-style:italic;">Сторона подписания ' + quantity + '</h2>'
      + '<p><span style="color: red">*</span> Полное наименование стороны (организации) – участника подписания соглашения:</p> <br>'
      + '<textarea rows="1"  class = "form-application" name = "nameOrganizationSide' + quantity + '" id = "nameOrganizationSide' + quantity + '"placeholder="Введите текст" required ></textarea> <br> '
      + '<p><span style="color: red">*</span> Должность подписанта:</p><br>'
      + '<textarea rows="1"  class = "form-application" name = "postSide1' + quantity + '" id = "postSide1' + quantity + '"placeholder="Введите текст" required ></textarea> <br>'
      + '<p><span style="color: red">*</span> Форма обращения:</p> <br>'
      + '<div class="gender">'
      + '<div ><input  type="radio"  name = "genderSide' + quantity + '" id = "genderSide' + quantity + '"required> Господин </div>'
      + '<div ><input type="radio"  name = "genderSide' + quantity + '" id = "genderSide' + quantity + '"required>Госпожа </div> </div> <br>'
      + '<p><span style="color: red">*</span> Фамилия:</p> <br>'
      + '<textarea rows="1"   class = "form-application" name = "lastname' + quantity + '" id = "lastname' + quantity + '"placeholder="Введите текст" required ></textarea> <br>'
      + '<p><span style="color: red">*</span> Имя:</p> <br>'
      + '<textarea rows="1"  class = "form-application" name = "name' + quantity + '" id = "name' + quantity + '"placeholder="Введите текст" required ></textarea> <br>'
      + '<p><span style="color: red">*</span> Отчество:</p> <br>'
      + '<textarea   class = "form-application" name = "middleName' + quantity + '" id = "middleName' + quantity + '"placeholder="В целях соблюдения протокола требуется обращаться к участникам церемонии в формате &laquo;имя отчество&raquo;. Если у подписанта отсутствует отчество, поставьте прочерк." required ></textarea> <br>'
      + '<p><span style="color: red">*</span> Написание <b>имени и фамилии</b> подписанта на английском языке:</p><br>'
      + '<textarea rows="1"  class = "form-application" name = "nameEnglishSide' + quantity + '" id = "nameEnglishSide' + quantity + '"placeholder="Введите текст" required ></textarea> <br>'
      + '<hr> </div> ';
  }
}


function MinSigningParty()//Функция удаления подписанта
{

  var quantity = document.getElementById("quantityOfPartiesSigningTheDocument").value;
  let quantity1 = parseInt(quantity, 10) + 1;
  const removeDiv = document.getElementById("client" + quantity1.toString());
  removeDiv.remove();

}


function checkhonoredGuestsYes()//Функция наличия почётных гостей
{

  var radioButton = document.getElementById("honoredGuestsYes");

  const numberHonoredGuests = document.getElementById("checkedHonoredGuestsTrue");
  if (radioButton.checked == true) {
    radioButton.disabled = true;
    numberHonoredGuests.innerHTML +=
      '<div id = "guestsTrue">'
      + '<p><span style="color: red">*</span>  Формат участия почетных гостей</p><br>'
      + '<div>'
      + '<input  type="radio"  name = "participationFormat"  id = "participationFormat1" required >Приглашаются вместе с подписантами. Во время церемонии стоят за спинами подписантов<br>'
      + '<input type="radio"  name = "participationFormat"  id = "participationFormat2" required >Присутствуют в зале, представляются модератором, но не выходят на сцену '
      + '</div> <br>'
      + '<p><b>Количество почетных гостей</b></p><br>'
      + '<button type="button" onclick="this.nextElementSibling.stepDown(); MinHonoredGuests();">-</button>'
      + '<input type="number" min="1" max="10" value="1" readonly class="raz" name = "quantityHonoredGuests" id = "quantityHonoredGuests">'
      + '<button type="button" onclick="AddHonoredGuests(); this.previousElementSibling.stepUp();">+</button></div>'
      + '<div id = guest1>'
      + '<hr ><h2 style="font-style:italic;">Почётный гость 1</h2>'
      + '<p><span style="color: red">*</span> Фамилия, имя, отчество почетного гостя:</p><br>'
      + '<textarea rows="1"  class = "form-application" name = "FIOGuest1" id = "FIOGuest1" placeholder="Введите текст" required ></textarea> <br>'
      + '<p> <span style="color: red">*</span> Должность почетного гостя с указанием организации: </p> <br>'
      + '<textarea rows="1"  class = "form-application" name = "postGuest1" id = "postGuest1" placeholder="Введите текст" required ></textarea> <br>'
      + '</div> ';

  }


}



function checkhonoredGuestsNo()//Функция отсутствия почётных гостей
{
  var radioButton = document.getElementById("honoredGuestsYes");
  var radioButtonNo = document.getElementById("honoredGuestsNo");
  if (radioButtonNo.checked == true) {

    radioButton.disabled = false;
  }
  var removeGuests = document.getElementById("guestsTrue");
  removeGuests.remove();
  for (i = 1; i < 11; i++) {
    const deleteNumberHonoredGuests = document.getElementById("guest" + i);
    deleteNumberHonoredGuests.remove();
  }
}

function AddHonoredGuests()//Функция добавления гостя
{
  var quantity = document.getElementById("quantityHonoredGuests").value;

  const numberHonoredGuests = document.getElementById("NumberHonoredGuests");

  if (quantity < 10) {
    quantity = parseInt(quantity) + 1;
    numberHonoredGuests.innerHTML +=
      '<div id = ' + 'guest' + quantity + '>'
      + '<hr><h2 style="font-style:italic;">Почётный гость ' + quantity + '</h2>'
      + '<p><span style="color: red">*</span> Фамилия, имя, отчество почетного гостя:</p><br>'
      + '<textarea rows="1"  class = "form-application" name = "FIOGuest' + quantity + '" id = "FIOGuest' + quantity + '" placeholder="Введите текст" required ></textarea> <br>'
      + '<p><span style="color: red">*</span> Должность почетного гостя с указанием организации:</p> <br>'
      + '<textarea rows="1"  class = "form-application" name = "postGuest' + quantity + '" id = "postGuest' + quantity + '" placeholder="Введите текст" required ></textarea> <br>'
      + '</div>';
  }
}
function MinHonoredGuests()//Функция удвления гостя
{
  var quantity = document.getElementById("quantityHonoredGuests").value;
  let quantity1 = parseInt(quantity, 10) + 1;
  const removeDivGuest = document.getElementById("guest" + quantity1.toString());
  removeDivGuest.remove();

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
    numberParticipants.appendChild(participantsDiv);
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
  removeParticipants.remove();
  for (i = 1; i < 11; i++) {
    const deleteNumberParticipants = document.getElementById("participant" + i);
    deleteNumberParticipants.remove();
  }
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

  var countSigning = document.getElementById("form-counter").value;
  console.log(countSigning);

  for (i = 1; i <= countSigning; i++) {
    const lastnameSigning = document.getElementById("lastname" + i).value;
    const nameSigning = document.getElementById("name" + i).value;
    const middleNameSigning = document.getElementById("middleName" + i).value;

    const option = document.createElement('option'); // Создание элемента <option>
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





function AddParticipants()//Функция добавления участника
{


  var quantity = document.getElementById("quantityParticipants").value;
  const numberHonoredGuests = document.getElementById("participants");
  var countSigning = document.getElementById("quantityOfPartiesSigningTheDocument").value;
  if (quantity < 10) {
    quantity = parseInt(quantity) + 1;
    const select = document.createElement('select'); // Создание элемента <select>
    select.className = "form-application"; // Присвоение класса

    for (i = 1; i <= countSigning; i++) {
      const lastnameSigning = document.getElementById("lastname" + i).value;
      const nameSigning = document.getElementById("name" + i).value;
      const middleNameSigning = document.getElementById("middleName" + i).value;

      const option = document.createElement('option'); // Создание элемента <option>
      if (middleNameSigning == "-" || middleNameSigning == "_") {
        fioSigning = lastnameSigning + " " + nameSigning;
        option.textContent = fioSigning; // Присвоение текста элементу <option>
        alert(fioSigning);
      } else {
        fioSigning = lastnameSigning + " " + nameSigning + " " + middleNameSigning;
        option.textContent = fioSigning; // Присвоение текста элементу <option>
      }
      select.appendChild(option); // Добавление элемента <option> в элемент <select>
    }

    const participantDiv = document.createElement('div'); // Создание обертки для элементов
    participantDiv.id = 'participant' + quantity;
    participantDiv.innerHTML =
      '<hr> <h2>Участник ' + quantity + '</h2>' +
      '<p>Фамилия, имя, отчество:</p><br>';
    participantDiv.appendChild(select); // Добавление элемента <select> в обертку

    numberHonoredGuests.appendChild(participantDiv); // Добавление обертки в основной контейнер

  }
}
function MinParticipants()//Функция удвления участника
{
  var quantity = document.getElementById("quantityParticipants").value;
  let quantity1 = parseInt(quantity, 10) + 1;
  const removeDivParticipant = document.getElementById("participant" + quantity1.toString());
  removeDivParticipant.remove();

}




function AddOnlineParticipant()//Функция добавления удалённого участника
{
  var checkboxFormatOnline = document.getElementById("formatOnline");
  const numberHonoredGuests = document.getElementById("OnlineParticipant");
  if (checkboxFormatOnline.checked == true) {
    checkboxFormatOnline.disabled = true;
    numberHonoredGuests.innerHTML +=
      '<div id = "Online">'
      + '<h2 style="margin-bottom: 0; font-style:italic;">Контактные данные представителя, присутствующего на удалённой площадке</h2>'
      + '<p style="color:grey; margin-top: 0; font-size:14px;">С этим лицом будем связываться по вопросам онлайн подключения участника</p> <br>'
      + '<p><span style="color: red">*</span>Фамилия имя отчество (полностью)</p><br>'
      + '<textarea rows="1"  class = "form-application" name = "FioOnlineParticipant" id = "FioOnlineParticipant" placeholder="Введите текст" required ></textarea> <br>'
      + '<p><span style="color: red">*</span>Организация</p><br>'
      + '<textarea rows="1"  class = "form-application" name = "NameOnlineOrganization" id = "NameOnlineOrganization" placeholder="Введите текст" required ></textarea> <br>'
      + '<p><span style="color: red">*</span>Должность</p><br>'
      + '<textarea rows="1"  class = "form-application" name = "PostOnlineParticipant" id = "PostOnlineParticipant" placeholder="Введите текст" required ></textarea> <br>'
      + '<p><span style="color: red">*</span>Мобильный телефон</p><br>'
      + '<textarea rows="1"  class = "form-application" name = "PhoneOnlineParticipant" id = "PhoneOnlineParticipant" placeholder="Введите текст" required ></textarea> <br>'
      + '<p><span style="color: red">*</span>Эл. почта</p><br>'
      + '<textarea rows="1"  class = "form-application" name = "EmailOnlineParticipant" id = "EmailOnlineParticipant" placeholder="Введите текст" required ></textarea> <br>'
      + '</div> ';

  }

}

function RemoveOnlineParticipant()//Функция удаления удалённого участника
{
  var checkboxFormatOnline = document.getElementById("formatOnline");
  var checkboxFormatOffline = document.getElementById("formatOffline");
  if (checkboxFormatOffline.checked == true) {
    checkboxFormatOnline.disabled = false;
    var removeParticipants = document.getElementById("Online");
    removeParticipants.remove();
  }


}


function CoincidenceNo()//Функция добавления представителя
{
  var checkboxCoincidence = document.getElementById("coincidenceNo");
  const numberHonoredGuests = document.getElementById("CoincidenceParticipants");
  if (checkboxCoincidence.checked == true) {
    checkboxCoincidence.disabled = true;
    numberHonoredGuests.innerHTML +=
      '<div id = "Representative">'
      + '<p><span style="color: red">*</span> Фамилия, имя, отчество (полностью):</p> <br>'
      + '<textarea rows="1"  class = "form-application"   name = "nameCoincidence" id = "nameCoincidence"  placeholder="Введите текст" required ></textarea> <br>'
      + '<p><span style="color: red">*</span> Организация:</p> <br>'
      + '<textarea rows="1"  class = "form-application"   name = "OrganizationCoincidence" id = "OrganizationCoincidence"  placeholder="Введите текст" required ></textarea> <br>'
      + '<p><span style="color: red">*</span> Должность:</p> <br>'
      + '<textarea rows="1"  class = "form-application"   name = "PostCoincidence" id = "PostCoincidence"  placeholder="Введите текст" required ></textarea> <br>'
      + '<p><span style="color: red">*</span> Мобильный телефон:</p> <br>'
      + '<textarea rows="1"  class = "form-application"   name = "PhoneCoincidence" id = "PhoneCoincidence"  placeholder="Введите текст" required ></textarea> <br>'
      + '<p><span style="color: red">*</span> Email:</p> <br>'
      + '<textarea rows="1"  class = "form-application"   name = "EmailCoincidence" id = "EmailCoincidence"  placeholder="Введите текст" required ></textarea> <br>'
      + '<hr>'
      + '</div> ';
  }
}

function CoincidenceYes()//Функция удаления представителя
{
  var checkboxCoincidenceNo = document.getElementById("coincidenceNo");
  var checkboxCoincidenceYes = document.getElementById("coincidenceYes");
  if (checkboxCoincidenceYes.checked == true) {
    checkboxCoincidenceNo.disabled = false;
    var removeParticipants = document.getElementById("Representative");
    removeParticipants.remove();
  }


}




//Показать\скрыть пароль
function show_hide_passwordReg(target) {

  var input = document.getElementById('regPassword');
  if (input.getAttribute('type') == 'password') {
    target.classList.add('Eye_Open');
    input.setAttribute('type', 'text');
  } else {
    target.classList.remove('Eye_Open');
    input.setAttribute('type', 'password');
  }

  return false;
}
function show_hide_passwordRepeat(target) {

  var input = document.getElementById('regPasswordRepeat');
  if (input.getAttribute('type') == 'password') {
    target.classList.add('Eye_Open');
    input.setAttribute('type', 'text');
  } else {
    target.classList.remove('Eye_Open');
    input.setAttribute('type', 'password');
  }

  return false;
}
function show_hide_password(target) {

  var input = document.getElementById('loginPassword');
  if (input.getAttribute('type') == 'password') {
    target.classList.add('Eye_Open');
    input.setAttribute('type', 'text');
  } else {
    target.classList.remove('Eye_Open');
    input.setAttribute('type', 'password');
  }

  return false;
}

//переход от формы авторизации к форме регистрации
function showRegistrationFormOpen() {

  document.getElementById("register-form").style.display = "block";
  document.getElementById("login-form").style.display = "none";
  return false;
}
//переход от формы регистрации к форме авторизации
function showAuthorizationFormOpen() {
  document.getElementById("register-form").style.display = "none";
  document.getElementById("login-form").style.display = "block";
  return false;

}