const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const clientSelectBox = document.getElementById("client");

const deleteDocument = (event) => {
  const documentId = event.target.value;

  if (confirm("해당 문서를 삭제 하시겠습니까?")) {
    $.ajax({
      type: "DELETE",
      url: `/document/${documentId}/`,
      dataType: "json",
      headers: { "X-CSRFToken": csrfToken },
      success: function (data) {
        const documentTable = $("#documentTable").DataTable();
        const successMsg = data.msg;
        alert(successMsg);
        documentTable.row(event.target.parentNode.parentNode).remove().draw();
      },
      error: function (request, status, error) {
        alert("문서를 삭제하는데 실패하였습니다.\n다시 시도해주세요.");
        location.href = location.href;
      },
    });
  } else return false;
};

const getClientAttachLists = (clientId) => {
  $.ajax({
    type: "GET",
    url: `/document/${clientId}/attach/lists/`,
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const documents = data.data;
      const documentTable = $("#documentTable").DataTable();
      documentTable.destroy();
      $("#documentTable").DataTable({
        data: documents,
        language: {
          paginate: {
            previous: "‹",
            next: "›",
          },
        },
        aoColumns: [
          { mData: "id" },
          {
            mData: "project",
            fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
              if (oData.project == 0) {
                oData.project = "N/A";
              }
              $(nTd).html(oData.project);
            },
          },
          {
            mData: function (data, type, dataToSet) {
              const link = `<a href="/document/${data.id}/download/">${data.attach_name}</a>`;
              return link;
            },
          },
          {
            mData: function (data, type, dataToSet) {
              const loginMemberName = data.login_member_name;
              const creator = data.creator;
              if (loginMemberName == creator) {
                const badge = `${data.product} <span class="badge badge-primary" data-toggle="modal" data-target="#productModal">수정</span>`;
                return badge;
              } else {
                return data.product;
              }
            },
          },
          {
            mData: function (data, type, dataToSet) {
              const loginMemberName = data.login_member_name;
              const creator = data.creator;

              if (loginMemberName == creator) {
                const badge = `${data.category} <span class="badge badge-primary" data-toggle="modal" data-target="#categoryModal">수정</span>`;
                return badge;
              } else {
                return data.product;
              }
            },
          },
          { mData: "creator" },
          { mData: "created_at" },
          { mData: "id" },
        ],
        initComplete: function () {
          this.api()
            .columns(1)
            .every(function () {
              var column = this;
              var select = $(
                '<select class="selectpicker" title="프로젝트 선택" data-live-search=true><option value="">전체</option></select>'
              )
                .appendTo($("#select-project").empty())
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
            .columns(3)
            .every(function () {
              var column = this;
              var select = $(
                '<select class="selectpicker" title="제품명 선택" data-live-search=true><option value="">전체</option></select>'
              )
                .appendTo($("#select-product").empty())
                .on("change", function () {
                  var val = $.fn.dataTable.util.escapeRegex($(this).val());
                  column.search(val, true, true).draw();
                });

              column
                .data()
                .unique()
                .sort()
                .each(function (d, j) {
                  d = d.split(" ")[0];
                  select.append('<option value="' + d + '">' + d + "</option>");
                });
            });

          this.api()
            .columns(4)
            .every(function () {
              var column = this;
              var select = $(
                '<select class="selectpicker" title="구분 선택" data-live-search=true><option value="">전체</option></select>'
              )
                .appendTo($("#select-category").empty())
                .on("change", function () {
                  var val = $.fn.dataTable.util.escapeRegex($(this).val());
                  column.search(val, true, true).draw();
                });

              column
                .data()
                .unique()
                .sort()
                .each(function (d, j) {
                  d = d.split(" ")[0];
                  select.append('<option value="' + d + '">' + d + "</option>");
                });
            });
        },
        columnDefs: [
          {
            targets: [0],
            serachable: false,
            visible: false,
          },
          {
            targets: -1,
            render: function (data, type, row) {
              return `<button type="button" class="btn btn-danger" value="${data}" onclick="deleteDocument(event)">삭제</button>`;
            },
          },
        ],
        order: [[6, "desc"]],
      });
      $(".selectpicker").prop("disabled", false);
      $(".selectpicker").selectpicker("refresh");
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
      $(".selectpicker").prop("disabled", true);
      $("#client").prop("disabled", false);
      $(".selectpicker").selectpicker("refresh");
      const documentTable = $("#documentTable").DataTable();
      documentTable.clear().draw();
    },
  });
};

const modifyInfo = (event) => {
  const documentId = document.querySelector(".document-id").value;
  const submitKind = event.target.id;
  const param = new Object();
  if (submitKind == "product-modify") {
    const productId = document.getElementById("product").value;
    if (productId) {
      param.modifyObject = "product";
      param.productId = productId;
    } else {
      alert("제품명을 선택하세요!");
      return false;
    }
  } else if (submitKind == "category-modify") {
    const category = document.getElementById("category").value;
    if (category) {
      param.modifyObject = "category";
      param.category = category;
    } else {
      alert("구분을 선택하세요!");
      return false;
    }
  }

  $.ajax({
    type: "PATCH",
    url: `/document/${documentId}/`,
    dataType: "json",
    data: param,
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const successMsg = data.msg;
      const clientId = data.client_id;
      const modifyObject = data.modify_object;
      alert(successMsg);
      if (modifyObject == "product") $("#productModal").modal("hide");
      else if (modifyObject == "category") $("#categoryModal").modal("hide");
      getClientAttachLists(clientId);
    },
    error: function (request, status, error) {
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
    },
  });
};

const init = () => {
  $("#documentTable").DataTable().destroy();
  $("#documentTable").DataTable({
    columnDefs: [
      {
        targets: [0],
        serachable: false,
        visible: false,
      },
    ],
  });
};
init();

// Event functions
$("#documentTable tbody").on("click", "tr", function () {
  const documentTable = $("#documentTable").DataTable();
  const documentId = documentTable.row(this).data().id;
  const documentIdInput = document.querySelector(".document-id");
  documentIdInput.value = documentId;
});

clientSelectBox.addEventListener("change", (event) => {
  const clientId = event.target.value;
  getClientAttachLists(clientId);
});
