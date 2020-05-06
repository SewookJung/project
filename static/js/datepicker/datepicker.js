$(function () {
  $(
    "#datepicker1, #datepicker2, #mnStDate, #mnEdDate, #pjStDate, #pjEdDate, #report_date, #rent_date, #return_date"
  ).datepicker({
    format: "yyyy-mm-dd", //데이터 포맷 형식(yyyy : 년 mm : 월 dd : 일 )
    autoclose: true, //사용자가 날짜를 클릭하면 자동 캘린더가 닫히는 옵션
    datesDisabled: ["2019-06-24", "2019-06-26"], //선택 불가능한 일 설정 하는 배열 위에 있는 format 과 형식이 같아야함.
    daysOfWeekHighlighted: [3], //강조 되어야 하는 요일 설정
    templates: {
      leftArrow: "&laquo;",
      rightArrow: "&raquo;",
    }, //다음달 이전달로 넘어가는 화살표 모양 커스텀 마이징
    showWeekDays: true, // 위에 요일 보여주는 옵션 기본값 : true
    todayHighlight: true, //오늘 날짜에 하이라이팅 기능 기본값 :false
    language: "ko", //달력의 언어 선택, 그에 맞는 js로 교체해줘야한다.
    todayBtn: "linked",
    showMonthAfterYear: true,
  }); //datepicker end
}); //ready end
