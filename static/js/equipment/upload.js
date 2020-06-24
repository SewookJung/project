function check_file_ext(sender) {
  var validExts = new Array(".xlsx", ".xls");
  var fileExt = sender.value;
  fileExt = fileExt.substring(fileExt.lastIndexOf("."));
  if (validExts.indexOf(fileExt) < 0) {
    alert("엑셀파일만 입력 가능 합니다. " + validExts.toString() + " types.");
    sender.value = "";
  }
}

function check_submit(sender) {
  if ($("#uploadfile").val() == "") alert("파일을 선택하세요");
  else $("#uploadform").submit();
}
