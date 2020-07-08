const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const maxUploadfile = 7;
const maxfilesize = 1024 * 1024 * 1024;
let fileCount = 0;
let addedFiles = 0;

function getCheckCode() {
  return $("#check_code").val();
}

function getDocumentId() {
  return $("#document_id").val();
}

function document_upload_cancel() {
  if (confirm("문서등록을 취소하시겠습니까?") == true) {
    location.href = "/sites/";
  } else {
    return false;
  }
}

$("select").on("change", function () {
  selecteMiddleClass();
});

function clearMiddleClass() {
  const middleClasses = document.querySelectorAll("#middle__class-form");
  middleClasses.forEach((selectBox) => {
    selectBox.style.display = "none";
  });
}

function selecteMiddleClass() {
  const documentKind = $("#kind").val();
  const preMiddleClass = document.querySelector(".pre__middle-class");
  const proMiddleClass = document.querySelector(".pro__middle-class");
  const exaMiddleClass = document.querySelector(".exa__middle-class");
  const manMiddleClass = document.querySelector(".man__middle-class");
  const etcMiddleClass = document.querySelector(".etc__middle-class");

  if (documentKind == "PRE") {
    clearMiddleClass();
    preMiddleClass.style.display = "block";
  } else if (documentKind == "PRO") {
    clearMiddleClass();
    proMiddleClass.style.display = "block";
  } else if (documentKind == "EXA") {
    clearMiddleClass();
    exaMiddleClass.style.display = "block";
  } else if (documentKind == "MAN") {
    clearMiddleClass();
    manMiddleClass.style.display = "block";
  } else {
    clearMiddleClass();
    etcMiddleClass.style.display = "block";
  }
}

$(document).ready(init());

let transfer;

function init() {
  const middleClass = document.getElementById("middle__class-form");
  middleClass.style.display = "none";
  selecteMiddleClass();
  $.ajax({
    type: "GET",
    url: "/sites/document/auth/",
    dataType: "json",
    success: function (data) {
      const memberInfo = data["member_info"];
      let settings = {
        tabNameText: "권한자 선택",
        rightTabNameText: "선택된 권한자",
        searchPlaceholderText: "검 색",
        groupDataArray: memberInfo,
        groupItemName: "groupName",
        groupArrayName: "groupData",
        itemName: "name",
        valueName: "value",
        callable: function (items) {},
      };
      transfer = $(".member_permission").transfer(settings);
    },
  });
}

function site_reg_document() {
  const acceptPermissionMember = transfer.getSelectedItems();
  const serializeData = JSON.stringify(acceptPermissionMember);
  const documentKind = $("#kind").val();

  if ($("#project").val() == "") {
    alert("프로젝트를 선택하세요");
    return false;
  }

  if (acceptPermissionMember.length == 0) {
    alert("문서등록에 대한 권한자를 선택해주세요");
    return null;
  }

  param = {};
  param.project = $("#project").val();
  param.kind = $("#kind").val();
  param.permission = serializeData;

  if (documentKind == "PRE") {
    param.middleClass = $("#preMiddleClass").val();
  } else if (documentKind == "PRO") {
    param.middleClass = $("#proMiddleClass").val();
  } else if (documentKind == "EXA") {
    param.middleClass = $("#exaMiddleClass").val();
  } else if (documentKind == "MAN") {
    param.middleClass = $("#manMiddleClass").val();
  } else {
    param.middleClass = $("#etcMiddleClass").val();
  }

  $.ajax({
    type: "POST",
    url: "/sites/document/reg/",
    headers: { "X-CSRFToken": csrfToken },
    dataType: "json",
    data: param,
    success: function (data) {
      if (data.success) {
        if (fileCount == 0) {
          location.href = "/sites/";
          alert("문서등록이 완료되었습니다.");
        } else {
          $("#document_id").val(data.document_id);
          $("#fine-uploader-manual-trigger").fineUploader("uploadStoredFiles");
        }
      } else {
        alert("문서등록 작업이 정상적으로 이루어 지지 않았습니다-0.");
      }
    },
    error: function (request, status, error) {
      alert("문서등록 작업이 정상적으로 이루어 지지 않았습니다-1.");
    },
  });
}

$("#submit-btn").click(function (event) {
  event.preventDefault();
  if (fileCount == 0) {
    if (!confirm("첨부 파일이 없습니다. 그대로 진행 하시겠습니까?")) return;
    else site_reg_document();
  } else {
    if (confirm("파일을 업로드하시겠습니까?")) site_reg_document();
  }
});

$("#fine-uploader-manual-trigger").fineUploader({
  template: "qq-template-manual-trigger",
  debug: false,
  autoUpload: false,
  maxConnections: maxUploadfile,
  validation: {
    allowedExtensions: [
      "pptx",
      "ppt",
      "doc",
      "docx",
      "xls",
      "xlsx",
      "jpg",
      "jpeg",
      "png",
      "gif",
      "pdf",
      "zip",
      "txt",
      "log",
    ],
    allowEmpty: false,
    itemLimit: maxUploadfile,
    sizeLimit: maxfilesize,
  },
  messages: {
    typeError: "업로드가 불가능 한 확장자 파일 입니다, {file}.",
    sizeError: "파일 사이즈는 10M를 넘을 수 없습니다, {file}",
  },
  request: {
    endpoint: "/sites/document/upload/apply/",
    customHeaders: {
      "X-SCRF-TOKEN": csrfToken,
    },
    params: {
      document_id: getDocumentId,
      check_code: getCheckCode,
    },
  },

  callbacks: {
    onComplete: function (id, fileName, responseJSON) {
      if (responseJSON.success) {
        addedFiles++;
        if (addedFiles == fileCount) {
          alert("문서등록이 완료되었습니다.");
          location.href = "/sites/";
        }
      } else {
        $.ajax({
          type: "POST",
          url: "/sites/document/reg/delete/",
          headers: { "X-CSRFToken": csrfToken },
          dataType: "json",
          data: { document_id: getDocumentId },
          success: function (data) {
            console.log(data.success);
            if (data.success) {
              alert(responseJSON.error);
              window.location = "/sites/document/upload/";
            }
          },
          error: function (request, status, error) {
            alert(
              "문서삭제가 정상적으로 이루어지지 않았습니다.\n다시 시도해주시기 바랍니다."
            );
          },
        });
      }
    },
    onSubmit: function (id, fileName, responseJSON) {
      fileCount++;
    },
    onCancel: function (id, filename) {
      fileCount--;
    },
  },
});
