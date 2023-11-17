document.addEventListener("DOMContentLoaded", function () {
  var listDropdown = '<select id="editListId" name="listid" required>';
  var openAddTaskModalBtn = document.getElementById("openAddTaskModalBtn"); //I would like to rename openAddItemModalBtn
  var openNewListModalBtn = document.getElementById("openNewListModalBtn");
  var openEditModalBtns = document.querySelectorAll(".openEditModalBtn"); //I would like to rename open EditItemModalBtns
  var openEditListModalBtns = document.querySelectorAll(
    ".openEditListModalBtn"
  );
  var addTaskModal = document.getElementById("addTaskModal"); //I would like to rename addItemModal
  var newListModal = document.getElementById("newListModal");
  var editModal = document.getElementById("editModal"); //I would like to rename editItemModal
  var editListModal = document.getElementById("editListModal");
  var closeModalBtns = document.querySelectorAll(".modal .close");
  var cancelBtns = document.querySelectorAll(".modal .cancel-btn");
  var taskDeleteButton = document.querySelectorAll(".task-delete-btn"); //rename itemDeleteButton
  var listDeleteButton = document.querySelectorAll(".list-delete-btn");

  openAddTaskModalBtn.addEventListener("click", function () {
    //rename openAddItemModalBtn
    //rename openAddItemModalButton
    addTaskModal.style.display = "block"; //rename addItemModal
  });

  openNewListModalBtn.addEventListener("click", function () {
    newListModal.style.display = "block";
  });

  openEditModalBtns.forEach(function (btn) {
    //rename openEditItemModalBtns
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

      //rename editItemModalHtml and all below refering to task to item there are a few and the variable should be editItemModalHtml
      var editModalHtml = ` 
      <div id="editModal-${itemId}" class="method modal">
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

      var editModalContainer = document.createElement("div"); //rename editItemModalContainer
      editModalContainer.innerHTML = editModalHtml; //rename
      document.body.appendChild(editModalContainer); //rename

      // Get the dynamically created edit item modal
      var editModal = document.getElementById("editModal-" + itemId); //rename editItemModal

      // Close modal functionality
      var closeModalBtn = editModal.querySelector(".close");
      var cancelBtn = editModal.querySelector(".cancel-btn"); //rename editItemModal

      closeModalBtn.addEventListener("click", function (event) {
        event.preventDefault();
        editModal.style.display = "none";
        editModal.remove(); // Remove the modal from the DOM
      });

      cancelBtn.addEventListener("click", function (event) {
        event.preventDefault();
        editModal.style.display = "none"; //rename editItemModal same with below
        editModal.remove(); // Remove the modal from the DOM
      });

      // Display the dynamically created edit item modal
      editModal.style.display = "block"; //rename editItemModal
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

  taskDeleteButton.forEach(function (button) {
    //rename itemDeleteButton
    //rename itemDeleteButton
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
