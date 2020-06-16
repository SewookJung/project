$(document).ready(function () {
  $("#ajaxForm").ajaxForm({
    success: function (data) {
      const comment = JSON.parse(data).comment;
      alert(comment);
      location.href = "/assets/";
    },
    error: function (data) {
      const comment = JSON.parse(data.responseText).comment;
      alert(comment);
      location.href = "/member/password/";
    },
  });
});

function checkValues() {
  const originPassword = $("#origin_password").val();
  const password1 = $("#password1").val();
  const password2 = $("#password2").val();

  if (originPassword == "") {
    alert("현재 비밀번호를 입력하세요.");
    return false;
  }

  if (password1 == "") {
    alert("변경할 비밀번호를 입력하세요.");
    return false;
  }

  if (password2 == "") {
    alert("변경 비밀번호 확인을 입력하세요.");
    return false;
  }
}
