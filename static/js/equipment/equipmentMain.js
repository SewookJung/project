const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const clientSelectBox = document.getElementById("client_id");
const mnfactureSelectBox = document.getElementById("mnfacture");
const equipmentHeader = document.querySelector(".contents__header");
const equipmentContent = document.querySelector(".contents__content");
let totalCount;

const getListClientEquipments = (clientId) => {
  $.ajax({
    url: `/equipment/${clientId}/all/list/`,
    type: "GET",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      getListMnfactures(clientId);
      const equipments = data.equipment_lists;
      drawEquipment(equipments);
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).error;
      alert(errorMsg);
      blockMnfactureSelectBox();
    },
  });
};

const getListMnfactures = (clientId) => {
  $.ajax({
    url: `/equipment/${clientId}/mnfacture/list/`,
    type: "GET",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const mnfactures = data.mnfactures;
      $("#mnfacture").find("option").remove();
      $("#mnfacture").prop("disabled", false);
      $("#mnfacture").selectpicker({ title: "제조사 선택" });
      $("#mnfacture").append('<option value="ALL">전체보기</option>');
      for (let i = 0; i < mnfactures.length; i++) {
        const mnfactureId = mnfactures[i]["mnfacture_id"];
        const mnfactureName = mnfactures[i]["mnfacture_name"];
        $("#mnfacture").append(
          `<option value="${mnfactureId}">${mnfactureName}</option>`
        );
      }
      $("#mnfacture").selectpicker("refresh");
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).error;
      alert(errorMsg);
    },
  });
};

const getEquipmentsByMnfacture = (clientId, mnfactureId) => {
  let url;
  if (mnfactureId == "ALL") url = `/equipment/${clientId}/all/list/`;
  else url = `/equipment/${clientId}/${mnfactureId}/list/`;

  $.ajax({
    url: url,
    type: "GET",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const equipments = data.equipment_lists;
      drawEquipment(equipments);
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).error;
      alert(errorMsg);
    },
  });
};

const drawEquipment = (equipments) => {
  equipmentContent.innerHTML = "";
  equipmentHeader.style.display = "block";
  equipmentContent.style.display = "block";

  const clientName = document.querySelector(".filter-option-inner-inner")
    .innerText;
  const clientNameDiv = document.querySelector(".header__client-name");
  const mnfactures = Object.keys(equipments[clientName]);
  let totalCountBadge = document.createElement("span");
  totalCount = equipments.totalCount;

  for (let i = 0; i < mnfactures.length; i++) {
    let card = document.createElement("div");
    let cardBody = document.createElement("div");
    let cardHeader = document.createElement("div");
    let mnfactureNameDiv = document.createElement("div");
    let equipListDiv = document.createElement("div");
    let mnfactureCountBadge = document.createElement("span");
    let mnfactureCount = 0;
    const mnfacture = mnfactures[i];
    const productModel = Object.keys(equipments[clientName][mnfactures[i]]);
    for (let f = 0; f < productModel.length; f++) {
      let modelHeaderDiv = document.createElement("div");
      let modelCountBadge = document.createElement("span");
      let modelContentDiv = document.createElement("div");

      const model = Object.keys(equipments[clientName][mnfactures[i]])[f];
      const count =
        equipments[clientName][mnfactures[i]][productModel[f]]["count"];

      equipListDiv.classList.add("equipments");
      modelContentDiv.classList.add("equipment__lists");
      modelHeaderDiv.classList.add("header", "equipment__list-header");
      modelCountBadge.classList.add("badge", "badge-dark");

      modelCountBadge.innerText = count;
      modelHeaderDiv.innerText = model;
      modelHeaderDiv.append(modelCountBadge);
      modelContentDiv.append(modelHeaderDiv);
      equipListDiv.append(modelContentDiv);

      modelHeaderDiv.setAttribute(
        "onclick",
        'modelDetailPage("' + model + '")'
      );
      mnfactureCount += count;
    }
    mnfactureNameDiv.innerText = mnfacture;
    mnfactureCountBadge.innerText = mnfactureCount;

    cardHeader.setAttribute(
      "onclick",
      'mnfactureDetailPage("' + mnfacture + '")'
    );
    mnfactureNameDiv.append(mnfactureCountBadge);
    cardHeader.append(mnfactureNameDiv);
    card.append(cardBody);
    cardBody.append(cardHeader);
    cardBody.append(equipListDiv);
    card.classList.add("card");
    cardBody.classList.add("card-body");
    cardHeader.classList.add("header", "mnfacture__header");
    mnfactureNameDiv.classList.add("mnfacture__header-title");
    mnfactureCountBadge.classList.add("badge", "badge-dark");
    equipmentContent.append(card);
  }

  clientNameDiv.innerText = clientName;
  totalCountBadge.innerText = totalCount;
  clientNameDiv.append(totalCountBadge);
  clientNameDiv.setAttribute("onclick", "onclick=equipmentAllPage()");
  totalCountBadge.classList.add("badge", "badge-dark");
};

const equipmentAllPage = () => {
  const clientId = document.getElementById("client_id").value;
  window.location = `/equipment/client/${clientId}/detail/`;
};

const mnfactureDetailPage = (mnfacture) => {
  const clientId = document.getElementById("client_id").value;

  $.ajax({
    url: `/common/get/mnfacture/${mnfacture}/id/`,
    type: "GET",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const mnfactureId = data.mnfacture_id;
      window.location = `/equipment/client/${clientId}/${mnfactureId}/detail/`;
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
    },
  });
};

const modelDetailPage = (model) => {
  const clientId = document.getElementById("client_id").value;

  $.ajax({
    url: `/common/get/model/${model}/id/`,
    type: "GET",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const mnfactureId = data.mnfacture_id;
      const modelId = data.model_id;
      window.location = `/equipment/client/${clientId}/${mnfactureId}/${modelId}/detail/`;
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
    },
  });
};

const clearContents = () => {
  const contentsHeader = document.querySelector(".header__client-name");
  const contentsContent = document.querySelector(".contents__content");
  contentsHeader.innerText = "";
  contentsContent.innerText = "";
};

const blockMnfactureSelectBox = () => {
  $("#mnfacture").find("option").remove();
  $("#mnfacture").prop("disabled", true);
  $("#mnfacture").selectpicker({ title: "고객사를 선택하세요" });
  $("#mnfacture").selectpicker("refresh");
  clearContents();
};

clientSelectBox.addEventListener("change", (event) => {
  const clientId = event.target.value;
  if (clientId == "") blockMnfactureSelectBox();
  else getListClientEquipments(clientId);
});

mnfactureSelectBox.addEventListener("change", () => {
  const clientId = document.getElementById("client_id").value;
  const mnfactureId = document.getElementById("mnfacture").value;
  getEquipmentsByMnfacture(clientId, mnfactureId);
});

const init = () => {
  equipmentHeader.style.display = "none";
  equipmentContent.style.display = "none";
};

init();
