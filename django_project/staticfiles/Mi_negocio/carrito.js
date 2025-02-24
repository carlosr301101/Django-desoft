document.addEventListener("DOMContentLoaded", function () {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  const cartCount = document.getElementById("cartCount");
  const cartItems = document.getElementById("cartItems");
  const cartTotal = document.getElementById("cartTotal");

  document
    .getElementById("checkoutForm")
    .addEventListener("submit", function (event) {
      if (cart.length === 0) {
        event.preventDefault(); // Evita enviar el formulario si el carrito está vacío
        alert("El carrito está vacío. Agrega artículos antes de comprar.");
        return;
      }

      // Serializar el carrito en formato JSON
      const cartDataInput = document.getElementById("cartData");
      cartDataInput.value = JSON.stringify(cart);
    });

  // Actualiza el contador del carrito

  function updateCartUI() {
    cartCount.textContent = cart.length;
    cartItems.innerHTML = ""; // Limpiar la lista antes de volver a renderizar
    let total = 0;

    cart.forEach((item, index) => {
      const li = document.createElement("li");
      li.style.display = "flex";
      li.style.justifyContent = "space-between";
      li.style.alignItems = "center";

      // Detalles del artículo
      const details = document.createElement("span");
      details.textContent = `${item.titulo} - $${item.precio} x ${item.quantity}`;
      li.appendChild(details);

      // Botón "X" para eliminar el artículo
      const removeButton = document.createElement("button");
      removeButton.textContent = "X";
      removeButton.style.backgroundColor = "#dc3545"; // Rojo
      removeButton.style.color = "white";
      removeButton.style.border = "none";
      removeButton.style.borderRadius = "10px";
      removeButton.style.cursor = "pointer";
      removeButton.style.padding = "5px 10px";

      // Evento para eliminar el artículo
      removeButton.addEventListener("click", function () {
        if (
          confirm(
            `¿Estás seguro de que deseas eliminar "${item.titulo}" del carrito?`
          )
        ) {
          cart.splice(index, 1); // Elimina el artículo del array
          localStorage.setItem("cart", JSON.stringify(cart)); // Actualiza el localStorage
          updateCartUI(); // Actualiza la interfaz del carrito
        }
      });

      li.appendChild(removeButton);
      cartItems.appendChild(li);

      // Calcular el total
      total += item.precio * item.quantity;
    });

    cartTotal.textContent = total.toFixed(2);
  }

  // Agregar artículo al carrito
  document.querySelectorAll(".add-to-cart").forEach((button) => {
    button.addEventListener("click", function () {
      const articuloId = this.dataset.id;
      const titulo = this.dataset.titulo;
      const precio = parseFloat(this.dataset.precio);

      const existingItem = cart.find((item) => item.id === articuloId);
      if (existingItem) {
        existingItem.quantity += 1;
      } else {
        cart.push({ id: articuloId, titulo, precio, quantity: 1 });
      }

      localStorage.setItem("cart", JSON.stringify(cart));
      updateCartUI();
    });
  });

  // Abrir y cerrar el modal del carrito
  document.getElementById("openCart").addEventListener("click", function (e) {
    e.preventDefault();
    document.getElementById("cartModal").style.display = "flex";
  });

  document.getElementById("closeCart").addEventListener("click", function () {
    document.getElementById("cartModal").style.display = "none";
  });

  document.getElementById("cleanButton").addEventListener("click", function () {
    if (confirm("¿Estás seguro de que deseas limpiar el carrito?")) {
      // Vaciar el carrito en localStorage
      localStorage.removeItem("cart");

      // Restablecer el carrito en memoria
      cart.length = 0;

      // Actualizar la interfaz del carrito
      updateCartUI();
      document.getElementById("cartModal").style.display = "none";
    }
  });

  document.getElementById("buyCart").addEventListener("click", function () {
    if (
      confirm(
        "Recuerda enviarle la factura en foma de pdf al propietario de la tienda"
      )
    ) {
      updateCartUI();
    }
  });

  // Inicializa la interfaz del carrito
  updateCartUI();
});
