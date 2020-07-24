const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

function stockAddCancel() {
  const equipmentAttachId = $("#equipment-attach-id").val();
  $.ajax({
    type: "POST",
    url: "/equipment/stock/upload-cancel/",
    dataType: "json",
    data: { equipment_attach_id: equipmentAttachId },
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const deleteSuccessMsg = data.msg;
      alert(deleteSuccessMsg);
      location.href = "/equipment/stock/";
    },
    error: function (request, status, error) {
      const deleteFailMsg = JSON.parse(request.responseText).error;
      alert(deleteFailMsg);
      location.href = "/equipment/stock/upload/";
    },
  });
}

function returnStockUpload() {
  window.location = "/equipment/stock/upload/";
}
