describe('Toggle todo-item', () => {
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

  //
  // Find and return the toggle icon element of the first todo-item
  //
  function firstTodoToggleIcon() {
    return cy.get('.popup .todo-list')  // ul
      .children()  // li
      .first()
      .children()  // 3 span
      .first()
  }

  it('change todo-item to done', () => {
    let toggleIcon = firstTodoToggleIcon();

    // Click the icon in front of the description
    toggleIcon
      .click();

    // Assert that the todo-item is done (checked)
    toggleIcon
      .should('have.class', 'checked');

    // Assert that the todo description has text-decoration line-through
    toggleIcon
      .next()
      .should('have.css', 'text-decoration-line', 'line-through');

    // Restore the active state
    toggleIcon
      .click();
  })

  it('change todo-item to active', () => {
    let toggleIcon = firstTodoToggleIcon();

    // Click the icon in front of the description 2 times
    toggleIcon
      .click();

    cy.wait(500);

    toggleIcon
      .click();

    // Assert that the todo-item is active (unchecked)
    toggleIcon
      .should('have.class', 'unchecked');

    // Assert that the todo description does not have text-decoration line-through
    toggleIcon
      .next()
      .should('not.have.css', 'text-decoration-line', 'line-through');
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
