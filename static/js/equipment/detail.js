function checkLoginId() {
  const inputElements = document.querySelectorAll("input");
  const textareaElement = document.querySelector("textarea");
  const loginId = document.getElementById("login_id").value;
  const projectCreator = document.getElementById("creator").value;

  if (loginId != projectCreator) {
    $(".selectpicker").prop("disabled", true);
    $(".selectpicker").selectpicker("refresh");
    textareaElement.disabled = "true";
    inputElements.forEach(function (item) {
      item.disabled = true;
    });
  }
}

function settingValues() {
  const clientId = $("#equip-client-id").val();
  $("select[name=client]").val(clientId);
  const productId = $("#equip-product-id").val();
  $("select[name=product_id]").val(productId);
  const modelId = $("#equip-model-id").val();
  $("select[name=product_model]").val(modelId);
  const mnfactureId = $("#equip-mnfacture-id").val();
  $("select[name=mnfacture]").val(mnfactureId);
  $(".selectpicker").selectpicker("refresh");

  getProductModelLists(mnfactureId, modelId);
}

function deleteEquipment() {
  if (confirm("해당 제품정보를 삭제하시겠습니까?")) {
    const equipmentId = $("#equipment_id").val();
    $.ajax({
      type: "GET",
      url: "/equipment/" + equipmentId + "/delete/",
      success: function (data) {
        const addSuccessMsg = JSON.parse(data).msg;
        alert(addSuccessMsg);
        location.href = "/equipment/";
      },
      error: function (request, status, error) {
        const addFailMsg = JSON.parse(request.responseText).msg;
        alert(addFailMsg);
        location.href = "/equipment/form/";
      },
    });
  } else return;
}

function equipmentEditCancel() {
  if (confirm("제품정보 수정을 취소하시겠습니까?")) {
    location.href = "/equipment/";
  } else return;
}

$(function () {
  checkLoginId();
  settingValues();

  $("#ajaxForm").ajaxForm({
    success: function (data) {
      const addSuccessMsg = JSON.parse(data).msg;
      alert(addSuccessMsg);
      window.location = "/equipment/";
    },
    error: function (request, status, error) {
      const requestData = JSON.parse(request.responseText);
      const failMsg = requestData.msg;
      const errorInfo = JSON.parse(request.responseText).error;

      if (errorInfo == "serial_error") {
        const serialInput = document.getElementById("serial");
        serialInput.value = "";
        alert(failMsg);
        window.location.focus();
      } else {
        alert(failMsg);
        window.location = "/equipment/form/";
      }
    },
    beforeSubmit: function () {
      const client = $("#client_id").val();
      const mnfacture = $("#mnfacture").val();
      const product = $("#product_id").val();
      const productModel = $("#product-model").val();
      const serial = $("#serial").val();
      const manager = $("#manager").val();
      const location = $("#location").val();
      const installDate = $("#equipment-install-date").val();

      if (client == "") {
        alert("고객사를 선택해주세요.");
        $("#client_id").focus();
        return false;
      } else if (mnfacture == "") {
        alert("제조사를 선택해주세요.");
        $("#mnfacture").focus();
        return false;
      } else if (product == "") {
        alert("제품명을 선택해주세요.");
        $("#product").focus();
        return false;
      } else if (productModel == "") {
        alert("모델명을 선택해주세요.");
        $("#productModel").focus();
        return false;
      } else if (serial == "") {
        alert("시리얼번호를 입력하세요.");
        $("#serial").focus();
        return false;
      } else if (manager == "") {
        alert("담당엔지니어를 입력하세요.");
        $("#manager").focus();
        return false;
      } else if (location == "") {
        alert("설치장소를 입력하세요");
        $("#location").focus();
        return false;
      } else if (installDate == "") {
        alert("설치 날짜를 선택하세요");
        $("#equipment-install-date").focus();
        return false;
      } else {
        return true;
      }
    },
  });
});
