const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

const stockApply = (stockId, mnfacture, product, product_model, serial) => {
  const stockIdInput = document.getElementById("stock_id");
  const mnfactureInput = document.getElementById("mnfacture");
  const productInput = document.getElementById("product");
  const productModelInput = document.getElementById("product-model");
  const serialInput = document.getElementById("serial");
  stockIdInput.value = stockId;
  mnfactureInput.value = mnfacture;
  productInput.value = product;
  productModelInput.value = product_model;
  serialInput.value = serial;
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

function checkTheBox(event) {
  const clickedElementId = event.target.id;
  if (clickedElementId == "blankCheckbox") return false;

  if (clickedElementId == "form-check") {
    const checkBox = event.target.childNodes[1];
    if (checkBox.checked == false) {
      checkBox.checked = true;
      return false;
    } else {
      checkBox.checked = false;
      return false;
    }
  }

  const checkBox = event.target.childNodes[1].childNodes[1];
  if (checkBox.checked == false) checkBox.checked = true;
  else checkBox.checked = false;
}
