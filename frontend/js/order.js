function populateCart() {
    var formSection = document.querySelector('.form');

    // Fetch data from the API endpoint
    fetch('http://127.0.0.1:5555/cart')
        .then(response => response.json())
        .then(data => {
            for (const restaurant in data) {
                if (Object.hasOwnProperty.call(data, restaurant)) {
                    const details = data[restaurant];
                    details.food.forEach(item => {
                        var row = document.createElement('div');
                        row.classList.add('row');

                        // Item Image
                        var imageColumn = document.createElement('div');
                        imageColumn.classList.add('column');
                        imageColumn.classList.add('item-image');
                        var img = document.createElement('img');
                        img.src = item.img;
                        img.alt = item.name;
                        imageColumn.appendChild(img);
                        row.appendChild(imageColumn);

                        // Item Name
                        var itemName = document.createElement('div');
                        itemName.classList.add('column');
                        itemName.classList.add('item');
                        itemName.textContent = item.name;
                        row.appendChild(itemName);

                        // Price
                        var price = document.createElement('div');
                        price.classList.add('column');
                        price.classList.add('price');
                        price.textContent = '$' + item.price.toFixed(2);
                        row.appendChild(price);

                        // Quantity
                        var quantityInput = document.createElement('input');
                        quantityInput.type = 'number';
                        quantityInput.min = 0;
                        quantityInput.value = item.quantity; // Set initial value to the quantity provided
                        quantityInput.classList.add('column');
                        quantityInput.classList.add('quantity');
                        quantityInput.addEventListener('input', updateTotal);
                        row.appendChild(quantityInput);

                        // Total
                        var totalColumn = document.createElement('div');
                        totalColumn.classList.add('column');
                        totalColumn.classList.add('total');
                        totalColumn.textContent = '$' + (item.price * item.quantity).toFixed(2); // Set initial total based on quantity
                        row.appendChild(totalColumn);

                        formSection.appendChild(row);
                    });
                }
            }
        })
        .catch(error => console.error('Error fetching cart data:', error));

    // Total Price element
    var totalPriceElement = document.createElement('p');
    totalPriceElement.textContent = 'Total Price (including 10% tax): $0.00';
    totalPriceElement.classList.add('total-price');
    formSection.appendChild(totalPriceElement);

    // Add Place Order button
    var placeOrderBtn = document.createElement('button');
    placeOrderBtn.textContent = 'Place Order';
    placeOrderBtn.addEventListener('click', placeOrder);
    formSection.appendChild(placeOrderBtn);

    // Update total price function
    function updateTotal() {
        var items = document.querySelectorAll('.row');
        var totalPrice = 0;
        items.forEach(function (item) {
            var price = parseFloat(item.querySelector('.price').textContent.split('$')[1]);
            var quantity = parseInt(item.querySelector('.quantity').value);
            var total = price * quantity;
            item.querySelector('.total').textContent = '$' + total.toFixed(2);
            totalPrice += total;
        });
        var totalWithTax = totalPrice * 1.1; // 10% tax
        totalPriceElement.textContent = 'Total Price (including 10% tax): $' + totalWithTax.toFixed(2);
    }

    updateTotal(); // Update total price initially
}

// Placeholder function for placeOrder
function placeOrder() {
    // Implement functionality to place order
}

populateCart();
