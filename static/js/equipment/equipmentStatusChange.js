const equipmentStatusSelectBox = document.getElementById("equipment-status");

equipmentStatusSelectBox.addEventListener("change", (event) => {
  const status = event.target.value;
  const rmaForm = document.getElementById("rma-form");

  if (status != "rma") rmaForm.style.display = "none";
  else rmaForm.style.display = "block";
});

const statusChangeBtnOnClient = (event) => {
  const rows = event.target.parentNode.parentNode.children;
  const serial = rows[0].innerText;
  const mnfacture = rows[1].innerText;
  const productModel = rows[2].innerText;
  const location = rows[3].innerText;
  const deliveryDate = rows[4].innerText;

  changeEquiupmentStatus(
    serial,
    productModel,
    location,
    deliveryDate,
    mnfacture
  );
};

const statusChangeBtnOnMnfacture = (event, mnfacture) => {
  const rows = event.target.parentNode.parentNode.children;
  const serial = rows[0].innerText;
  const productModel = rows[1].innerText;
  const location = rows[2].innerText;
  const deliveryDate = rows[3].innerText;

  changeEquiupmentStatus(
    serial,
    productModel,
    location,
    deliveryDate,
    mnfacture
  );
};

const statusChangeBtnOnProductModel = (event, mnfacture, productModel) => {
  const rows = event.target.parentNode.parentNode.children;
  const serial = rows[0].innerText;
  const location = rows[1].innerText;
  const deliveryDate = rows[2].innerText;

  changeEquiupmentStatus(
    serial,
    productModel,
    location,
    deliveryDate,
    mnfacture
  );
};

const changeEquiupmentStatus = (
  serial,
  productModel,
  location,
  deliveryDate,
  mnfacture
) => {
  const serialDiv = document.getElementById("equipment-info-serial");
  const mnfactureDiv = document.getElementById("equipment-mnfacture");
  const productModelDiv = document.getElementById("equipment-info-model");
  const locationDiv = document.getElementById("equipment-info-location");
  const deliveryDateDiv = document.getElementById(
    "equipment-info-deliveryDate"
  );

  serialDiv.innerText = serial;
  mnfactureDiv.innerText = mnfacture;
  productModelDiv.innerText = productModel;
  locationDiv.innerText = location;
  deliveryDateDiv.innerText = deliveryDate;
};

const init = () => {
  const rmaForm = document.getElementById("rma-form");
  rmaForm.style.display = "none";
};

const submitStatusChange = () => {
  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  const status = equipmentStatusSelectBox.value;
  const comments = document.getElementById("comments").value;
  const equipmentSerial = document.getElementById("equipment-info-serial")
    .innerText;

  if (!status) {
    alert("⚠ 구분을 선택하여 주세요");
    return;
  } else if (status != "rma") {
    param = {};
    param.equipmentSerial = equipmentSerial;
    param.status = status;
    param.comments = comments;
  } else {
    const mnfacture = document.getElementById("mnfacture").value;
    const productModel = document.getElementById("product-model").value;
    const changeSerial = document.getElementById("serial").value;

    if (!mnfacture) {
      alert("⚠ 제조사를 선택하세요");
      return;
    }
    if (!productModel) {
      alert("⚠ 모델명을 선택하세요");
      return;
    }
    if (!changeSerial) {
      alert("⚠ 시리얼을 입력하세요");
      return;
    }

    param = {};
    param.equipmentSerial = equipmentSerial;
    param.status = status;
    param.mnfacture = mnfacture;
    param.productModel = productModel;
    param.changeSerial = changeSerial;
    param.comments = comments;
  }

  $.ajax({
    url: "/equipment/status/change/",
    data: param,
    type: "POST",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const successMsg = data.msg;
      const url = window.location.href;
      alert(successMsg);
      window.location = url;
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
    },
  });
};

init();
