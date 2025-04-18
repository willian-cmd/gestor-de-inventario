document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('product-form');
  const tabla = document.getElementById('tabla').querySelector('tbody');
  const searchInput = document.getElementById('search-input');
  const searchBtn = document.getElementById('search-btn');
  const submitBtn = document.getElementById('submit-btn');
  const cancelEditBtn = document.getElementById('cancel-edit');
  const editIdInput = document.getElementById('edit-id');
  
  let inventory = JSON.parse(localStorage.getItem('inventory')) || [];
  let isEditing = false;

  // Mostrar inventario al cargar
  renderInventory();

  // Manejar envío del formulario
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const nombre = document.getElementById('nombre').value.trim();
    const cantidad = document.getElementById('cantidad').value;
    const categoria = document.getElementById('categoria').value.trim();
    
    if (!nombre || !cantidad || !categoria) {
      alert('Por favor complete todos los campos');
      return;
    }
    
    if (isEditing) {
      // Editar producto existente
      const id = parseInt(editIdInput.value);
      const index = inventory.findIndex(item => item.id === id);
      
      if (index !== -1) {
        inventory[index] = { id, nombre, cantidad, categoria };
      }
      
      cancelEdit();
    } else {
      // Agregar nuevo producto
      const newProduct = {
        id: Date.now(),
        nombre,
        cantidad,
        categoria
      };
      inventory.push(newProduct);
    }
    
    saveInventory();
    renderInventory();
    this.reset();
  });

  // Función para renderizar el inventario
  function renderInventory(filteredList = null) {
    const items = filteredList || inventory;
    tabla.innerHTML = '';
    
    if (items.length === 0) {
      tabla.innerHTML = '<tr><td colspan="4">No hay productos en el inventario</td></tr>';
      return;
    }
    
    items.forEach(product => {
      const fila = document.createElement('tr');
      fila.innerHTML = `
        <td>${product.nombre}</td>
        <td>${product.cantidad}</td>
        <td>${product.categoria}</td>
        <td>
          <button class="action-btn edit-btn" data-id="${product.id}">Editar</button>
          <button class="action-btn delete-btn" data-id="${product.id}">Eliminar</button>
        </td>
      `;
      tabla.appendChild(fila);
    });
    
    // Agregar eventos a los botones
    document.querySelectorAll('.edit-btn').forEach(btn => {
      btn.addEventListener('click', editProduct);
    });
    
    document.querySelectorAll('.delete-btn').forEach(btn => {
      btn.addEventListener('click', deleteProduct);
    });
  }

  // Función para editar producto
  function editProduct(e) {
    const id = parseInt(e.target.getAttribute('data-id'));
    const product = inventory.find(item => item.id === id);
    
    if (product) {
      document.getElementById('nombre').value = product.nombre;
      document.getElementById('cantidad').value = product.cantidad;
      document.getElementById('categoria').value = product.categoria;
      editIdInput.value = product.id;
      
      isEditing = true;
      submitBtn.textContent = 'Actualizar';
      cancelEditBtn.style.display = 'inline-block';
    }
  }

  // Función para cancelar edición
  function cancelEdit() {
    form.reset();
    editIdInput.value = '';
    isEditing = false;
    submitBtn.textContent = 'Agregar';
    cancelEditBtn.style.display = 'none';
  }

  // Función para eliminar producto
  function deleteProduct(e) {
    if (confirm('¿Está seguro de eliminar este producto?')) {
      const id = parseInt(e.target.getAttribute('data-id'));
      inventory = inventory.filter(product => product.id !== id);
      saveInventory();
      renderInventory();
    }
  }

  // Función para buscar productos
  function searchProducts() {
    const searchTerm = searchInput.value.toLowerCase();
    
    if (!searchTerm) {
      renderInventory();
      return;
    }
    
    const filtered = inventory.filter(product => 
      product.nombre.toLowerCase().includes(searchTerm) || 
      product.categoria.toLowerCase().includes(searchTerm)
    );
    
    renderInventory(filtered);
  }

  // Función para guardar en localStorage
  function saveInventory() {
    localStorage.setItem('inventory', JSON.stringify(inventory));
  }

  // Event listeners
  cancelEditBtn.addEventListener('click', cancelEdit);
  searchBtn.addEventListener('click', searchProducts);
  searchInput.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') searchProducts();
  });
});