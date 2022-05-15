
var id_delete
var id_edit
var amount

function delete_order(id) {
    console.log(id)
    id_delete = id
    t = "¿Seguro que quiere eliminar la orden " + id_delete + "?"
    $("#eliminarSpan").text(t)
}

function edit_order(id) {
    console.log(id)
    id_edit = id
    id_amount = "#amount-" + id
    amount = $(id_amount).text()
    console.log(amount)
    $("#inputEdit").val(amount)
}

function update_order(id) {
    btn = "#status" + id
    $(btn).toggleClass("badge-success")
    $(btn).toggleClass("badge-danger")
    v = $(btn).val()
    console.log(v)
    if (v == "True") {
        $(btn).text("Pendiente")
        $(btn).val("False")
    }
    else {
        $(btn).text("Lista")
        $(btn).val("True")
    }
    $.ajax({
        type: "POST",
        url: "/update-order",
        data: {
            id: id,
        }
    });
}

$("#modificarConfirmar").click(function () {
    amount = $("#inputEdit").val()
    $.ajax({
        type: "POST",
        url: "/edit-amount",
        data: {
            id: id_edit,
            new_amount: amount
        },
        async: false,
        success:
            window.location.href = '/edit-success'
    });
})

$("#eliminarConfirmar").click(function () {
    $.ajax({
        type: "POST",
        url: "/delete-order",
        data: {
            id: id_delete
        },
        async: false,
        success:
            window.location.href = '/delete-success'
    });
})