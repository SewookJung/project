$(document).ready(init());

let transfer;

function init() {
  $.ajax({
    type: "GET",
    url: "/common/member/info/",
    dataType: "json",
    success: function (data) {
      const memberInfo = data["members_data"];
      let settings = {
        tabNameText: "권한자 선택",
        rightTabNameText: "선택된 권한자",
        searchPlaceholderText: "검 색",
        groupDataArray: memberInfo,
        groupItemName: "groupName",
        groupArrayName: "groupData",
        itemName: "name",
        valueName: "value",
        callable: function (items) {},
      };
      transfer = $(".member_permission").transfer(settings);
    },
  });
}
