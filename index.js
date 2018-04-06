const express = require('express')
const request = require('request')
const app = express()

app.get('/google/:isbn', (req, res) => {
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


app.get('/worldcat/:isbn', (req, res) => {
	res.setHeader('Content-Type', 'application/json');

	var options = {
		url: `http://www.worldcat.org/search?q=bn%3A${req.params.isbn}&qt=advanced`,
		headers: {
			'User-Agent': `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36.${Math.floor(Math.random() * 500000)} (KHTML, like Gecko) Chrome`,
			'Connection':'close'
		}
	}
	request(options, function (error, response, body) {
	  if (error){
	  	res.send(JSON.stringify(null));
	  	return
	  }

	  res.send(JSON.stringify({id: req.params.isbn, results: body }));
	  return

	});
})

app.get('/classify/:isbn', (req, res) => {
        res.setHeader('Content-Type', 'application/json');

        var options = {
                url: `http://classify.oclc.org/classify2/Classify?isbn=${req.params.isbn}&maxRecs=100`,
                headers: {
			'User-Agent': `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36.${Math.floor(Math.random() * 500000)} (KHTML, like Gecko) Chrome`,
                        'Connection':'close'
                }
        }
        request(options, function (error, response, body) {
          if (error){
                res.send(JSON.stringify(null));
                return
          }

          res.send(JSON.stringify({id: req.params.isbn, results: body }));
          return

        });
})


app.get('/worldcathtml/:oclc', (req, res) => {
        res.setHeader('Content-Type', 'application/json');

        var options = {
                url: `http://www.worldcat.org/oclc/${req.params.oclc}`,
                headers: {
			'User-Agent': `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36.${Math.floor(Math.random() * 500000)} (KHTML, like Gecko) Chrome`,
                        'Connection':'close'
                }
        }
        request(options, function (error, response, body) {
          if (error){
                res.send(JSON.stringify(null));
                return
          }

          res.send(JSON.stringify({id: req.params.isbn, results: body }));
          return

        });
})


app.get('/worldcatld/:oclc', (req, res) => {
	res.setHeader('Content-Type', 'application/json');

	var options = {
		url: `http://experiment.worldcat.org/oclc/${req.params.oclc}.jsonld`,
		headers: {
			'User-Agent': `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36.${Math.floor(Math.random() * 500000)} (KHTML, like Gecko) Chrome`,
			'Connection':'close'
		}
	}
	request(options, function (error, response, body) {
	  if (error){
	  	res.send(JSON.stringify(null));
	  	return
	  }

	  res.send(JSON.stringify({id: req.params.oclc, results: body }));
	  return

	});
})
app.get('/xisbn/:isbn', (req, res) => {
	res.setHeader('Content-Type', 'application/json');

	var options = {
		url: `http://xisbn.worldcat.org/webservices/xid/isbn/${req.params.isbn}?method=getEditions&fl=*&format=json`,
		headers: {
			'User-Agent': `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36.${Math.floor(Math.random() * 500000)} (KHTML, like Gecko) Chrome`,
			'Connection':'close'
		}
	}
	request(options, function (error, response, body) {
	  if (error){
	  	res.send(JSON.stringify(null));
	  	return
	  }

	  res.send(JSON.stringify({id: req.params.isbn, results: JSON.parse(body) }));
	  return

	});
})
app.listen(3000, () => console.log('Example app listening on port 3000!'))
