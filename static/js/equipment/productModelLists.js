const mnfactureSelectBox = document.getElementById("mnfacture");

mnfactureSelectBox.addEventListener("change", (event) => {
  mnfactureId = event.target.value;

  if (!mnfactureId) return;
  else {
    $.ajax({
      url: `/common/get/model/${mnfactureId}/lists/`,
      type: "GET",
      dataType: "json",
      success: function (data) {
        const productModels = data.product_models;
        $("#product-model").find("option").remove();
        $("#product-model").selectpicker({ title: "모델명 선택" });
        for (let i = 0; i < productModels.length; i++) {
          const id = productModels[i]["id"];
          const name = productModels[i]["name"];
          $("#product-model").append(`<option value="${id}">${name}</option>`);
        }
        $("#product-model").selectpicker("refresh");
      },
      error: function (request, status, error) {
        const errorMsg = JSON.parse(request.responseText).msg;
        alert(errorMsg);
      },
    });
  }
});

const getProductModelLists = (mnfactureId, modelId) => {
  $.ajax({
    url: `/common/get/model/${mnfactureId}/lists/`,
    type: "GET",
    dataType: "json",
    success: function (data) {
      const productModels = data.product_models;
      $("#product-model").find("option").remove();
      $("#product-model").selectpicker({ title: "모델명 선택" });
      for (let i = 0; i < productModels.length; i++) {
        const id = productModels[i]["id"];
        const name = productModels[i]["name"];
        $("#product-model").append(`<option value="${id}">${name}</option>`);
      }
      $("#product-model").val(modelId);
      $("#product-model").selectpicker("refresh");
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
    },
  });
};
