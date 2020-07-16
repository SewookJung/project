const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

function clientSearchFunction() {
  let input = document.getElementById("client-search");
  let filter = input.value.replace(/ /gi, "").toUpperCase();
  let ul = document.getElementById("clientUL");
  let li = ul.getElementsByTagName("li");
  let i, txtValue;

  for (i = 0; i < li.length; i++) {
    txtValue =
      li[i].textContent.replace(/ /gi, "") ||
      li[i].innerText.replace(/ /gi, "");
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "block";
    } else {
      li[i].style.display = "none";
    }
  }
}

function mnfactureSearchFunction() {
  let input = document.getElementById("mnfacture-search");
  let filter = input.value.replace(/ /gi, "").toUpperCase();
  let ul = document.getElementById("mnfactureUL");
  let li = ul.getElementsByTagName("li");
  let i, txtValue;

  for (i = 0; i < li.length; i++) {
    txtValue =
      li[i].textContent.replace(/ /gi, "") ||
      li[i].innerText.replace(/ /gi, "");
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "block";
    } else {
      li[i].style.display = "none";
    }
  }
}

function productSearchFunction() {
  let input = document.getElementById("product-search");
  let filter = input.value.replace(/ /gi, "").toUpperCase();
  let ul = document.getElementById("productUL");
  let li = ul.getElementsByTagName("li");
  let i, txtValue;

  for (i = 0; i < li.length; i++) {
    txtValue =
      li[i].textContent.replace(/ /gi, "") ||
      li[i].innerText.replace(/ /gi, "");
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "block";
    } else {
      li[i].style.display = "none";
    }
  }
}

function productModelSearchFunction() {
  let input = document.getElementById("product-model-search");
  let filter = input.value.replace(/ /gi, "").toUpperCase();
  let ul = document.getElementById("productModelUL");
  let li = ul.getElementsByTagName("li");
  let i, txtValue;

  for (i = 0; i < li.length; i++) {
    txtValue =
      li[i].textContent.replace(/ /gi, "") ||
      li[i].innerText.replace(/ /gi, "");
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "block";
    } else {
      li[i].style.display = "none";
    }
  }
}

function checkDupClient() {
  const clientSearchInput = document.getElementById("client__search-field");
  const txtValue = clientSearchInput.value;
  if (txtValue == "") {
    clientSearchInput.focus();
    alert("고객사를 입력하세요.");
  } else {
    dupCheckOfClient();
  }
}

function dupCheckOfClient() {
  const txtValue = document.getElementById("client__search-field").value;
  const addClientAlert = document.querySelector(".alert");
  const checkDupInput = document.querySelector(".check-dup-client");

  param = {};
  param.clientName = txtValue;

  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrfToken },
    dataType: "json",
    data: param,
    url: "/common/client/dup/check/",
    success: function (data) {
      const similarClientList = data.similar_client_list;
      const createUl = document.createElement("ul");
      const similarComment = document.createElement("small");
      const resultContent = document.querySelector(".contents__similar-list");
      const exsitsSimilarComment = document.querySelector("small");
      const exsitsList = resultContent.childNodes[2];

      if (similarClientList.length < 1) {
        similarComment.innerText =
          "📢 검색어와 비슷한 고객사가 존재하지 않습니다.";
      } else {
        similarComment.innerText =
          "📢 검색어와 비슷한 고객사 리스트 입니다.\n다시 한번 확인 후 등록하시기 바랍니다.";
      }

      if (exsitsSimilarComment != null) {
        const similarParentNode = exsitsSimilarComment.parentNode;
        similarParentNode.removeChild(exsitsSimilarComment);
      }

      if (exsitsList != undefined) {
        const listParentNode = exsitsList.parentNode;
        listParentNode.removeChild(exsitsList);
      }

      checkDupInput.value = txtValue;
      createUl.classList.add("list-group");
      addClientAlert.style.display = "block";
      addClientAlert.classList = "";
      addClientAlert.classList.add("alert");
      addClientAlert.classList.add("alert-success");
      addClientAlert.innerText = "";
      addClientAlert.innerText =
        '✔ 검색하신 "' + txtValue + '" 고객사는 등록이 가능합니다.';
      similarClientList.forEach(function (ele) {
        const createLi = document.createElement("li");
        createLi.innerHTML = ele;
        createLi.classList.add("list-group-item");
        createUl.appendChild(createLi);
      });
      resultContent.append(similarComment);
      resultContent.appendChild(createUl);
      console.log(checkDupInput.value);
    },

    error: function (request, status, error) {
      const clientSearchInput = document.getElementById("client__search-field");
      const similarClientList = request.responseJSON.similar_client_list;
      const resultContent = document.querySelector(".contents__similar-list");
      const createUl = document.createElement("ul");
      const exsitsSimilarComment = document.querySelector("small");
      const exsitsList = resultContent.childNodes[2];
      const similarComment = document.createElement("small");

      checkDupInput.value = "";
      clientSearchInput.value = "";
      clientSearchInput.focus();
      addClientAlert.style.display = "block";
      addClientAlert.classList = "";
      addClientAlert.classList.add("alert");
      addClientAlert.classList.add("alert-danger");

      addClientAlert.innerText = "";
      addClientAlert.innerText =
        '❌ 검색하신 "' + txtValue + '" 고객사가 이미 존재합니다.';

      similarComment.innerText =
        "📢 검색어와 비슷한 고객사 리스트 입니다.\n다시 한번 확인 후 등록하시기 바랍니다.";

      if (exsitsSimilarComment != null) {
        const similarParentNode = exsitsSimilarComment.parentNode;
        similarParentNode.removeChild(exsitsSimilarComment);
      }

      if (exsitsList != undefined) {
        const listParentNode = exsitsList.parentNode;
        listParentNode.removeChild(exsitsList);
      }

      similarClientList.forEach(function (ele) {
        const createLi = document.createElement("li");
        createLi.innerHTML = ele;
        createLi.classList.add("list-group-item");
        createUl.appendChild(createLi);
      });
      resultContent.append(similarComment);
      resultContent.appendChild(createUl);
    },
  });
}

function init() {
  const addClientAlert = document.querySelector(".alert");
  addClientAlert.style.display = "none";
  similarWords();
}

init();

function similarWords() {
  const words = document.querySelectorAll(".similar-word");
  words.forEach((ele) => (ele.style.display = "none"));
}

function checkValue() {
  const checkDupinput = document.querySelector(".check-dup-client");
  if (checkDupinput.value != "") {
    param.clientName = checkDupinput.value;
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrfToken },
      dataType: "json",
      data: param,
      url: "/common/client/add/apply/",
      success: function (data) {
        const successMsg = data.msg;
        alert(successMsg);
        window.location = "/equipment/info/";
      },
      error: function (request, status, error) {
        const errorMsg = request.responseJSON.msg;
        alert(errorMsg);
        window.location = "/equipment/info/";
      },
    });
  } else {
    alert("중복 조회를 다시 시도해주시기 바랍니다.");
    const clientSearchInput = document.getElementById("client__search-field");
    clientSearchInput.focus();
  }
}
