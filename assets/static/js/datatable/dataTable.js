$(document).ready(function() {
  $("#asset__table").DataTable({
    order: [
      [3, "asc"],
      [0, "asc"]
    ]
  });
  $("#myTable1").DataTable({});
  $("#myTable2").DataTable({});
});
