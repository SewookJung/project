const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

function equipment_add_cancel() {
  const equipmentAttachId = $("#equipment-attach-id").val();
  $.ajax({
    type: "POST",
    url: "/equipment/upload_cancel/",
    dataType: "json",
    data: { equipment_attach_id: equipmentAttachId },
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const deleteSuccessMsg = data.msg;
      alert(deleteSuccessMsg);
      location.href = "/equipment/";
    },
    error: function (request, status, error) {
      const deleteFailMsg = JSON.parse(request.responseText).error;
      alert(deleteFailMsg);
      location.href = "/equipment/upload/";
    },
  });
}
