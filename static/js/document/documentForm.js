const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const maxUploadfile = 7;
const maxfilesize = 1024 * 1024 * 1024;

let addedFiles = 0;
let fileCount = 0;

const checkCode = () => {
  const checkCodeValue = document.getElementById("checkCode").value;
  return checkCodeValue;
};

const title = () => {
  const title = document.getElementById("title").value;
  return title;
};

const description = () => {
  const description = document.getElementById("description").value;
  return description;
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
    endpoint: "/document/form/upload/apply/",
    customHeaders: {
      "X-SCRF-TOKEN": csrfToken,
    },
    params: {
      checkCode: checkCode,
      title: title,
      desc: description,
    },
  },

  callbacks: {
    onComplete: function (id, fileName, responseJSON) {
      addedFiles++;
      if (addedFiles == fileCount) {
        alert(responseJSON.msg);
        window.location = "/document/form/";
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

const attachFiles = () => {
  $("#fine-uploader-manual-trigger").fineUploader("uploadStoredFiles");
};

const documentBasicFormExistsCheck = (event) => {
  const documentId = event.target.value;
  $.ajax({
    type: "GET",
    url: `/document/form/${documentId}/`,
    headers: { "X-CSRFToken": csrfToken },
    dataType: "json",
    success: function (data) {
      window.location = `/document/form/${documentId}/download/`;
    },
    error: function (request, status, error) {
      const errorMsg = request.responseJSON.msg;
      alert(errorMsg);
    },
  });
};

const documentBasicFormDelete = (documentId) => {
  if (confirm("양식을 삭제 하시겠습니까?")) {
    $.ajax({
      type: "DELETE",
      url: `/document/form/${documentId}/delete/`,
      headers: { "X-CSRFToken": csrfToken },
      dataType: "json",
      success: function (data) {
        const successMsg = data.msg;
        alert(successMsg);
        window.location = "/document/form/";
      },
      error: function (request, status, error) {
        const errorMsg = request.responseJSON.msg;
        alert(errorMsg);
      },
    });
  } else return false;
};

const formUploadSubmit = () => {
  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;

  if (!title) {
    alert("제목을 입력해 주세요.");
    return false;
  }

  if (!description) {
    alert("설명을 입력해 주세요.");
    return false;
  }
  attachFiles();
};
