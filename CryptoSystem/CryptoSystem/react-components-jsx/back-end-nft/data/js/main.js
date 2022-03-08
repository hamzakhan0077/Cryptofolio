import { MY_API_KEY } from './config.js';

fetch("https://rarible-data-scraper.p.rapidapi.com/top_collection/7/10", {
	"method": "GET",
	"headers": {
		"x-rapidapi-host": "rarible-data-scraper.p.rapidapi.com",
		"x-rapidapi-key": "956b93970amsh0557a4725a6aec2p1f7630jsnd6516534bfa7"
	}
	
})
// read the data in json file
.then(response => response.json())
.then(response => {
	console.log(response);
	console.log(response.list);
	const html =  response.list.map(user => {
		return `
		<p>Name: ${user.name}</p>;
		<p>Name: ${user.id}</p>;
		<p>Name: ${user.sum}</p>;
		<img className="photo" src = ${user.pic}/>`;
		

	})
	.join('');
	console.log(html);
	document.querySelector('#app').insertAdjacentHTML('afterbegin',html);
})
.catch(err => {
	console.error(err);
});