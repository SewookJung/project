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
  });
});
