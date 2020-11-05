const authCheck = (event) => {
  event.preventDefault();

  const memberId = document.getElementById("memberId").value;
  const memberPw = document.getElementById("memberPw").value;
  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  if (!memberId) {
    alert("아이디를 입력하세요");
    return false;
  }

  if (!memberPw) {
    alert("패스워드를 입력하세요");
    return false;
  }

  let param = new Object();
  param.memberId = memberId;
  param.memberPw = memberPw;

  $.ajax({
    type: "POST",
    url: "/login/check/",
    data: param,
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      window.location = data.redirect_url;
    },
    error: function (request, status, error) {
      const errorMsg = request.responseJSON.msg;
      alert(errorMsg);
      location.reload();
    },
  });
};
