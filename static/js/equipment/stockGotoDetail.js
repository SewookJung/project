const goToDetailPage = (event, productId, status) => {
  const selectedTd = event.target.innerText;
  const selectedStockCount = Number(selectedTd.charAt(0));

  if (selectedStockCount < 1) alert("선택한 목록이 존재하지 않습니다.");
  else window.location = `/equipment/stock/${productId}/${status}`;
};

const goToAllStockPage = (mnfacture) => {
  window.location = `/equipment/stock/${mnfacture}/all/detail/`;
};
