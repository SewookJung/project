function checkFileExt(sender) {
  const validExts = new Array(".xlsx", ".xls");
  let fileExt = sender.value;
  const fileTarget = $(".file-upload .upload-hidden");
  const inputField = $(".upload-name");

  fileExt = fileExt.substring(fileExt.lastIndexOf("."));
  if (validExts.indexOf(fileExt) < 0 && fileExt == "") {
    inputField.val("");
  } else if (validExts.indexOf(fileExt) < 0) {
    alert("엑셀파일만 입력 가능 합니다. " + validExts.toString() + " types.");
    sender.value = "";
  } else {
    const fileName = fileTarget[0].files[0].name;
    inputField.val(fileName);
  }
}

function downloadSample() {
  $.ajax({
    url: "/equipment/download/stock/sample/check/",
    success: function (data) {
      window.location = "/equipment/download/stock/sample/";
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
      window.location = "/equipment/stock/upload/";
    },
  });
}

function checkSubmit() {
  if ($("#uploadfile").val() == "") alert("파일을 선택하세요");
  else $("#uploadform").submit();
}
