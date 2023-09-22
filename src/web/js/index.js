// Requiring modules
const express = require('express');
const app = express();
const mssql = require("mysql");

// Get request
//app.get('/', function (req, res) {

	// Config your database credential
	const config = {
		user: 'root',
		password: 'root',
		server: 'localhost',
		database: 'exlaw'
	};
	mssql.connect(config, function (err) {

		// Create Request object to perform
		// query operation
		let request = new mssql.Request();

		// Query to the database and get the records
		request.query('select * from exlaw',
			function (err, records) {

				if (err) console.log(err)
                console.log(records);
				// Send records as a response
				// to browser
            	//res.send(records);

			});
	});
//});
	// Connect to your database
//var request_exlaw=()=>{
	
//};

let server = app.listen(5000, function () {
	console.log('Server is listening at port 5000...');
});
//module.exports={request_exlaw};
