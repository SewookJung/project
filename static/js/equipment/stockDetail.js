const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const modalContent = document.getElementById("modal-content");
const waringContent = document.getElementById("waring-content");
const multiContent = document.getElementById("multi-delivery");
const singleContent = document.getElementById("single-delivery");
const accordion = document.getElementById("accordion");

let selectedStockIds = new Array();
let stockInfoOjbect = new Object();
let stockInfoResult = new Object();
let rowData;
let checkBox;
let serial;
let mnfacture;
let deleteStockObject;
let checkBoxStatus;

$(document).ready(function () {
  const stockTable = $("#stock-table").DataTable({
    pageLength: 15,
    lengthMenu: [5, 10, 15, 20, 30, 50, 100],
    columnDefs: [
      { orderable: true, targets: [1, 2, 3, 4] },
      { orderable: false, targets: "_all" },
    ],
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
    order: [[2, "dec"]],
  });

  $("#stock-table").on("page.dt", function (event) {
    let rows = stockTable.rows().nodes();
    let pageIdx = stockTable.page.info().page + 1;
    checkSelectCheckBox(rows, pageIdx);
  });
});

const stockApply = (stockId, mnfacture, productModel, serial, receiveDate) => {
  const stockIdInput = document.getElementById("stock_id");
  const titleOfMnfacture = document.getElementById("media-title");
  const liOfProductModel = document.getElementById("stock-product-model");
  const liOfSerial = document.getElementById("stock-serial");
  const liOfReceiveDate = document.getElementById("stock-receive-date");
  const submitBtn = document.getElementById("sumbit-btn");
  submitBtn.setAttribute("onclick", "valueCheck()");
  modalContent.style.display = "block";
  waringContent.style.display = "none";
  multiContent.style.display = "none";
  singleContent.style.display = "block";
  stockIdInput.value = stockId;
  titleOfMnfacture.innerText = mnfacture;
  liOfProductModel.innerText = productModel;
  liOfSerial.innerText = serial;
  liOfReceiveDate.innerText = receiveDate + " 입고";
};

const stockReturnApply = (
  stockId,
  mnfacture,
  productModel,
  serial,
  receiveDate
) => {
  const stockIdInput = document.getElementById("return-stock-id");
  const titleOfMnfacture = document.getElementById("return-mnfacture");
  const liOfProductModel = document.getElementById("return-product-model");
  const liOfSerial = document.getElementById("return-serial");
  const liOfReceiveDate = document.getElementById("return-receive-date");
  stockIdInput.value = stockId;
  titleOfMnfacture.innerText = mnfacture;
  liOfProductModel.innerText = productModel;
  liOfSerial.innerText = serial;
  liOfReceiveDate.innerText = receiveDate + " 입고";
};

const stockDisposalApply = (
  stockId,
  mnfacture,
  productModel,
  serial,
  receiveDate
) => {
  const stockIdInput = document.getElementById("disposal-stock-id");
  const titleOfMnfacture = document.getElementById("disposal-mnfacture");
  const liOfProductModel = document.getElementById("disposal-product-model");
  const liOfSerial = document.getElementById("disposal-serial");
  const liOfReceiveDate = document.getElementById("disposal-receive-date");
  stockIdInput.value = stockId;
  titleOfMnfacture.innerText = mnfacture;
  liOfProductModel.innerText = productModel;
  liOfSerial.innerText = serial;
  liOfReceiveDate.innerText = receiveDate + " 입고";
};

const valueCheck = () => {
  const client = document.getElementById("client_id");
  const deliveryDate = document.getElementById("equipment-install-date");
  const location = document.getElementById("location");
  const maintenanceDate = document.getElementById("equipment-maintenance-date");
  const stockIdValue = document.getElementById("stock_id").value;
  const clientVlaue = client.options[client.selectedIndex].value;
  const deliveryDateValue = deliveryDate.value;
  const locationValue = location.value;
  const maintenanceDateValue = maintenanceDate.value;

  if (clientVlaue == "") {
    alert("❗ 납품 고객사를 선택해주세요.");
    return false;
  }

  if (deliveryDateValue == "") {
    alert("❗ 납품 날짜를 선택해주세요.");
    return false;
  }

  if (maintenanceDateValue == "") {
    alert("❗ 유지보수 만료 일자를 선택해주세요.");
    return false;
  }

  if (locationValue == "") {
    alert("❗ 납품 장소를 작성해주세요.");
    return false;
  }

  param = {};
  param.client = clientVlaue;
  param.deliveryDate = deliveryDateValue;
  param.location = locationValue;
  param.stockId = stockIdValue;
  param.maintenanceDate = maintenanceDateValue;

  $.ajax({
    url: "/equipment/stock/delivery/apply/",
    data: param,
    type: "POST",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const successMsg = data.msg;
      alert(successMsg);
      window.location = "/equipment/";
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
      window.location = "/equipment/stock/";
    },
  });
};

const stockReturnSubmit = () => {
  const returnDate = document.getElementById("stock-return-date").value;
  const returnComments = document.getElementById("stock-return-comments").value;
  const returnStockId = document.getElementById("return-stock-id").value;

  if (returnDate == "") {
    alert("❗ 반납 일자를 선택해주세요.");
    return false;
  }

  if (returnComments == "") {
    alert("❗ 반납 사유를 입력해주세요.");
    return false;
  }

  param = {};
  param.returnStockId = returnStockId;
  param.returnDate = returnDate;
  param.returnComments = returnComments;

  $.ajax({
    url: "/equipment/stock/return/apply/",
    data: param,
    type: "POST",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const successMsg = data.msg;
      alert(successMsg);
      window.location = "/equipment/stock/";
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
      window.location = "/equipment/stock/";
    },
  });
};

const stockDisposalSubmit = () => {
  const disposalDate = document.getElementById("stock-disposal-date").value;
  const disposalComments = document.getElementById("stock-disposal-comments")
    .value;
  const disposalStockId = document.getElementById("disposal-stock-id").value;

  if (disposalDate == "") {
    alert("❗ 폐기 일자를 선택해주세요.");
    return false;
  }

  if (disposalComments == "") {
    alert("❗ 폐기 사유를 입력해주세요.");
    return false;
  }

  param = {};
  param.disposalStockId = disposalStockId;
  param.disposalDate = disposalDate;
  param.disposalComments = disposalComments;

  $.ajax({
    url: "/equipment/stock/disposal/apply/",
    data: param,
    type: "POST",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const successMsg = data.msg;
      alert(successMsg);
      window.location = "/equipment/stock/";
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
      window.location = "/equipment/stock/";
    },
  });
};

const checkTheBox = (event) => {
  const clickedElementId = event.target.id;
  let modelName = document.getElementById("stock-model-name").value;
  stockInfoOjbect = new Object();
  switch (clickedElementId) {
    case "blankCheckbox":
      checkBox = event.target;
      checkBoxStatus = checkBox.checked;
      rowData = event.target.parentNode.parentNode.children;
      if (checkBoxStatus == true) {
        if (!(modelName in stockInfoResult)) {
          stockInfoResult[modelName] = new Array();
        }
        stockInfoOjbect.id = checkBox.value;
        stockInfoOjbect.serial = rowData[1].innerText;
        stockInfoOjbect.location = rowData[2].innerText;
        stockInfoOjbect.receiveDate = rowData[3].innerText;
        stockInfoResult[modelName].push(stockInfoOjbect);
        selectedStockIds.push(stockInfoOjbect.id);
      } else {
        serial = rowData[1].innerText;
        deleteStockObject = stockInfoResult[modelName].findIndex(function (
          item
        ) {
          return item.serial === serial;
        });
        if (deleteStockObject > -1)
          stockInfoResult[modelName].splice(deleteStockObject, 1);
        if (stockInfoResult[modelName].length < 1)
          delete stockInfoResult[modelName];
        const selectReleaseStock = selectedStockIds.findIndex(function (item) {
          return item === checkBox.value;
        });
        if (selectReleaseStock > -1) {
          selectedStockIds.splice(selectReleaseStock, 1);
        }
      }
      break;

    case "td-checkbox":
      checkBox = event.target.childNodes[1];
      checkBoxStatus = checkBox.checked;
      rowData = event.target.parentNode.children;
      if (checkBox.checked == false) {
        checkBox.checked = true;
        if (!(modelName in stockInfoResult)) {
          stockInfoResult[modelName] = new Array();
        }
        stockInfoOjbect.id = checkBox.value;
        stockInfoOjbect.serial = rowData[1].innerText;
        stockInfoOjbect.location = rowData[2].innerText;
        stockInfoOjbect.receiveDate = rowData[3].innerText;
        stockInfoResult[modelName].push(stockInfoOjbect);
        selectedStockIds.push(stockInfoOjbect.id);
      } else {
        checkBox.checked = false;
        serial = rowData[1].innerText;
        deleteStockObject = stockInfoResult[modelName].findIndex(function (
          item
        ) {
          return item.serial === serial;
        });
        if (deleteStockObject > -1)
          stockInfoResult[modelName].splice(deleteStockObject, 1);
        if (stockInfoResult[modelName].length < 1)
          delete stockInfoResult[modelName];
        const selectReleaseStock = selectedStockIds.findIndex(function (item) {
          return item === checkBox.value;
        });
        if (selectReleaseStock > -1) {
          selectedStockIds.splice(selectReleaseStock, 1);
        }
      }
      break;
  }
};

const deleteCards = () => {
  const cards = accordion.querySelectorAll(".card");
  if (cards.length > 0) {
    for (let i = 0; i < cards.length; i++) {
      cards[i].remove();
    }
  }
};

const checkSelectedStocks = () => {
  const selectedStocklength = Object.keys(stockInfoResult).length;
  deleteCards();
  if (selectedStocklength > 0) {
    multiContent.style.display = "block";
    modalContent.style.display = "block";
    waringContent.style.display = "none";
    singleContent.style.display = "none";
    const selectedStockKeys = Object.keys(stockInfoResult);

    selectedStockKeys.forEach(function (mnfacture) {
      const card = document.createElement("div");
      const cardHeader = document.createElement("div");
      const anchor = document.createElement("a");
      const collapseDiv = document.createElement("div");
      const cardBody = document.createElement("div");
      const ul = document.createElement("ul");
      const span = document.createElement("span");
      const selectedStocks = stockInfoResult[mnfacture];
      const submitBtn = document.getElementById("sumbit-btn");

      submitBtn.setAttribute("onclick", "multiStocksApply()");
      card.classList.add("card");
      cardHeader.classList.add("card-header");
      anchor.classList.add("card-link");
      anchor.dataset.toggle = "collapse";
      anchor.innerText = mnfacture;
      anchor.href = "#" + mnfacture;
      collapseDiv.id = mnfacture;
      collapseDiv.classList.add("collapse");
      cardBody.classList.add("card-body");
      ul.classList.add("list-group");
      span.classList.add("badge");
      span.classList.add("badge-dark");

      card.appendChild(cardHeader);
      cardHeader.append(anchor);
      cardHeader.append(span);
      card.appendChild(collapseDiv);
      collapseDiv.appendChild(cardBody);
      cardBody.appendChild(ul);

      for (let i = 0; i < selectedStocks.length; i++) {
        const li = document.createElement("li");
        const deleteBadge = document.createElement("span");
        const stockInfo = selectedStocks[i].serial + "  ";
        deleteBadge.setAttribute("onclick", "deleteStockOfList(event)");
        deleteBadge.classList.add("badge");
        deleteBadge.classList.add("badge-danger");
        deleteBadge.innerText = "삭제";
        li.classList.add("list-group-item");
        li.innerText = stockInfo;
        li.id = selectedStocks[i].id;
        li.appendChild(deleteBadge);
        ul.append(li);
      }
      span.innerText = selectedStocks.length;
      accordion.append(card);
    });
  } else {
    waringContent.style.display = "block";
    modalContent.style.display = "none";
  }
};

const deleteStocks = () => {
  const selectedStocklength = Object.keys(stockInfoResult).length;
  const deleteSelectErrorContent = document.getElementById(
    "delete-select-error"
  );
  const deleteSuccessContent = document.getElementById("delete-success");
  const deletePermissionErrorContent = document.getElementById(
    "delete-permission-denied"
  );

  if (selectedStocklength > 0) {
    param = {};
    param.stockIds = selectedStockIds;

    $.ajax({
      url: "/equipment/stock/permission/check/",
      data: param,
      type: "POST",
      dataType: "json",
      headers: { "X-CSRFToken": csrfToken },
      success: function (data) {
        deleteSelectErrorContent.style.display = "none";
        deletePermissionErrorContent.style.display = "none";
        deleteSuccessContent.style.display = "block";
      },
      error: function (request, status, error) {
        const deniedStockLists = document.getElementById("denied-stock-ul");
        const permissionDeniedContent = document.getElementById(
          "permission-denied-body"
        );

        if (deniedStockLists != null) {
          deniedStockLists.remove();
        }

        const ul = document.createElement("ul");
        ul.classList.add("list-group");
        ul.id = "denied-stock-ul";

        permissionDeniedContent.append(ul);
        deleteSelectErrorContent.style.display = "none";
        deleteSuccessContent.style.display = "none";
        deletePermissionErrorContent.style.display = "block";

        const deniedLists = JSON.parse(request.responseText).denied_lists;
        for (let i = 0; i < deniedLists.length; i++) {
          const li = document.createElement("li");
          const stockInfo =
            deniedLists[i].product_model +
            "  " +
            deniedLists[i].serial +
            "\n   🙍‍♂️" +
            deniedLists[i].creator;
          li.classList.add("list-group-item");
          li.innerText = stockInfo;
          ul.append(li);
        }
        permissionDeniedContent.append(ul);
      },
    });
  } else {
    deletePermissionErrorContent.style.display = "none";
    deleteSuccessContent.style.display = "none";
    deleteSelectErrorContent.style.display = "block";
  }
};

const returnStocks = () => {
  const selectedStocklength = Object.keys(stockInfoResult).length;
  const failReturnFrom = document.getElementById("fail-return-form");
  const successReturnForm = document.getElementById("success-return-form");
  const accordion = document.getElementById("multi-return-accordion");
  failReturnFrom.style.display = "none";
  if (selectedStocklength == 0) {
    failReturnFrom.style.display = "block";
    successReturnForm.style.display = "none";
  } else {
    accordion.innerHTML = "";
    const selectedStockKeys = Object.keys(stockInfoResult);
    makeSelectedStocksList(selectedStockKeys, accordion);
    failReturnFrom.style.display = "none";
    successReturnForm.style.display = "block";
  }
};

const disposalStocks = () => {
  const selectedStocklength = Object.keys(stockInfoResult).length;
  const failDisposalFrom = document.getElementById("fail-disposal-form");
  const successDisposalForm = document.getElementById("success-disposal-form");
  const accordion = document.getElementById("multi-disposal-accordion");
  failDisposalFrom.style.display = "none";
  if (selectedStocklength == 0) {
    failDisposalFrom.style.display = "block";
    successDisposalForm.style.display = "none";
  } else {
    accordion.innerHTML = "";
    const selectedStockKeys = Object.keys(stockInfoResult);
    makeSelectedStocksList(selectedStockKeys, accordion);
    failDisposalFrom.style.display = "none";
    successDisposalForm.style.display = "block";
  }
};

const multiStocksApply = () => {
  const client = document.getElementById("client_id");
  const deliveryDate = document.getElementById("equipment-install-date");
  const maintenanceDate = document.getElementById("equipment-maintenance-date");
  const location = document.getElementById("location");
  const clientVlaue = client.options[client.selectedIndex].value;
  const deliveryDateValue = deliveryDate.value;
  const locationValue = location.value;
  const maintenanceValue = maintenanceDate.value;

  if (clientVlaue == "") {
    alert("❗ 납품 고객사를 선택해주세요.");
    return false;
  }

  if (deliveryDateValue == "") {
    alert("❗ 납품 일자를 선택해주세요.");
    return false;
  }

  if (maintenanceValue == "") {
    alert("❗ 유지보수 만료 일자를 선택해주세요.");
    return false;
  }

  if (locationValue == "") {
    alert("❗ 납품처를 작성해주세요.");
    return false;
  }

  if (selectedStockIds.length < 1) {
    alert(
      "❗ 선택된 재고가 없습니다.\n   다시 일괄납품을 신청하여 주시기 바랍니다. "
    );
    return (window.location = "/equipment/stock/");
  }

  param = {};
  param.client = clientVlaue;
  param.deliveryDate = deliveryDateValue;
  param.location = locationValue;
  param.stockIds = selectedStockIds;
  param.maintenanceDate = maintenanceValue;

  $.ajax({
    url: "/equipment/stock/multi/apply/",
    data: param,
    type: "POST",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const successMsg = data.msg;
      alert(successMsg);
      window.location = "/equipment/";
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
      window.location = "/equipment/stock/";
    },
  });
};

const multiStocksReturn = () => {
  const returnDate = document.getElementById("multi-return-date").value;
  const returnComments = document.getElementById("multi-return-comments").value;

  if (returnDate == "") {
    alert("❗ 반납 일자를 선택해주세요.");
    return false;
  }

  if (returnComments == "") {
    alert("❗ 반납 사유를 입력해주세요.");
    return false;
  }

  if (selectedStockIds.length < 1) {
    alert(
      "❗ 선택된 재고가 없습니다.\n   다시 일괄납품을 신청하여 주시기 바랍니다. "
    );
    return (window.location = "/equipment/stock/");
  }

  param = {};
  param.stockIds = selectedStockIds;
  param.returnDate = returnDate;
  param.returnComments = returnComments;

  $.ajax({
    url: "/equipment/stock/multi/return/",
    data: param,
    type: "POST",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const successMsg = data.msg;
      alert(successMsg);
      window.location = "/equipment/stock/";
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
      window.location = "/equipment/stock/";
    },
  });
};

const multiStocksDisposal = () => {
  const disposalDate = document.getElementById("multi-disposal-date").value;
  const disposalComments = document.getElementById("multi-disposal-comments")
    .value;

  if (disposalDate == "") {
    alert("❗ 폐기 일자를 선택해주세요.");
    return false;
  }

  if (disposalComments == "") {
    alert("❗ 폐기 사유를 입력해주세요.");
    return false;
  }

  if (selectedStockIds.length < 1) {
    alert(
      "❗ 선택된 재고가 없습니다.\n   다시 일괄납품을 신청하여 주시기 바랍니다. "
    );
    return (window.location = "/equipment/stock/");
  }

  param = {};
  param.stockIds = selectedStockIds;
  param.disposalDate = disposalDate;
  param.disposalComments = disposalComments;

  $.ajax({
    url: "/equipment/stock/multi/disposal/",
    data: param,
    type: "POST",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const successMsg = data.msg;
      alert(successMsg);
      window.location = "/equipment/stock/";
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
      window.location = "/equipment/stock/";
    },
  });
};

const stockMultiDelete = () => {
  param = {};
  param.stockIds = selectedStockIds;
  $.ajax({
    url: "/equipment/stock/multi/delete/",
    data: param,
    type: "POST",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const successMsg = data.msg;
      alert(successMsg);
      window.location = "/equipment/stock/";
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
      window.location = "/equipment/stock/";
    },
  });
};

const deleteStockOfList = (event) => {
  const deleteLi = event.target.parentElement;
  const deleteStockId = event.target.parentElement.id;
  let badgeOfStock =
    deleteLi.parentElement.parentElement.parentElement.parentElement.firstChild
      .lastChild;
  let countOfSelectedStocks = Number(badgeOfStock.innerText);
  deleteLi.remove();
  countOfSelectedStocks--;
  badgeOfStock.innerText = countOfSelectedStocks;
  const idxOfExceptStock = selectedStockIds.findIndex(function (ele) {
    return ele === deleteStockId;
  });

  if (idxOfExceptStock > -1) {
    selectedStockIds.splice(idxOfExceptStock, 1);
  }
};

const settingMaintenance = (event) => {
  const maintenanceField = document.getElementById(
    "equipment-maintenance-date"
  );
  const getDeliveryDateValue = event.target.value.split("-");
  const DeliveryDate = new Date(
    getDeliveryDateValue[0],
    getDeliveryDateValue[1],
    getDeliveryDateValue[2]
  );
  DeliveryDate.setFullYear(DeliveryDate.getFullYear() + 1);

  const year = DeliveryDate.getFullYear();
  const month = ("0" + DeliveryDate.getMonth()).slice(-2);
  const day = ("0" + DeliveryDate.getDate()).slice(-2);
  const defaultMaintenanceValue = `${year}-${month}-${day}`;
  maintenanceField.value = defaultMaintenanceValue;
};

const makeSelectedStocksList = (selectedStockKeys, accordion) => {
  selectedStockKeys.forEach(function (mnfacture) {
    const card = document.createElement("div");
    const cardHeader = document.createElement("div");
    const anchor = document.createElement("a");
    const collapseDiv = document.createElement("div");
    const cardBody = document.createElement("div");
    const ul = document.createElement("ul");
    const span = document.createElement("span");
    const selectedStocks = stockInfoResult[mnfacture];
    const submitBtn = document.getElementById("sumbit-btn");

    submitBtn.setAttribute("onclick", "multiStocksApply()");
    card.classList.add("card");
    cardHeader.classList.add("card-header");
    anchor.classList.add("card-link");
    anchor.dataset.toggle = "collapse";
    anchor.innerText = mnfacture;
    anchor.href = "#" + mnfacture;
    collapseDiv.id = mnfacture;
    collapseDiv.classList.add("collapse");
    cardBody.classList.add("card-body");
    ul.classList.add("list-group");
    span.classList.add("badge");
    span.classList.add("badge-dark");

    card.appendChild(cardHeader);
    cardHeader.append(anchor);
    cardHeader.append(span);
    card.appendChild(collapseDiv);
    collapseDiv.appendChild(cardBody);
    cardBody.appendChild(ul);

    for (let i = 0; i < selectedStocks.length; i++) {
      const li = document.createElement("li");
      const deleteBadge = document.createElement("span");
      const stockInfo = selectedStocks[i].serial + "  ";
      deleteBadge.setAttribute("onclick", "deleteStockOfList(event)");
      deleteBadge.classList.add("badge");
      deleteBadge.classList.add("badge-danger");
      deleteBadge.innerText = "삭제";
      li.classList.add("list-group-item");
      li.innerText = stockInfo;
      li.id = selectedStocks[i].id;
      li.appendChild(deleteBadge);
      ul.append(li);
    }
    span.innerText = selectedStocks.length;
    accordion.append(card);
  });
};

const pageCheckTheBox = (event) => {
  const clickedElementId = event.target.id;
  let entries = Number(document.querySelector(".custom-select").value);
  let rows = document.querySelectorAll(".rows");
  let startIdx = 0;
  let endIdx = entries;
  let checkBox;
  let checkBoxStatus;

  switch (clickedElementId) {
    case "pageCheckBox":
      checkBox = event.target;
      checkBoxStatus = checkBox.checked;
      if (checkBoxStatus == true) {
        addStocks(rows, startIdx, endIdx);
      } else {
        removeStocks(rows, startIdx, endIdx);
      }
      break;

    case "th-checkBox":
      checkBox = event.target.children[0];
      checkBoxStatus = checkBox.checked;
      if (checkBoxStatus == true) {
        checkBox.checked = false;
        removeStocks(rows, startIdx, endIdx);
      } else {
        checkBox.checked = true;
        addStocks(rows, startIdx, endIdx);
      }
      break;
  }
};

const addStocks = (rows, startIdx, endIdx) => {
  let modelName = document.getElementById("stock-model-name").value;

  if (rows.length < endIdx) endIdx = rows.length;

  for (startIdx; startIdx < endIdx; startIdx++) {
    let checkBox = rows[startIdx].children[0].children[0];
    let rowData = rows[startIdx].children;
    let serial = rowData[1].innerText;
    stockInfoOjbect = new Object();

    checkBox.checked = true;
    if (!(modelName in stockInfoResult))
      stockInfoResult[modelName] = new Array();

    const existCheckOfArray = stockInfoResult[modelName].findIndex(function (
      item
    ) {
      return item.serial === serial;
    });

    if (existCheckOfArray == -1) {
      stockInfoOjbect.id = checkBox.value;
      stockInfoOjbect.serial = rowData[1].innerText;
      stockInfoOjbect.product = rowData[2].innerText;
      stockInfoOjbect.location = rowData[3].innerText;
      stockInfoResult[modelName].push(stockInfoOjbect);
      selectedStockIds.push(stockInfoOjbect.id);
    }
  }
  stockInfoResult[modelName].sort(function (a, b) {
    return Number(a.id - b.id);
  });
};

const removeStocks = (rows, startIdx, endIdx) => {
  let modelName = document.getElementById("stock-model-name").value;

  if (rows.length < endIdx) endIdx = rows.length;

  for (startIdx; startIdx < endIdx; startIdx++) {
    let checkBox = rows[startIdx].children[0].children[0];
    let rowData = rows[startIdx].children;
    let serial = rowData[1].innerText;
    stockInfoOjbect = new Object();
    checkBox.checked = false;
    const deleteStockObject = stockInfoResult[modelName].findIndex(function (
      item
    ) {
      return item.serial === serial;
    });
    if (deleteStockObject > -1)
      stockInfoResult[modelName].splice(deleteStockObject, 1);
    if (stockInfoResult[modelName].length < 1)
      delete stockInfoResult[modelName];
    const selectReleaseStock = selectedStockIds.findIndex(function (item) {
      return item === checkBox.value;
    });
    if (selectReleaseStock > -1) {
      selectedStockIds.splice(selectReleaseStock, 1);
    }
  }
};

const checkSelectCheckBox = (rows, pageIdx) => {
  let entries = Number(document.querySelector(".custom-select").value);
  let startIdx = entries * (pageIdx - 1);
  let endIdx = entries * pageIdx - 1;
  let pageCheckBox = document.getElementById("pageCheckBox");

  if (endIdx > rows.length) endIdx = rows.length - 1;

  checkBoxStatus = new Array();

  for (startIdx; startIdx <= endIdx; startIdx++) {
    let checkBox = rows[startIdx].children[0].children[0];
    checkBoxStatus.push(checkBox.checked);
  }

  if (checkBoxStatus.includes(false)) pageCheckBox.checked = false;
  else pageCheckBox.checked = true;
};
