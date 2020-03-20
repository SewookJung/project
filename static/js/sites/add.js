function site_add_cancel() {
  if (confirm("문서등록을 취소하시겠습니까?") == true) {
    location.href = "/sites/";
  } else {
    return false;
  }
}

function checkValues() {
  const projectName = $("#project_name").val();
  const status = $("#status").val();
  const clientId = $("#client_id").val();
  const productId = $("#product_id").val();
  const sales = $("#sales").val();
  const eng = $("#member_id").val();
  const pjStDate = $("#pjStDate").val();
  const pjEdDate = $("#pjEdDate").val();
  const mnStDate = $("#mnStDate").val();
  const mnEdDate = $("#mnEdDate").val();
  const mnCycle = $("#cycle").val();

  if (projectName == "") {
    alert("프로젝트 명을 입력하세요");
    return false;
  }

  if (clientId == "") {
    alert("고객사를 선택하세요");
    return false;
  }

  if (productId == "") {
    alert("제조사를 선택하세요");
    return false;
  }

  if (status == "") {
    alert("진행상태를 입력하세요");
    return false;
  }
  if (sales == "") {
    alert("담당 영업을 선택하세요");
    return false;
  }

  if (eng == "") {
    alert("담당 엔지니어를 선택하세요");
    return false;
  }

  if (pjStDate == "") {
    alert("시작일을 입력하세요");
    return false;
  }

  if (pjEdDate == "") {
    alert("종료 예정일을 입력하세요");
    return false;
  }

  if (mnCycle == "") {
    alert("유지보수 주기를 선택하세요");
    return false;
  }

  if (mnStDate == "") {
    alert("유지보수 시작일을 선택하세요");
    return false;
  }

  if (mnEdDate == "") {
    alert("유지보수 종료일을 선택하세요");
    return false;
  }
}
