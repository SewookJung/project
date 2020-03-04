function asset_rent(asset_id, asset_mnfacture, asset_model) {
  $("#asset_mnfacture").append(asset_mnfacture, " (", asset_model, ")");
  $("#asset_id").val(asset_id);
  $("#exampleModal").modal("show");
}

function asset_rent_cancel() {
  $("#exampleModal").modal("hide");
  $("#asset_mnfacture").text("");
  $("#datepicker1").val("");
  $("#datepicker2").val("");
  $("#asset_comments").val("");
}

function asset_rent_apply() {
  const selectValue = document.querySelector(".filter-option-inner-inner")
    .innerHTML;
  param = {};
  param.mnfacture = $.trim($("#asset_mnfacture").text());
  param.stDate = $.trim($("#datepicker1").val());
  param.edDate = $.trim($("#datepicker2").val());
  param.comments = $.trim($("#asset_comments").val());
  param.assetId = $.trim($("#asset_id").val());
  param.memberId = $.trim($("#member_id").val());
  param.memberName = $.trim(selectValue);

  if (param.stDate == "") {
    $("#datepicker1").val("");
    alert("대여 날짜를 선택하세요");
    return null;
  }

  if (param.edDate == "") {
    $("#datepicker2").val("");
    alert("반납 날짜를 선택하세요");
    return null;
  }

  if (selectValue == "---------") {
    alert("대여자를 선택하시오!");
    return null;
  }

  const url = "/assets/status/apply/";
  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  $.ajax({
    type: "POST",
    url: url,
    headers: { "X-CSRFToken": csrfToken },
    data: param,
    success: function() {
      alert("자산신청이 완료되었습니다.");
      window.location.href = "/assets/status";
    },
    error: function(request, status, error) {
      alert("자산신청에 실패하였습니다.");
    }
  });
}
