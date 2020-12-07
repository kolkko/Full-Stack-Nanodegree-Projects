// // create an AJAX request like in the course, using:
// // - `querySelectorAll`: To select the items or the buttons
// // - `forEach`: To loop through all the buttons you want to target, with the *onclick* event listener.
// // - `e.preventDefault();` To prevent the button from refreshing the page.
// // - `fetch`: method of course to send the request and handle the response with then.

// // Add new task to task list
// document.getElementById('create_venue').onsubmit = function(e) {
//     e.preventDefault(); // prevents page refresh
//     fetch('/venues/create', {
//         method: 'POST',
//         body: JSON.stringify({
//             'name': document.getElementById('form.name').value
//         }),
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     })
//     .then(function(response) {
//         return response.json();
//     })
//     .then(function(jsonResponse) {
//         console.log(jsonResponse);
//         const liItem = document.createElement('LI');
//         liItem.innerHTML = jsonResponse['description'];
//         document.getElementById('tasks').appendChild(liItem);
//         document.getElementById('error').className = 'hidden';
//     })
//     .catch(function() {
//         document.getElementById('error').className = '';
//     })

// }

// //Delete a task from task list
// const deleteBtns = document.querySelectorAll('.delete-tasks');
// for (let i = 0; i < deleteBtns.length; i++) {
//     const deleteBtn = deleteBtns[i];
//     deleteBtn.onclick = function(e) {
//         fetch('/venues/create', {
//             method: 'DELETE',
//         });
//     }
// }