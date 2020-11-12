window.onload = function () {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let price_arr = [];
    let quantity_arr = [];
    console.log(price_arr)
    let TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;
    let total = TOTAL_FORMS-1


    for (var i=0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }
    if (!order_total_quantity) {
        for (let i=0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    }

    $('.order_form').on('click', 'input[type="number"]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        }
    });


    function deleteOrderItem(row) {
        let target_name= row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        delta_quantity = -quantity_arr[orderitem_num];
       quantity_arr[orderitem_num] = 0;
       if (!isNaN(price_arr[orderitem_num]) && !isNaN(delta_quantity)) {
       orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
   }
}



    $('.order_form select').change(function () {
        let target = event.target;
//        console.log(target);
    });


    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;

        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_cost').html(order_total_cost.toString());
        $('.order_total_quantity').html(order_total_quantity.toString());
    }

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });


//     var n = document.getElementById('#id_orderitems-'+total+'-product').options.selectedIndex;
//     console.log(n)
//    console.log(total, '---')
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



$(document).on('change', '.order_form select', function () {
   var target = event.target;
   orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
   var orderitem_product_pk = target.options[target.selectedIndex].value;

   if (orderitem_product_pk) {
       $.ajax({
           url: "/order/product/" + orderitem_product_pk + "/price/",
           success: function (data) {
               if (data.price) {
                   price_arr[orderitem_num] = parseFloat(data.price);
                   if (isNaN(quantity_arr[orderitem_num])) {
                       quantity_arr[orderitem_num] = 0;
                   }
                   var price_html = '<span>' + data.price.toString().replace('.', ',') +'</span> руб';
                   var current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');


                   current_tr.find('td:eq(2)').html(price_html);

                   if (isNaN(current_tr.find('input[type="number"]').val())) {
                       current_tr.find('input[type="number"]').val(0);
                   }
                   orderSummaryRecalc();
               }
           },
       });
   }
});

if (!order_total_quantity) {
   orderSummaryRecalc();
}

function orderSummaryRecalc() {
   order_total_quantity = 0;
   order_total_cost = 0;

   for (var i=0; i < TOTAL_FORMS; i++) {
       order_total_quantity += quantity_arr[i];
       order_total_cost += quantity_arr[i] * price_arr[i];
   }
   $('.order_total_quantity').html(order_total_quantity.toString());
   $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
}


//function ajax_add() {
//            var $data = {};
//            // переберём все элементы input, textarea и select формы с id="myForm "
//            $('form').find('input, textearea, select').each(function() {
//                console.log('rewrwer')
//              // добавим новое свойство к объекту $data
//              // имя свойства – значение атрибута name элемента
//              // значение свойства – значение свойство value элемента
//              $data[this.name] = $(this).val();
//            });
//            var target = event.target;
//            var csrftoken = getCookie('csrftoken');
//            console.log(csrftoken, 'csrftoken')
//            console.log('++++')
//            var form = $('.form').serialize();
////            var formData = new FormData(this);
//            console.log(form)
//            console.log($data)
//            let id = document.getElementById('id_orderitems-'+total+'-order')
//            console.log(id.value)
//
//
//              $.ajax({
//                    url: "/order/add/form/"+id.value+'/',
////                   url: "/order/add/form/",
//                   type:"POST",
//                   data: $data,
//
//                    success: function($data, status, url, result) {
//                        $('form').html($data);
//
//                        console.log('ajax done')
//                        return
//
//                    }
//              });
//
//        };
//
//
//console.log('adsad')






//     $('#id_orderitems-'+total+'-product').change('click', function () {
//
//           var form_data = $(this).serialize();
//            let id = document.getElementById('id_orderitems-'+total+'-order')
//           let target = event.target;
//           console.log(target.value)
//           console.log(id)
//           console.log(form, 'dfd')
//           console.log(id.value)
//          console.log(form_data)
//
//                 $.ajax({
//                   url: "/order/add/form/",
//                    success: function(data, status, url) {
//                        $('.order_form').html(data);
//                        console.log(url)
//                        console.log('ajax done')
//                    }
//                    });
//});

//    //         if (target) {
//    //            $.ajax({
//    //                type: "POST"
//    //                url: "/order/update/" + id.value + "/",
//    //                data: form_data,
//    //                success: function (data) {
//    //                    console.log(data)
//    //                    $('html').html(data);
//    //
//    //                    console.log('ajax done');
//    //                },
//    //            });
//    //            }
//            });


}