document.addEventListener("DOMContentLoaded", () => {
  const openAddItemModalBtn = document.getElementById("openAddItemModalBtn");
  const openNewListModalBtn = document.getElementById("openNewListModalBtn");
  const openEditItemModalBtns = document.querySelectorAll(".openEditItemModalBtn");
  const openEditListModalBtns = document.querySelectorAll(".openEditListModalBtn");
  const addItemModal = document.getElementById("addItemModal");
  const newListModal = document.getElementById("newListModal");
  const closeModalBtns = document.querySelectorAll(".modal .close");
  const cancelBtns = document.querySelectorAll(".modal .cancel-btn");
  const itemDeleteButton = document.querySelectorAll(".item-delete-btn");
  const listDeleteButton = document.querySelectorAll(".list-delete-btn");

  openAddItemModalBtn.addEventListener("click", () => {
    addItemModal.style.display = "block";
  });

  openNewListModalBtn.addEventListener("click", () => {
    newListModal.style.display = "block";
  });

  openEditItemModalBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      let itemId = btn.getAttribute("data-itemid");
      let itemName = btn.getAttribute("data-itemname");
      let currentListId = btn.getAttribute("data-listid");

      let listDropdown = '<select id="editListId" name="listid" required>'; //resets list

      listData.forEach( (list_item) => {
        listDropdown += '<option value="' + list_item.listid + '"';
        if (list_item.listid === currentListId) {
          listDropdown += " selected";
        }
        listDropdown += ">" + list_item.listname + "</option>";
      });

      listDropdown += "</select>";

      let editItemModalHtml = ` 
      <div id="editItemModal-${itemId}" class="method modal">
        <div class="modal-content">
          <a href="#close" class="close">&times;</a>
          <h2 class="modal-heading">Edit Item</h2>
          <form action="/edit_item" method="post">
            <input type="hidden" name="itemid" value="${itemId}">
            <label for="itemname">New Item Name:</label>
            <input type="text" id="itemname" name="itemname" value="${itemName}" required /><br />
            <label for="listid">Select List:</label>
            ${listDropdown}<br />
            <input type="submit" class="btn" value="Save Changes" />
            <button type="button" class="cancel-btn btn">Cancel</button>
          </form>
        </div>
      </div>
    `;

      let editItemModalContainer = document.createElement("div");
      editItemModalContainer.innerHTML = editItemModalHtml;
      document.body.appendChild(editItemModalContainer);

      // Get the dynamically created edit item modal
      let editItemModal = document.getElementById("editItemModal-" + itemId);

      // Close modal functionality
      let closeModalBtn = editItemModal.querySelector(".close");
      let cancelBtn = editItemModal.querySelector(".cancel-btn");

      closeModalBtn.addEventListener("click", (event) => {
        event.preventDefault();
        editItemModal.style.display = "none";
        editItemModal.remove(); // Remove the modal from the DOM
      });

      cancelBtn.addEventListener("click", (event) => {
        event.preventDefault();
        editItemModal.style.display = "none";
        editItemModal.remove(); // Remove the modal from the DOM
      });

      // Display the dynamically created edit item modal
      editItemModal.style.display = "block";
    });
  });

  openEditListModalBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      let listId = btn.getAttribute("data-listid");
      let listName = btn.getAttribute("data-listname");

      let editListModalHTML = `
      <div id="editListModal-${listId}" class="method modal">
        <div class="modal-content">
          <a href="#close" class="close">&times;</a>
          <h2 class="modal-heading">Edit List</h2>
          <form action="/edit_list" method="post">
            <input type="hidden" name="listid" value="${listId}">
            <label for="listname">New List Name:</label>
            <input type="text" id="listname" name="listname" value="${listName}" required /><br />
            <!-- Add hidden input for listId and updated listName -->
            <input type="hidden" name="original_listid" value="${listId}">
            <input type="hidden" name="updated_listname" value="${listName}">
            <input type="submit" class="btn" value="Save Changes" />
            <button type="button" class="cancel-btn btn">Cancel</button>
          </form>
        </div>
      </div>
      `;

      let listEditModalContainer = document.createElement("div");
      listEditModalContainer.innerHTML = editListModalHTML;
      document.body.appendChild(listEditModalContainer);

      let editListModal = document.getElementById("editListModal-" + listId);

      let listNameInput = editListModal.querySelector("#listname");
      listNameInput.value = listName;

      let closeModalBtn = editListModal.querySelector(".close");
      let cancelBtn = editListModal.querySelector(".cancel-btn");

      closeModalBtn.addEventListener("click", (event) => {
        event.preventDefault();
        editListModal.style.display = "none";
        editListModal.remove(); // Remove the modal from the DOM
      });

      cancelBtn.addEventListener("click", (event) => {
        event.preventDefault();
        editListModal.style.display = "none";
        editListModal.remove(); // Remove the modal from the DOM
      });

      editListModal.style.display = "block";
    });
  });

  closeModalBtns.forEach( (btn) => {
    btn.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent the default anchor behavior
      btn.closest(".modal").style.display = "none";
    });
  });

  cancelBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.closest(".modal").style.display = "none";
    });
  });

  itemDeleteButton.forEach( (button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent the form submission

      let confirmDelete = confirm("Are you sure you want to delete this item?");
      if (confirmDelete) {
        // If user confirms, submit the form
        button.closest("form").submit();
      }
    });
  });

  listDeleteButton.forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent the form submission

      let confirmDelete = confirm(
        "Are you sure you want to delete this list? \n All items associated with this list will also be deleted!"
      );
      if (confirmDelete) {
        // If user confirms, submit the form
        button.closest("form").submit();
      }
    });
  });
});
