const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
let fileCount = 0;
let addedFiles = 0;

function equipment_add_cancle() {
  if (confirm("고객사 장비운용 등록을 취소하시겠습니까?") == true) {
    location.href = "/equipment/";
  } else {
    return false;
  }
}

$("#submit-btn").click(function(event) {
  event.preventDefault();
  console.log(fileCount);
  const confirmCheck = confirm("파일을 업로드하시겠습니까?");
  if (confirmCheck == true) {
    $("#fine-uploader-manual-trigger").fineUploader("uploadStoredFiles");
  } else {
    return null;
  }
});

$("#fine-uploader-manual-trigger").fineUploader({
  template: "qq-template-manual-trigger",
  request: {
    endpoint: "/equipment/upload/",
    customHeaders: {
      "X-SCRF-TOKEN": csrfToken
    }
  },
  validation: {
    allowedExtensions: ["xlsx"]
  },
  multiple: false,
  messages: {
    typeError:
      "업로드 가능한 파일 확장자는 '*.xlsx'이며, 시트명은'Sheet1'입니다."
  },
  autoUpload: false,
  callbacks: {
    onComplete: function(id, fileName, responseJSON) {
      if (responseJSON.success) {
        addedFiles++;
        if (addedFiles == fileCount) {
          alert("문서등록이 완료되었습니다.");
          location.href = "/equipment/";
        }
      }
    },
    onError: function() {
      alert("파일 업로드에 실패하였습니다. 다시 시도하여주세요");
    },
    onSubmit: function(id, fileName) {
      fileCount++;
      console.log(fileCount);
    },
    onCancel: function(id, filename) {
      fileCount--;
      console.log(fileCount);
    }
  }
});
