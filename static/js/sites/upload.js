const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
let fileCount = 0;
let addedFiles = 0;

function getProjectValue() {
  return $("#project").val();
}

function getKindValue() {
  return $("#kind").val();
}

$("#submit-btn").click(function(event) {
  event.preventDefault();
  const getProjectValue = $("#project").val();
  if (getProjectValue == "") {
    alert("프로젝트를 선택하세요");
    return false;
  } else {
    const confirmCheck = confirm("파일을 업로드하시겠습니까?");
    if (confirmCheck == true) {
      $("#fine-uploader-manual-trigger").fineUploader("uploadStoredFiles");
    } else {
      return null;
    }
  }
});

$("#fine-uploader-manual-trigger").fineUploader({
  template: "qq-template-manual-trigger",
  request: {
    endpoint: "/sites/document/upload/apply/",
    customHeaders: {
      "X-SCRF-TOKEN": csrfToken
    },
    params: {
      project: getProjectValue,
      kind: getKindValue
    }
  },
  thumbnails: {
    placeholders: {
      waitingPath: "/static/img/waiting-generic.png",
      notAvailablePath: "/static/img/not_available-generic.png"
    }
  },
  autoUpload: false,
  callbacks: {
    onComplete: function(id, fileName, responseJSON) {
      if (responseJSON.success) {
        addedFiles++;
        if (addedFiles == fileCount) {
          alert("문서등록이 완료되었습니다.");
          location.href = "/sites/";
        }
      }
    },
    onError: function() {
      alert("파일 업로드에 실패하였습니다. 다시 시도하여주세요");
      location.href = "/sites/document/upload/";
    },
    onSubmit: function(id, fileName) {
      fileCount++;
    }
  }
});
