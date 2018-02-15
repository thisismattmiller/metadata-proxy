const express = require('express')
const request = require('request')
const app = express()

app.get('/:isbn', (req, res) => {
	res.setHeader('Content-Type', 'application/json');
	request(`https://www.googleapis.com/books/v1/volumes?q=isbn:${req.params.isbn}`, function (error, response, body) {
	  if (error){
	  	res.send(JSON.stringify(null));
	  	return
	  }
	  if (parseInt(response.statusCode) == 403){
	  	res.send(JSON.stringify(null));
	  	return	  	
	  }else{
	  	res.send(JSON.stringify({id: req.params.isbn, results: JSON.parse(body) }));
	  	return
	  }
	});
})

app.listen(3000, () => console.log('Example app listening on port 3000!'))