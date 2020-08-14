function equipmentAddCancel() {
  if (confirm("제품정보 수정을 취소하시겠습니까?"))
    location.href = "/equipment/";
  else return;
}

$(function () {
  $("#ajaxForm").ajaxForm({
    success: function (data) {
      const addSuccessMsg = JSON.parse(data).msg;
      alert(addSuccessMsg);
      location.href = "/equipment/";
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
        location.href = "/equipment/form/";
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
