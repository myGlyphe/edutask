describe('Add a todo-item', () => {
  // Define variables that we need on multiple occasions
  let uid;   // user id
  let email; // email of the user
  let taskTitle; // Task title

  before(function () {
    // Create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid;
          email = user.email;
        });
      });

    // Create a fabricated task from a fixture
    // ('task.json' is in .gitignore so use 'task1.json')
    cy.fixture('task1.json')
      .then((task1) => {
        task1.userid = uid;
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/tasks/create',
          form: true,
          body: task1
        }).then((response) => {
          taskTitle = task1.title;
        });
      });
  });

  beforeEach(function () {
    cy.viewport(1024, 800);

    // Enter the main page
    cy.visit('http://localhost:3000');

    // Login using the created user

    // Find the input and type email (in a declarative way)
    cy.contains('Email Address')  // Gets label element
      .next()
      .type(email);

    // Submit the form on this page
    cy.get('form')
      .submit();

    // Find and click on the created task
    cy.get('.container-element')
      .contains(taskTitle)
      .click();

  })

  it('1.1 Create a todo-item with a description', () => {
    // Find the input box in the popup, type a description and submit
    const description = "Test todo";

    cy.get('.popup .todo-list')
      .find('input[type=text]')
      .type(description);

    cy.get('.popup .todo-list')
      .find('form')
      .submit();

    // Find the elements of the last (added) todo-item
    cy.get('.popup .todo-list')  // ul
      .children()  // li
      .last()      // li form
      .prev()
      .children()  // 3 span
      .as('lastTodoItem');

    // Assert that the todo-item is appended to the list
    cy.get('@lastTodoItem')
      .first()
      .next()
      .should('have.text', description);

    // Assert that the todo-item is active (unchecked)
    cy.get('@lastTodoItem')
      .first()
      .should('have.class', 'unchecked');

    // Remove the added todo-item
    cy.get('@lastTodoItem')
      .last()
      .click();
  })

  it('1.2 Try to create a todo-item with no description', () => {
    // Assert that the Add-button is initially disabled
    // (will fail due to latest update of frontend)
    cy.get('.popup .todo-list')
      .find('input[type=submit]')
      .should('have.prop', 'disabled', true);
  })

  after(function () {
    // Clean up by deleting the user from the database.
    // Any associated tasks are also deleted.
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    });
  });
});
