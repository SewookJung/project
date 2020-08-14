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

const stockApply = (
  stockId,
  mnfacture,
  product,
  productModel,
  serial,
  receiveDate
) => {
  const stockIdInput = document.getElementById("stock_id");
  const titleOfMnfacture = document.getElementById("media-title");
  const liOfProduct = document.getElementById("stock-product");
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
  liOfProduct.innerText = product;
  liOfProductModel.innerText = productModel;
  liOfSerial.innerText = serial;
  liOfReceiveDate.innerText = receiveDate + " 입고";
};

const valueCheck = () => {
  const client = document.getElementById("client_id");
  const deliveryDate = document.getElementById("equipment-install-date");
  const manager = document.getElementById("manager");
  const location = document.getElementById("location");
  const stockIdValue = document.getElementById("stock_id").value;
  const clientVlaue = client.options[client.selectedIndex].value;
  const deliveryDateValue = deliveryDate.value;
  const managerValue = manager.value;
  const locationValue = location.value;

  if (clientVlaue == "") {
    alert("❗ 납품 고객사를 선택해주세요.");
    return false;
  }

  if (deliveryDateValue == "") {
    alert("❗ 납품 날짜를 선택해주세요.");
    return false;
  }

  if (managerValue == "") {
    alert("❗ 납품 장비 담당자를 작성해주세요.");
    return false;
  }

  if (locationValue == "") {
    alert("❗ 납품 장소를 작성해주세요.");
    return false;
  }

  param = {};
  param.client = clientVlaue;
  param.deliveryDate = deliveryDateValue;
  param.manager = managerValue;
  param.location = locationValue;
  param.stockId = stockIdValue;

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

const checkTheBox = (event) => {
  const clickedElementId = event.target.id;
  stockInfoOjbect = new Object();
  switch (clickedElementId) {
    case "blankCheckbox":
      checkBox = event.target;
      checkBoxStatus = checkBox.checked;
      rowData = event.target.parentNode.parentNode.children;
      if (checkBoxStatus == true) {
        modelName = document.getElementById("stock-model-name").innerText;
        if (!(modelName in stockInfoResult)) {
          stockInfoResult[modelName] = new Array();
        }
        stockInfoOjbect.id = checkBox.value;
        stockInfoOjbect.serial = rowData[1].innerText;
        stockInfoOjbect.product = rowData[2].innerText;
        stockInfoOjbect.location = rowData[3].innerText;
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
        modelName = document.getElementById("stock-model-name").innerText;
        if (!(modelName in stockInfoResult)) {
          stockInfoResult[modelName] = new Array();
        }
        stockInfoOjbect.id = checkBox.value;
        stockInfoOjbect.serial = rowData[1].innerText;
        stockInfoOjbect.product = rowData[2].innerText;
        stockInfoOjbect.location = rowData[3].innerText;
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
        const stockInfo =
          selectedStocks[i].serial + "  " + selectedStocks[i].product;
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

const multiStocksApply = () => {
  const client = document.getElementById("client_id");
  const deliveryDate = document.getElementById("equipment-install-date");
  const manager = document.getElementById("manager");
  const location = document.getElementById("location");
  const clientVlaue = client.options[client.selectedIndex].value;
  const deliveryDateValue = deliveryDate.value;
  const managerValue = manager.value;
  const locationValue = location.value;

  if (clientVlaue == "") {
    alert("❗ 납품 고객사를 선택해주세요.");
    return false;
  }

  if (deliveryDateValue == "") {
    alert("❗ 납품 날짜를 선택해주세요.");
    return false;
  }

  if (locationValue == "") {
    alert("❗ 납품 장소를 작성해주세요.");
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
  param.manager = managerValue;
  param.location = locationValue;
  param.stockIds = selectedStockIds;

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
            deniedLists[i].product +
            "  " +
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
