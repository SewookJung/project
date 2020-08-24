const goToDetailPage = (event, productId, status) => {
  const selectedStockCount = Number(event.target.innerText);
  if (selectedStockCount < 1) alert("선택한 목록이 존재하지 않습니다.");
  else window.location = `/equipment/stock/${productId}/${status}`;
};
