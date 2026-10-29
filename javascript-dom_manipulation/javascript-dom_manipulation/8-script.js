document.addEventListener('DOMContentLoaded', function () {
  const hello = document.querySelector('#hello');
  const url = 'https://hellosalut.stefanbohacek.com/?lang=fr';

  fetch(url)
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      hello.textContent = data.hello;
    })
    .catch(function (error) {
      console.error(error);
    });
});
