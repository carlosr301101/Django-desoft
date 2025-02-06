document.addEventListener("DOMContentLoaded", function () {
  const cart = JSON.parse(sessionStorage.getItem("cart")) || [];
  const cartCount = document.getElementById("cartCount");
  const cartItems = document.getElementById("cartItems");
  const cartTotal = document.getElementById("cartTotal");
  //1
  let isReloading = false;

  // Detectar si la página se está recargando
  window.addEventListener("load", function () {
    isReloading =
      performance.navigation.type === performance.navigation.TYPE_RELOAD;
  });

  // Limpiar el carrito solo cuando el usuario abandona la página
  window.addEventListener("beforeunload", function () {
    if (!isReloading) {
      // Limpiar el carrito en sessionStorage
      sessionStorage.removeItem("cart");
      console.log("Carrito limpiado al salir de la página.");
    }
  });
  //1
  updateCartUI();
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
      const div = document.createElement("div");
      div.className = "d-flex align-items-center";
      li.className = "d-flex align-items-center";
      li.style.display = "flex";
      li.style.justifyContent = "space-between";
      li.style.alignItems = "right";

      // Detalles del artículo
      const details = document.createElement("span");
      details.textContent = `${item.titulo} - $${item.precio} x ${item.quantity}`;
      li.appendChild(details);

      // Botón "X" para eliminar el artículo
      const removeButton = document.createElement("button");
      removeButton.textContent = "X";
      removeButton.style.backgroundColor = "#dc3545";
      removeButton.style.color = "white";
      removeButton.style.border = "none";
      removeButton.style.borderRadius = "10px";
      removeButton.style.cursor = "pointer";
      removeButton.style.padding = "5px 10px";
      removeButton.style.alignItems = "right";

      const add_1Button = document.createElement("button");
      add_1Button.textContent = "+";
      add_1Button.style.backgroundColor = "blue";
      add_1Button.style.color = "white";
      add_1Button.style.border = "none";
      add_1Button.style.borderRadius = "10px";
      add_1Button.style.cursor = "pointer";
      add_1Button.style.padding = "5px 10px";
      add_1Button.style.alignItems = "right";

      add_1Button.addEventListener("click", function () {
        cart[index]["quantity"] += 1; // Elimina el artículo del array
        sessionStorage.setItem("cart", JSON.stringify(cart)); // Actualiza el localStorage
        updateCartUI(); // Actualiza la interfaz del crrito
      });

      removeButton.addEventListener("click", function () {
        if (
          confirm(
            `¿Estás seguro de que deseas eliminar "${item.titulo}" del carrito?`
          )
        ) {
          cart.splice(index, 1); // Elimina el artículo del array
          sessionStorage.setItem("cart", JSON.stringify(cart)); // Actualiza el localStorage
          updateCartUI(); // Actualiza la interfaz del carrito
        }
      });

      div.appendChild(add_1Button);
      div.appendChild(removeButton);
      li.appendChild(div);
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

      sessionStorage.setItem("cart", JSON.stringify(cart));

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
      sessionStorage.removeItem("cart");

      // Restablecer el carrito en memoria
      cart.length = 0;

      // Actualizar la interfaz del carrito
      updateCartUI();
      document.getElementById("cartModal").style.display = "none";
    }
  });

  document.getElementById("qrButton").addEventListener("click", function () {
    alert("Comparte este Código QR que contiene el link de tu tienda");
  });
  updateCartUI();
});
