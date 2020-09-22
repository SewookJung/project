const checkLoginId = () => {
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
};

const settingValues = () => {
  const clientId = $("#stock-client-id").val();
  $("select[name=client]").val(clientId);
  const productId = $("#stock-product-id").val();
  $("select[name=product_id]").val(productId);
  const modelId = $("#stock-model-id").val();
  $("select[name=product_model]").val(modelId);
  const mnfactureId = $("#stock-mnfacture-id").val();
  $("select[name=mnfacture]").val(mnfactureId);
  $(".selectpicker").selectpicker("refresh");
};

const deleteStock = () => {
  if (confirm("해당 재고를 삭제하시겠습니까?")) {
    const stockId = $("#stock_id").val();
    $.ajax({
      type: "GET",
      url: "/equipment/stock/" + stockId + "/delete/",
      success: function (data) {
        const addSuccessMsg = JSON.parse(data).msg;
        alert(addSuccessMsg);
        location.href = "/equipment/stock/";
      },
      error: function (request, status, error) {
        const addFailMsg = JSON.parse(request.responseText).msg;
        alert(addFailMsg);
        location.href = "/equipment/stock/";
      },
    });
  } else return;
};

function stockEditCancel() {
  if (confirm("재고 정보 수정을 취소하시겠습니까?")) {
    location.href = "/equipment/stock/";
  } else return;
}

$(function () {
  checkLoginId();
  settingValues();

  $("#ajaxForm").ajaxForm({
    success: function (data) {
      const addSuccessMsg = JSON.parse(data).msg;
      alert(addSuccessMsg);
      window.location = "/equipment/stock/";
    },
    error: function (request, status, error) {
      const requestData = JSON.parse(request.responseText);
      const failMsg = requestData.msg;
      const errorInfo = JSON.parse(request.responseText).error;

      if (errorInfo == "serial_error") {
        const serialInput = document.getElementById("serial");
        serialInput.value = "";
        alert(failMsg);
        serialInput.focus();
      } else {
        alert(failMsg);
        window.location = "/equipment/stock/";
      }
    },
    beforeSubmit: function () {
      const mnfacture = $("#mnfacture").val();
      const product = $("#product_id").val();
      const productModel = $("#product-model").val();
      const serial = $("#serial").val();
      const location = $("#location").val();
      const installDate = $("#stock-install-date").val();

      if (mnfacture == "") {
        alert("제조사를 선택해주세요.");
        $("#mnfacture").focus();
        return false;
      } else if (product == "") {
        alert("제품명을 선택해주세요.");
        $("#product_id").focus();
        return false;
      } else if (productModel == "") {
        alert("모델명을 선택해주세요.");
        $("#product-model").focus();
        return false;
      } else if (serial == "") {
        alert("시리얼번호를 입력하세요.");
        $("#serial").focus();
        return false;
      } else if (location == "") {
        alert("재고 위치를 입력하세요.");
        $("#location").focus();
        return false;
      } else if (installDate == "") {
        alert("입고 일자를 입력하세요.");
        $("#stock-install-date").focus();
        return false;
      } else {
        return true;
      }
    },
  });
});
