document.addEventListener("DOMContentLoaded", function () {
  var listDropdown = '<select id="editListId" name="listid" required>';
  var openAddItemModalBtn = document.getElementById("openAddItemModalBtn");
  var openNewListModalBtn = document.getElementById("openNewListModalBtn");
  var openEditItemModalBtns = document.querySelectorAll(
    ".openEditItemModalBtn"
  );
  var openEditListModalBtns = document.querySelectorAll(
    ".openEditListModalBtn"
  );
  var addItemModal = document.getElementById("addItemModal");
  var newListModal = document.getElementById("newListModal");
  var editItemModal = document.getElementById("editItemModal");
  var editListModal = document.getElementById("editListModal");
  var closeModalBtns = document.querySelectorAll(".modal .close");
  var cancelBtns = document.querySelectorAll(".modal .cancel-btn");
  var itemDeleteButton = document.querySelectorAll(".item-delete-btn");
  var listDeleteButton = document.querySelectorAll(".list-delete-btn");

  openAddItemModalBtn.addEventListener("click", function () {
    addItemModal.style.display = "block";
  });

  openNewListModalBtn.addEventListener("click", function () {
    newListModal.style.display = "block";
  });

  openEditItemModalBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var itemId = btn.getAttribute("data-itemid");
      var itemName = btn.getAttribute("data-itemname");
      var currentListId = btn.getAttribute("data-listid");
      var currentListName = btn.getAttribute("data-listname");

      var listDropdown = '<select id="editListId" name="listid" required>'; //resets list

      listData.forEach(function (list_item) {
        listDropdown += '<option value="' + list_item.listid + '"';
        if (list_item.listid === currentListId) {
          listDropdown += " selected";
        }
        listDropdown += ">" + list_item.listname + "</option>";
      });

      listDropdown += "</select>";

      var editItemModalHtml = ` 
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

      var editItemModalContainer = document.createElement("div");
      editItemModalContainer.innerHTML = editItemModalHtml;
      document.body.appendChild(editItemModalContainer);

      // Get the dynamically created edit item modal
      var editItemModal = document.getElementById("editItemModal-" + itemId);

      // Close modal functionality
      var closeModalBtn = editItemModal.querySelector(".close");
      var cancelBtn = editItemModal.querySelector(".cancel-btn");

      closeModalBtn.addEventListener("click", function (event) {
        event.preventDefault();
        editItemModal.style.display = "none";
        editItemModal.remove(); // Remove the modal from the DOM
      });

      cancelBtn.addEventListener("click", function (event) {
        event.preventDefault();
        editItemModal.style.display = "none";
        editItemModal.remove(); // Remove the modal from the DOM
      });

      // Display the dynamically created edit item modal
      editItemModal.style.display = "block";
    });
  });

  openEditListModalBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var listId = btn.getAttribute("data-listid");
      var listName = btn.getAttribute("data-listname");

      var editListModal = `
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

      var listEditModalContainer = document.createElement("div");
      listEditModalContainer.innerHTML = editListModal;
      document.body.appendChild(listEditModalContainer);

      var editListModal = document.getElementById("editListModal-" + listId);

      var listNameInput = editListModal.querySelector("#listname");
      listNameInput.value = listName;

      var closeModalBtn = editListModal.querySelector(".close");
      var cancelBtn = editListModal.querySelector(".cancel-btn");

      closeModalBtn.addEventListener("click", function (event) {
        event.preventDefault();
        editListModal.style.display = "none";
        editListModal.remove(); // Remove the modal from the DOM
      });

      cancelBtn.addEventListener("click", function (event) {
        event.preventDefault();
        editListModal.style.display = "none";
        editListModal.remove(); // Remove the modal from the DOM
      });

      editListModal.style.display = "block";
    });
  });

  closeModalBtns.forEach(function (btn) {
    btn.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent the default anchor behavior
      btn.closest(".modal").style.display = "none";
    });
  });

  cancelBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.closest(".modal").style.display = "none";
    });
  });

  itemDeleteButton.forEach(function (button) {
    button.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent the form submission

      var confirmDelete = confirm("Are you sure you want to delete this item?");
      if (confirmDelete) {
        // If user confirms, submit the form
        button.closest("form").submit();
      }
    });
  });

  listDeleteButton.forEach(function (button) {
    button.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent the form submission

      var confirmDelete = confirm(
        "Are you sure you want to delete this list? \n All items associated with this list will also be deleted!"
      );
      if (confirmDelete) {
        // If user confirms, submit the form
        button.closest("form").submit();
      }
    });
  });
});
