const listMovies = document.querySelector('#list_movies');
const url = 'https://swapi-api.hbtn.io/api/films/?format=json';

fetch(url)
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    data.results.forEach(function (film) {
      const li = document.createElement('li');
      li.textContent = film.title;
      listMovies.appendChild(li);
    });
  })
  .catch(function (error) {
    console.error(error);
  });
