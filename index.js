const express = require('express');
const path = require('path');
const exec = require('await-exec')
const bodyParser = require('body-parser');

const app = express();
const port = process.env.PORT || process.argv[2] || 3000;
const processa = "python " + __dirname + "/bin/sql.py ";

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// configurando views
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// configurando assets
app.use('/js', express.static(__dirname + '/node_modules/bootstrap/dist/js')); 
app.use('/js', express.static(__dirname + '/node_modules/jquery/dist')); 
app.use('/js', express.static(__dirname + '/assets/js')); 
app.use('/css', express.static(__dirname + '/node_modules/bootstrap/dist/css')); 
app.use('/css', express.static(__dirname + '/assets/css'));  

app.get('/', function (req, res) {
  res.render('index',{});
});

app.post('/processa', async function (req, res) {
  try {
    console.log("Processando consulta: " + req.body.consulta);
    const { stdout, stderr } = await exec(processa + '\'' + req.body.consulta + '\'');
    res.end(stdout);
  } catch (error) {
    console.log(error);
  }
});

app.listen(port, function () {
  console.log('Escutando porta ' + port + '!');
});