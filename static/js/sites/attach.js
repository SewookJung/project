const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
console.log(csrfToken);
const maxUploadfile = 1;
const maxfilesize = 1024 * 1024 * 1024;
let fileCount = 0;
let addedFiles = 0;

function getCheckCode() {
  return $("#check_code").val();
}

function getDocumentId() {
  return $("#document_id").val();
}

function document_delete() {
  const attachmentId = $("input[name=document_attach-id").val();
  if (confirm("업로드한 파일을 삭제하시겠습니까?") == true) {
    location.href = "/sites/document/" + attachmentId + "/delete/";
  } else {
    return false;
  }
}

$(document).ready(init());

let transfer;

function init() {
  const projectId = $("input[name=project_id]").val();
  const attachmentId = $("input[name=document_attach-id").val();
  const documentKind = $("input[name=document_kind]").val();
  $("select[name=project]").val(projectId);
  $("select[name=kind]").val(documentKind);
  $("select[name=project]").prop("disabled", true);
  $(".selectpicker").selectpicker("refresh");
  $.ajax({
    type: "GET",
    url: "/sites/document/" + attachmentId + "/auth/",
    dataType: "json",
    data: { attachmentId: attachmentId },
    success: function (data) {
      const memberInfo = data["auth_info"];
      let settings = {
        tabNameText: "권한자 선택",
        rightTabNameText: "선택된 권한자",
        searchPlaceholderText: "검 색",
        groupDataArray: memberInfo,
        groupItemName: "groupName",
        groupArrayName: "groupData",
        itemName: "name",
        valueName: "value",
        callable: function (items) {
          console.log(items);
        },
      };
      transfer = $(".member_permission").transfer(settings);
    },
  });
}

function site_reg_document() {
  const acceptPermissionMember = transfer.getSelectedItems();
  const serializeData = JSON.stringify(acceptPermissionMember);
  const attachmentId = $("input[name=document_attach-id").val();

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

  $.ajax({
    type: "POST",
    url: "/sites/document/" + attachmentId + "/detail/apply/",
    headers: { "X-CSRFToken": csrfToken },
    dataType: "json",
    data: param,
    success: function (data) {
      if (data.success) {
        $("#document_id").val(data.document_id);
        $("#fine-uploader-manual-trigger").fineUploader("uploadStoredFiles");
      } else {
        alert("문서등록 작업이 정상적으로 이루어 지지 않았습니다.");
      }
    },
    error: function (request, status, error) {
      alert("문서등록 작업이 정상적으로 이루어 지지 않았습니다.");
    },
  });
}

function document_modify_cancel() {
  if (confirm("수정을 취소하시겠습니까?")) {
    location.href = "/sites/";
  } else {
    return false;
  }
}

$("#submit-btn").click(function (event) {
  event.preventDefault();
  if (fileCount == 0) {
    if (!confirm("첨부 파일이 없습니다. 그대로 진행 하시겠습니까?")) return;
  }
  if (confirm("파일을 업로드하시겠습니까?")) site_reg_document();
});

$("#fine-uploader-manual-trigger").fineUploader({
  template: "qq-template-manual-trigger",
  debug: false,
  autoUpload: false,
  maxConnections: maxUploadfile,
  multiple: false,
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
    endpoint: "/sites/document/attach/detail/apply/",
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
        alert(
          "파일 업로드에 실패하였습니다. 다시 시도하여주세요." +
            responseJSON.error
        );
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
