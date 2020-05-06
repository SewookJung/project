$(document).ready(function () {
  $(".return_form").hide();
  $(".rent_form").hide();
  $(".renter_form").hide();

  const selectboxs = document.querySelectorAll("#member_id");
  selectboxs[1].id = "renter_id";

  $("#asset_is-state").on("change", function (e) {
    const isStateValue = this.value;
    if (isStateValue == 3) {
      $(".return_form").show();
      $(".rent_form").show();
      $(".renter_form").show();
    } else {
      $(".return_form").hide();
      $(".rent_form").hide();
      $(".renter_form").hide();
    }
  });
});

function asset_add_cancel() {
  if (confirm("자산 등록을 취소하시겠습니까?") == true) {
    location.href = "/assets/";
  } else {
    return false;
  }
}

function asset_add_apply() {
  const isStateValue = $("#asset_is-state").val();

  param = {};
  param.mnfacture = $.trim($("#asset_mnfacture").val());
  param.purchase_date = $.trim($("#datepicker1").val());
  param.comments = $.trim($("#asset_comments").val());
  param.memberId = $.trim($("#member_id").val());
  param.where = $.trim($("#asset_is-where").val());
  param.hardDisk = $.trim($("#asset_harddisk").val());
  param.cpu = $.trim($("#asset_cpu").val());
  param.model = $.trim($("#asset_model").val());
  param.serial = $.trim($("#asset_serial").val());
  param.state = $.trim($("#asset_is-state").val());
  param.memory = $.trim($("#asset_memory").val());

  if (isStateValue == 3) {
    const getButtonElements = document.querySelectorAll("button");
    getButtonElements.forEach((buttons) => {
      let getButtonElements = buttons.getAttribute("data-id");
      if (getButtonElements == "renter_id") {
        let memberNameValue = buttons.innerText;
        param.memberName = memberNameValue;
      }
    });
    param.rentDate = $.trim($("#rent_date").val());
    param.returnDate = $.trim($("#return_date").val());
  }

  if (param.memberId == "") {
    $("#member_id").val("");
    alert("소유자를 선택하세요");
    return null;
  }

  if (param.mnfacture == "") {
    $("#asset_mnfacture").val("");
    alert("제조사를 입력하세요");
    return null;
  }

  if (param.model == "") {
    $("#asset_model").val("");
    alert("모델명을 입력하세요");
    return null;
  }

  if (param.serial == "") {
    $("#asset_serial").val("");
    alert("시리얼을 입력하세요");
    return null;
  }

  if (param.state == "") {
    $("#asset_is-state").val("");
    alert("자산 상태를 선택하세요");
    return null;
  }

  if (param.cpu == "") {
    $("#asset_cpu").val("");
    alert("CPU를 입력하세요");
    return null;
  }

  if (param.memory == "") {
    $("#asset_memory").val("");
    alert("메모리를 입력하세요");
    return null;
  }

  if (param.hardDisk == "") {
    $("#asset_hardDisk").val("");
    alert("디스크를 입력하세요");
    return null;
  }

  if (param.where == "") {
    $("#asset_is-state").val("");
    alert("사용장소를 입력하세요");
    return null;
  }

  if (param.purchase_date == "") {
    $("#datepicker1").val("");
    alert("구매 날짜를 선택하세요");
    return null;
  }

  if (param.rentDate == "") {
    $("#rent_date").val("");
    alert("대여 날짜를 선택하세요");
    return null;
  }

  if (param.returnDate == "") {
    $("#return_date").val("");
    alert("반납 날짜를 선택하세요");
    return null;
  }
  const url = "/assets/add/apply";
  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  $.ajax({
    type: "POST",
    url: url,
    headers: { "X-CSRFToken": csrfToken },
    data: param,
    success: function () {
      alert("자산등록이 완료 되었습니다.");
      window.location.href = "/assets/";
    },
    error: function (request, status, error) {
      alert("자산등록이 정상적으로 등록되지 않았습니다.");
    },
  });
}
