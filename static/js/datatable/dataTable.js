$(document).ready(function () {
  $("#asset__table").DataTable({
    order: [
      [3, "asc"],
      [0, "asc"],
    ],
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
  });

  $("#myTable1").DataTable({
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
  });

  $("#sites_table").DataTable({
    columnDefs: [
      { orderable: true, targets: [0] },
      { orderable: false, targets: "_all" },
    ],
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
  });

  $("#weekly_table").DataTable({
    pageLength: 15,
    lengthMenu: [5, 10, 15, 20, 30, 50, 100],
    columnDefs: [
      { orderable: true, targets: [0, 1] },
      { orderable: false, targets: "_all" },
    ],
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
  });

  $("#doument_attach").DataTable({
    pageLength: 15,
    lengthMenu: [5, 10, 15, 20, 30, 50, 100],
    columnDefs: [
      { orderable: true, targets: [2] },
      { orderable: false, targets: "_all" },
    ],
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
    order: [[2, "dec"]],
  });

  $("#doument_attach_detail").DataTable({
    pageLength: 15,
    lengthMenu: [5, 10, 15, 20, 30, 50, 100],
    columnDefs: [
      { orderable: true, targets: [1] },
      { orderable: false, targets: "_all" },
    ],
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
    order: [[1, "dec"]],
  });

  $("#equipmentAllTable").DataTable({
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
    initComplete: function () {
      this.api()
        .columns(1)
        .every(function () {
          var column = this;
          var select = $(
            '<select class="selectpicker" title="제조사 선택" data-live-search=true><option value="">전체</option></select>'
          )
            .appendTo($("#select-mnfacture").empty())
            .on("change", function () {
              var val = $.fn.dataTable.util.escapeRegex($(this).val());
              column.search(val ? "^" + val + "$" : "", true, false).draw();
            });

          column
            .data()
            .unique()
            .sort()
            .each(function (d, j) {
              select.append('<option value="' + d + '">' + d + "</option>");
            });
        });
    },
  });

  $("#stockAllTable").DataTable({
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
    order: [[3, "desc"]],
    columnDefs: [
      {
        targets: [4],
        visible: false,
      },
    ],
    initComplete: function () {
      this.api()
        .columns(1)
        .every(function () {
          var column = this;
          var select = $(
            '<select class="selectpicker" title="모델명" data-live-search=true><option value="">전체</option></select>'
          )
            .appendTo($("#stock-product-model").empty())
            .on("change", function () {
              var val = $.fn.dataTable.util.escapeRegex($(this).val());
              column.search(val ? "^" + val + "$" : "", true, false).draw();
            });

          column
            .data()
            .unique()
            .sort()
            .each(function (d, j) {
              select.append('<option value="' + d + '">' + d + "</option>");
            });
        });

      this.api()
        .columns(4)
        .every(function () {
          var column = this;
          var select = $(
            '<select class="selectpicker" title="입고 일자" data-live-search=true><option value="">전체</option></select>'
          )
            .appendTo($("#stock-receive-date").empty())
            .on("change", function () {
              var val = $.fn.dataTable.util.escapeRegex($(this).val());
              column.search(val ? "^" + val + "$" : "", true, false).draw();
              var stockTable = $("#stockAllTable").DataTable();
              stockTable.column("3:visible").order("desc").draw();
            });

          column
            .data()
            .unique()
            .sort()
            .each(function (d, j) {
              select.append('<option value="' + d + '">' + d + "</option>");
            });
        });

      this.api()
        .columns(5)
        .every(function () {
          var column = this;
          var select = $(
            '<select class="selectpicker" title="상태" data-live-search=true><option value="">전체</option></select>'
          )
            .appendTo($("#stock-status").empty())
            .on("change", function () {
              var val = $.fn.dataTable.util.escapeRegex($(this).val());
              column.search(val ? "^" + val + "$" : "", true, false).draw();
            });

          column
            .data()
            .unique()
            .sort()
            .each(function (d, j) {
              select.append('<option value="' + d + '">' + d + "</option>");
            });
        });
    },
  });

  $("#documentBasicFormTable").DataTable({
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
  });
});
