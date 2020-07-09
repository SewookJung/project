function downloadFile(documentId) {
  $.ajax({
    url: "/sites/document/download/check/" + documentId + "/",
    success: function (data) {
      window.location = "/sites/document/download/" + documentId + "/";
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
      window.location = "/sites/";
    },
  });
}
