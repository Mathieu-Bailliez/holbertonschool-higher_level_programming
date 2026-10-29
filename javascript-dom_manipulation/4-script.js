const addItem = document.querySelector('#add_item');
const myList = document.querySelector('ul.my_list');

addItem.addEventListener('click', function () {
  const li = document.createElement('li');
  li.textContent = 'Item';
  myList.appendChild(li);
});
