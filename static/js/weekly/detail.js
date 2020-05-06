function delete_report() {
  const reportPkValue = $("input[name=report_pk]").val();
  if (confirm("주간업무보고를 삭제 하시겠습니까?") == true) {
    location.href = `/weekly/${reportPkValue}/delete/`;
  } else {
    return false;
  }
}

function report_add_cancel() {
  const reportPkValue = $("input[name=report_pk]").val();
  if (reportPkValue == "") {
    if (confirm("주간업무보고를 취소하시겠습니까?") == true) {
      location.href = "/weekly/";
    }
  } else {
    if (confirm("주간업무보고 수정을 취소하시겠습니까?") == true) {
      location.href = "/weekly/";
    }
  }
}

$(document).ready(function () {
  const productId = $("input[name=product_id]").val();
  const salesType = $("input[name=sales_type_value]").val();
  $("select[name=product]").val(productId);
  $("select[name=sales_type]").val(salesType);
  $(".selectpicker").selectpicker("refresh");
  $("#ajaxForm").ajaxForm({
    success: function (data) {
      alert("주간업무보고 작성을 완료하였습니다.");
      location.href = "/weekly/";
    },
    error: function () {
      alert("주간업무보고 작성에 실패하였습니다.");
    },
  });
});

function checkValues() {
  const product = $("#product_id").val();
  const sales_type = $("#sales_type_id").val();
  const report_date = $("#report_date").val();
  const weekly_comments = $("#weekly_comments").val();

  if (product == "") {
    alert("제조사를 선택하세요");
    return false;
  }

  if (sales_type == "") {
    alert("분류를 선택하세요");
    return false;
  }

  if (report_date == "") {
    alert("일자를 선택하세요");
    return false;
  }

  if (weekly_comments == "") {
    alert("금주 진행사항을 입력하세요");
    return false;
  }
}
