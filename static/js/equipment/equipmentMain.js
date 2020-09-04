const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const clientSelectBox = document.getElementById("client_id");
const equipmentHeader = document.querySelector(".contents__header");
const equipmentContent = document.querySelector(".contents__content");

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
      for (let i = 0; i < mnfactures.length; i++) {
        const mnfactureId = mnfactures[i]["mnfacture_id"];
        const mnfactureName = mnfactures[i]["mnfacture_name"];
        $("#mnfacture").append(
          `<option value="${mnfactureId}">${mnfactureName}</option>;`
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

const drawEquipment = (equipments) => {
  equipmentContent.innerHTML = "";
  equipmentHeader.style.display = "block";
  equipmentContent.style.display = "block";

  const clientName = document.querySelector(".filter-option-inner-inner")
    .innerText;
  const clientNameDiv = document.querySelector(".header__client-name");
  const mnfactures = Object.keys(equipments[clientName]);
  let totalCountBadge = document.createElement("span");
  let totalCount = 0;

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
      let modelSerachDiv = document.createElement("div");
      let searchBar = document.createElement("input");
      let modelContentDiv = document.createElement("div");
      let ul = document.createElement("ul");

      const model = Object.keys(equipments[clientName][mnfactures[i]])[f];
      const count =
        equipments[clientName][mnfactures[i]][productModel[f]].length;
      const equipmentLists =
        equipments[clientName][mnfactures[i]][productModel[f]];

      for (let s = 0; s < equipmentLists.length; s++) {
        let li = document.createElement("li");
        const serial =
          equipments[clientName][mnfactures[i]][productModel[f]][s]["serial"];
        const installDate =
          equipments[clientName][mnfactures[i]][productModel[f]][s][
            "install_date"
          ];
        const location =
          equipments[clientName][mnfactures[i]][productModel[f]][s]["location"];

        li.innerText = `${serial} / ${location} / ${installDate}`;
        li.classList.add("list-group-item");
        ul.append(li);
      }

      ul.classList.add("list-group");
      equipListDiv.classList.add("equipments");
      modelContentDiv.classList.add("equipment__lists");
      modelHeaderDiv.classList.add("header", "equipment__list-header");
      modelCountBadge.classList.add("badge", "badge-dark");

      modelCountBadge.innerText = count;
      modelHeaderDiv.innerText = model;
      modelHeaderDiv.append(modelCountBadge);
      modelContentDiv.append(modelHeaderDiv);
      modelContentDiv.append(ul);
      equipListDiv.append(modelContentDiv);

      modelHeaderDiv.setAttribute(
        "onclick",
        'mnfactureDetailPage("' + mnfacture + '")'
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

    totalCount += mnfactureCount;
  }

  clientNameDiv.innerText = clientName;
  totalCountBadge.innerText = totalCount;
  clientNameDiv.append(totalCountBadge);
  clientNameDiv.setAttribute("onclick", "onclick=goToAllEquipment()");
  totalCountBadge.classList.add("badge", "badge-dark");
};

const goToAllEquipment = () => {
  const clientId = document.getElementById("client_id").value;
  window.location = `/equipment/client/${clientId}/detail/`;
};

const mnfactureDetailPage = (mnfacture) => {
  const clientId = document.getElementById("client_id").value;
  window.location = `/equipment/client/${clientId}/${mnfacture}/detail/`;
};

const modelDetailPage = (model) => {
  const clientId = document.getElementById("client_id").value;
  window.location = `/equipment/client/${clientId}/${model}/detail/`;
};

clientSelectBox.addEventListener("change", (event) => {
  const clientId = event.target.value;
  if (!clientId == "") getListClientEquipments(clientId);
});

const init = () => {
  equipmentHeader.style.display = "none";
  equipmentContent.style.display = "none";
};

init();
