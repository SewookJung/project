function report_add_cancel() {
  if (confirm("주간업무보고 신규등록을 취소 하시겠습니까?") == true) {
    location.href = "/weekly/";
  }
}

function checkValues() {
  const client = $("#client_id").val();
  const product = $("#product_id").val();
  const report_date = $("#report_date").val();
  const weekly_comments = $("#weekly_comments").val();

  if (client == "") {
    alert("고객사를 선택하세요");
    return false;
  }

  if (product == "") {
    alert("제품을 선택하세요");
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
