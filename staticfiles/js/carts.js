$(document).ready(function () {
    // 全局变量：各类 checkbox 的 jQuery 对象
    var $allCheckbox = $('input[type="checkbox"]'),
        $wholeCheckbox = $('.whole_check'),
        $cartBox = $('.cartBox'),
        $shopCheckbox = $('.shopChoice'),
        $sonCheckbox = $('.son_check');

    /*-------------------------------------------
     * 1. Checkbox 选中样式处理
     -------------------------------------------*/
    // 全局 checkbox 点击时添加/移除样式
    $allCheckbox.on('click', function () {
        var $label = $(this).next('label');
        if ($(this).is(':checked')) {
            $label.addClass('mark');
        } else {
            $label.removeClass('mark');
        }
    });

    // 全局全选控制所有 checkbox
    $wholeCheckbox.on('click', function () {
        var $checkboxes = $cartBox.find('input[type="checkbox"]');
        if ($(this).is(':checked')) {
            $checkboxes.prop("checked", true)
                       .next('label').addClass('mark');
        } else {
            $checkboxes.prop("checked", false)
                       .next('label').removeClass('mark');
        }
        updateTotal();
    });

    // 单个商品 checkbox 点击事件
    $sonCheckbox.each(function () {
        $(this).on('click', function () {
            // 当所有子 checkbox 全选时，全局全选也打勾
            if ($sonCheckbox.filter(':checked').length === $sonCheckbox.length) {
                $wholeCheckbox.prop("checked", true)
                              .next('label').addClass('mark');
            } else {
                $wholeCheckbox.prop("checked", false)
                              .next('label').removeClass('mark');
            }
            updateTotal();
        });
    });

    // 每个商铺的全选
    $shopCheckbox.each(function () {
        $(this).on('click', function () {
            var $parentCartBox = $(this).closest('.cartBox');
            if ($(this).is(':checked')) {
                // 如果店铺全选，则所有该商铺下商品 checkbox 选中
                $parentCartBox.find('.son_check').prop("checked", true)
                             .next('label').addClass('mark');
            } else {
                $parentCartBox.find('.son_check').prop("checked", false)
                             .next('label').removeClass('mark');
            }
            // 如果所有店铺都选中，全局全选打勾
            if ($shopCheckbox.filter(':checked').length === $shopCheckbox.length) {
                $wholeCheckbox.prop("checked", true)
                              .next('label').addClass('mark');
            } else {
                $wholeCheckbox.prop("checked", false)
                              .next('label').removeClass('mark');
            }
            updateTotal();
        });
    });

    // 每个商铺内的商品 checkbox 关联店铺全选
    $cartBox.each(function () {
        var $thisCartBox = $(this);
        var $childChecks = $thisCartBox.find('.son_check');
        $childChecks.on('click', function () {
            if ($childChecks.filter(':checked').length === $childChecks.length) {
                $thisCartBox.find('.shopChoice').prop("checked", true)
                          .next('label').addClass('mark');
            } else {
                $thisCartBox.find('.shopChoice').prop("checked", false)
                          .next('label').removeClass('mark');
            }
            updateTotal();
        });
    });

    /*-------------------------------------------
     * 2. 商品数量控制
     -------------------------------------------*/
    // Plus 按钮
    $('.plus').on('click', function () {
        var $input = $(this).prev('input');
        var newCount = parseInt($input.val(), 10) + 1;
        var $reduceBtn = $(this).closest('.amount_box').find('.reduce');
        var $sumPriceElem = $(this).closest('.order_lists').find('.sum_price');
        var priceText = $(this).closest('.order_lists').find('.price').text(); // e.g. "£10"
        var unitPrice = parseFloat(priceText.substring(1)); // 去掉前面的£
        var newSubtotal = newCount * unitPrice;

        $input.val(newCount);
        $sumPriceElem.text('£' + newSubtotal);
        if(newCount > 1 && $reduceBtn.hasClass('reSty')){
            $reduceBtn.removeClass('reSty');
        }
        updateTotal();
    });

    // Reduce 按钮
    $('.reduce').on('click', function () {
        var $input = $(this).next('input');
        var currentCount = parseInt($input.val(), 10);
        if (currentCount <= 1) {
            $(this).addClass('reSty');
            return;
        }
        var newCount = currentCount - 1;
        var $sumPriceElem = $(this).closest('.order_lists').find('.sum_price');
        var priceText = $(this).closest('.order_lists').find('.price').text();
        var unitPrice = parseFloat(priceText.substring(1));
        var newSubtotal = newCount * unitPrice;

        $input.val(newCount);
        $sumPriceElem.text('£' + newSubtotal);
        if(newCount === 1){
            $(this).addClass('reSty');
        }
        updateTotal();
    });

    // 直接输入数量时实时更新（keyup 事件）
    $('.sum').on('keyup', function () {
        var $input = $(this);
        var $sumPriceElem = $input.closest('.order_lists').find('.sum_price');
        var priceText = $input.closest('.order_lists').find('.price').text();
        var unitPrice = parseFloat(priceText.substring(1));
        // 只允许数字且去掉前导零
        $input.val($input.val().replace(/\D|^0/g, ''));
        var count = parseInt($input.val(), 10) || 1;
        var newSubtotal = count * unitPrice;
        $input.attr('value', count);
        $sumPriceElem.text('£' + newSubtotal);
        updateTotal();
    });

    /*-------------------------------------------
     * 3. 移除商品（模态框处理）
     -------------------------------------------*/
    var $orderLists, $orderContent;
    $('.delBtn').on('click', function () {
        $orderLists = $(this).closest('.order_lists');
        $orderContent = $orderLists.closest('.order_content');
        $('.model_bg').fadeIn(300);
        $('.my_model').fadeIn(300);
    });

    $('.closeModel, .dialog-close').on('click', function () {
        closeModal();
    });

    function closeModal() {
        $('.model_bg').fadeOut(300);
        $('.my_model').fadeOut(300);
    }

    // 确认删除
    $('.dialog-sure').on('click', function () {
        $orderLists.remove();
        if ($orderContent.html().trim().length === 0) {
            $orderContent.closest('.cartBox').remove();
        }
        closeModal();
        // 重新获取所有子商品 checkbox 后更新总计
        updateTotal();
    });

    /*-------------------------------------------
     * 4. 总计计算
     -------------------------------------------*/
    function updateTotal() {
        var totalMoney = 0;
        var totalCount = 0;
        var $checkoutBtn = $('.calBtn a');
        $sonCheckbox.each(function () {
            if ($(this).is(':checked')) {
                // 从 sum_price 中去除 £ 并转换成数值
                var itemSubtotal = parseFloat($(this).closest('.order_lists').find('.sum_price').text().substring(1));
                var itemCount = parseInt($(this).closest('.order_lists').find('.sum').val(), 10);
                totalMoney += itemSubtotal;
                totalCount += itemCount;
            }
        });
        $('.total_text').text('£' + totalMoney.toFixed(2));
        $('.piece_num').text(totalCount);

        // 更新结算按钮样式
        if (totalMoney !== 0 && totalCount !== 0) {
            $checkoutBtn.addClass('btn_sty');
        } else {
            $checkoutBtn.removeClass('btn_sty');
        }
    }

    /*-------------------------------------------
     * 5. 结算按钮，收集选中购物项信息
     -------------------------------------------*/
    $('#jiesuan').on('click', function () {
        var selectedItems = [];
        $sonCheckbox.each(function () {
            if ($(this).is(':checked')) {
                var product_id = $(this).closest('.order_lists').attr('product_id');
                var size_id = $(this).closest('.order_lists').attr('size_id');
                var color_id = $(this).closest('.order_lists').attr('color_id');
                selectedItems.push(JSON.stringify({
                    'product_id': product_id,
                    'size_id': size_id,
                    'color_id': color_id
                }));
            }
        });
        if (selectedItems.length === 0) {
            return;
        }
        var url = '/order/create/?cartitems=' + selectedItems;
        $(this).attr('href', url);
    });
});