const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const clientSelectBox = document.getElementById("client");
const existsCheckClient = document.getElementById("existsClient");
const maxUploadfile = 7;
const maxfilesize = 1024 * 1024 * 1024;

let addedFiles = 0;
let fileCount = 0;
let transfer;

const category = () => {
  const categoryValue = document.getElementById("category").value;
  return categoryValue;
};

const checkCode = () => {
  const checkCodeValue = document.getElementById("checkCode").value;
  return checkCodeValue;
};

const client = () => {
  const clientValue = document.getElementById("client").value;
  return clientValue;
};

const mnfacture = () => {
  const mnfactureValue = document.getElementById("mnfacture").value;
  return mnfactureValue;
};

const permissions = () => {
  const acceptPermissionMember = transfer.getSelectedItems();
  const serializePermissions = JSON.stringify(acceptPermissionMember);
  return serializePermissions;
};

const project = () => {
  const projectValue = document.getElementById("project").value;
  return projectValue;
};

const product = () => {
  const productValue = document.getElementById("product").value;
  return productValue;
};

const document_upload_cancel = () => {
  if (confirm("문서등록을 취소하시겠습니까?") == true) {
    location.href = "/document/";
  } else {
    return false;
  }
};

const init = () => {
  $.ajax({
    type: "GET",
    url: "/document/auth/",
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
  $(".selectpicker").prop("disabled", true);
  $("#client").prop("disabled", false);
  $(".selectpicker").selectpicker("refresh");
};

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
    endpoint: "/document/upload/apply/",
    customHeaders: {
      "X-SCRF-TOKEN": csrfToken,
    },
    params: {
      client: client,
      category: category,
      checkCode: checkCode,
      mnfacture: mnfacture,
      permissions: permissions,
      product: product,
      project: project,
    },
  },

  callbacks: {
    onComplete: function (id, fileName, responseJSON) {
      addedFiles++;
      if (addedFiles == fileCount) {
        alert(responseJSON.msg);
        window.location = "/document/";
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

clientSelectBox.addEventListener("change", (event) => {
  const clientId = event.target.value;
  if (clientId) {
    $.ajax({
      type: "GET",
      url: `/project/${clientId}/lists/`,
      headers: { "X-CSRFToken": csrfToken },
      dataType: "json",
      success: function (data) {
        const reports = data.reports;
        $(".selectpicker").prop("disabled", false);
        $("#project").find("option").remove();
        $("#project").append('<option value="0">선택 안함</option>');
        $("#project").append('<option data-divider="true"></option>');
        $("#project").selectpicker({ title: "프로젝트 선택" });

        for (let i = 0; i < reports.length; i++) {
          const reportId = reports[i]["id"];
          const reportTitle = reports[i]["title"];
          $("#project").append(
            `<option value="${reportId}">${reportTitle}</option>`
          );
        }

        $(".selectpicker").selectpicker("refresh");
      },
      error: function (request, status, error) {
        $("#project").find("option").remove();
        $("#project").append('<option value="0">선택 안함</option>');
        $(".selectpicker").prop("disabled", false);
        $(".selectpicker").selectpicker("refresh");
      },
    });
  } else {
    $(".selectpicker").prop("disabled", true);
    $("#client").prop("disabled", false);
    $(".selectpicker").selectpicker("refresh");
  }
});

init();

const attachFiles = () => {
  $("#fine-uploader-manual-trigger").fineUploader("uploadStoredFiles");
};

const document_upload_apply = (event) => {
  event.preventDefault();
  const acceptPermissionMember = transfer.getSelectedItems();
  const clientValue = document.getElementById("client").value;
  const projectValue = document.getElementById("project").value;

  if (!clientValue) {
    alert("고객사를 선택하세요");
    return false;
  }

  if (!projectValue) {
    alert("관련 프로젝트를 선택하세요");
    return false;
  }

  if (!acceptPermissionMember.length) {
    alert("문서등록에 대한 권한자를 선택해주세요");
    return false;
  }

  if (fileCount == 0) {
    if (confirm("첨부 파일이 없습니다. 그대로 진행하시겠습니까?"))
      attachFiles();
    else return false;
  } else {
    if (confirm("파일을 업로드 하시겠습니까?")) attachFiles();
    else return false;
  }
};
