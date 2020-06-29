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
}

function delete_equipment() {
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

function checkValues() {
  const serial = $("#serial").val();
  const manager = $("#manager").val();
  const location = $("#location").val();
  const installDate = $("#equipment-install-date").val();
  if (serial == "") {
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
    alert("모델명을 선택하세요");
    $("#equipment-install-date").focus();
  } else {
    return true;
}

function equipment_edit_cancel() {
  if (confirm("제품정보 수정을 취소하시겠습니까?")) {
    location.href = "/equipment/";
  } else return;
}

function init() {
  checkLoginId();
  settingValues();
}

init();
