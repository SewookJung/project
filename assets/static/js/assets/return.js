function asset_return(asset_id) {
  if (confirm("자산을 반납하시겠습니까?") == true) {
    const url = "/assets/status/return/";
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0]
      .value;

    param = {};
    param.assetId = asset_id;

    $.ajax({
      type: "POST",
      url: url,
      headers: { "X-CSRFToken": csrfToken },
      data: param,
      success: function() {
        alert("자산이 반납 되었습니다.");
        window.location.href = "/assets/status";
      },
      error: function(request, status, error) {
        alert("자산 반납에 실패하였습니다.");
      }
    });
  } else {
    return false;
  }
}
