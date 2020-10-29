const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const mnfactureBox = document.getElementById("mnfacture");

const getListsProductModel = (param) => {
  $.ajax({
    url: "/equipment/stock/get/list/test/",
    data: param,
    type: "POST",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const stocks = data.stocks.data;
      const stockTable = $("#stockTable").DataTable();
      stockTable.destroy();

      $("#stockTable").DataTable({
        data: stocks,
        language: {
          paginate: {
            previous: "‹",
            next: "›",
          },
        },
        columns: [
          { data: "name" },
          {
            data: "keep",
            fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
              $(nTd).html(oData.keep + "개");
              $(nTd).attr(
                "onclick",
                `goToDetailPage(event, ${oData.id}, 'keep')`
              );
              $(nTd).css("cursor", "pointer");
            },
          },
          {
            data: "sold",
            fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
              $(nTd).html(oData.sold + "개");
              $(nTd).attr(
                "onclick",
                `goToDetailPage(event, ${oData.id}, 'sold')`
              );
              $(nTd).css("cursor", "pointer");
            },
          },
          {
            data: "return",
            fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
              $(nTd).html(oData.return + "개");
              $(nTd).attr(
                "onclick",
                `goToDetailPage(event, ${oData.id}, 'return')`
              );
              $(nTd).css("cursor", "pointer");
            },
          },
          {
            data: "disposal",
            fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
              $(nTd).html(oData.disposal + "개");
              $(nTd).attr(
                "onclick",
                `goToDetailPage(event, ${oData.id}, 'disposal')`
              );
              $(nTd).css("cursor", "pointer");
            },
          },
          {
            data: "total",
            fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
              $(nTd).html(oData.total + "개");
            },
          },
        ],
      });
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
    },
  });
};

mnfactureBox.addEventListener("change", (event) => {
  const mnfactureId = event.target.value;
  if (!mnfactureId == "") {
    param = {};
    param.mnfactureId = mnfactureId;
    getListsProductModel(param);
  }
});

$(document).ready(function () {
  const coreEdgeId = 4;
  const defaultMnfactureId = coreEdgeId;
  $("select[name=mnfacture]").val(defaultMnfactureId);
  $(".selectpicker").selectpicker("refresh");
  param = {};
  param.mnfactureId = defaultMnfactureId;
  getListsProductModel(param);
});
