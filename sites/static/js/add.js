function salesIdAdd() {
  const memberId = document.querySelector("#member_id");
  memberId.id = "";
  memberId.id = "sales";
}

salesIdAdd();

function site_add_cancel() {
  if (confirm("문서등록을 취소하시겠습니까?") == true) {
    location.href = "/site";
  } else {
    return false;
  }
}

function site_add_apply() {
  param = {};
  param.project_name = $.trim($("#project_name").val());
  param.status = $.trim($("#status").val());
  param.client_id = $.trim($("#client_id").val());
  param.product_id = $.trim($("#product_id").val());
  param.model_id = $.trim($("#model_id").val());
  param.count = $.trim($("#count").val());
  param.sales = $.trim($("#sales").val());
  param.eng = $.trim($("#member_id").val());
  param.pjStDate = $.trim($("#pjStDate").val());
  param.pjEdDate = $.trim($("#pjEdDate").val());
  param.mnStDate = $.trim($("#mnStDate").val());
  param.mnEdDate = $.trim($("#mnEdDate").val());
  param.comments = $.trim($("#sites_comments").val());

  if (param.project_name == "") {
    $("#project_name").val("");
    alert("프로젝트 명을 입력하세요");
    return null;
  }

  if (param.status == "") {
    $("#status").val("");
    alert("진행상태를 입력하세요");
    return null;
  }

  if (param.client_id == "") {
    $("#client_id").val("");
    alert("고객사를 선택하세요");
    return null;
  }

  if (param.product_id == "") {
    $("#product_id").val("");
    alert("제조사를 선택하세요");
    return null;
  }

  if (param.model_id == "") {
    $("#model_id").val("");
    alert("모델명을 선택하세요");
    return null;
  }

  if (param.count == "") {
    $("#count").val("");
    alert("수량을 선택하세요");
    return null;
  }

  if (param.sales == "") {
    $("#sales").val("");
    alert("담당 영업을 선택하세요");
    return null;
  }

  if (param.eng == "") {
    $("#member_id").val("");
    alert("담당 엔지니어를 선택하세요");
    return null;
  }

  if (param.pjStDate == "") {
    $("#pjStDate").val("");
    alert("시작일을 입력하세요");
    return null;
  }

  if (param.pjEdDate == "") {
    $("#pjEdDate").val("");
    alert("종료 예정일을 입력하세요");
    return null;
  }

  if (param.mnStDate == "") {
    $("#mnStDate").val("");
    alert("유지보수 시작일을 선택하세요");
    return null;
  }

  if (param.mnEdDate == "") {
    $("#mnEdDate").val("");
    alert("유지보수 종료일을 선택하세요");
    return null;
  }

  if (param.comments == "") {
    $("#sites_comments").val("");
    alert("기타를 입력하여주세요");
    return null;
  }

  const url = "/sites/add/apply";
  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  $.ajax({
    type: "POST",
    url: url,
    headers: { "X-CSRFToken": csrfToken },
    data: param,
    success: function() {
      alert("문서가 정상적으로 등록 되었습니다.");
      location.href = "/sites";
    },
    error: function(request, status, error) {
      alert("자산등록이 정상적으로 등록되지 않았습니다.");
    }
  });
}
