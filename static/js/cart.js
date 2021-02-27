const updateBtns = document.getElementsByClassName('update-cart-or-wishlist')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        const productId = this.dataset.product;
        const action = this.dataset.action;
        const update = this.dataset.update;
        let quantity = '1';
        if (document.getElementById('product_quantity_id')) {
            quantity = document.getElementById('product_quantity_id').value
        }
        console.log(quantity)
        updateUserOrder(productId, action, quantity, update)
    })
}

function updateUserOrder(productId, action, quantity, update) {
    const url = '/ru/cart/update_cart/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action,
            'quantity': quantity,
            'update': update,
        })
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            location.reload()
        })
}